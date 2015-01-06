#
# spec file for package SFElibupnp
#
# includes module(s): libupnp
#
%include Solaris.inc

%define	src_name libupnp
%define	src_url	http://nchc.dl.sourceforge.net/sourceforge/pupnp

Name:                SFElibupnp
IPS_Package_Name:	system/library/libupnp
Summary:             Portable C library for UPnP
URL:                 http://sourceforge.net/projects/pupnp/
Version:             1.6.19
Source:              %{src_url}/%{src_name}-%{version}.tar.bz2
#Patch1:		     libupnp-01-solaris.spec
#Patch2:	     libupnp-02-inline.spec
Group:		System/Libraries
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%description
The portable Universal Plug and Play (UPnP) SDK provides support for
building UPnP-compliant control points, devices, and bridges on several
operating systems.

%prep
%setup -q -n %{src_name}-%version
#%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-DSOLARIS -D_POSIX_PTHREAD_SEMANTICS"
export CFLAGS="%optflags -D__const=const"
export LDFLAGS="%_ldflags -lsocket -lnsl"

./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Tue Jan  6 2015 - Thomas Wagner
- bump to 1.6.19
- remove patch1 libupnp-01-solaris.spec
- add -D__const=const or get compile error
* Thu Nov 13 2008 - alfred.peng@sun.com
- Bump to 1.6.6. Removee the inline patch.
  Update the solaris related patch.
* Sun Jul 15 2007 - dougs@truemail.co.th
- Initial spec
