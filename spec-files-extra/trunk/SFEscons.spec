#
# spec file for package SFEscons
#
# includes module(s): SCons
#

%include Solaris.inc
%include packagenamemacros.inc

Name:                    SFEscons
IPS_Package_Name:	developer/build/scons
Summary:                 SCons - a software construction tool (make replacement)
Group:		Development/Distribution Tools
Version:                 2.3.4
URL:                     http://www.scons.org/
License:                 MIT
SUNW_copyright:          scons.copyright
Source:                  %{sf_download}/scons/scons-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires: 	         %{pnm_requires_python_default}
BuildRequires: 	         %{pnm_buildrequires_python_default}

%include default-depend.inc

%description
SCons is an Open Source software construction tool that is,
a next-generation build tool. Think of SCons as an improved,
cross-platform substitute for the classic Make utility with
integrated functionality similar to autoconf/automake and
compiler caches such as ccache. In short, SCons is an easier,
more reliable and faster way to build software.

%prep
%setup -q -n scons-%version

%build
python setup.py build \
    --build-base=$RPM_BUILD_ROOT%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix $RPM_BUILD_ROOT%{_prefix}

mkdir $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_datadir} 

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/scons-*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*

%changelog
* Sun Jan 18 2015 - Thomas Wagner
- bump to 2.3.4
* Fri Nov  2 2012 - Thomas Wagner
- add description
- bump to 2.2.0
* Tue Sep 27 2011 - Alex Viskovatoff
- bump to 2.1.0; add SUNW_copyright
* Thu Nov 04 2010 - Milan Jurik
- bump to 2.0.1
* Thu Apr 22 2010 - Milan Jurik
- update to 1.3.0
* Sat Feb 21 2009 - sobotkap@gmail.com
- Bump to 1.2.0
* Sat Sep 13 2008 - sobotkap@gmail.com
- Bump to 1.01
* Wed May 23 2007 - nonsea@users.sourceforge.net
- Bump to 0.97
* Tue Mar 06 2007 - nonsea@users.sourceforge.net
- Initial spec file
