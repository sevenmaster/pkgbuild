# ldd packages/PKGS/SFErdesktop/reloc/bin/rdesktop 
#         libcrypto.so.1.0.0 =>    /usr/lib/libcrypto.so.1.0.0
#         libsocket.so.1 =>        /usr/lib/libsocket.so.1
#         libXrandr.so.2 =>        /usr/lib/libXrandr.so.2
#         libsamplerate.so.0 =>    /usr/lib/libsamplerate.so.0
#         libao.so.4 =>    /usr/lib/libao.so.4
#         libnsl.so.1 =>   /usr/lib/libnsl.so.1
#         libX11.so.4 =>   /usr/lib/libX11.so.4
#         libc.so.1 =>     /usr/lib/libc.so.1
#         libXext.so.0 =>  /usr/lib/libXext.so.0
#         libXrender.so.1 =>       /usr/lib/libXrender.so.1
#         libm.so.2 =>     /lib/libm.so.2
#         libpthread.so.1 =>       /lib/libpthread.so.1
#         libmp.so.2 =>    /lib/libmp.so.2
#         libmd.so.1 =>    /lib/libmd.so.1
#         libxcb.so.1 =>   /usr/lib/libxcb.so.1
#         libsoftcrypto.so.1 =>    /lib/libsoftcrypto.so.1
#         libelf.so.1 =>   /lib/libelf.so.1
#         libXau.so.6 =>   /usr/lib/libXau.so.6
#         libXdmcp.so.6 =>         /usr/lib/libXdmcp.so.6
#         libcryptoutil.so.1 =>    /lib/libcryptoutil.so.1
#         libz.so.1 =>     /lib/libz.so.1
#         libXevie.so.1 =>         /usr/lib/libXevie.so.1
#         libXss.so.1 =>   /usr/lib/libXss.so.1


#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include usr-gnu.inc
%include base.inc

Name:                SFErdesktop
Summary:             RDP, Microsoft Terminal Services client (/usr/gnu)
IPS_Package_Name:    desktop/remote-desktop/gnu/rdesktop
Version:             1.7.1
#Version:             1.8.2
Source:              %{sf_download}/rdesktop/rdesktop-%{version}.tar.gz
URL:			http://rdesktop.sourceforge.net/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

#Requires: SUNWopenssl-commands
#BuildRequires: SFEgsslib
#Requires: SFEgsslib

%prep
%setup -q -n rdesktop-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

bash ./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \

	    #--with-openssl="/usr/sfw"

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Sat Oct 25 2014 - Thomas Wagner
- add IPS_Package_Name
- %include usr-gnu.inc
* Thu Dec 27 2012 - Thomas Wagner
- bump to 1.7.1
- fix download URL
* Tue Jul 26 2011 - Thomas Wagner
- bump to 1.7.0
* Mon Dec  4 2006 - Thomas Wagner
- Upgrade from 1.4.1 to 1.5.0
* Sun Sep 24 2006 - Eric Boutilier
- Initial spec
