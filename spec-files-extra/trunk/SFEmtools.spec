#
# spec file for package SFEmtools
#
# includes module(s): mtools
#
%include Solaris.inc

Name:                    SFEmtools
Summary:                 mtools - utilities to access MS-DOS disks from Unix
Version:                 4.0.17
#Source:			 http://mtools.linux.lu/mtools-%{version}.tar.bz2
#temporary download location (they do not keep <4.0 files)
#Source:                  http://pkgs.fedoraproject.org/repo/pkgs/mtools/mtools-3.9.11.tar.bz2/8508a3ea9b612a926f3ed0f229e6c21a/mtools-3.9.11.tar.bz2
Source:			ftp://ftp.gnu.org/gnu/mtools/mtools-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n mtools-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lnsl"

./configure --prefix=%{_prefix}			\
	    --mandir=%{_mandir}                 \
            --infodir=%{_infodir}
	    		
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'mtools.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'mtools.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr(0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*.5
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*

%changelog
* Tue Jul 24 2012 - Thomas Wagner
- bump to 4.0.17
* Sun Apr 01 2012 - Pavel Heimlich
- download location
* Wed Oct 10 2007 - trisk@acm.jhu.edu
- Initial spec
