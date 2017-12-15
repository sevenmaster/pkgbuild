#
# spec file for package SFEsshfs
#
#
# you will need FUSE see: http://www.opensolaris.org/os/project/fuse

%include Solaris.inc

%define src_name sshfs
%include base.inc

Name:                    SFEsshfs
IPS_package_name: system/file-system/fuse-sshfs
Summary:                 sshfs - filesystem access over SSH
Version:                 2.10
IPS_package_name:	system/file-system/sshfs
License:                 GPLv2
Source:			http://github.com/libfuse/sshfs/archive/sshfs-%{version}.tar.gz
Patch1:                  sshfs-fuse-01-sunpro.diff
Url:                     https://github.com/libfuse/sshfs
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
%define _execprefix %{_prefix}

BuildRequires: SFElibfuse
Requires: SFEfusefs
Requires: SFElibfuse


%description
Mount remote diretories through a SSH connection.
#
sudo -i;
mkdir /tmp/ssh-remount-mount;
sshfs remoteuser@remotehost:/this/remote/filesystem_path /tmp/ssh-remount-mount;
#
For umount run "umount /tmp/ssh-remount-mount"

Make sure to check the various options (including sync / async)

%prep
#sshfs-sshfs-2.10
%setup -q -n %{src_name}-%{src_name}-%{version}
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"

aclocal
autoheader
autoconf
automake -a -c -f

CFLAGS="%{optflags} -I/usr/gnu/include/fuse" \
LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib" \
PKG_CONFIG_PATH=/usr/gnu/lib/pkgconfig		\
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
	    --mandir=%{_mandir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
mkdir -p $RPM_BUILD_ROOT%{_libdir}/fs/sshfs
ln -s %{_bindir}/sshfs $RPM_BUILD_ROOT%{_libdir}/fs/sshfs/mount
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_libdir}/fs
%dir %attr (0755, root, sys) %{_libdir}/fs/sshfs
%{_libdir}/fs/sshfs/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*


%changelog
* Thu Dec  7 2017 - Thomas Wagner
- bump to 2.10
- new Download URL (archive)
* Tue Feb 14 2017 - Thomas Wagner
- fix Source, update URL
* Tue Nov 15 2016 - Thomas Wagner
- bump to 2.8
* Sat Sep 28 2013 - Milan Jurik
- bump to 2.3
* Sat May 29 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec.
