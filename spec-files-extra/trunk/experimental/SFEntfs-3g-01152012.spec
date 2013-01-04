#
# spec file for package SFEntfs-3g
#
#
# you will need FUSE see: http://www.opensolaris.org/os/project/fuse
#
# Build with GCC 3.4.3 only
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc


Name:                    SFEntfs-3g
IPS_Package_Name:	 system/file-system/ntfs-3g
Summary:                 NTFS-3G Stable Read/Write Driver
Version:                 2012.1.15AR.8
License:                 GPLv2
#
# Latest tested source for OpenIndiana version. 
#
Source:                  http://jp-andre.pagesperso-orange.fr/ntfs-3g_ntfsprogs-%{version}.tgz
Url:                     http://jp-andre.pagesperso-orange.fr/openindiana-ntfs-3g.html
Group:		System/File System
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
%define _execprefix %{_prefix}

BuildRequires:	SUNWgnome-common-devel

#
# This uses the SFE patched FUSE kernel module approved and tested
# with the Tuxera NTFS-3G 2012.1.15AR.8 driver
#
Requires:	SFEfusefs
Requires:	SFElibfuse

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

BuildRequires:	SFElibfuse-devel
Requires:	SFElibfuse

%prep
%setup -q -n ntfs-3g_ntfsprogs-%version

cat <<_EOF > fstyp
#!/bin/sh
while [ -n "\$1" ];  do
        case "\$1" in
        -*)
                shift   
                ;;
        *)
                %{_bindir}/ntfs-3g.probe --readonly "\$1" >/dev/null 2>&1 && echo "ntfs-3g" && exit 0
                exit 1
                ;;
        esac
done
exit 1
_EOF

%build

#
# Use only GCC 3.4.3 (developer/gcc-3)
#
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CFLAGS="%optflags -I%{gnu_inc} %{gnu_lib_path}"
export FUSE_MODULE_CFLAGS="$CFLAGS %{gnu_lib_path} -D_FILE_OFFSET_BITS=64 -I/usr/gnu/include/fuse"
export FUSE_MODULE_LIBS="%{gnu_lib_path} -pthread -lfuse"

./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}                 \
	    --mandir=%{_mandir}                 \
            --sysconfdir=%{_sysconfdir}         \
	    --datadir=%{_datadir}               \
            --bindir=%{_bindir}                 \
            --includedir=%{_includedir}         \
            --exec-prefix=%{_execprefix}	\
	    --disable-static 	   		\
	    --enable-posix-acls		 	\
	    --enable-xattr-mappings		\
	    --enable-extras		 	\
	    --enable-crypto		 	\
	    --with-fuse=external

gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -r $RPM_BUILD_ROOT%{_prefix}/sbin
mkdir -p $RPM_BUILD_ROOT%{_libdir}/fs/ntfs-3g
cp fstyp $RPM_BUILD_ROOT%{_libdir}/fs/ntfs-3g/fstyp
chmod 755 $RPM_BUILD_ROOT%{_libdir}/fs/ntfs-3g/fstyp
ln -s %{_bindir}/ntfs-3g $RPM_BUILD_ROOT%{_libdir}/fs/ntfs-3g/mount
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libntfs-3g.so*
%dir %attr (0755, root, sys) %{_libdir}/fs
%dir %attr (0755, root, sys) %{_libdir}/fs/ntfs-3g
%{_libdir}/fs/ntfs-3g/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*



%changelog
* Thu Jan 3 2013 - Ken Mays <kmays2000@gmail.com>
- Bump to 2012.1.15AR.8
* Sat Mar 31 2012 - Pavel Heimlich
- fix download location
* Sat Jan 28 2012 - Thomas Wagner
- use gcc3 (or get missing definitions for __BYTE_ORDER)
* Wed Jan 11 2012 - Thomas Wagner
- go for SFElibfuse/SFEfusefs in any case (SUNWlibfuse was not contained in distros)
* Tue Sep 27 2011 - Alex Viskovatoff
- Build with gcc-3, as does not duild with gcc 4.6
* Thu Jul 07 2011 - Alex Viskovatoff
- Revert the previous change, so the package gets built
* Mon Jun 06 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 2011.4.12
* Tue Mar 22 2011 - Thomas Wagner
- Bump to 2011.1.15
* Sat Jun 19 2010 - Milan Jurik
- support SFEfusefs
* Fri Mar 26 2010 - Albert Lee <trisk@opensolaris.org>
- Bump to 2010.3.6
- Update URL, License
- Add mount helper
* Sun Jun 21 2009 - trisk@forkgnu.org
- Bump to 2009.4.4
* Tue Mar 24 2009 - andras.barna@gmail.com
- bump version
* Fri Aug 15 2008 - andras.barna@gmail.com
- new version: 1.2812 
* Wed Aug 06 2008 - andras.barna@gmail.com
- initial spec
