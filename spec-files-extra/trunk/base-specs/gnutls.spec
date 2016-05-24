#
#
Name:     	gnutls
Version: 	3.5.0
Copyright:	LGPL/GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Docdir:         %{_datadir}/doc
URL:		http://www.gnutls.org
%define        major_minor_version %( echo %{version} |  awk -F'.' '{print $1 "." $2}' )
Source:        ftp://ftp.gnutls.org/gcrypt/gnutls/v%{major_minor_version}/gnutls-%{version}.tar.xz
Source2:       guile-config_remove_compiler_defines_pthreads
Patch1:        gnutls-01-ENABLE_PKCS11.diff


%prep
#don't unpack please
%setup -q -c -T -n %{name}-%{version}
xz -dc %SOURCE0 | (cd ..; tar xf -)

#%if %( expr %{solaris11} '|' %{solaris12} '|' %{omnios} )
#pkcs11_common
%patch1 -p1 
#%endif

mkdir bin
cp %{SOURCE2} bin/guile-config
chmod 0755 bin/guile-config
#note: %{_arch64} is edited into the path by the mail spec file

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CPP="${CC} -E"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

export CFLAGS="%optflags -I/usr/include/idn -I%{gnu_inc} -D__EXTENSIONS__"
export CXXFLAGS="%cxx_optflags -I/usr/include/idn -I%{gnu_inc}"
export LDFLAGS="%{_ldflags} %{gpp_lib_path} %{gnu_lib_path} -liconv"

export PKG_CONFIG_PATH=%{_pkg_config_path}

#find fixed guile-config (remove invalid flags)
export PATH=`pwd`/bin:$PATH
#using the wrapper in `pwd`/bin/guile-tools
export GUILE_TOOLS=guile-tools
export GUILE_CFLAGS="${gcc_optflags} `$GUILE_TOOLS compile`"

echo "using PKG_CONFIG_PATH=$PKG_CONFIG_PATH"

#linker complains about _start not defined (is in /usr/lib/libguile.so as UNDEF)
#pkgbuild@s11175> grep "no_undefined_flag=' -z defs'" configure
#      no_undefined_flag=' -z defs'
#at linking time
#_start                              /usr/lib/libguile.so
%if %{solaris11}
gsed -i.bak_-z_defs -e '/no_undefined_flag=. -z defs./ s?^?# removed by SFE spec-file ?' configure
%endif


./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --bindir=%{_bindir} \
    --sysconfdir=%{_sysconfdir} \
    --mandir=%{_mandir} \
    --infodir=%{_datadir}/info \
    --localstatedir=%{_localstatedir} \
    --without-p11-kit \
    --disable-cxx \
    --enable-guile \

gmake V=2 -j$CPUS

%install
gmake V=2 install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Tue May 24 2016 - Thomas Wagner
- enable patch1 for any osdistro (OIH)
- move CPP variable to base-specs/gnutls.spec (guile-snarf not seeing CPP)
- edit %_arch64 into wrapper script bin/guile-config
- bump to 3.5.0
- CFLAGS add -D__EXTENSIONS__
- LDFLAGS add -liconv
- edit configure to remove "-z defs" as it stubles over unused UNDEF function _start in /usr/lib/libguile.so (S11)
* Wed Apr 13 2016 - Thomas Wagner
- bump to 3.4.11
* Sat Jan 16 2016 - Thomas Wagner
- enable patch1 for disable pkcs11 on (OM)
- fix %files guile for (OM), see if necessary on other OS as well, ##TODO## revisit once SFEguile.spec is 32/64-bit
* Fri Jan  8 2016 - Thomas Wagner
- add patch1 gnutls-01-ENABLE_PKCS11.diff or get unresolved symbol pkcs11_common  tpmtool.o (S11 S12)
- bump to 3.4.8
* Sun Oct 11 2015 - Thomas Wagner
- add to *FLAGS  -I/usr/include/idn to find idna.h
- add BuildRequires SFEicu-gpp SFElibtasn1-gnu pnm_buildrequires_library_guile pnm_buildrequires_library_libidn
* Sat Oct 10 2015 - Thomas Wagner
- bump to 3.4.5
- add BuildRequires SFEunbound
- --without-p11-kit (check later if this makes sense on SunOS)
* Thu Aug 20 2015 - Thomas Wagner
- bump to 3.4.4
* Tue Aug  4 2015 - Thomas Wagner
- remove %{pnm_buildrequires_SUNWlibgcrypt}
- fix Requires for -devel to be SFEgnutls
- bump to 3.3.16
* Thu Jun 18 2015 - Thomas Wagner
- unarchvied
- relocate to /usr/gnu, add IPS_Package_Name
- bump to 3.3.15
