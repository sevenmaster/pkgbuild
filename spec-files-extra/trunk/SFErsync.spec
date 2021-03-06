#
# spec file for package SFErsync
#

%include Solaris.inc
%include usr-gnu.inc

Name:                    SFErsync
IPS_Package_Name:	 sfe/network/rsync
Summary:                 rsync - fast incremental file transfer (%{_basedir}/gnu/bin/rsync)
URL:                     http://rsync.samba.org/
Version:                 3.1.2
Source:                  http://rsync.samba.org/ftp/rsync/rsync-%{version}.tar.gz
Patch1:                  rsync-01-15730984.diff
Patch4:                  rsync-04-CVE-2017-17433.diff
License:		 GPLv3
SUNW_Copyright:		 rsync.copyright

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc


%prep
%setup -q -n rsync-%version

#shorten path names referencing source file names
%patch1 -p1

#CVE-2017-17433
%patch4 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
##export CC=/usr/gnu/bin/gcc
##export CXX=/usr/gnu/bin/g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --disable-static


gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
#in case old pkgbuild does not automaticly place %doc files there
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc COPYING INSTALL NEWS OLDNEWS README TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Sat Dec  9 2017 - Thomas Wagner
- patch4 fix for CVE-2017-17433 (rsync-04-CVE-2017-17433.diff) imported
- patch1 remove path from source file names (rsync-01-15730984.diff) imported
* Sat Feb 13 2016 - Thomas Wagner
- bump to 3.1.2 - bug and security fix
* Fri Jan 24 2014 - Thomas Wagner
- bump to 3.1.0
- add IPS_Package_Name
* Sat Mar 31 2012 - Pavel Heimlich
- rsync 3.0.9
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Fri Apr 01 2011 - Thomas Wagner
- Initial spec
