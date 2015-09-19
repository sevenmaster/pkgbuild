#
# spec file for package SFEtaglib
#
#

%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc
%include packagenamemacros.inc
%define srcname taglib
%define _use_internal_dependency_generator 0


Name:		SFEtaglib-gpp
IPS_Package_Name:	library/audio/g++/taglib
Summary:	A library for reading and editing the meta-data of several popular audio formats (/usr/g++)
Group:		System/Multimedia Libraries
URL:		http://taglib.github.io/
Version:	1.9.1
Source:		http://taglib.github.io/releases/%srcname-%version.tar.gz
License:	LGPLv2.1
Patch1:		taglib-01-map.diff
SUNW_Copyright:	taglib.copyright
%include default-depend.inc
BuildRequires:	SFEcmake

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %srcname-%version
%patch1 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -Wl,-zmuldefs"

cmake -DCMAKE_INSTALL_PREFIX=%_prefix -DCMAKE_RELEASE_TYPE=Release -DWITH_MP4=ON -DWITH_ASF=ON  .
make -j$CPUS 

%install
rm -rf %buildroot
make install DESTDIR=%buildroot

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sat Sep 19 2015 - Alex Viskovatoff <herzen@imap.org>
- bump to 1.9.1; clean up
* Fri Jan  9 2015 - Thomas Wagner
- switch off pkgdepend. doesn't to the right thing: find the other taglib package and add false dependencies
* Fri Jan  2 2015 - Thomas Wagner
- make g++ version
- bump to 1.7.2
* Sun Jun 24 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWlibstdcxx4}, %include packagenamacros.inc
* Sun Oct 23 2011 - Milan Jurik
- bump top 1.7
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Tue Apr 27 2010 - brian.cameron@sun.com
- Bump to 1.6.3.
* Tue Dec 22 2009 - brian.cameron@sun.com
- Bump to 1.6.1.
* Tue Nov 24 2009 - brian.cameron@sun.com
- Bump to 1.6.
* Tue Sep 08 2009 - brian.cameron@sun.com
- Bump to 1.5.
* Fri Jan 18 2008 - moinak.ghosh@sun.com
- Allow build using g++
* Sun Nov 04 2007 - trisk@acm.jhu.edu
- Initial spec
