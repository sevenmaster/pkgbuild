#
# spec file for package SFElibtar
#
# includes module(s): libtar
#
%include Solaris.inc

%define	src_name libtar
%define	src_url	ftp://ftp.feep.net/pub/software/%{src_name}

Name:                SFElibtar
IPS_Package_Name:	library/libtar
Summary:             C library for manipulating POSIX tar files
URL:                 http://www.feep.net/libtar/
Version:             1.2.11
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     libtar-01-shared.diff
Group:		System/Libraries
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

%if %cc_is_gcc
gsed -i.bak_remove_KPIC_cc_is_gcc -e 's?-KPIC??' lib/Makefile*
%endif

libtoolize --copy --force
autoconf -f -I autoconf
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared

#Add ${LDFLAGS} to linking libtar.so to get "-m32" effective
gsed -i.bak_LDFLAGS '/\$(CC) -G -o libtar.so/ s?-o libtar.so?\${LDFLAGS} -o libtar.so?' lib/Makefile

gmake V=2 -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_bindir}
%{_mandir}/man3

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
- Mon Dec 12 2016 - Thomas Wagner
- Makefile should use LDFLAGS to get in "-m32" with new developerstudio defaulting to -m64
* Sun Nov 29 2015 - Thomas Wager
- fix removal of -KPIC in case cc_is_gcc
* Thu Aug 13 2015 - Thomas Wagner
- remove -KPIC from Makefile if cc_is_gcc
* Sat Jul 14 2007 - dougs@truemail.co.th
- Initial spec
