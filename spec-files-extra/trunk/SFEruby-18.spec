#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SFEruby
#
# includes module(s): ruby
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define release_version 1.8.7
%define patch_level 371

Name:         SFEruby-18
IPS_Package_Name:	sfe/runtime/ruby-18
Summary:      ruby - object oriented scripting language
URL:          http://www.ruby-lang.org/
Version:      %{release_version}.%{patch_level}
%define tarball_version %{release_version}-p%{patch_level}
Source:	      http://ftp.ruby-lang.org/pub/ruby/1.8/ruby-%{tarball_version}.tar.bz2
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:     SUNWlibmsr
Requires:     SUNWopenssl-libraries
Requires:     SUNWzlib
Conflicts:    SUNWruby18u
BuildRequires:     SFElibyaml
Requires:     SFElibyaml

%prep
%setup -q -n ruby-%{tarball_version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}              \
            --mandir=%{_mandir}              \
            --libdir=%{_libdir}              \
            --enable-shared

make -j$CPUS
	
%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install-doc DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.*
%{_libdir}/ruby/*
#%dir %attr (0755, root, other) %{_libdir}/pkgconfig
#%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/ri
#%dir %attr (0755, root, other) %{_docdir}
#%{_docdir}/ruby
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
#%dir %attr (0755, root, bin) %{_includedir}
#%{_includedir}/*

%changelog
* Sat Jan 26 2013 - Logan Bruns <logan@gedanken.org>
- forked from 1.9 back to 1.8 series to get newer patched version of 1.8.7
- switched to gcc
- added back in libruby-static
* Fri Dec 21 2012 - Logan Bruns <logan@gedanken.org>
- added (build)requires libyaml.
* Thu Dec 20 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.9.3-p327
- added ips name
- fixed some permissions
* Sun Sep 25 2011 - Thomas Wagner
- bump to 1.9.3
* Thu Jan 24 2008 - nonsea@users.sourceforge.net
- Add Conflicts: SUNWruby18u
* Sun Jan 06 2008 - moinak.ghosh@sun.com
- Enable building libruby.so shared library
* Thu Dec 27 2007 - sobotkap@centrum.cz
- bump to 1.9.0
* Sun Oct 14 2007 - laca@sun.com
- bump to 1.8.6-p111; delete upstream patch
* Sun Sep 09 2007 - Ananth Shrinivas <ananth@sun.com>
- YAML files required for ruby RDoc documentation need to be installed
* Sat Apr 21 2007 - dougs@truemail.co.th
- added isinf to configure.in to force configureto not add internal isinf
- for Solaris 11
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Bump to 1.8.6
- Add URL
- Remove patch ieeefp.diff, upstreamed.
* Tue Sep 26 2006 - halton.huo@sun.com
- Add Requires after check-deps.pl run
* Mon Sep 11 2006 - halton.huo@sun.com
- Bump to 1.8.5
* Sun Jul  2 2006 - laca@sun.com
- rename to SFEruby
- delete -share subpkg
- update file attributes
- add patch eeefp.diff that fixes the build where functions like
  finite() and isnan() are undefined
* Wed Nov 16 2005 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec

