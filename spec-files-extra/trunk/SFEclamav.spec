#
# spec file for package SFEclamav
#
# includes module(s): clamav
#
%include Solaris.inc
%include packagenamemacros.inc


%define	src_name clamav
%define _pkg_docdir %_docdir/%src_name

Name:                SFEclamav
IPS_Package_Name:	antivirus/clamav
Summary:             Unix anti-virus scanner
License:             GPLv2
SUNW_Copyright:      clamav.copyright
Version:             0.99
URL:                 http://www.clamav.net/
Source:              %{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
Source2:             clamav.xml
Source3:             clamav-milter.xml
Group:               Applications/System Utilities
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: %{pnm_buildrequires_SUNWncurses_devel}
Requires:      %{pnm_requires_SUNWncurses}
BuildRequires:	SUNWsndmu
Requires:	SUNWsndmu

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package doc
Summary:                 %{summary} - Documentation
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
cp %{SOURCE2} clamav.xml
cp %{SOURCE3} clamav-milter.xml

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
            --sbindir=%{_sbindir}		\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --sysconfdir=%{_sysconfdir}		\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --with-libncurses-prefix=/usr/gnu	\
	    --disable-static			\
	    --enable-shared			\
	    --enable-milter			\
	    --disable-clamav			\
	    --with-dbdir=%{_localstatedir}/clamav

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/clamav
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp clamav.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp clamav-milter.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%clean
rm -rf $RPM_BUILD_ROOT

%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/groupadd clamav';
  echo '/usr/sbin/useradd -d /var/clamav -s /bin/true -g clamav clamav';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%postun root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/userdel clamav';
  echo '/usr/sbin/groupdel clamav';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%actions
#group groupname="clamav"
user ftpuser=false gcos-field="ClamAV Reserved UID" username="clamav" password=NP group="other"

%files
%defattr (-, root, bin)
%{_bindir}
%{_sbindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin) 
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files root
%defattr (-, root, sys)
%{_sysconfdir}
%dir %attr (0775, clamav, clamav) %{_localstatedir}/clamav
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/clamav.xml
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/clamav-milter.xml

%files doc
%defattr (-, root, bin)
%doc FAQ README ChangeLog COPYING COPYING.LGPL COPYING.bzip2 COPYING.file COPYING.getopt COPYING.llvm COPYING.lzma COPYING.regex COPYING.unrar COPYING.zlib
%doc -d docs clamdoc.pdf phishsigs_howto.pdf signatures.pdf
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}

%changelog
* Wed Jan  3 2016 - Thomas Wagner
- bump to 0.98
- fix %files
* Tue Dec 10 2013 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWncurses_devel}, %include packagenamemacros.inc
* Mon Nov 4 2013 - Logan Bruns <logan@gedanken.org>
- updated to 0.98
* Sat Jun 29 2013 - Logan Bruns <logan@gedanken.org>
- updated to 0.97.8
* Tue Mar 19 2013 - Logan Bruns <logan@gedanken.org>
- updated to 0.97.7
* Tue Jan 15 2013 - Logan Bruns <logan@gedanken.org>
- added smf services for clamd and clamav-milter
* Mon Oct 01 2012 - Milan Jurik
- bump to 0.97.6
* Sun Jul 29 2012 - Milan Jurik
- bump to 0.97.5
* Sat Jun 02 2012 - Milan Jurik
- bump to 0.97.4
* Sun Dec 11 2011 - Milan Jurik
- bump to 0.97.3
* Tue Aug 23 2011 - Milan Jurik
- bump to 0.97.2
- move docs to doc package and fix docdir group
* Thu Jul 28 2011 - Alex Viskovatoff
- add SUNW_Copyright and package some files in /usr/share/doc/clamav
* Tue Jul 12 2011 - Milan Jurik
- bump to 0.97.1
* Sun Feb 13 2011 - Milan Jurik
- bump to 0.97
* Tue Nov 30 2010 - Milan Jurik
- bump to 0.96.5
* Fri Sep 24 2010 - Milan Jurik
- bump to 0.96.3
* Tue Sep 07 2010 - Milan Jurik
- bump to 0.96.2
* Sun Aug 08 2010 - Milan Jurik
- bump to 0.96.1
* Sun Apr 25 2010 - Milan Jurik
- added IPS support
* Thu Apr 01 2010 - Milan Jurik
- update to 0.96
* Sat Sep 19 2009 - Milan Jurik
- update to 0.95.2
* Fri Jul 27 2007 - dougs@truemail.co.th
- Initial spec
