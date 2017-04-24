



#
# spec file for package SFEautossh
#
# includes module(s): autossh
#
%include Solaris.inc
%include packagenamemacros.inc
%define srcname autossh

Name:		SFEautossh
IPS_Package_Name:	system/network/autossh
Summary:	Automatically restart SSH sessions and tunnels
Group:		Applications/Internet
URL:		http://www.harding.motd.ca/autossh/
License:	Distributable
Version:	1.4e
IPS_Component_Version: 1.4.0.5
Source:		http://www.harding.motd.ca/autossh/autossh-%version.tgz
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc


%description
autossh
Automatically restart SSH sessions and tunnels
autossh is a program to start a copy of ssh and monitor it, restarting
it as necessary should it die or stop passing traffic.


%prep
%setup -q -n autossh-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

gsed -i.bak -e 's?-std=c99??' configure

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}

install autossh $RPM_BUILD_ROOT%{_bindir}
install autossh.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/autossh
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/autossh.1

%changelog
* Mon Apr 24 2017 - Thomas Wagner
- Initial spec version 1.4e (IPS 1.4.0.5)
