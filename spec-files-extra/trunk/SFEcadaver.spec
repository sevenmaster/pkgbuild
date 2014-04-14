#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name cadaver
%define src_url http://www.webdav.org/cadaver/

Name:		SFEcadaver
IPS_Package_Name:	web/cadaver
Summary:	command-line WebDAV client for Unix
Group:		Applications/Internet
Version:	0.23.3
License:	GPLv2+ and LGPLv2+
SUNW_Copyright:	cadaver.copyright
URL:		http://www.webdav.org/cadaver/
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		cadaver-01-locale.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SFEneon-gnu
Requires:	SFEneon-gnu

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
./configure --prefix=%{_prefix}		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir}	\
	--enable-threads=solaris

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
#REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Thu Apr 10 2014 - Thomas Wagner
- Needs /usr/gnu/lib*curses* and /usr/gnu/libreadline or get tgetent not implemented error
  change (Build)Requires SFEneon (will be found first, so we should depend on it)
- add IPS_Package_Name and group
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sat Mar 26 2011 - Milan Jurik
- initial spec
