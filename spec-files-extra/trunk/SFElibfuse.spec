#
# spec file for package SFElibfuse.spec
#
%include Solaris.inc
%include usr-gnu.inc
%include osdistrofeatures.inc

%define src_name libfuse
%define src_url http://sfe.opencsw.org/files
%define tarball_version 20100615

Name:		SFElibfuse
IPS_Package_Name:	 system/file-system/libfuse 
Summary:	Library for FUSE (/usr/gnu)
License:	LGPLv2
SUNW_Copyright:	libfuse.copyright
Version:	0.%{tarball_version}
Group:		System/File System
#is gone! URL:		http://hub.opensolaris.org/bin/view/Project+fuse/
Source:		%{src_url}/%{src_name}-%{tarball_version}.tgz
Source1:	libfuse.exec_attr
Source2:	libfuse.prof_attr
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%name-%version
%include default-depend.inc
Patch0:		fuse-2.7.6-update.diff
Requires:	%{name}-root
Requires:	SFEfusefs
BuildRequires:	SFEfusefs

%description
FUSE stands for 'File system in User Space'. It provides a simple
interface to allow implementation of a fully functional file system
in user-space.  FUSE originates from the Linux community and is
included in the Linux kernel (2.6.14+).

%package devel
Summary:	%{summary} - development files
Requires:	%name

%description devel
This package contains development libraries and C header files needed for
building applications which use libfuse.

%package root
Summary:	%{summary} - root files
SUNW_BaseDir:	/
%include default-depend.inc

%description root
This package contains root files for libfuse.

%prep
%setup -q -n %{src_name}
%patch0 -p0

gsed -i -e 's?/usr/lib?/usr/gnu/lib?' -e 's?/usr/bin?/usr/gnu/bin?' -e 's?/usr/include?/usr/gnu/include?' fusermount sparcv9/Makefile amd64/Makefile Makefile Makefile.com

%build
export MAKE=/usr/ccs/bin/make

/usr/ccs/bin/make

%install
rm -rf $RPM_BUILD_ROOT
/usr/ccs/bin/make install

mkdir -p $RPM_BUILD_ROOT/usr/gnu/
#cp -r proto/usr/* $RPM_BUILD_ROOT/usr/gnu
cp -r proto/usr/* $RPM_BUILD_ROOT/usr/

##TODO## create switch to merge into exec_attr / prof_attr for SVR4 systems or before osbuild 151
mkdir -p $RPM_BUILD_ROOT%{_std_sysconfdir}/security/exec_attr.d
cp %{SOURCE1} $RPM_BUILD_ROOT%{_std_sysconfdir}/security/exec_attr.d/libfuse

mkdir -p $RPM_BUILD_ROOT%{_std_sysconfdir}/security/prof_attr.d
cp %{SOURCE2} $RPM_BUILD_ROOT%{_std_sysconfdir}/security/prof_attr.d/libfuse

cd $RPM_BUILD_ROOT%{_libdir} && ln -s libfuse.so.* libfuse.so

%ifarch amd64 sparcv9
cd $RPM_BUILD_ROOT%{_libdir}/%{_arch64} && ln -s libfuse.so.* libfuse.so
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri rbac

%postun
%restart_fmri rbac

%files
%defattr(-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_libdir}/fs
%{_libdir}/fs/fuse

%files devel
%defattr(-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/fuse.pc

%files root
%defattr (-, root, sys)
%if %{etc_security_directorylayout}
%dir %attr (0755, root, other) %{_std_sysconfdir}/security/exec_attr.d
%dir %attr (0755, root, other) %{_std_sysconfdir}/security/prof_attr.d
%{_std_sysconfdir}/security/exec_attr.d/libfuse
%{_std_sysconfdir}/security/prof_attr.d/libfuse
%else
%{_std_sysconfdir}
%endif


%changelog
* Thu Jun 20 2013 - Thomas Wagner
- new download url
- prepared for switching old/new layout in /etc/security/<$1|$1.d/>,
  %include osdistrofeatures.inc
* Sat Jul 23 2012 - Thomas Wagner
- hard replace paths to use /gnu/ in Makefile*
- fix paths used with "cp" in %install
* Wed Jan 11 2012 - Thomas Wagner
- relocate to /usr/gnu because we now have a different fuse variant
  on Solaris 11
* Wed Nov 9 2011 - Ken Mays <kmays2000@gmail.com>
- Bumped to fuse 2.7.6
- Added ulockmgr.h
* Wed Jul 20 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Wed Jun 19 2010 - Milan Jurik
- Initial spec
