#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#


%define _use_internal_dependency_generator 0


%include Solaris.inc
%define cc_is_gcc 1
%include usr-gnu.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libunistring64 = libunistring.spec
%endif

%include base.inc
%use libunistring = libunistring.spec

Name:		SFElibunistring-gnu
IPS_Package_Name:	system/library/gnu/unistring
Summary:        functions for manipulating Unicode strings and for manipulating C strings according to the Unicode standard. (/usr/gnu)
Group:		System/Libraries
Version:             %{libunistring.version}
URL:		http://www.gnu.org/software/libunistring
License:	LGPLv2
SUNW_Copyright: %{license}.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires: SFElibiconv
Requires:      SFElibiconv

%prep
rm -rf %name-%version
mkdir -p %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libunistring64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libunistring.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libunistring64.build -d %name-%version/%_arch64
%endif

%libunistring.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libunistring64.install -d %name-%version/%_arch64
%endif

%libunistring.install -d %name-%version/%{base_arch}
##TODO## find $RPM_BUILD_ROOT%{_libdir} -name \*.la -exec rm {} \;

[ -d "$RPM_BUILD_ROOT%{_std_datadir}" ] && rmdir $RPM_BUILD_ROOT%{_std_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
#%{_bindir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/libunistring/*
#%dir %attr(0755, root, bin) %{_infodir}
#%{_infodir}/*



%defattr (-, root, bin)
%{_includedir}


%changelog
* Sun Aug 20 2017 - Thomas Wagner
- bump to 0.9.7
- relocate to usr-gnu.inc
- make it 32/64 bit (for gnutls being 32/64-bit)
* Fri Apr 15 2016 - Thomas Wagner
- Initial spec
