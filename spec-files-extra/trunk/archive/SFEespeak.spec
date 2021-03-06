%include Solaris.inc

%define src_name espeak
%define src_url http://downloads.sourceforge.net/%{src_name}

Name:		SFEespeak
Summary:	eSpeak - compact open source software speech synthesizer
Version:	1.37
Source:		%{src_url}/%{src_name}-%{version}-source.zip
Patch1:         espeak-01-makefile.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%{version}-source
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi
cd src
make -j$CPUS EXTRA_LIBS=-lm AUDIO=sada
make install EXTRA_LIBS=-lm AUDIO=sada DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Thu Aug 20 2008 - Willie Walker
- Move to archive.  espeak is now in SUNWespeak.spec in jds/spec-files
* Tue Aug 12 2008 - Willie Walker
- Port to SunStudio (thanks Brian Cameron!)
* Tue Apr 15 2008 - Willie Walker
- Upgrade to version 1.37 which contains direct SADA support and eliminates
  all PulseAudio and other dependencies.
* Tue Jan 29 2008 - Willie Walker
- Initial spec
