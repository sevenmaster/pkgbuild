#
# spec file for package SFEcppunit.spec
#
# includes module(s): cppunit
#
%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc  1
%include base.inc

%include packagenamemacros.inc

%define src_name	cppunit

Name:		SFEcppunit-gpp
IPS_Package_Name:	developer/g++/cppunit
Summary:	C++ port of JUnit (/usr/g++)
Version:	1.12.1
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
Patch1:		cppunit-01-finite.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: %{pnm_buildrequires_SUNWdoxygen}
BuildRequires: %{pnm_buildrequires_SUNWgraphviz}

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++

export CFLAGS="%{optflags}"
export LDFLAGS="%_ldflags -lm"

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static

gmake -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755,root,other) %{_datadir}/doc
%dir %attr (0755,root,other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/doc/*


%changelog
* Thu Oct 29 2015 - Thomas Wagner
- relocate to usr-g++.inc
- use gcc/g++
* Wed Aug  5 2015 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWgraphviz} %{pnm_buildrequires_SUNWdoxygen}, %include packagenamemacros.inc
- add sfe/ to IPS_Package_Name only on OIH or get duplicate package name (at the end, don't build on oihipter for now - subject to change)
* Mon May 14 2012 - Milan Jurik
- bump to 1.12.1
* Fri Jan 18 2008 - moinak.ghosh@sun.com
- Added doxygen,graphviz as buildrequires
* Mon May  7 2007 - dougs@truemail.co.th
- Initial version
