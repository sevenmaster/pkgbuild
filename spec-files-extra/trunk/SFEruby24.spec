##TODO## %files section has troubles using %{_arch64} paths, at the moment enteres manually
##TODO## verify the whole install. Is everything found propperly?


#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define cc_is_gcc 1
%define major_minor_version 2.4
%define major_minor_version_no_dot 24
%define ruby_prefix %{_basedir}/ruby/%{major_minor_version}
%define _prefix %{ruby_prefix}
%include base.inc
%include arch64.inc
%include packagenamemacros.inc

Name:         SFEruby
IPS_Package_Name:	runtime/ruby-24
Summary:      Object oriented scripting language (64bit)
URL:          http://www.ruby-lang.org/
Version:      2.4.2
Source:       http://cache.ruby-lang.org/pub/ruby/2.4/ruby-%{version}.tar.bz2


#Patch1:       ruby-01-endian.diff

#Kudos to Userland repo, patches reworked only partly
Patch1: patches/ruby24-01-ruby_1.patch.diff
Patch2: patches/ruby24-02-config.patch.diff
Patch3: patches/ruby24-03-common_mk.patch.diff
Patch4: patches/ruby24-04-ext_openssl_extconf_rb.patch.diff
Patch5: patches/ruby24-05-test-ruby-test_process_rb.patch.diff
#not applicable Patch6: patches/ruby24-06-CVE-2016-2337.patch.diff


SUNW_BaseDir: %{_basedir}
%include default-depend.inc
BuildRequires:   %{pnm_buildrequires_SUNWlibms_devel}
Requires:        %{pnm_requires_SUNWlibms}
BuildRequires:   %{pnm_buildrequires_SUNWopenssl}
Requires:        %{pnm_requires_SUNWopenssl}
BuildRequires:   %{pnm_buildrequires_SUNWzlib_devel}
Requires:        %{pnm_requires_SUNWzlib}
BuildRequires:   %{pnm_buildrequires_SFElibyaml}
Requires:        %{pnm_requires_SFElibyaml}


##TODO## check dependencies
#REQUIRED_PACKAGES += library/database/gdbm
#REQUIRED_PACKAGES += library/gmp
#REQUIRED_PACKAGES += library/libffi
#REQUIRED_PACKAGES += library/ncurses
#REQUIRED_PACKAGES += library/readline
#REQUIRED_PACKAGES += library/security/openssl
#REQUIRED_PACKAGES += library/security/openssl/openssl-fips-140
#REQUIRED_PACKAGES += library/zlib
#REQUIRED_PACKAGES += runtime/tcl-8
#REQUIRED_PACKAGES += runtime/tk-8
#REQUIRED_PACKAGES += shell/bash
#REQUIRED_PACKAGES += system/core-os
#REQUIRED_PACKAGES += system/library/gcc/gcc-c-runtime
#REQUIRED_PACKAGES += system/library/math
#REQUIRED_PACKAGES += system/linker
#REQUIRED_PACKAGES += x11/library/libx11


%prep
%setup -q -n ruby-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
#not applicable %patch6 -p1

echo "variables:
_prefix	%{_prefix}
_bindir	%{_bindir}
_libdir	%{_libdir}
"


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
#export CFLAGS="-xc99 %{optflags}"
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"

#CFLAGS += -DFFI_NO_RAW_API
export CFLAGS="$CFLAGS -DFFI_NO_RAW_API"

#spaeter, sparc:
#iropt -X02 works around
#studio_OPT.sparc.64 = -xO2
#against "ISA not supported"
#studio_XBITS.i386.64 += -D__amd64

#
#done#CONFIGURE_PREFIX = $(USRDIR)/$(COMPONENT_NAME)/$(RUBY_VER)
#CONFIGURE_OPTIONS +=	--with-rubylibprefix=$(CONFIGURE_LIBDIR.32)/ruby
#CONFIGURE_OPTIONS +=	--enable-shared
#CONFIGURE_OPTIONS +=	--enable-rpath
## Don't need docs for ruby C source files
#CONFIGURE_OPTIONS +=	--disable-install-capi
#CONFIGURE_OPTIONS +=	--disable-option-checking
#CONFIGURE_OPTIONS +=	--with-openssl
## If Ruby is configured with __builtin_setjmp, may cause
## problems with gems compiled with gcc.  Studio compiler doesn't 
## report an error for __builtin_setjmp, but gcc would.
#CONFIGURE_OPTIONS +=	--with-setjmp-type=_setjmp
#CONFIGURE_OPTIONS +=	DTRACE="$(USRSBINDIR)/dtrace"
## ensure we use the 64-bit configuration file, not the 32-bit one
#CONFIGURE_OPTIONS +=	--with-tclConfig-file=$(USRLIBDIR)/64/tclConfig.sh
#	# set mantype to "man" so tool/mdoc2man.rb is used to convert
#	# the manpages from doc to man format; otherwise mantype is "doc" and
#	# headers we add to the manpages will not work properly
#CONFIGURE_OPTIONS +=	--with-mantype=man

autoconf
#NOTE: _prefix is already /usr/ruby/2.4/
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --with-rubylibprefix=%{_libdir} \
	    --disable-install-capi \
	    --disable-option-checking \
	    --with-openssl \
	    --with-setjmp-type=_setjmp \
	    DTRACE="%{_basedir}/bin/dtrace" \
	    --with-tclConfig-file=%{_basedir}/lib/64/tclConfig.sh \
	    --with-mantype=man \
            --enable-shared \
            --enable-rpath \

gmake -j$CPUS
	
%install
rm -rf $RPM_BUILD_ROOT

#from userland:
#Prevent re-compile of ripper.so during install
#COMPONENT_PRE_INSTALL_ACTION += \
#	$(GSED) -i -e "s/^static: check/static: all/" $(BUILD_DIR_64)/ext/ripper/Makefile ; \
#	$(TOUCH) -r $(BUILD_DIR_64)/ext/ripper/ripper.o $(BUILD_DIR_64)/ext/ripper/Makefile

make install DESTDIR=$RPM_BUILD_ROOT
make install-doc DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libruby*.a

#tweak entries in rbconfig.rb to find library in the right path
#there should be a more clever solution possible, eventually
##TODO## once everything is correct & verified, remove the ".bak" part and keep only "-i"
##TODO## replace amd64 with pkgbuild variable for name of 64-bit-arch
##/usr/ruby/2.4/lib/amd64/2.4.0/i386-solaris2.11/rbconfig.rb
##  CONFIG["libdir"] = "$(exec_prefix)/lib/amd64"
sed -i.bak -e '/CONFIG..libdir.. =/ s?/lib"?/lib/amd64"?' %{buildroot}/%{_libdir}/%{version}/*/rbconfig.rb

##TODO## verify symlinks do the right thing
#make isaexec symlinks into /usr/ruby/2.4/bin/ for binaries found in /usr/ruby/2.4/bin/%{_arch64} 
for i in `ls -1 %{buildroot}%{_bindir}/*`; do
  #go into  %{buildroot}/ruby/2.4/bin/ (therefore the /..)
  cd %{buildroot}%{_bindir}/.. && ln -s ../lib/isaexec `basename $i`
done

##TODO## check if we need something from here:
#COMPONENT_POST_INSTALL_ACTION += \
#	$(GSED) -e "s/RUBY_VER_NO_DOT/$(RUBY_VER_NO_DOT)/g" \
#	    -e "s/RUBY_VER/$(RUBY_VER)/g" \
#	    -e "s/RUBY_LIB_VER/$(RUBY_LIB_VER)/g" Solaris/gem.1-generic \
#	    > Solaris/gem.1 ; \
#	$(GSED) -e "s/RUBY_VER_NO_DOT/$(RUBY_VER_NO_DOT)/g" \
#	    -e "s/RUBY_VER/$(RUBY_VER)/g" \
#	    -e "s/RUBY_LIB_VER/$(RUBY_LIB_VER)/g" Solaris/ruby.1.sedscript \
#	    > Solaris/ruby.1.sedscript.mod ; \
#	$(GSED) -e  "s/RUBY_VER/$(RUBY_VER)/g" \
#	    -e "s/RUBY_LIB_VER/$(RUBY_LIB_VER)/g" Solaris/rbconfig.sedscript \
#	    > Solaris/rbconfig.sedscript.mod ; \
#	$(GSED) -i -f Solaris/ruby.1.sedscript.mod \
#	    $(PROTORUBYDIR)/share/man/man1/ruby.1 ; \
#	/usr/bin/sed -f Solaris/rbconfig.sedscript.mod \
#	$(PROTO_RBCONFIG_FILE) > rbconfig.rb.mod ; \
#	$(MV) rbconfig.rb.mod $(PROTO_RBCONFIG_FILE)


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_basedir}/ruby/2.4/bin
%{_basedir}/ruby/2.4/bin/irb
%{_basedir}/ruby/2.4/bin/rake
%{_basedir}/ruby/2.4/bin/gem
%{_basedir}/ruby/2.4/bin/ruby
%{_basedir}/ruby/2.4/bin/erb
%{_basedir}/ruby/2.4/bin/rdoc
%{_basedir}/ruby/2.4/bin/ri
%dir %attr (0755, root, bin) %{_basedir}/ruby/2.4/bin/amd64
%{_basedir}/ruby/2.4/bin/amd64/*
%dir %attr (0755, root, bin)  %{_basedir}/ruby/2.4/lib/amd64
%{_basedir}/ruby/2.4/lib/amd64/*
%dir %attr (0755, root, bin)  %{_basedir}/ruby/2.4/lib
#%dir %attr (0755, root, other) %{_basedir}/ruby/2.4/lib/amd64/pkgconfig
#%{_basedir}/ruby/2.4/lib/amd64/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/ri
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/ruby
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Sat Oct 14 2017 - Thomas Wagner
- svn copy from 2.1.7 to 2.4.2, make it 64-bit only for now
- early version, everything is subject to change
