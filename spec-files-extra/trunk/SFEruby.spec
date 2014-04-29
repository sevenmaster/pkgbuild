#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include packagenamemacros.inc

Name:         SFEruby
IPS_Package_Name:	runtime/ruby-21
Summary:      Object oriented scripting language
URL:          http://www.ruby-lang.org/
Version:      2.1.1
Source:       http://cache.ruby-lang.org/pub/ruby/2.1/ruby-%version.tar.gz
Patch1:       ruby-01-endian.diff
#Patch2:       ruby-02-small-files-for-libelf.diff
SUNW_BaseDir: %{_basedir}
%include default-depend.inc
Requires:     SUNWlibmsr
Requires:     %{pnm_requires_openssl}
Requires:     SUNWzlib
Conflicts:    SUNWruby18u
BuildRequires:     SFElibyaml

%prep
%setup -q -n ruby-%version
%patch1 -p1
#%patch2 -p1


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
export CFLAGS="-xc99 %optflags"
export LDFLAGS="%_ldflags"
autoconf
./configure --prefix=%_prefix              \
            --enable-shared

make -j$CPUS
	
%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install-doc DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libruby*.a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.*
%{_libdir}/ruby/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/ri
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/ruby
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Apr 29 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- update to 2.1.1
* Mon Mar 24 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- %include packagenamemacros.inc
- change Requires to %{pnm_requires_openssl}
* Sat Feb 22 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Fix libyaml (build)requires name
* Thu Jan 30 2014 - Alex Viskovatoff
- update to 2.1.0
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

