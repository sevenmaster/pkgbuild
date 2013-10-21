#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# spec file for package SUNWgmp
#
# includes module(s): GNU gmp
#

##TODO## think on usr-gnu.inc define infodir inside /usr/gnu/share to avoid conflicts
%define _infodir           %{_datadir}/info

Name:		gmp
Version:	5.1.3
Source:		http://ftp.sunet.se/pub/gnu/gmp/gmp-%{version}.tar.bz2
%if %cc_is_gcc
%else
Patch2:		gmp-5.1.1-02-libtool.diff
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %name-%version
%if %cc_is_gcc
%else
%endif

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags -L/usr/gnu/lib -R/usr/gnu/lib"
export CXXFLAGS="%cxx_optflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export ABI=64
else
        export ABI=32
fi

./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --infodir=%{_infodir}	\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --disable-static		\
	    --enable-cxx                \
	    --enable-fat

%if %cc_is_gcc
%else
%patch2 -p1
%endif
make -j$CPUS 

#Make Check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Oct 21 2013 - Thomas Wagner
- bump to 5.1.3 (small bug fixes)
* Thu Jun 26 2013 - Thomas Wagner
- bump to 5.1.2
- remove obsolete patch1 gmp-5.1.1-01-solaris.diff
* Thu Feb 21 2013 - Logan Bruns <logan@gedanken.org>
- Fork to create g++ version of gmp.
* Wed Feb 13 2013 - Ken Mays <kmays2000@gmail.com>
- Bump to 5.1.1, use -library=stlport4
* Tue May 29 2012 - Milan Jurik
- bump to 5.0.5
* Fri Mar 9 2012 - Ken Mays <kmays2000@gmail.com>
- Bump to 5.0.4
- Fixed SIMD detection on legacy x86 computers
* Mon Oct 10 2011 - Milan Jurik
- go with proper multiarch
