#
#
# spec file for package SFEfusefs
#
# includes module(s): fusefs
#
%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

%define usr_kernel /usr/kernel
%define drv_base %{usr_kernel}/drv

Name:		SFEfusefs
IPS_Package_Name:	system/file-system/fusefs
Summary:	Kernel modules for File system in User Space
Version:	1.3.1
%define src_name illumos-fusefs-Version-%{version}
License:	CDDL
Group:		System/File System
SUNW_Copyright:	fusefs.copyright
URL: http://jp-andre.pagesperso-orange.fr/openindiana-ntfs-3g.html
Source:		 http://github.com/jurikm/illumos-fusefs/archive/Version-%{version}.tar.gz
Patch1:		fusefs-01-remove-ADDR_VACALIGN-choose_addr-fuse_vnops.c.diff
Patch2:		fusefs-02-s12-rctl_action__donts_cache_attributes.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	%{pnm_buildrequires_SUNWonbld}

#pseudo code, as it is not really clear if pkgtool can handle this propperly down to the build number
#might need an extra IPS tag added
%if %( expr %{solaris12} '>=' 1 '&' %{osdistro_entire_padded_number4}.0 '>=' 0005001200000000000001000001.0 )
#build 100 and higher, rctl private interface has changed quite a bit
#idee: anderes Paket das mit build 100 hinzugekommen war und immer installiert ist anfordern
#idee: anderes Paket das mit build 100 hinzugekommen war und immer installiert ist anfordern
#depend fmri=pkg:/system/kernel@5.12-5.12.0.0.0.100 type=require

%endif


%if %{solaris12}
%description

WARNING: This fusefs module is *not* extensively tested for Solaris 12. You may risk your data.
You may risk your data. Yes, you may risk your data.

The code for the kernel module had to be changed and attribute caching is switched off.

You may report your test cases and which setup worked for your and what did not.

Compile-Option -DDONT_CACHE_ATTRIBUTES is set, so this may have an performance impact

Call for code-review! Please if you can read and improve kernel code, then please make a
code review of the code found in package fusefs/src .


%endif

%description

FUSE stands for 'File system in User Space'. It provides a simple
interface to allow implementation of a fully functional file system
in user-space.  FUSE originates from the Linux community and is
included in the Linux kernel (2.6.14+).

This is the kernel module.


%prep
#illumos-fusefs-Version-1.3.1
%setup -q -n %{src_name}

#only Solaris 12 wants 5 arguments, Hipster, Solaris 11 wants 6 arguments including int vacalign
#/usr/include/sys/vmsystm.h:#define ADDR_VACALIGN   1
%if %( expr %{solaris12} '>=' 1 )
#expect only 5 arguments to choose_addr
%patch1 -p1
%endif

%if %( expr %{solaris12} '>=' 1 '&' %{osdistro_entire_padded_number4}.0 '>=' 0005001200000000000001000001.0 )
#build 100 and higher, rctl private interface has changed quite a bit
#permanent patch for rctl, but temporary patch for disabling attribute caches
%patch2 -p1
%endif

%build
export PATH=/opt/onbld/bin/`uname -p`:$PATH

cd kernel

%if %{solaris12}
  #64-bit only
  #rm i386/Makefile
  #rm sparc/Makefile
%endif

/usr/ccs/bin/make

%install
rm -rf $RPM_BUILD_ROOT
cd kernel

/usr/ccs/bin/make install

cp -r proto/ $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
( retval=0; 
  /usr/sbin/add_drv -m 'fuse 0666 root sys' fuse || retval=1;
  [ "$retval" = 0 ] && ln -s /devices/pseudo/fuse@0:fuse /dev/fuse || retval=1;
  exit $retval
)

%preun
( retval=0;
  /usr/sbin/rem_drv fuse || retval=1;
  [ "$retval" = 0 ] && rm /dev/fuse || retval=1;
  exit $retval
)

%actions
driver name=fuse devlink=type=ddi_pseudo;name=fuse\t\D perms="* 0666 root sys"

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{usr_kernel}
%dir %attr (0755, root, sys) %{drv_base}
%{drv_base}/fuse*
#%{drv_base}/fuse
#%{drv_base}/fuse.conf
%ifarch amd64 sparcv9
%dir %attr (0755, root, sys) %{drv_base}/%{_arch64}
%{drv_base}/%{_arch64}/fuse
%endif

%changelog
* Sat Nov 26 2016 - Thomas Wagner
- add patch2 (permanent patch for rctl, but temporary patch for disabling attribute caches) only for (S12)
* Wed Nov 16 2016 - Thomas Wagner
- fix missing expr to detect S12 for patch1
* Sat Nov 12 2016 - Thomas Wagner
- bump to 1.3.1
- load source from new URL on github
- add patch1 for S12 to only expect 5 arguments to /usr/include/sys/vmsystm.h: choose_addr
* Sun Apr 17 2016 - Thomas Wagner
- update to source tarball from Jean-Pierre 
- bump to 1.2AR.7
* Wed Jan 30 2014 - Thomas Wagner
- change to (Build)Requires: %{pnm_buildrequires_SUNWonbld}, #include packagenamemacros.inc
* Thu Jun 20 2013 - Thomas Wagner
- new download url
* Fri Aug 31 2012 - Milan Jurik
- bump version with new patch from Jean-Pierre Andre 
* Sat Jan 28 2012 - Milan Jurik
- add patches from Jean-Pierre Andre 
* Fri Nov 04 2011 - Guido Berhoerster <gber@openindiana.org>
- fixed driver action to create devlinks entry
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Thu Jul 07 2011 - Alex Viskovatoff
- Revert previous change: source file does not get found
* Mon Jun 06 2011 - Ken Mays <kmays2000@igmail.com>
- Bumped to 2.8.5
* Sat Jun 19 2010 - Milan Jurik
- Initial spec
