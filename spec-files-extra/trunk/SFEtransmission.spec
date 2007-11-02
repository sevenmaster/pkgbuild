#
# spec file for package SFEtransmission
#
%include Solaris.inc
%define source_name transmission

Name:                    SFEtransmission
Summary:                 Transmission - GTK and console BitTorrent client
Version:                 0.91
Source:                  http://download.m0k.org/transmission/files/transmission-%{version}.tar.bz2
URL:                     http://transmission.m0k.org/
Patch1:                  transmission-01-sunpro.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{source_name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-base-libs
BuildRequires: SUNWopenssl-include
Requires: SUNWgnome-base-libs
Requires: SUNWopenssl-libraries

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
%setup -q -n %{source_name}-%{version}
# temporary workaround for missing parent dir in 0.82
#%setup -q -c -n %{name}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -mt -I/usr/sfw/include"
export CXXFLAGS="%cxx_optflags -mt -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"

./configure --prefix=%{_prefix}   \
            --datadir=%{_datadir} \
	    --mandir=%{_mandir}   \
            --program-prefix=""

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT%{_mandir}

#mkdir -p $RPM_BUILD_ROOT%{_prefix}/sfw/share/zsh
#mv $RPM_BUILD_ROOT%{_datadir}/zsh/* $RPM_BUILD_ROOT%{_prefix}/sfw/share/zsh 
#rm -rf $RPM_BUILD_ROOT%{_datadir}/zsh

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (-, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
#%dir %attr (0755, root, bin) %{_prefix}/sfw
#%dir %attr (0755, root, bin) %{_prefix}/sfw/share
#%{_prefix}/sfw/share/zsh
#%{_prefix}/share/zsh

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (-, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Nov 01 2007 - trisk@acm.jhu.edu
- Bump to 0.91, replace patch1
* Mon Sep 10 2007 - trisk@acm.jhu.edu
- Bump to 0.82
* Thu Sep 6 2007 - Petr Sobotka sobotkap@centum.cz
- Fix typo in changelog
* Wed Aug 29 2007 - trisk@acm.jhu.edu
- Bump to 0.81, add workaround for broken tarball
* Mon Aug 20 2007 - trisk@acm.jhu.edu
- Clean up, allow building with Studio
* Sun Aug 19 2007 - Petr Sobotka sobotkap@centrum.cz
- Initial spec
