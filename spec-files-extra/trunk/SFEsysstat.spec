# spec file for package SFEsysstat
#
# includes module(s): sysstat
#
%include Solaris.inc

Name:		SFEsysstat
IPS_Package_Name:	diagnostic/sysstat
Summary:	Most important perf metrics at a single glance
Version:	20111025
IPS_component_version: 2011.10.25
License:	GPLv3
Source:		http://www.maier-komor.de/sysstat/sysstat-%{version}.tgz
URL:		http://www.maier-komor.de/sysstat.html
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWcsl
Requires: SUNWcsl

%prep
%setup -q -n sysstat-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

# Make configure find ncurses in /usr/gnu...
# perl -i.orig -lpe 'print "DIRS=/usr/gnu\n" if $. == 4' configure

./configure --prefix=%{_prefix}
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

%ifarch sparc
make install PROC=sparcv7 PREFIX=$RPM_BUILD_ROOT%{_prefix} LN="ln -s"
%else
make install PROC=i86 PREFIX=$RPM_BUILD_ROOT%{_prefix} LN="ln -s"
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_sbindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
#%dir %attr (0755, root, bin) %{_mandir}/man1m
#%{_mandir}/man1m/sysstat.1m

%changelog
* Tue Jan  5 2016 - Thomas Wagner
- use LN="ln -s" or get error about hardlink to isaexec on other FS-mountpoint fails
* Wed Dec 28 2011 - Milan Jurik
- bump version to 20111025
* Wed Jun 30 2010 - Milan Jurik
- bump version to 20100528, fix sparc install
* Mon Aug 10 2009 - matt@greenviolet.net
- Bump version to 20090805
- Change dependency from ncurses to curses.
* Wed Apr 07 2007 - Eric Boutilier
- Initial spec
