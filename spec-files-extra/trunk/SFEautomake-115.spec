#
# spec file for package SFEautomake-115
#
# includes module(s): automake
#
%include Solaris.inc
##%include osdistro.inc

%define _use_internal_dependency_generator 0

##TODO## make auto-rename package to upgrade automake-111 to this one here
##       if that works. old spec file would require -111 and automaticly
##       get -115 installed.

Name:		SFEautomake-115
IPS_Package_Name:	developer/build/automake-115
Summary:	GNU Automake 1.15
License:	GPLv2
URL:		http://http://www.gnu.org/software/automake/
Version:	1.15
Source:		http://ftp.gnu.org/gnu/automake/automake-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEautoconf-gnu
Requires:      SFEautoconf-gnu
##%endif


%description
additional package to get automake-%{version} added.
Note: this package does not deliver all documentation,
it delivers versioned manpages

%prep
%setup -q -n automake-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}

make -j$CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
/bin/rm -f %{buildroot}/%{_bindir}/aclocal
/bin/rm -f %{buildroot}/%{_bindir}/automake
/bin/rm -rf %{buildroot}/%{_infodir}
/bin/rm -rf %{buildroot}/%{_datadir}/doc
/bin/rm -rf %{buildroot}/%{_datadir}/aclocal
/bin/rm -rf %{buildroot}/%{_mandir}/man1/automake.1
/bin/rm -rf %{buildroot}/%{_mandir}/man1/aclocal.1

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/aclocal-%{version}
%{_datadir}/automake-%{version}
%{_mandir}

%changelog
* Wed Dec  2 2015 - Thomas Wagner
- bump to 1.15 after svn copy SFEautomake-114.spec SFEautomake-115.spec
* Wed Jan  1 2014 - Thomas Wagner
- try (Build)Requires: SFEautoconf-gnu unconditionally
* Mon Dec 23 2013 - Thomas Wagner
- add (Build)Requires: SFEautoconf-gnu >= 2.65
* Fri Dec  6 2013 - Thomas Wagner
- bump to 1.14
* Tue Oct 11 2011 - Milan Jurik
- Initial spec
* Wed Oct 19 2011 - brian.cameron@oracle.com
- Do not install %{_datadir}/doc since it conflicts with the installed 
  automake if installed via IPS.
