#
# spec file for package SFEtwolame
#
# includes module(s): twolame
#
%include Solaris.inc

Name:                    SFEtwolame
Summary:                 twolame - MP3 Encoder
Version:                 0.3.10
Source:                  http://www.ecs.soton.ac.uk/~njh/twolame/twolame-%{version}.tar.gz
Patch1:			 twolame-01-configure.diff
Patch2: 		 twolame-02-crossfile_inline.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibsndfile
Requires: SUNWlibms
BuildRequires: SFElibsndfile-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFElibsndfile-devel

%prep
%setup -q -n twolame-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -xcrossfile=1"
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Nov 4 2007 - markwright@internode.on.net
- Bump to 0.3.10.  Bump patch1 and patch2.
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEtwolame
- delete -share subpkg
- update file attributes
- add missing dep
* Mon Jun 13 2006 - drdoug007@yahoo.com.au
- Initial version
