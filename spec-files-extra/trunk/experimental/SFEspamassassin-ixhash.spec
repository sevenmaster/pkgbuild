#
# spec file for package SFEspamassassin-ixhash
#

%include Solaris.inc

%define perl_version 5.8.4

%define pluginlocationold /etc/mail/spamassassin/iXhash.pm
%define pluginlocationnew %{_prefix}/perl5/vendor_perl/%{perl_version}/Mail/SpamAssassin/Plugin/iXhash.pm
%define gnumd5sum /usr/gnu/bin/md5sum
%define gnutr /usr/gnu/bin/tr



Name:                    SFEspamassassin-ixhash
Summary:                 spamassassin-ixhash - plugin to use german ix magazine's spam email detection
Version:                 1.5.5
Source:                  %{sf_download}/project/ixhash/iXhash/iXhash-%{version}/iXhash-%{version}.tgz
URL:			 http://www.heise.de/ix/nixspam/
##URL2:			 http://ixhash.sourceforge.net/listinfo.html


SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

Requires:      SFEspamassassin
#like gnu/tr gnu/md5sum
Requires:      SUNWgnu-coreutils

%include default-depend.inc


%prep
%setup -q -n iXhash-%version

perl -w -pi.bak1 -e "s,%{pluginlocationold},%{pluginlocationnew}," iXhash/iXhash.cf
perl -w -pi.bak2 -e "s,/usr/bin/tr,%{gnutr}," iXhash/iXhash.cf
perl -w -pi.bak3 -e "s,/usr/bin/md5sum,%{gnumd5sum}," iXhash/iXhash.cf


%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/perl5/vendor_perl/%{perl_version}/Mail/SpamAssassin/Plugin/
cp -p iXhash/iXhash.pm $RPM_BUILD_ROOT/%{_prefix}/perl5/vendor_perl/%{perl_version}/Mail/SpamAssassin/Plugin/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/spamassassin/
cp -p iXhash/iXhash.cf $RPM_BUILD_ROOT/%{_sysconfdir}/spamassassin/
#in case old pkgbuild does not automaticly place %doc files there
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir -p $RPM_BUILD_ROOT%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

%files
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr(0755, root, bin) %{_prefix}/perl5
%{_prefix}/perl5/*
%attr (0755, root, sys) %dir %{_sysconfdir}
%attr (0755, root, bin) %dir %{_sysconfdir}/spamassassin
%class(renamenew) %{_sysconfdir}/spamassassin/*
%defattr(-, root, bin)
#%doc README CHANGELOG INSTALL LICENSE WHERE_ARE_THE_OTHER_FILES
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}

%changelog
* Thr Aug 07 2009  - Thomas Wagner
- Initial spec
