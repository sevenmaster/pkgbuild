#
# spec file for package SFEautoconf
#
# includes module(s): GNU autoconf
#
%include Solaris.inc
%include usr-gnu.inc

%define _infodir           %{_datadir}/info

##TODO## look for a better way to handle multiple versions of
##       autoconf and find a maybe better location then /usr/gnu/
##       if there is any. Or decide if its better to just use
##       this newer version randomly in our spec files (it will
##       be found by PATH=/usr/gnu/bin:$PATH accidentially and
##       then we have an unstable build-time-dependency chain...
##       Do we want a versioned pacakge name similar to SFEautomake-114?
##       developer/build/gnu/autoconf-269 

Name:                    SFEautoconf-gnu
IPS_Package_name:	developer/build/gnu/autoconf
Summary:                 GNU autoconf - scripts and macros for configuring source code packages (installs in /usr/gnu)
Version:                 2.69
Source:			 http://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %(pkginfo -q SUNWgm4 && echo 1 || echo 0)
Requires: SUNWgm4
%else
Requires: SFEm4
%endif
Requires: SUNWpostrun
Requires: SUNWtexi
##TODO## check if we need SFEemacs
#update description
#Requires: SFEemacs


%description
autoconf version %{version}, needed by some spec files to
build. Stored in /usr/gnu to keep away from OS provided 
autoconf. This package delivers no documentation files
other then /usr/gnu/share/man/man1/autoconf.1
Emacs support currently not included.


%prep
%setup -q -n autoconf-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export PATH=/usr/gnu/bin:$PATH
export PERL=/usr/perl5/bin/perl
export M4="/usr/gnu/bin/m4"
./configure --prefix=%{_prefix}			\
	    --libexecdir=%{_libexecdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_infodir}

# Note: do not try to use parallel build, it will break with broken deps
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_datadir}/info/dir
/bin/rm -rf %{buildroot}/%{_infodir}
/bin/rm -rf %{buildroot}/%{_datadir}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'autoconf.info standards.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'autoconf.info standards.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/autoconf
#%{_datadir}/info
##TODO## check if we need SFEemacs
#%dir %attr (0755, root, root) %{_datadir}/emacs
#%dir %attr (0755, root, root) %{_datadir}/emacs/site-lisp
#%{_datadir}/emacs/site-lisp/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Tue Dev 24 2013 - Thomas Wagner
- remove %{_datadir}/info from %files for the moment
* Thu Dec  5 2013 - Thomas Wagner
- bump to 2.69
- un-archive spec file
- relocate to prefix /usr/autoconf/2.69
* Thu May 22 2008 - Mark Wright <markwright@internode.on.net>
- Bump to 2.62.
* Wed Oct 17 2007 - laca@sun.com
- add support for building with either SFEm4 or SUNWgm4
* Sat Apr 21 2007 - dougs@truemail.co.th
- Add Requires: SFEemacs
* Mon Mar 18 2007 - dougs@truemail.co.th
- Changed Required Gnu m4 from SFEm4 SUNWgm4
* Mon Jan 15 2007 - daymobrew@users.sourceforge.net
- Add SUNWtexi dependency.
* Sat Jan  6 2007 - laca@sun.com
- update for SFEm4 move to /usr/gnu
- install info file and update info dir file using postrun scripts
* Fri Jan 05 2007 - daymobrew@users.sourceforge.net
- Bump to 2.61.
* Wed Sep  6 2006 - laca@Sun.com
- disable parallel build as it breaks the build
* Sun Jan 18 2006 - laca@sun.com
- rename to SFEgawk; update summary
- remove -share pkg
- make /usr/gnu/bin/awk a symlink to /usr/bin/gawk
* Thu Apr  6 2006 - damien.carbery@sun.com
- Move Build/Requires to be listed under base package to be useful.
* Sun Dec  4 2005 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec
