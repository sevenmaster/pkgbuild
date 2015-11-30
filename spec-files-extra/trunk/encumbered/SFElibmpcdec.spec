#
# spec file for package SFElibmpcdec
#
# includes module(s): libmpcdec
#
%include Solaris.inc
%include packagenamemacros.inc


Name:                    SFElibmpcdec
IPS_Package_Name:	library/audio/libmpcdec 
Summary:                 Portable Musepack decoder library
License:                 BSD
SUNW_Copyright:	         libmpcdec.copyright
URL:                     http://musepack.net/
Version:                 1.2.6
Source:                  http://files.musepack.net/source/libmpcdec-%{version}.tar.bz2
Patch1:			 libmpcdec-01-configure.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: %{pnm_buildrequires_SFElibsndfile_devel}
Requires:      %{pnm_requires_SFElibsndfile}

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libmpcdec-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CPPFLAGS="-D__inline=inline"
export CFLAGS="%optflags"

%if %cc_is_gcc
#or get: configure: error: No signed 16 bit type found on this platform.
gsed -i.bak_remove_KPIC_cc_is_gcc -e '/^CFLAGS.*CFLAGS.*KPIC/ s?-KPIC??' configure.ac configure
%endif

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

gmake -j$CPUS 

%install
gmake install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sun Nov 29 2015 - Thomas Wagner
- remove -KPIC if cc_is_gcc or get configure: error: No signed 16 bit type found on this platform.
* Fri Jul  5 2013 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SFElibsndfile_devel}, %include packagenamemacros.inc
##TODO## include and link against correct libsndfile
* Mon Oct 10 2011 - Milan Jurik
- add IPS package name
* Thu Jul 21 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sun Oct  3 2010 - Alex Viskovatoff
- Use gmake.
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
* Fri May 23 2008 - michal.bielicki@voiceworks.pl
- fix of source URL by Giles Dauphin
* Sun Nov 4 2007 - markwright@internode.on.net
- Bump to 1.2.6
* Thu Apr 05 2007 - Thomas Wagner
- bump to 1.2.5
- refresh patch/libmpcdec-01-configure.diff
* Fri Jun 23 2006 - laca@sun.com
- rename to SFElibmpcdec
- update file attributes
* Mon Jun 13 2006 - drdoug007@yahoo.com.au
- Initial version
