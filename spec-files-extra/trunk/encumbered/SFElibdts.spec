#
# spec file for package SFElibdts
#
# includes module(s): libdts
#
%include Solaris.inc

%define src_name	 libdca 

Name:                    SFElibdts
IPS_Package_Name:	 library/audio/libdca 
Summary:                 A free library for decoding DTS Coherent Acoustics streams
URL:                     http://www.videolan.org/developers/libdca.html
Version:                 0.0.5
Source:                  http://download.videolan.org/pub/videolan/%src_name/%{version}/%{src_name}-%{version}.tar.bz2
#Patch1:		 libdts-01-sigtype.diff
#Patch2:                 libdts-02-picflags.diff
#Patch2:                 libdts-02-shared.diff
#Patch3:                 libdts-03-opt.diff
Patch4:                  libdts-04-tweaks-to-fix-trivial-compiler-errors.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{src_name}-%{version}-build
%include default-depend.inc
Requires:	%{pnm_buildrequires_SUNWlibms}
Requires:	SFEliba52

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:	%name
Requires:	SFEliba52-devel

%prep
%setup -q -n %src_name-%version
#%patch1 -p1
#%patch2 -p1 -b .pic
#%patch2 -p1
#%patch3 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CPPPFLAGS="-I/usr/include/a52dec"
%if %cc_is_gcc
export CFLAGS="%optflags -KPIC"
%else
export CFLAGS="%optflags"
%endif

aclocal $ACLOCAL_FLAGS
libtoolize --force
autoheader
automake
autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Fri Aug 14 2015 - Thomas Wagner
- only add -KPIC if cc_is_gcc is not true
* Mon Dec 31 2007 - markwright@internode.on.net
- Bump to 0.0.5. Comment patch1, patch2 and patch3.
- Add patch 4 to fix trivial compiler errors.
* Fri Aug  3 2007 - dougs@truemail.co.th
- Build a shared library
* Sun Jan 21 2007 - laca@sun.com
- add patch picflags.diff
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFElibdts
- changed to root:bin to follow other JDS pkgs.
- moved lib*.a to -devel
- added dependencies
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
