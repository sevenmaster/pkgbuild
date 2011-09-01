#
# spec file for package SFEmpg123.spec
#
%include Solaris.inc

Name:           SFEmpg123
Summary:        mpg123 - fast console MPEG Audio Player and decoder library
Version:        1.13.3
URL:            http://www.mpg123.org/
Source:         %{sf_download}/mpg123/mpg123/%{version}/mpg123-%{version}.tar.bz2
License:        LGPL,GPL
Group:          Applications/Multimedia
SUNW_Copyright: %{name}.copyright
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:       SUNWltdl
Requires:       SUNWlibsdl
Requires:       SUNWlibms
BuildRequires:	SUNWaudh
BuildRequires:	SUNWgnome-common-devel
Requires:       %{name}-devel

%description
mpg123 is a real time MPEG 1.0/2.0/2.5 audio player/decoder for layers
1, 2, and 3 (MPEG 1.0 layer 3 aka MP3 most commonly tested). mpg123
includes a terminal-based player, the ability to redirect the raw sound
data to stdout, gapless playback of MP3 files, a decoder library for use
with other applications, and much more.

%package devel
Summary:        mpg123 - developer files, /usr
Group:          Development/Libraries
SUNW_BaseDir:   %{_basedir}
Requires:       %name
%include default-depend.inc

%prep
%setup -q -n mpg123-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared             \
            --disable-static            \
            --enable-int-quality=yes    \
            --enable-fifo=yes		\
            --enable-network=yes	\
            --with-cpu=generic_fpu	\
            --with-default-audio=oss	\
            --enable-ipv6=yes 		\
            --with-optimization=0

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/mpg123/output_*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%{_libdir}/libmpg123.so.*
%{_libdir}/mpg123/output_*.so

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/libmpg123.pc
%{_includedir}
%{_libdir}/libmpg123.so

%changelog
* Thu Sep 01 2011 - Milan Jurik
- bump to 1.13.3
* Mon Aug 25 2009 - matt@greenviolet.net
- Initial version
