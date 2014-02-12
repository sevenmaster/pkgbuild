#
# spec file for package SFEpkgbuild
#

# Vanilla pkgbuild's default install prefix is /opt/pkgbuild
# We follow the SFE convention of installing in /usr
# Use pkgbuild --define 'pkgbuild_prefix /path/to/dir'
# to define a different install prefix.

%{?!pkgbuild_prefix:%define pkgbuild_prefix /usr}
%define _prefix %{pkgbuild_prefix}

%define srcname pkgbuild
%define _pkg_docdir %_docdir/%srcname
%include packagenamemacros.inc

Name:         SFEpkgbuild
IPS_Package_Name: package/pkgbuild
License:      GPL
Group:        Development/Tools/Other
URL:	      http://pkgbuild.sourceforge.net/
Version:      1.3.105
Release:      1
BuildArch:    noarch
Vendor:	      OpenSolaris Community
Summary:      rpmbuild-like tool for building Solaris packages
Source:       http://prdownloads.sourceforge.net/pkgbuild/pkgbuild-%{version}.tar.bz2
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%if %_is_pkgbuild
#SUNW_Pkg:                  SFpkgbuild
SUNW_MaxInst:              1000
SUNW_BaseDir:              %{pkgbuild_prefix}
SUNW_Copyright:            http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
# OpenSolaris IPS Package Manifest Fields
Meta(info.upstream):	 	Laszlo (Laca) Peter <laca@sun.com>
Meta(info.maintainer):	 	Laszlo (Laca) Peter <laca@opensolaris.org>
Meta(info.repository_url):	http://pkgbuild.cvs.sourceforge.net/viewvc/pkgbuild/pkgbuild/
Meta(info.classification):	org.opensolaris.category.2008:System/Packaging
%endif

%ifos Solaris
Requires:     SUNWbash
Requires:     %pnm_requires_perl_default
Requires:     SUNWgpch
%else
Requires:     perl >= 5.0.0
Requires:     patch
%endif

%description
A tool for building Solaris SVr4 packages based on RPM spec files.
Most features and some extensions of the spec format are implemented.

%prep
%setup -q -n pkgbuild-%version

%build
./configure --prefix=%{pkgbuild_prefix} --docdir=%_docdir/%srcname
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc COPYING AUTHORS NEWS
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%attr (0755, root, bin) %{_bindir}
%attr (0755, root, bin) %{_libdir}
%{_datadir}/%{srcname}
%{_mandir}

%changelog
* Wed Feb 12 2014 - Alex Viskovatoff <herzen@imap.cc>
- bump to 1.3.105
- remove all patches; they can be found at
  http://hg.openindiana.org/projects/sfe/oi-sfe-tools/file/14fc6fd0ac2d/pkgbuild
* Sun Apr 10 2011 - Alex Viskovatoff <herzen@imap.cc>
- add patches from oi-cbe, rearranging patches
* Sat Apr  2 2011 - Alex Viskovatoff <herzen@imap.cc>
- bump to 1.3.104 pre-release, creating a custom tarball with ./configure in it
- disable patches 2 and 3, since we don't use their functionality
* Fri Apr  1 2011 - Alex Viskovatoff <herzen@imap.cc>
- new experimental SFEpkgbuild.spec, using 4 patches
* Tue Jun 22 2010 - laca@sun.com
- updated %files for new doc and man pages
* Fri Apr 17 2009 - laca@sun.com
- add IPS Meta tags
* Fri Aug 11 2006 - <laca@sun.com>
- delete topdir stuff, we have per-user topdirs now
* Mon Aug 08 2005 - <laca@sun.com>
- add GNU Patch dependency
* Thu Dec 09 2004 - <laca@sun.com>
- Remove %topdir/* from the pkgmap and create these directories in %post
* Fri Mar 05 2004 - <laca@sun.com>
- fix %files
* Wed Jan 07 2004 - <laszlo.peter@sun.com>
- initial version of the spec file
