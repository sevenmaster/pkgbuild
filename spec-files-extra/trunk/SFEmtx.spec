# 
# spec file for package SFEmtx
# 
%include Solaris.inc
%include packagenamemacros.inc

%define src_name mtx

Name:                SFEmtx
IPS_Package_Name:	 media/mtx
License:             GPLv2
Summary:             SCSI media changer control program
Version:             1.3.12
Source:              %{sf_download}/project/mtx/mtx-stable/%{version}/mtx-%{version}.tar.gz
URL:                 https://sourceforge.net/projects/mtx
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{license}.copyright
Group:		      	 Applications/System
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

./configure --prefix=%{_prefix}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make prefix="$RPM_BUILD_ROOT/usr" sbindir="$RPM_BUILD_ROOT/usr/sbin" mandir="$RPM_BUILD_ROOT/usr/share/man" install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Fri Jan  5 2018 - Thomas Wagner
- fix download URL
* Mon Jun 12 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec to replace obsoleted vendor package
