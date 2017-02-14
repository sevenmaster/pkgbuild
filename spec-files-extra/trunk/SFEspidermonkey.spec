# spec file for package SFEspidermonkey
#
# includes module(s): spidermonkey
#
%define cc_is_gcc 1
%include Solaris.inc
%include packagenamemacros.inc

Name:                    SFEspidermonkey
IPS_Package_Name:	runtime/javascript/spidermonkey
Summary:                 Mozilla SpiderMonkey JavaScript Engine.
#note no automatic change to the download URL!
Version:                 1.8.5
%define download_version 185-1.0.0
Source:                  http://ftp.mozilla.org/pub/mozilla.org/js/js%{download_version}.tar.gz
# Note these patches are copied from spec-files, the latest patches for Firefox
# version 4.
Patch1:                  spidermonkey-01-js-ctypes.diff
Patch2:                  spidermonkey-02-jsfunc.diff
Patch3:                  spidermonkey-03-methodjit-sparc.diff
Patch4:                  spidermonkey-04-jemalloc.diff
Patch5:                  spidermonkey-05-pgo-ss12_2.diff
Patch6:                  spidermonkey-06-use-system-libffi.diff
Patch7:                  spidermonkey-07-makefile.diff
# see b.g.o 619721 and 595447
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

##TODO## pnn_macro to resolve pnm_buildrequires_SUNWprd_devel to library/security/nss if osdistro >=160
#resolves to library/nspr/header-nspr but this was
#renamed to:
#depend fmri=library/nspr@0.5.11-0.160 type=require
#so for the moment, require library/nspr
#BuildRequires: %{pnm_buildrequires_SUNWprd_devel}
#We want the libs. For compiling add the headers
#S11 library/security/nss@4.17.2,5.11-0.175.3.0.0.20.0
#S12 library/security/nss@4.17.2,5.12-5.12.0.0.0.67.0
#pkgname for runtime libs? probably the same
#BuildRequires: %{pnm_requires_library_nspr_header_nspr}
#old: SUNWtlsd -> mps/ssl.h
#pkg:/library/security/nss -> usr/include/mps/ssl.h     
BuildRequires: library/security/nss
#       library/mozilla-nss
#system/library/mozilla-nss
#Requires:      %{pnm_requires_tls}
Requires:      library/security/nss

BuildRequires: %{pnm_buildrequires_SUNWpr}
Requires:      %{pnm_requires_SUNWpr}
BuildRequires: SUNWzip

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%prep
%setup -q -n js-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
#libnspr4.so in /usr/lib/mps
export LDFLAGS="-B direct -z ignore -R/usr/lib/mps -L/usr/lib/mps"
export CFLAGS="-xlibmopt"
export OS_DEFINES="-D__USE_LEGACY_PROTOTYPES__"
export CXXFLAGS="-xlibmil -xlibmopt -D_XOPEN_SOURCE=500 -D__EXTENSIONS__"

cd js/src
./configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --mandir=%{_mandir} \
            --with-nspr-cflags='-I/usr/include/mps'   \
            --with-nspr-libs="-L/usr/lib/mps -lnspr4" \
            --enable-threadsafe
make

%install

cd js/src
make install DESTDIR=$RPM_BUILD_ROOT

#deliver a unversioned symlink libmozjs.so as well
#e.g. mediatomb looks for -ljs and -lsmjs and -lmozjs
#ln -s $RPM_BUILD_ROOT/%{_libdir}/libmozjs.so libmozjs185.so
ln -s libmozjs185.so $RPM_BUILD_ROOT/%{_libdir}/libmozjs.so 

find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.a" -exec rm -f {} ';'

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

%changelog
* Mon Aug 17 2015 - Thomas Wagner
- add rpath to find libnspr4.so in /usr/lib/mps/
- add symlink libmozjs.so for mediatomb to libmozjs185.so.1.0.0
- add BuildRequires is unfinished, for now library/security/nss
* Fri Jan  2 2015 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWprd_devel} %{pnm_buildrequires_SUNWpr}, %include packagenamemacros.inc, needs more work in pnm_macros: library/nspr/header-nspr is renamed to library/nspr >= 160
- fix patch spidermonkey-04-jemalloc.diff (you might verify this, it was an empty section at the end)
- rework spidermonkey-07-makefile.diff to remove multiple definitions -h and -soname for mozjs185.so (newer Solaris LD complains)
* Thu Oct 20 2011 - Brian.Cameron  <brian.cameron@sun.com>
- Created.
