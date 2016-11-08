%define src_name orc

Name:		SFEorc
Version:	0.4.26
Summary:	The Oil Run-time Compiler

Group:		System Environment/Libraries
License:	BSD
URL:		http://code.entropywave.com/projects/orc/
Source:         http://gstreamer.freedesktop.org/src/orc/orc-%{version}.tar.xz
BuildRoot:	%{_tmppath}/%{name}-%{version}-build


%prep
#don't unpack please
%setup -q -c -T -n %{src_name}-%version
xz -dc %SOURCE0 | (cd ..; tar xf -)

perl -i.orig -lpe 'if ($. == 1){s/^.*$/#!\/bin\/bash/}' configure

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lm"
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
        export LDFLAGS="$LDFLAGS -m64"
fi

./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}                 \
            --datadir=%{_datadir}               \
            --with-pic                          \
            --disable-gtk-doc                   \
            --disable-static
# --enable-gtk-doc

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Remove unneeded files.
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.a
rm -rf $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT/%{_libdir}/orc


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Tue Nov  8 2016 - Thomas Wagner
- bump to 0.4.26
* Sun Nov 29 2015 - Thomas Wagner
- bump to 0.4.23
- new source URL
- --with-pic
- disable doc building, error in XML
* Mon Oct 17 2011 - Milan Jurik
- bump to 0.4.16
* Tue Jul 26 2011 - Alex Viskovatoff
- Revert to 0.4.11, since SFElibschroedinger does't build with later versions
* Thu Jul 21 2011 - Alex Viskovatoff
- Update to 0.4.14, disabling the sole patch
* Tue Jul 13 2010 - Thomas Wagner
- change shell of configure to be real bash
* Fri Jun 18 2010 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 0.4.5.
* Sun Apr 11 2010 - Milan Jurik
- do not depend on GNU find
* Fri Apr 09 2010 - Milan Jurik
- initial multiarch support
