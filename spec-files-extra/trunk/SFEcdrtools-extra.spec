#
# spec file for package SFEcdrtools-extra
# Sun's cdrtools package does not include all of the utilities.
# This package provides missing binaries and manpages.
#

%include Solaris.inc

Name:		SFEcdrtools-extra
IPS_Package_Name:	media/cdrtools/extra
Summary:	CD/DVD/BluRay command line recording software - extra utilities
Version:	3.0
Group:		System/Media
License:	GPLv2
URL:		http://cdrecord.berlios.de/private/cdrecord.html
Source:		ftp://ftp.berlios.de/pub/cdrecord/cdrtools-%{version}0.tar.bz2
SUNW_BaseDir:	%{_basedir}
SUNW_Copyright: %{license}.copyright
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
%setup -q -n cdrtools-%{version}0

%build

export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mv $RPM_BUILD_ROOT/opt/schily/bin/* $RPM_BUILD_ROOT/%{_bindir}
rm -rf $RPM_BUILD_ROOT/%{_bindir}/btcflash
rm -rf $RPM_BUILD_ROOT/%{_bindir}/cdda2wav
rm -rf $RPM_BUILD_ROOT/%{_bindir}/cdrecord
rm -rf $RPM_BUILD_ROOT/%{_bindir}/mkhybrid
rm -rf $RPM_BUILD_ROOT/%{_bindir}/mkisofs
rm -rf $RPM_BUILD_ROOT/%{_bindir}/readcd
rm -rf $RPM_BUILD_ROOT/%{_bindir}/scg*

mkdir -p $RPM_BUILD_ROOT/%{_mandir}
mv $RPM_BUILD_ROOT/opt/schily/share/man/* $RPM_BUILD_ROOT/%{_mandir}
rm -rf $RPM_BUILD_ROOT/%{_mandir}/man1/btcflash.1
rm -rf $RPM_BUILD_ROOT/%{_mandir}/man1/cdda2wav.1
rm -rf $RPM_BUILD_ROOT/%{_mandir}/man1/cdrecord.1
rm -rf $RPM_BUILD_ROOT/%{_mandir}/man1/readcd.1
rm -rf $RPM_BUILD_ROOT/%{_mandir}/man1/rscsi.1
rm -rf $RPM_BUILD_ROOT/%{_mandir}/man8/mkisofs.8

rm -rf $RPM_BUILD_ROOT/etc
rm -rf $RPM_BUILD_ROOT/opt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_bindir}/*
%dir %{_mandir}
%{_mandir}/*

%changelog
* Mon Mar 24 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec version 3.0
