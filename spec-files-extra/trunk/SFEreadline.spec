#
# spec file for package SFEreadline
#
# includes module(s): GNU readline
#
%include Solaris.inc
%include usr-gnu.inc
%include base.inc

Name:                    SFEreadline
IPS_Package_Name:	 library/gnu/readline
Summary:                 GNU readline - library for editing typed command lines (/usr/gnu)
Version:                 6.3
Source:			 http://ftp.gnu.org/gnu/readline/readline-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWpostrun
Requires: SUNWtexi

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -pr readline-%{version} readline-%{version}-64
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

#export CFLAGS32="%optflags -I/usr/sfw/include -DANSICPP"
#export CFLAGS64="%optflags64 -I/usr/sfw/include -DANSICPP"
export CFLAGS32="%optflags -DANSICPP"
export CFLAGS64="%optflags64 -DANSICPP"
export LDFLAGS32="%_ldflags -lcurses"
export LDFLAGS64="%_ldflags -lcurses"

%ifarch amd64 sparcv9
export CC=${CC64:-$CC}
export CXX=${CXX64:-$CXX}
export CFLAGS="$CFLAGS64"
export CXXFLAGS="$CXXFLAGS64"
export LDFLAGS="$LDFLAGS64"

cd readline-%{version}-64

./configure --prefix=%{_prefix}				\
	    --libdir=%{_libdir}/%{_arch64}		\
	    --libexecdir=%{_libexecdir}/%{_arch64}	\
	    --mandir=%{_mandir}                 	\
	    --datadir=%{_datadir}               	\
            --infodir=%{_datadir}/info
	    		
make -j$CPUS
cd ..
%endif

cd readline-%{version}

export CC=${CC32:-$CC}
export CFLAGS="$CFLAGS32"
export LDFLAGS="$LDFLAGS32"

./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}                 \
	    --libexecdir=%{_libexecdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info
	    		
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd readline-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd readline-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3gnu
sed -e 's/^\.TH \([^ ]*\) "*3"*/.TH \1 "3GNU"/' $RPM_BUILD_ROOT%{_mandir}/man3/history.3 > $RPM_BUILD_ROOT%{_mandir}/man3gnu/history.3
rm $RPM_BUILD_ROOT%{_mandir}/man3/history.3
rm $RPM_BUILD_ROOT%{_datadir}/info/dir

rm $RPM_BUILD_ROOT%{_libdir}/lib*a

#looks empty
rmdir $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*
%dir %attr(0755, root, other) %_docdir
%_docdir/readline
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/*


%changelog
* Sat Sep 19 2015 - Alex Viskovatoff
- update to 6.3; remove %post and %preun sections "discouraged" by the documentation
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
* Wed Aug 14 2013 - Thomas Wagner
- fix %files
* Sun Dec 16 2012 - Thomas Wagner
- move to /usr/gnu to avoid duplicate files with OS provided readline
- add IPS_Package_Name
* Tue Jun  7 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 6.2
* Mon May 14 2007 - dougs@truemail.co.th
- Forced to link with libcurses
* Tue Mar  7 2007 - dougs@truemail.co.th
- enabled 64-bit build
* Mon Jan 15 2007 - daymobrew@users.sourceforge.net
- Add SUNWtexi dependency.
* Sun Nov  5 2006 - laca@sun.com
- Create
