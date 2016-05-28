%include Solaris.inc
%define cc_is_gcc 1
%include usr-gnu.inc
%include base.inc
%include packagenamemacros.inc

Name:                SFEgit
IPS_Package_Name:    sfe/developer/versioning/git
Summary:             A fast version control system
Version:             2.8.3
License:             GPLv2
SUNW_Copyright:      git.copyright
URL:                 http://git-scm.com/
Source:		     http://www.kernel.org/pub/software/scm/git/git-%version.tar.xz
SUNW_BaseDir:        %{_basedir}

%include default-depend.inc
Requires: SUNWzlib
Requires: %{pnm_requires_SUNWsshu}
BuildRequires: %{pnm_buildrequires_SUNWopenssl_include}
Requires: %{pnm_requires_SUNWopenssl_libraries}
Requires: SUNWlexpt
Requires: SUNWcurl
Requires: %{pnm_requires_perl_default}
Requires: SUNWbash
Requires: SUNWlexpt
Requires: %{pnm_requires_text_gnu_diffutils}
Requires: SUNWTk
BuildRequires: %{pnm_buildrequires_SFEasciidoc}
BuildRequires: developer/documentation-tool/xmlto
BuildRequires: library/pcre

%prep
%setup -q -n git-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export CPPFLAGS=-I/usr/include/pcre
make configure
./configure \
	--prefix=%_prefix \
	--libexecdir=%_libexecdir \
	--with-libpcre \
	--with-editor=emacsclient \
	--with-perl=/usr/perl5/bin/perl \
	--with-python=/usr/bin/python3
make -j$CPUS all doc
# Making info files requires docbook2X, which requires a little effor to get working
#make -j$CPUS all man info


%install
rm -rf %buildroot

make install install-doc DESTDIR=$RPM_BUILD_ROOT INSTALL=install
#make install install-man install-info DESTDIR=%buirdroot INSTALL=install

# remove unwanted stuff like .packlist and perllocal.pod
#rm $RPM_BUILD_ROOT%{_libdir}/*-solaris-*/perllocal.pod
#rmdir $RPM_BUILD_ROOT%{_libdir}/*-solaris-*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/git*
%_libdir
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gitk
%dir %{_datadir}/git-core
%dir %{_datadir}/git-core/templates
%{_datadir}/git-core/templates/branches
%{_datadir}/git-core/templates/description
%{_datadir}/git-core/templates/info
%dir %{_datadir}/git-core/templates/hooks
%defattr (0644, root, bin)
%{_datadir}/git-core/templates/hooks/*
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_datadir}/git-gui
%dir %attr (0755, root, bin) %{_datadir}/git-gui/lib
%{_datadir}/git-gui/lib/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man?
%{_mandir}/man?/*
%{_datadir}/gitweb
%if %{_share_locale_group_changed}
%dir %attr (0755, root, %{_share_locale_group}) %{_datadir}/locale
%defattr (-, root, %{_share_locale_group})
%else
%dir %attr (0755, root, other) %{_datadir}/locale
%defattr (-, root, other)
%endif
#END if _share_locale_group_changed
%{_datadir}/locale/*

%changelog
* Fri May 27 2016 - Alex Viskovatoff <herzen@imap.cc>
- bump to 2.8.3
* Tue Mar 22 2016 - Alex Viskovatoff <herzen@imap.cc>
- bump to 2.7.4
* Sun Jan 31 2016 - Alex Viskovatoff <herzen@imap.cc>
- update to 2.7.0; enable support for Perl-compatible regexes
- fix git-svn by not making the spec interfere with upstream's standard install
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
* Fri Apr 26 2014 - Thomas Wagner
- use auto-switch for changing group owner of /usr/gnu/share/locale
- change (Build)Requires to %{pnm_buildrequires_SFEasciidoc} (S12)
* Sun Feb 9  2014 - Alex Viskovatoff
- update to 1.8.5.4
* Thu Sep 12 2013 - Alex Viskovatoff
- bump to 1.8.3
* Sat Apr 6 2012 - Logan Bruns <logan@gedanken.org>
- updated to 1.8.2
* Thu Mar 7 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.8.1.3
* Mon Feb 4 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.8.1.2
* Sat Jan 12 2013 - Logan Bruns <logan@gedanken.org>
- bump to 1.8.1
* Wed Dec 12 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.8.0.2
* Thu Oct 25 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.8.0 and updated a patch.
* Fri Sep 7 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.7.12
* Tue Aug 16 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.7.11.5
* Sat Jun 23 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.7.11.1 and switch to python3.2
* Mon Jun 18 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.7.11
* Wed Jun 6 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.7.10.4
* Sun May 28 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.7.10.3
* Sun May 20 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.7.10.2
* Tue May 8 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.7.10.1
* Fri Apr 20 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.7.10, update a patch and update files.
* Tue Feb 14 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.7.9
* Wed Oct 13 2011 - Alex Viskovatoff
- Bump to 1.7.7; add IPS_package_name
* Sun Aug  7 2011 - Alex Viskovatoff
- install in /usr/gnu, to avoid conflict with system package
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Tue Jun 7 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 1.7.5.4
* Sat Apr 16 2011 - Alex Viskovatoff
- Bump to 1.7.4.4
* Sat Mar 26 2011 - Thomas Wagner
- fix compiler options by setting cc_is_gcc 1 and gcc to be sfw version
* Mon Mar 21 2011 - Alex Viskovatoff
- Update to 1.7.4.1, adding one patch
* Tue Oct 21 2008 - halton.huo@sun.com
- Bump to 1.6.0.2
* Tue Sep 02 2008 - halton.huo@sun.com
- Bump to 1.6.0.1
- Remove upstreamed patch git-03-tr.diff
* Wed Apr 23 2008 - trisk@acm.jhu.edu
- Add patch3 to fix bisect problem with non-GNU tr
* Thu Mar 13 2008 - nonsea@users.sourceforge.net
- s/SFEcurl/SUNWcurl
* Fri feb 22 2008 - brian.cameron@sun.com
- Add patch git-02-fixshell.diff to fix a build problem caused
  by a script that requires bash.
* Thu Feb 21 2008 - nonsea@users.sourceforge.net
- Bump to 1.5.4.2
* Thu Dec 06 2007 - brian.cameron@sun.com
- Bump to 1.5.3.7.
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Change LDFLAGS to work for gcc.
* Tue Sep 18 2007 - brian.cameron@sun.com
- Bump to 1.5.3.
* Thu Jul 05 2007 - alberto.ruiz@sun.com
- fixing hook templates permisions
* Tue Jul 03 2007 - alberto.ruiz@sun.com
- changing version to 1.5.2.2 and declaring new files
* Fri Jun 22 2007 - laca@sun.com
- make it build with either SUNWgnu-diffutils or SFEdiffutils
* Tue Feb 13 2007 - laca@sun.com
- finish Erwann's spec
* Tue Feb 13 2007 - erwann@sun.com
- Initial spec
