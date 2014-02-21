# 
# spec file for package SFEkasumi 
# 

%include Solaris.inc
%include packagenamemacros.inc

Name:                SFEkasumi
IPS_Package_Name:	 system/input-method/ibus/anthy/kasumi
License:             GPLv2
Summary:             A dictionary management tool for Anthy
Version:             2.5
Source:				 http://jaist.dl.sourceforge.jp/kasumi/41436/kasumi-%{version}.tar.gz
Patch0:				 kasumi-00-sunstudio.diff
Patch1:				 kasumi-01-setlocale.diff
URL:                 http://kasumi.sourceforge.jp/index.php?FrontPage
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{license}.copyright
Group:		     	 System/Internationalization
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:		%{pnm_buildrequires_SUNWlibanthy_devel}
Requires:			%{pnm_requires_SUNWlibanthy}

%description
A dictionary management tool for Anthy.

%prep
%setup -q -n kasumi-%{version}
%patch0 -p1
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

echo $LDFLAGS

./configure --prefix=/usr
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) /usr/share
%dir %attr (0755, root, other) /usr/share/applications
/usr/share/applications/*
%dir %attr (0755, root, other) /usr/share/locale
%dir %attr (0755, root, other) /usr/share/locale/it
%dir %attr (0755, root, other) /usr/share/locale/it/LC_MESSAGES
%attr (0644, root, other) /usr/share/locale/it/LC_MESSAGES/*
%dir %attr (0755, root, other) /usr/share/locale/ja
%dir %attr (0755, root, other) /usr/share/locale/ja/LC_MESSAGES
%attr (0644, root, other) /usr/share/locale/ja/LC_MESSAGES/*
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, other) /usr/share/pixmaps
/usr/share/pixmaps/*

%changelog
* Fri Feb 21 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- typo in %{_ldflags}
* Fri Feb 21 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- export CFLAGS=%{optflags}, export LDFLAGS=%{ldflags}
* Fri Feb 21 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- export CXXFLAGS=%{cxx_optflags}
* Fri Feb 21 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Remove redundant %include base.inc
* Fri Feb 21 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec version 2.5
