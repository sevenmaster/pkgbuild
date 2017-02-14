# spec file for package SFEcmake
#
# includes module(s): cmake
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc                                                                                                                                                                                                                                                                        
%include usr-gnu.inc
%include osdistro.inc
%include buildparameter.inc                                                                                                                                                                                                                                                                 
%define cc_is_gcc 1                                                                                                                                                                                                                                                                         
%include base.inc                  


#S12 build >= 70
#developer/build/cmake                             2.8.6-5.12.0.0.0.70.0      ---

#S11.3
#2.8.6-0.175.3.0.0.18.0
#0000017500030000000000180000

Name:		SFEcmake
IPS_Package_Name:	sfe/developer/build/cmake 
Summary:	Cross platform make system
Version:	3.5.2
License:	BSD3c
SUNW_Copyright:	cmake.copyright
%define major_minor_version %( echo %{version} |  awk -F'.' '{print $1 "." $2}' )
Source:		http://www.cmake.org/files/v%{major_minor_version}/cmake-%{version}.tar.gz
Patch3:         cmake-03-01-usr-local.patch
Patch4:		cmake-04-02-cmState.cxx.patch
URL:		http://www.cmake.org
Group:		Development/Distribution Tools
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
%setup -q -n cmake-%{version}

%patch3 -p1
%patch4 -p1

cd Modules
ggrep -l '/opt/csw' *.cmake | /usr/bin/xargs -I \{\} gsed -i -e '/^[ ]*\/opt\/csw/d' \{\}
cd ..

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=/usr/gcc/bin/gcc
export CXX=/usr/gcc/bin/g++

#from userland gate: The default -O3 is *MUCH* too aggressive
export CFLAGS="%optflags -O2"
export CXXFLAGS="%cxx_optflags -O2"

./configure --prefix=%{_prefix} \
	    --docdir=/share/doc/cmake \
	    --mandir=/share/man \
            --parallel=$CPUS \
            --system-curl \
            --system-expat \
            --system-zlib \
            --system-bzip2 \
            --system-libarchive \
            --system-liblzma \


#If Ext2 Filesystem headers are present and found, compile errors occur
#disable this: HAVE_EXT2FS_EXT2_FS_H:INTERNAL=1
gsed -i.bak.ext2_fs_h -e 's/^HAVE_EXT2FS_EXT2_FS_H:INTERNAL=.*/HAVE_EXT2FS_EXT2_FS_H:INTERNAL=/' CMakeCache.txt 

gmake -j$CPUS

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

##TODO##
#fetch manpages from solaris userland gate
mkdir %{buildroot}%{_prefix}/share/man

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755,root,other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/cmake-*
%{_mandir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/cmake

%changelog
* Sun Jan 15 2017 - Thomas Wagner
- bump to 3.5.2
- remove old patch1 patch2
- imported patch3, patch4 and portions of Makefile from solaris userland gate
* Mon Mar 21 2016 - Thomas Wagner
- bump to 2.8.12.2.0.1 add 0.1 to get most recent package when pkg solver runs (OIH)
* Sun Feb 14 2016 - Thomas Wagner
- bump to 2.8.12.2 (for stellarium 0.14.2)
- add patch1 cmake-01-remove-special-case-linking-C++-shared-libraries.diff (integrated in cmake 3.4.x)
  SunOS: Drop special case for linking C++ shared libraries with gcc
- add patch2 (modified) cmake-02-SystemInformation.cxx-backtrace_prototype.diff
  SystemInformation.cxx", line 1382: Error: The function "backtrace_symbols" must have a prototype.
- make IPS unique again for S11.3 (sfe/)
* Sun Sep 01 2013 - Milan Jurik
- bump to 2.8.11
* Sun Nov 11 2012 - Logan Bruns <logan@gedanken.org>
- bump to 2.8.10
* Sun Jun 17 2012 - Thomas Wagner
- fix permissions %dir %attr (0755,root,other) %{_datadir}/aclocal/*
* Wed May 16 2012 - Thomas Wagner
- fix permissions %dir %attr (0755,root,other) %{_datadir}/aclocal
* Fri Apr 20 2012 - Logan Bruns <logan@gedanken.org>
- bump to 2.8.8 and enable parallel build.
* Sat Feb 11 2012 - Milan Jurik
- bump to 2.8.7
* Tue Oct 11 2011 - Thomas Wagner
- some sed don't support -i , change to "gsed" (and gmake)
* Tue Oct 11 2011 - Milan Jurik
- bump to 2.8.6, add IPS package name
* Wed Aug 24 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 2.8.5
* Sat Mar  5 2011 - Alex Viskovatoff
- bump to 2.8.4; install documentation files in cmake's own directory
* Thu Feb 10 2011 - Thomas Wagner
- fix compile errors on (all) distros if configure thinks that EXT2 is present
  (archive_write_disk.c", line 2237: warning: implicit function declaration: _IOR)
* Thu Feb 10 2011 - Milan Jurik
- reintroducing and bump to 2.8.3
* Thu Oct 20 2008 - jedy.wang@sun.com
- Bump to 2.6.2
* Mon Aug 11 2008 - nonsea@users.sourceforge.net
- Bump to 2.6.1
* Tue May 13 2008 - nonsea@users.sourceforge.net
- Bump to 2.6.0
* Fri Mar 07 2008 - nonsea@users.sourceforge.net
- Bump to 2.4.8
* Mon Oct 22 2007 - nonsea@users.sourceforge.net
- Bump to 2.4.7
* Mon Mar 19 2007 - dougs@truemail.co.th
- Initial spec
