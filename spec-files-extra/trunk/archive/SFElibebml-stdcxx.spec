#
# spec file for package SFElibebml
#
# includes module(s): libebml
#

%define _basedir /usr/stdcxx
%include Solaris.inc
%include packagenamemacros.inc
%define srcname libebml

Name:		SFElibebml
IPS_package_name:	library/stdcxx/libebml
License:	LGPL
Summary:	Extensible Binary Meta Language (stdcxx4-built)
Group:		System Environment/Libraries
URL:		http://ebml.sourceforge.net
Vendor:		Moritz Bunkus <moritz@bunkus.org>
Version:	1.2.2
Source:		http://dl.matroska.org/downloads/%srcname/%srcname-%version.tar.bz2
Patch1:		libebml-01-makefile.diff
Patch2:		libebml-02-headers.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SUNWgmake
BuildRequires:	%{pnm_buildrequires_SUNWgnu_coreutils}
BuildRequires:	SUNWloc

BuildRequires: %{pnm_buildrequires_SUNWlibstdcxx4}
Requires:      %{pnm_requires_SUNWlibstdcxx4}

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %srcname-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CXXFLAGS="%cxx_optflags -library=stdcxx4"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT=/usr/bin/msgfmt

cd make/linux
gmake -j$CPUS CXX=CC AR=CC  DEBUGFLAGS=-g WARNINGFLAGS="" \
ARFLAGS="-xar -o" LOFLAGS=-Kpic LIBSOFLAGS="%_ldflags -library=stdcxx4 -G -h "

%install
rm -rf $RPM_BUILD_ROOT
cd make/linux
gmake install_headers prefix=$RPM_BUILD_ROOT%{_prefix} INSTALL=ginstall
gmake install_sharedlib prefix=$RPM_BUILD_ROOT%{_prefix} INSTALL=ginstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Wed Feb 05 2014 - Alex Viskovatoff
- Archive, since it is unlikely that any customers of this spec will ever be
  built with Studio; rename to SFElibebml-stdcxx.spec
* Thu Jul 11 2013 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWgnu_coreutils}
* Sun Jun 24 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWlibstdcxx4}, %include packagenamacros.inc
* Sun Jul 29 2012 - Milan Jurik
- bump to 1.2.2
* Fri Jun 22 2012 - Logan Bruns <logan@gedanken.org>
- Accept either SFEcoreutils or SUNWgnu-coreutils for buildrequires.
* Sat Feb  5 2011 - Alex Viskovatoff
- Update to 1.2.0, adding one patch
* Thu Jan 27 2011 - Alex Viskovatoff
- Go back to using -library=stdcxx4
* Tue Nov 23 2010 - Alex Viskovatoff
- Use stdcxx.inc instead of -library=stdcxx4; install in /usr/stdcxx
* Fri Oct  1 2010 - Alex Viskovatoff
- Update to 1.0.0; use stdcxx (requires Solaris Studio 12u1)
- Patch linux Makefile so that it works with Linux and Solaris
  instead of creating a new Makefile for Solaris.
* Fri Jul 13 2007 - dougs@truemail.co.th
- Initial version
