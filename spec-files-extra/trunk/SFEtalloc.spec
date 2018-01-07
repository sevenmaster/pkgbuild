##TODO## make 32/64-bit and provide python loadable module according to platform default python bittness

#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc
%if %( expr %{oihipster} '|' %{omnios} )
%define cc_is_gcc 1
%include base.inc
%endif


Name:                SFEtalloc
IPS_Package_Name:    library/libtalloc
Summary:             A hierarchical pool based memory system with destructors.
Version:             2.1.10
URL:                 https://talloc.samba.org/
Source:              http://www.samba.org/ftp/talloc/talloc-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: %{pnm_buildrequires_developer_swig}
Requires:      %{pnm_requires_developer_swig}

%prep
rm -rf  %name-%version
%setup -q -c -n  %name-%version 

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

%if %{cc_is_gcc}
export CC=gcc
export CFLAGS="%optflags"
%else
export CFLAGS="-mt %optflags"
%endif

export LDFLAGS="-z ignore %_ldflags"

#cd %{source_name}/lib/talloc
#cd talloc-%{version}/lib/replace
cd talloc-%{version}

#./configure --prefix=%{_prefix}  \
#            --enable-static=no
./configure --prefix=/usr  --bundled-libraries=NONE --builtin-libraries=replace --disable-silent-rules

%if %{cc_is_gcc}
#noting
%else
#remove this  replace_test_cflags="-Wno-format-zero-length"
gsed -i.bak \
     -e '/replace_test_cflags.*-Wno-format-zero-length/ s?-Wno-format-zero-length??' \
     lib/replace/wscript \
%endif

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
#cd talloc-%{version}/lib/replace
cd talloc-%{version}

gmake install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

#%if %{omnios}
rm -r ${RPM_BUILD_ROOT}/usr/lib/python%{python_version}
#%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%if %{omnios}
#why don't we have the man page on OmniOS
%else
#%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/swig/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%endif

%changelog
* Fri Jan  5 2018 - Thomas Wagner
- bump version to 2.1.10
- add IPS_Package_Name
- change (Build)Requires to pnm_buildrequires_developer_swig, %include packagenamemacros.inc
- on OmniOS and Hipster build with CC=gcc (OM, OIH)
- for CC=gcc remove "-mt"
- for now remove python loadable object on all OS
- remove -Wno-format-zero-length if compiler is studio
* Sat Mar 13 2010 - brian.lu@sun.com
- Build talloc under SFEtalloc-2.0.1 direcotory
* Wed Dec 02 2009 - brian.lu@sun.com
- Bump to samba4 alpha9
* Thu Aug 27 2009 - brian.lu@sun.com
- add "-mt" to CFLAGS to set errno correctly in MT environment
* Wed Jun 03 2009 - brian.lu@sun.com
- Add dependency SUNWswig
* Wed Feb 18 2009 - jedy.wang@sun.com
- Do not use optimization option for now.
* Tue Feb 17 2009 - jedy.wang@sun.com
- Fix file attribute problem.
* Tue Feb 10 2009 - jedy.wang@sun.com
- Initial spec
