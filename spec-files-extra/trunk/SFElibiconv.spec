
%include Solaris.inc
%include usr-gnu.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libiconv64 = libiconv.spec
%endif

%include base.inc

%use libiconv = libiconv.spec

#stumbles into OS provided libs
%define _use_internal_dependency_generator 0


##TODO## Bug SUNWncurses and SUNWtixi do not define group "other" for /usr/gnu/share/doc
##TODO## Bug No SUNWncurses TBD 
##TODO## Bug No SUNWtixi    TBD 

# s12_37 sfe ~ pkg contents -r -m terminal/tack | grep usr/gnu/share/doc
# dir facet.doc=true group=other mode=0755 owner=root path=usr/gnu/share/doc
# dir facet.doc=true group=bin mode=0755 owner=root path=usr/gnu/share/doc/SUNWtack
# 
##TODO## /usr/gnu/share/doc might not already exist! maybe replace with querying IPS package on a os2nnn system!!
%define workaround_gnu_share_doc_group %( /usr/bin/ls -dl /usr/gnu/share/doc | grep " root.*bin " > /dev/null 2>&1 && echo bin || echo other )


Name:		SFElibiconv
##TODO## one day we can change the name to /gnu/
IPS_Package_Name:	library/libiconv 
Summary:	GNU iconv - Code set conversion (/usr/gnu)
Group:		System/Libraries
License:	LGPLv2
SUNW_Copyright:	libiconv.copyright
URL:		http://www.gnu.org/s/libiconv/
Version:	%{libiconv.version}
Source:		http://ftp.gnu.org/pub/gnu/libiconv/libiconv-%{version}.tar.gz
Patch2:		libiconv-02-646.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%name

%prep
rm -rf %name-%version
mkdir -p %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libiconv64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libiconv.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libiconv64.build -d %name-%version/%_arch64
%endif

%libiconv.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libiconv64.install -d %name-%version/%_arch64
%endif

%libiconv.install -d %name-%version/%{base_arch}

##TODO##RAUS##[ -f ${RPM_BUILD_ROOT}%{_datadir}/info/dir ] && rm ${RPM_BUILD_ROOT}%{_datadir}/info/dir

##TODO##PRUEFEN##
find $RPM_BUILD_ROOT -name '*.la' -exec rm {} \; -o -name '*.a'  -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/iconv
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/iconv.1
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/iconv*.3
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_datadir}/locale
%{_datadir}/locale/*


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
##TODO## fix see bugs on top of the spec
#%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, %{workaround_gnu_share_doc_group}) %{_datadir}/doc
%{_datadir}/doc/*


%changelog
* Tue Jun 16 2015 - Thomas Wagner
- make it 32/64-bit
* Thu Oct 06 2011 - Milan Jurik
- bump to 1.14, add IPS package name
* Wed Jul 20 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Wed Feb 23 2011 - Milan Jurik
- fix packaging
* May 30 2010 - Thomas Wagner
- build workaround to build this package according to the group set on the
  building machine's directory /usr/gnu/share/doc/, reason behind is
  SUNWncurses creates /usr/gnu/share/doc with root:bin instead root:other
* Wed Feb 24 2010 - Milan Jurik
- update to 1.13.1
- remove runpath patch as not needed
* Fri Oct 09 2009 - Milan Jurik
- update to 1.13
- fix /usr/gnu/share/doc group
* Sun Aug 17 2008 - nonsea@users.sourceforge.net
- Bump to 1.12
- Add patch intmax.diff to fix build issue.
* Sun Jun 29 2008 - river@wikimedia.org
- use rm -fr instead of rm -r, since this directory doesn't seem to exist always
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Add l10n package.
* Sun Apr 21 2007 - Doug Scott
- Added -L/usr/gnu/lib -R/usr/gnu/lib
* Mon Mar 12 2007 - Eric Boutilier
- Initial spec
