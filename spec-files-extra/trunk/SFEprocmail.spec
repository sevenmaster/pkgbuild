# this spec file only makes sense on OmniOSce
# every other OSDISTRO has procmail in the repositories


#
# spec file for package SFEprocmail
#
# includes module(s): procmail
#
%include Solaris.inc

Name:                    SFEprocmail
IPS_Package_Name:        mail/procmail
Summary:                 Procmail
Version:                 3.22
#Source:                 http://www.procmail.org/procmail-%{version}.tar.gz
Source:                  ftp://ftp.informatik.rwth-aachen.de/pub/packages/procmail/procmail-%version.tar.gz
#Patch1:			 procmail-01-configuration.diff
#Patch2:			 procmail-02-debian.diff
#Patch3:			 procmail-03-large-files.diff



#import patches from openindiana userland - merge 01-procmail-3.22-8.debian.patch with our's and put remaining lines into procmail-22-patches-merged-debian-sfe.diff below
Patch1:			procmail-01-procmail-3.22-8.debian.patch
Patch2:			procmail-02-procmail-3.22-getline.patch
Patch3:			procmail-03-procmail-3.22-ipv6.patch
Patch4:			procmail-04-procmail-3.22-rhconfig.patch
Patch5:			procmail-05-procmail-3.22-truncate.patch
Patch6:			procmail-06-CVE-2014-3618.patch
Patch7:			procmail-07-CVE-2017-16844.patch

#older patche had more then procmail-01-procmail-3.22-8.debian.patch
Patch22:			procmail-22-patches-merged-debian-sfe.diff
#try if this is still necessary
Patch23:			procmail-23-large-files.diff

#import patches form solaris userland
Patch27:		procmail-27-07-use-libc-strstr.patch
Patch28:		procmail-28-08-binary-logic.patch


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms


%prep
%setup -q -n procmail-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%patch22 -p1
%patch23 -p1

%patch27 -p1
%patch28 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make BASENAME=${RPM_BUILD_ROOT}%{_prefix}	\
     MANDIR=${RPM_BUILD_ROOT}%{_mandir} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/formail
%attr (2755,root,mail) %{_bindir}/lockfile
%{_bindir}/mailstat
%attr (6755,root,mail) %{_bindir}/procmail
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*

%changelog
* Sat Jan 13 2018 - Thomas Wagner
- add IPS_Package_Name mail/procmail
- merge with OpenIndiana userland patches, including procmail-06-CVE-2014-3618.patch procmail-07-CVE-2017-16844.patch
- import solaris userland patches procmail-27-07-use-libc-strstr.patch procmail-28-08-binary-logic.patch
* Sat Apr 16 2011 - Alex Viskovatoff
- update source URL (does not currently build, apparently because of a change in Sun Studio)
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEprocmail
- remove unnecessary env variables
- update file attributes to match JDS
* Thu Oct 21 2005 - glynn.foster@sun.com
- Initial spec
