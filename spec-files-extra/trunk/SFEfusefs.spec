# do not enforce new BEs and reboots by IPS flags. fuse can be loaded / unloaded without reboots.

#
#
# spec file for package SFEfusefs
#
# includes module(s): fusefs
#
%include Solaris.inc
%include packagenamemacros.inc

%if %( expr %{oihipster} '|' %{omnios} )
%define cc_is_gcc 1
%include base.inc
%endif

%define _use_internal_dependency_generator 0

%define usr_kernel /usr/kernel
%define drv_base %{usr_kernel}/drv

Name:		SFEfusefs
IPS_Package_Name:	sfe/system/file-system/fusefs
Summary:	Kernel modules for File system in User Space
Version:	1.3.2
%define src_name illumos-fusefs-Version-%{version}
License:	CDDL
Group:		System/File System
SUNW_Copyright:	fusefs.copyright
URL: http://jp-andre.pagesperso-orange.fr/openindiana-ntfs-3g.html
Source:		 http://github.com/jurikm/illumos-fusefs/archive/Version-%{version}.tar.gz?%{src_name}.tar.gz
Patch3:         fusefs-03-s12-makefile-64bit-only-kernel.diff
Patch4:         fusefs-04-makefile-compiler-gcc.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	%{pnm_buildrequires_SUNWonbld}

%include pkg-renamed.inc
%package -n %{name}-noinst-1

#example 'category/newpackagename = *'
#example 'category/newpackagename >= 1.1.1'
#do not omit version equation!
%define renamed_from_oldname      system/file-system/fusefs
%define renamed_to_newnameversion sfe/system/file-system/fusefs = *
%include pkg-renamed-package.inc



%if %( expr %{solaris12} '|' %{s110400} )
%description

WARNING: This fusefs module is *not* extensively tested for Solaris 11.4 (12). You may risk your data.
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

%if %{cc_is_gcc}
export CC=gcc
#fix CFLAGS if gcc is used
%patch4 -p1
#fix CC = cc to be CC = gcc
gsed -i.bak -e '/CC.*=.*cc/ s?CC.*=.*cc?CC = gcc?' kernel/Makefile.com
%endif

%if %( expr  %{s110400} '>=' 1 '|' %{solaris12} '>=' 1 '&' %{osdistro_entire_padded_number4}.0 '>=' 0005001200000000000001000001.0 )
%patch3 -p1
%endif

#if there is /usr/include/sys/cred_impl.h requiring c2/audit.h but is not there
grep "include <c2/audit.h>" /usr/include/sys/cred_impl.h && [ ! -r /usr/include/c2/audit.h ] \
  && { 
     mkdir -p kernel/include/c2
     cp -p /usr/include/bsm/audit.h kernel/include/c2  
     gsed -i.bak -e '/CFLAGS *=/ s?$? -Iinclude?' kernel/Makefile.com
     gsed -i.bak -e '/CFLAGS *=/ s?$? -I../include?' kernel/sparcv9/Makefile kernel/amd64/Makefile
     }

%build
export PATH=/opt/onbld/bin/`uname -p`:$PATH


%if %{cc_is_gcc}
export CC=gcc
%endif

[ -r kernel/include/c2/audit.h ] && export CFLAGS="-I`pwd`/kernel/include"

cd kernel

export CPP="$CC -E"

%if %( expr  %{s110400} '>=' 1 '|' %{solaris12} '>=' 1 )
  #64-bit only
  #rm i386/Makefile
  #rm sparc/Makefile
%endif

#remove once /usr/ccs/bin/make points to working make capable to make kernel modules
#symlink /usr/ccs/bin/make -> /usr/make is broken in pkg://omnios/developer/build/make@0.5.11,5.11-0.151014:20150402T191828Z
#use dmake from solaris developer studio
%if %{omnios}
dmake
%else
/usr/ccs/bin/make
%endif

%install
rm -rf $RPM_BUILD_ROOT
cd kernel

#remove once /usr/ccs/bin/make points to working make capable to make kernel modules
#symlink /usr/ccs/bin/make -> /usr/make is broken in pkg://omnios/developer/build/make@0.5.11,5.11-0.151014:20150402T191828Z
#use dmake from solaris developer studio
%if %{omnios}
dmake install
%else
/usr/ccs/bin/make install
%endif

cp -r proto/ $RPM_BUILD_ROOT

%actions
depend fmri=system/file-system/fusefs@%{ips_version_release_renamedbranch} type=optional

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
* Sun Nov 18 2018 - Thomas Wagner
- fix automatic uninstall of pkg://publisher/system/file-system/fusefs by assigning %actions depend oldname type=optional
* Sat Jan 21 2018 - Thomas Wagner
- bump to 1.3.2, obsoleted patch1 fusefs-01-remove-ADDR_VACALIGN-choose_addr-fuse_vnops.c.diff, 
- rename to IPS_Package_Name sfe/system/file-system/fusefs
- rework all patches (partly obsoleted by 1.3.2)
- add patch3 fusefs-03-s12-makefile-64bit-only-kernel.diff (S11.4 / S12)
- fix builds with gcc compiler on (OM OIH)
- add patch4 fusefs-04-makefile-compiler-gcc.diff apply if cc_is_gcc (OM OIH)
* Fri Feb 17 2017 - Thomas Wagner
- improve Source URL to get src_name into download file
- set CPP
- fix missing include file (S12)
* Tue Feb 14 2017 - Thomas Wagner
- add workaround and use dmake able to make kernel modules (OM)
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
