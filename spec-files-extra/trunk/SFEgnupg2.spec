#
# spec file for package SFEgnupg
#
# includes module(s): gnupg
#
#

%include Solaris.inc
%include packagenamemacros.inc
%include usr-gnu.inc

%use gnupg = gnupg2.spec

Name:          SFEgnupg2
IPS_component_version: crypto/gnupg2
Summary:       %{gnupg.summary} (/usr/gnu)
Version:       %{gnupg.version}
Patch1:        gnupg2-01-asschk.diff
Patch2:        gnupg2-02-inittests.diff
Patch3:        gnupg2-03-jnlib-Makefile.diff
Patch4:        gnupg2-04-keyserver-sm-Makefile.diff
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWbzip
Requires: SUNWzlib
Requires: %{pnm_requires_library_readline}
BuildRequires: %{pnm_buildrequires_library_readline}
BuildRequires: SFElibksba
#BuildRequires: SFEpth
BuildRequires: SUNWpth
BuildRequires: SFElibassuan
Requires: SFElibksba
#Requires: SFEpth
Requires: SUNWpth
Requires: SFElibassuan
Requires: SUNWcurl
%if %build_l10n
Requires: SFEgettext
Requires: SFElibiconv
%endif

%if %build_l10n
%package l10n
IPS_component_version: sfe/crypto/gnupg2-l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %{name}
%endif

%prep
rm -rf %name-%version
mkdir -p %name-%version
%gnupg.prep -d %name-%version
cd %name-%version
#%patch1 -p0
#%patch2 -p0
#%patch3 -p0
#%patch4 -p0
cd ..

%build
export PATH="$PATH:%{_bindir}"
export CFLAGS="%optflags %{gnu_inc}"
export MSGFMT="/usr/bin/msgfmt"
export LDFLAGS="%{gnu_lib_path} %_ldflags -lsocket"
%if %build_l10n
LDFLAGS="$LDFLAGS -lintl -liconv"
LIBINTL="/usr/gnu/lib/libintl.so"
%endif
%gnupg.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gnupg.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -rf $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm -rf $RPM_BUILD_ROOT%{_datadir}/info

#
# Rename 2 files to be compatible with SFEgnupg (GnuPG version 1.x)
# package.
#
mv $RPM_BUILD_ROOT%{_docdir}/gnupg/FAQ \
    $RPM_BUILD_ROOT%{_docdir}/gnupg/FAQ2
mv $RPM_BUILD_ROOT%{_docdir}/gnupg/faq.html \
    $RPM_BUILD_ROOT%{_docdir}/gnupg/faq2.html

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gnupg
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/gnupg
%{_docdir}/gnupg/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (0755, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (0755, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Oct 14 2013 - Thomas Wagner
- bump to 2.0.22
* Wed Oct  2 2013 - Thomas Wagner
- add %{gnu_inc} to CFLAGS (find SFElibassuan)
- change (Build)Requires to SUNWpth (2.0.7 is good enough)
* Sat Dec 15 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_library_readline}, %include packagenamemacros.inc
* Thu May 17 2012 - Thomas Wagner
- add IPS package name
* Mars 24 2010 - Gilles dauphin
- look at _bindir in PATH , (where it install)
- some software is here...
* Sat Jul 11 2009 - Thomas Wagner
- add (Build-)Requires: SFElibksba, SFEpth, SFElibassuan
- switch (Build-)Requires: from SFEreadline(-devel) to SUNWgnu-readline
* Thu Oct 2 2008 - markwright@internode.on.net
- Add patch 3 and 4 from KDE4 project to fix build issues on sol10
* Sun Jan 20 2008 - moinak.ghosh@sun.com
- Fixed various nits.
- Fixed build using SUN Studio.
* Sat Dec 29 2007 - jijun.yu@sun.com
- initial version created
