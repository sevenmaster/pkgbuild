#Workaround on S12
#diff -u /usr/share/guile/1.8/srfi/srfi-1.scm.orig /usr/share/guile/1.8/srfi/srfi-1.scm
#--- /usr/share/guile/1.8/srfi/srfi-1.scm.orig   2016-04-13 20:05:29.586989662 +0200
#+++ /usr/share/guile/1.8/srfi/srfi-1.scm        2016-05-25 18:28:30.687253724 +0200
#@@ -220,7 +220,7 @@
# 
# ;; Load the compiled primitives from the shared library.
# ;;
#-(load-extension "libguile-srfi-srfi-1-v-3" "scm_init_srfi_1")
#+(load-extension "/usr/lib/64/libguile-srfi-srfi-1-v-3" "scm_init_srfi_1")
# 
# 
# ;;; Constructors


##TODO## see where the ca-certificate.crt is read from. could be by default the system-wide location by 
#        kepping the config directory at the /etc/gnu/ localtion

#Test gnutls:  -->> Wiki
#./gnutls-cli --x509cafile /etc/certs/ca-certificates.crt --starttls-proto=imap yourimapserver -p 143

##TODO## optional 

#is this needed/wanted?
#*** p11-kit >= 0.23.1 was not found. To disable PKCS #11 support
#*** use --without-p11-kit, otherwise you may get p11-kit from
#*** http://p11-glue.freedesktop.org/p11-kit.html


##TODO## OmniOS OM: SFEguile.spec in dual 32/64-bit, then enable interfacing libs in %files section


#
# gnutls
#
%include Solaris.inc
#%define cc_is_gcc 1
#%include base.inc

%include packagenamemacros.inc
%include usr-gnu.inc

%define _use_internal_dependency_generator 0

%ifarch amd64 sparcv9
%include arch64.inc
%use gnutls64 = gnutls.spec
%endif

%include base.inc
%use gnutls = gnutls.spec

Name:          SFEgnutls
IPS_package_name: library/gnu/gnutls
Group:         System/Libraries
Summary:       GNU transport layer security library (/usr/gnu)
Version:       %{gnutls.version}
%define        major_minor_version %( echo %{version} |  awk -F'.' '{print $1 "." $2}' )
Source:        ftp://ftp.gnutls.org/gcrypt/gnutls/v%{major_minor_version}/gnutls-%{version}.tar.xz
Patch1:        gnutls-01-ENABLE_PKCS11.diff
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SFEnettle-gnu-devel
Requires:	SFEnettle-gnu

BuildRequires:  SFEunbound
Requires:       SFEunbound

BuildRequires:  SFElibtasn1-gnu
Requires:       SFElibtasn1-gnu

BuildRequires:  SFElibunistring-gnu
Requires:       SFElibunistring-gnu

#./gnutls-idna.h:29:19: fatal error: idna.h: No such file or directory
BuildRequires:  SFEicu-gpp
Requires:       SFEicu-gpp

BuildRequires:  %{pnm_buildrequires_library_guile}
Requires:       %{pnm_requires_library_guile}
BuildRequires:  %{pnm_buildrequires_library_libidn}
Requires:       %{pnm_requires_library_libidn}

##TODO## obsolete, we use nettle BuildRequires:           %{pnm_buildrequires_SUNWlibgcrypt_devel}
##TODO## obsolete, we use nettle Requires:                %{pnm_buildrequires_SUNWlibgcrypt}

BuildRequires:           %{pnm_buildrequires_SUNWzlib_devel}
Requires:                %{pnm_buildrequires_SUNWzlib}


#only S12 and OIH has fresh enough autogen (>=5.16.2)
# or get "missing sourcecode files" 
%if %( expr %{solaris12} '+' %{oihipster} '>=' 1 )
BuildRequires:  %{pnm_buildrequires_developer_build_autogen}
%else
BuildRequires:  SFEautogen
%endif




%package devel
%include default-depend.inc
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires: SFEgnutls


%prep
rm -rf %name-%version
mkdir -p %name-%version
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%gnutls64.prep -d %name-%version/%_arch64
%if %{solaris12}
echo "Info: only 64-bit /usr/bin/guile available, libraries are dual and pkgconfig files %base_arch / %_arch64 specific guile*.pc files are available"
%else
echo "Info: patch %_arch64 into bin/guile-config"
gsed -i -e '/^  *\/usr\/bin\/guile-config / s?/usr/bin/?/usr/bin/%_arch64/?' %name-%version/%_arch64/gnutls-%version/bin/guile-config
%endif
%endif

mkdir -p %name-%version/%base_arch
%gnutls.prep -d %name-%version/%base_arch

%build
#export CC=gcc
#export CXX=g++

%ifarch amd64 sparcv9
%gnutls64.build -d %name-%version/%_arch64
%endif

%gnutls.build -d %name-%version/%base_arch


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%gnutls64.install -d %name-%version/%_arch64
rm -rf $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/psktool
%endif

%gnutls.install -d %name-%version/%base_arch
rm -rf $RPM_BUILD_ROOT%{_datadir}/man
rm -rf $RPM_BUILD_ROOT%{_datadir}/info
rm -rf $RPM_BUILD_ROOT%{_bindir}/psktool



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/certtool
%{_bindir}/danetool
%{_bindir}/srptool
%{_bindir}/gnutls-serv
%{_bindir}/ocsptool
#3.5.0 has no tpmtool
#%{_bindir}/tpmtool
%{_bindir}/gnutls-cli-debug
%{_bindir}/gnutls-cli
%ifarch amd64 sparcv9
%{_bindir}/%{_arch64}/*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/guile/*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/guile/*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch sparcv9 amd64
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/locale
%{_datadir}/locale/*
%{_datadir}/guile/site/*

%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*


%changelog
* Sat Aug  9 2019 - Thomas Wagner
- new nettle has changed function name s/nettle_secp_..../nettle_get_secp_..../ in pk.c
* Fri Aug  9 2019 - Thomas Wagner
- enhance fix guile-config_remove_compiler_defines_pthreads
* Thu Jul 25 2019 - Thomas Wagner
- bump to 3.6.9
* Wed Mar 13 2019 - Thomas Wagner
- bump to 3.6.6
* Wed Mar 14 2018 - Thomas Wagner
- use --without-libidn2 to get idn.h instead of idn2.h
* Wed Nov  1 2017 - Thomas Wagner
- bump to 3.5.16
* Sun Aug 20 2017 - Thomas Wagner
- bump to 3.5.14
- change (Build)Requires to SFElibunistring-gnu
* Wed May 25 2016 - Thomas Wagner
- do not edit path into wrapper script bin/guile-config *if* we run in S12
* Tue May 24 2016 - Thomas Wagner
- enable patch1 for any osdistro (OIH)
- move CPP variable to base-specs/gnutls.spec (guile-snarf not seeing CPP)
- edit %_arch64 into wrapper script bin/guile-config
- bump to 3.5.0, removed is /usr/gnu/bin/tpmtool
- CFLAGS add -D__EXTENSIONS__
- LDFLAGS add -liconv
- edit configure to remove "-z defs" as it stubles over unused UNDEF function _start in /usr/lib/libguile.so (S11)
* Tue May 24 2016 - Thomas Wagner
- enable patch1 for any osdistro (OIH)
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
