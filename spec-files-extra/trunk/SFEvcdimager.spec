#
# spec file for package SFEvcdimager
#
# includes module(s): vcdimager
#
%include Solaris.inc
%include packagenamemacros.inc

%define	src_url	ftp://mirrors.kernel.org/gnu/vcdimager

Name:                SFEvcdimager
IPS_Package_Name:	 media/vcdimager 
Summary:             VCD mastering suite
Version:             0.7.24
%if %{oihipster}
#need to stay above the OI provided version
IPS_Component_Version: %{version}.0.1
%endif
Source:              %{src_url}/vcdimager-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

BuildRequires: SFElibcdio-devel
Requires: SFElibcdio


BuildRequires: SUNWlibms
Requires: SUNWlibms
BuildRequires: %{pnm_buildrequires_SUNWlibpopt_devel}
Requires:      %{pnm_requires_SUNWlibpopt}
BuildRequires: %{pnm_buildrequires_SUNWlxml_devel}
Requires:      %{pnm_requires_SUNWlxml}
BuildRequires: %{pnm_buildrequires_SUNWzlib}
Requires:      %{pnm_requires_SUNWzlib}


%prep
%setup -q -n vcdimager-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="-O4 -fno-omit-frame-pointer"
export CXXFLAGS="$CFLAGS"
export LDFLAGS="%arch_ldadd %ldadd ${EXTRA_LDFLAGS}"
export LD=`which ld-wrapper`
export PKG_CONFIG_PATH="/usr/lib/pkgconfig:/usr/share/pkgconfig:%{_libdir}/pkgconfig"

#libtoolize --copy --force
#aclocal -I .
#autoheader
#automake -a -f
#autoconf -f
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
            --without-versioned-libs    \
	    --disable-static		\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/lib*.*a
rm $RPM_BUILD_ROOT/%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'vcd-info.info vcdimager.info vcdxrip.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'vcd-info.info vcdimager.info vcdxrip.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE
%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_bindir}
%{_mandir}/man1
%{_datadir}/info/*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Wed Feb  1 2017 - Thomas Wagner
- need to stay above the OI provided version - add .0.1 to IPS_component_version
* Sun Nov 29 2015 - Thomas Wagner 
- change (Build)Requires to %{pnm_buildrequires_SUNWzlib} (OIH)
* Thu Jul 11 2013 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWlibpopt_devel} %{pnm_buildrequires_SUNWlxml_devel}, %include packagenamemacros.inc
* Sat Aug 18 2012 - Milan Jurik
- bump to 0.7.24
* Wed Auf 19 2009 - Thomas Wagner
- add BuildRequires: SFElibcdio-devel
- add (Build)Requires: SUNWlibms,SUNWlibpopt-devel,SUNWlibpopt,SUNWlxml-devel,SUNWlxml,SUNWzlib
* Tue Mar 17 2009 - Thomas Wagner
- builds around  > snv104 (snv104 works, 107/110 don't) start trapping over 
  detection for versioned libs, linker complains syntax, add --without-versioned-libs
* Fri May 23 2008 - michal.bielicki <at> voceworks.pl
- dependency fix, thanks to Giles Dauphin for the fix
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Build with gcc.
* Sat Jul 14 2007 - dougs@truemail.co.th
- Initial spec
