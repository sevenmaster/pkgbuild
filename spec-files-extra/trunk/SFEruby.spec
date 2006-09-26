#
# spec file for package SFEruby
#
# includes module(s): ruby
#
%include Solaris.inc

Name:         SFEruby
Summary:      ruby - object oriented scripting language
Version:      1.8.5
Source:	      ftp://ftp.ruby-lang.org/pub/ruby/ruby-%{version}.tar.gz
Patch1:       ruby-01-ieeefp.diff
URL:          http://www.ruby-lang.org
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:     SUNWlibmsr
Requires:     SUNWopenssl-libraries
Requires:     SUNWzlib

%prep
%setup -q -n ruby-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
autoconf
./configure --prefix=%{_prefix}              \
            --mandir=%{_mandir}              \
            --libdir=%{_libdir}

make -j$CPUS
	
%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%changelog
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

