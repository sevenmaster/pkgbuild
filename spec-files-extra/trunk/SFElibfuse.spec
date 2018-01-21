#
# spec file for package SFElibfuse.spec
#
%include Solaris.inc
%include usr-gnu.inc
%include osdistro.inc
%include osdistrofeatures.inc

#avoid detection of osdistro delivered fuse package
%define _use_internal_dependency_generator 0

%if %( expr %{oihipster} '|' %{omnios} )
%define cc_is_gcc 1
%include base.inc
%endif

%define src_name libfuse
%define src_url http://sfe.opencsw.org/files
%define tarball_version 20100615

Name:		SFElibfuse
IPS_Package_Name:	 system/file-system/libfuse 
Summary:	Library for FUSE (/usr/gnu)
License:	LGPLv2
SUNW_Copyright:	libfuse.copyright
#Version:	0.%{tarball_version}
# 0.1 to indicate it is patched first round. increment for next added or changed patch
Version:	2.7.6.0.3
Group:		System/File System
#is gone! URL:		http://hub.opensolaris.org/bin/view/Project+fuse/
Source:		%{src_url}/%{src_name}-%{tarball_version}.tgz
Source1:	libfuse.exec_attr
Source2:	libfuse.prof_attr
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%name-%version
%include default-depend.inc
#Patch0:		fuse-2.7.6-update.diff
Patch1:		libfuse-01-fuse-2.7.6-update.diff
Patch3:		libfuse-03-mount_util.c.diff
Patch4:		libfuse-04-utimensat-fuse.c.diff
Patch5:		libfuse-05-cflags.diff
Patch6:		libfuse-06-fuse_lowlevel.c.diff
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
%patch1 -p1
%patch3 -p0
%patch4 -p0
%patch5 -p1
%patch6 -p1

gsed -i.bak1.gnu.include -e 's?/usr/lib?/usr/gnu/lib?' -e 's?/usr/bin?/usr/gnu/bin?' -e 's?/usr/include?/usr/gnu/include?' fusermount sparcv9/Makefile amd64/Makefile Makefile Makefile.com

#new compilers default to 64-bit, so we need to get the i386 build back to 32-bit with -m32
#add default extra CFLAGS_32 above
#append CFLAGS_32
gsed -i.bak.cflags_32 \
                      -e '/^CCFLAGS/ iCFLAGS_32 =' \
                      -e '/^CCFLAGS/ s?\(= \$(CFLAGS)\)?\1 $(CFLAGS_32) ?' \
                      Makefile.com 
#add default extra CFLAGS_32 -m32 below
gsed -i.bak.i386.cflags_32.-m32 \
                      -e '/^include/ aCFLAGS_32 = -m32' \
                      i386/Makefile 

%if %{cc_is_gcc}
export CC=gcc
#fix CC = cc to be CC = gcc
gsed -i.bak -e '/CC.*=.*cc/ s?CC.*=.*cc?CC = gcc?' Makefile.com
%else
#studio
gsed -i.bak2 -e 's?-std=c99?-xc99?' Makefile.com
%endif

%build

#remove once /usr/ccs/bin/make points to working make capable to make kernel modules
#symlink /usr/ccs/bin/make -> /usr/make is broken in pkg://omnios/developer/build/make@0.5.11,5.11-0.151014:20150402T191828Z
#use dmake from solaris developer studio
%if %{omnios}
export MAKE=dmake
dmake
%else
export MAKE=/usr/ccs/bin/make
/usr/ccs/bin/make
%endif


%install
rm -rf $RPM_BUILD_ROOT
#remove once /usr/ccs/bin/make points to working make capable to make kernel modules
#symlink /usr/ccs/bin/make -> /usr/make is broken in pkg://omnios/developer/build/make@0.5.11,5.11-0.151014:20150402T191828Z
#use dmake from solaris developer studio
%if %{omnios}
export MAKE=dmake
dmake install
%else
/usr/ccs/bin/make install
%endif

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
%{_std_sysconfdir}/security/exec_attr.d/libfuse
%{_std_sysconfdir}/security/prof_attr.d/libfuse
%else
%{_std_sysconfdir}
%endif


%changelog
* Sun Jan 21 2018 - Thomas Wagner
- use gcc on %{oihipster} %{omnios}
- %define _use_internal_dependency_generator 0
- bump to 2.7.6.0.3
* Thu Dec  7 2017 - Thomas Wagner
- fix patch to mount binary to be /sbin/ , change invalid options, use empty envionment (libfuse-03-mount_util.c.diff)
- bump to 2.7.6.0.2
* Tue Feb 14 2017 - Thomas Wagner
- add workaround and use dmake (OM)
* Sat Nov 17 2016 - Thomas Wagner
- fix build with compiler defaulting to -m64 (S12/developerstudio)
* Wed Nov 16 2016 - Thomas Wagner
- go with the version number from libfuse.so.2.7.6 library name. Add/increment (IPS) nano-version to indicate every new extra patch
- merge & rework patches from Pierre and OI
* Sat Nov 12 2016 - Thomas Wagner
- fix %files group for /security/exec_attr.d /security/prof_attr.d by removing them from manifest
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
