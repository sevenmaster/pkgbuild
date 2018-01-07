#
# spec file for package SFEunison
#
# includes module(s): unison
#

%include Solaris.inc
%include usr-gnu.inc
%include packagenamemacros.inc

Name:                    SFEunison-gnu
IPS_Package_Name:	network/gnu/unison	
Summary:                 unison - file synchronization tool (usr/gnu)
#Version:                 2.51.0
Version:                 2.45.28
Source:                  http://www.seas.upenn.edu/~bcpierce/unison/download/releases/unison-%{version}/unison-%{version}.tar.gz
#Patch1:                  unison-01-port-sol.diff
#Patch2:                  unison-02-remote-shell.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires:    %{pnm_buildrequires_SUNWocaml}
Requires:      %{pnm_requires_SUNWocaml}
BuildRequires: SFElablgtk

%prep
%setup -q -c -n unison-%version
#%patch1 -p0
#%patch2 -p0

%build

[ -d src ] && cd src
[ -d unison* ] && cd unison*

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS=""
export LDFLAGS=""

#FIXME: make -i$CPUS fail on multiple cpus machines
#make -j$CPUS UISTYLE=text
make UISTYLE=text
mv unison unison-%{version}
#make -j$CPUS UISTYLE=gtk2
#make UISTYLE=gtk2
#mv unison unisongui
#mv unison-%{version} unison

%install
rm -rf $RPM_BUILD_ROOT

#[ -d src ] && cd src
#[ -d unison* ] && cd unison*

mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp unison $RPM_BUILD_ROOT%{_bindir}
#cp unisongui $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Thu Dec 14 2017 - Thomas Wagner
- bump to 2.51.0
* Sun Jul 20 2014 - Thomas Wagner
- bump to 2.45.28
- %include usr-gnu.inc
- rename to  SFEunison-gnu
- add IPS_Package_Name network/gnu/unison	
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to 2.27.57
* Tue Sep 18 2007 - flistellox@gmail.com
- Version Bump to 2.27.29
* Thu Aug 24 2006 - halton.huo@sun.com
- Rename patch1, add new patch patches/unison-02-remote-shell.diff.
* Thu Jul 27 2006 - halton.huo@sun.com
- Change SFEocaml and SFElablgtk to BuildRequires.
- Correct make fail on multiple machines, need fix it later.
* Sat Jul 15 2006 - laca@sun.com
- split ocaml and lablgtk into their own pkgs
- simplify build
* Tue May 30 2006 - halton.huo@sun.com
- Add patch unison-01.diff.
* Mon May 29 2006 - halton.huo@sun.com
- Initial spec file
