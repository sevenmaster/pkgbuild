#
# spec file for package libvpx
#

Name:		libvpx
License:	BSD
#Version:	1.5.0
Version:	1.4.0
#versioned snapshots: http://downloads.webmproject.org/releases/webm/index.html
Source:         http://github.com/webmproject/%{name}/archive/v%{version}.tar.gz -O %{_sourcedir}/%{name}-%{version}.tar.gz

Patch1:		libvpx-01-shared.diff
#Patch2:		libvpx-02-mapfile.diff
Patch2:		libvpx-02-1.4.0-mapfile.diff
#Patch3:		libvpx-03-rtcd.diff

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1
#%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%define archis64 %( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} && echo 1 || echo 0 )

%if %archis64
%define _target x86_64-solaris-gcc
%else
%define _target x86-solaris-gcc
%endif

%ifarch sparc
%define _target sparc-solaris-gcc
%endif

export CC=gcc
export CXX=g++

export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix} --libdir=%{_libdir} \
	--enable-vp8 --enable-postproc --enable-runtime-cpu-detect \
	--enable-shared \
        --disable-static \
        --disable-examples \
	--disable-unit-tests \
	--target=%{_target}

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Clean up unpackaged files.
ls -1 $RPM_BUILD_ROOT%{_libdir}/*.*a >/dev/null 2>&1 && rm $RPM_BUILD_ROOT%{_libdir}/*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Jan 16 2017 - Thomas Wagner
- --disable-static or get (S12)  [LD] libvpx.so.2.0.0 gar: `u' modifier ignored since `D' is the default (see `U') [STRIP] libvpx.a < libvpx_g.a CC: Fatal error in /usr/ccs/bin/ld Error 139
- add CFLAGS, CXXFLAGS, LDFLAGS as on S12 with developerstudio12.5 linking by $CXX fails with error CC: Fatal error in /usr/ccs/bin/ld CC: Status 139
* Tue Nov  9 2016 - Thomas Wagner
- relocate to /usr/gnu (S12, all)
- bump to 1.4.0.0.1 to better distinguish from OSDistro libpx (S12 and OIH only)
* Sun Apr 24 2016 - Thomas Wagner
- fix osdistro detection (OIH)
* Wed Mar 16 2016 - Thomas Wagner
- make IPS_Component_Version a bit higher to trick IPS solver on OpenIndiana Hipster to be SFE package selected over OIH one
* Sat Feb 27 2016 - Thomas Wagner
- bump to 1.4.0.0.1 trick the IPS solver to stay ahead with the OpenIndiana Hipster delivered version of libvpx by using IPS_Component_Version
- fix download filename (no >v<)
* Fri Feb 26 2016 - Thomas Wagner
#- bump to 1.5.0 need patch rework
- bump to 1.4.0 - pause patch3, import patch2 for 1.4.0 from OI
- new Source URL and trick stupid gitub causing duplicate filenames between different projects ( "think-1.1.1.tar" and "otherproject-1.1.1.tar" would be both SOURCES/1.1.1.tar )
* Sun Mar 23 2014 - Ian Johnson
- add --disable-unit-tests to configure line (test suite fails to build on Solaris 11.1)
* Sat Sep 28 2013 - Milan Jurik
- bump to 1.2.0 (trigger autobuild)
* Tue Nov  1 2011 - Alex Viskovatoff
- Fix directory attributes
* Sun Aug 05 2012 - Milan Jurik
- bump to 1.1.0
* Thu Jul 21 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sun Oct 23 2011 - Milan Jurik
- bump to 0.9.7-p1
* Fri Mar 18 2011 - Milan Jurik
- fix x86 multiarch
* Thu Mar 17 2011 - Milan Jurik
- initial spec
