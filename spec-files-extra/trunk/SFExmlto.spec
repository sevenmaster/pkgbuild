#
# spec file for package SFExmlto
#
# includes module(s): xmlto
#
%include Solaris.inc
%include packagenamemacros.inc

Name:                    SFExmlto
IPS_Package_Name:	 developer/documentation-tool/xmlto
Summary:                 Converts an XML file into a specified format
Group:                   Development/Distribution Tools
Version:                 0.0.28
URL:                     http://fedorahosted.org/xmlto/
Source:                  http://fedorahosted.org/releases/x/m/xmlto/xmlto-%{version}.tar.bz2
License: 		 GPLv2
Patch1:                  xmlto-01-find.diff
SUNW_Copyright:          xmlto.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: %{pnm_buildrequires_SUNWlxsl_devel}
Requires:      %{pnm_requires_SUNWlxsl_devel}
BuildRequires: %{pnm_buildrequires_SUNWlxml_devel}
Requires:      %{pnm_requires_SUNWlxml_devel}

##%if %( expr %{osbuild} '>=' 175 )
# Note: this is temporary since tom wants to rework the package macros
# to handle this case in a different way. I'm not sure when Sun/Oracle
# broke data/docbook into multiple packages. On OI it is just
# data/docbook but on S11 175 (and probably some earlier version) it is
# split into three packages.
##Requires: data/docbook/docbook-dtds
##Requires: data/docbook/docbook-style-dsssl
##Requires: data/docbook/docbook-style-xsl
##%else
# Note: these are equivalent to the data/docbook package on OI
##Requires: SUNWgnome-xml-share
##Requires: SUNWgnome-xml-root
##%endif
BuildRequires: %{pnm_buildrequires_data_docbook}
Requires:      %{pnm_requires_data_docbook}
Requires:      %{pnm_requires_web_browser_w3m}
BuildRequires: %{pnm_buildrequires_SFEgnugetopt}
Requires:      %{pnm_requires_SFEgnugetopt}

%prep
rm -rf %name-%version
%setup -q -n xmlto-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export GETOPT="/usr/gnu/bin/getopt"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_datadir}/xmlto/xsl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/xmlto
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Thu Mar 24 2016 - Thomas Wagner
- bump to 0.0.28
- change (Build)Requires to pnm_requires_SUNWlxsl_devel, pnm_requires_SUNWlxml_devel, pnm_requires_SUNWw3m
* Mon Mar 24 2014 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_data_docbook}
* Sun Mar 23 2014 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SFEgnugetopt} to fix build on >= S11.2, S12
* Sun Jun 24 2012 - Logan Bruns <logan@gedanken.org>
- for now, use a conditional to choose required packages based on os.
* Sat Jun 23 2012 - Logan Bruns <logan@gedanken.org>
- replaced requires SUNWgnome-xml-* with requires
  data/docbook/docbook-style-xsl to make s11 happy.
* Fri Apr 20 2011 - Logan Bruns <logan@gedanken.org>
- bump to 0.0.25, added ips name and removed now unnecessary patch.
* Tue Jul 26 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Tue Apr 05 2011 - Thomas Wagner
- commit missing patch2 after removing typo 
* Sat Mar 26 2011 - Thomas Wagner
- add patch2, disable xmlto verification (final solution tbd ##TODO##)
* Sun Sep 19 2010 - Milan Jurik
- bump to 0.0.23
* Sat Aug 16 2008 - nonsea@users.sourceforge.net
- Add Requires to SUNWgnome-xml-root and SUNWw3m
* Tue Jun 17 2008 - simon.zheng@sun.com
- Add patch 01-find.diff, remove depedency of
  GNU find utility.
* Sun Mar 02 2008 - simon.zheng@sun.com
- By default, Solaris has already installed package 
  SUNWgnugetopt. Let's depend on it instead of
  SFEgetopt.
* Thu Feb 21 2008 - nonsea@users.sourceforge.net
- Bump to 0.0.20
* Tue Feb 13 2007 - laca@sun.com
- create
