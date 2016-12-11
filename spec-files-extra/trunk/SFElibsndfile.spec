#
# spec file for package SFElibsndfile
#
# includes module(s): libsndfile
#
%include Solaris.inc
%include usr-gnu.inc
%include packagenamemacros.inc
%include pkgbuild-features.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libsndfile64 = libsndfile.spec
%endif

%include base.inc
%use libsndfile = libsndfile.spec


Name:                    SFElibsndfile
IPS_Package_Name:	 library/gnu/libsndfile
Summary:                 %{libsndfile.summary} (/usr/gnu)
Version:                 %{libsndfile.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: %{pnm_buildrequires_SUNWogg_vorbis_devel}
Requires:      %{pnm_requires_SUNWogg_vorbis}
BuildRequires: %{pnm_buildrequires_SUNWflac_devel}
Requires:      %{pnm_requires_SUNWflac}
BuildRequires: %{pnm_buildrequires_SUNWlibms_devel}
Requires:      %{pnm_requires_SUNWlibms}
BuildRequires: %{pnm_buildrequires_SUNWaudh}

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

#remember to %include pkgbuild-features.inc
%if %{pkgbuild_ips_legacy}
%package -n %{name}-renamed-noinst
Summary:                 %{summary} - was renamed to library/gnu/libsndfile
#STRONG NOTE: put the old name which is going away into IPS_Package_Name !!!
#this might be SFElibsndfile -> library/gnu/libsndfile then use pkg:/"SFElibsndfile"
IPS_package_name:	 SFElibsndfile
#aus programmcode: /opt/dtbld/lib/pkgbuild-1.3.104/pkgbuild.pl
#%_use_internal_dependency_generator
%define _use_internal_dependency_generator 0
IPS_legacy: false
SUNW_Pkg: SFElibsndfile
#NOTE: need a version rule, or get ignored. >= 1.1.1 or = * 
#renamed_to: library/gnu/libsndfile >= %{version}
Meta(pkg.renamed): true
Meta(pkg.waldfeebasis): true
#not allowed to place a depend into a obsoleted package! #Meta(pkg.obsolete): true
Meta(variant.opensolaris.zone): global, nonglobal
PkgBuild_Make_Empty_Package: true
Renamed_To: library/gnu/libsndfile = *
#%endif
#END os2nnn
#%endif
#END pkgbuild_ver_numeric >= 001003104 
#%package -n              SUNWgnome-l10ndocument-noinst
#IPS_package_name:        gnome/documentation/locale/noinst
#SUNW_Pkg: SUNWgnome-l10nmessages
#IPS_component_version: %{default_pkg_version}
#IPS_build_version: 5.11
#IPS_vendor_version: 0.175.0.0.0.0.0
#IPS_legacy: false
#Meta(pkg.obsolete): true
#Meta(org.opensolaris.consolidation): desktop
#Meta(variant.opensolaris.zone): global, nonglobal
#PkgBuild_Make_Empty_Package: true
%endif
#END pkgbuild_ips_legacy


%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libsndfile64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libsndfile.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libsndfile64.build -d %name-%version/%_arch64
%endif

%libsndfile.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libsndfile64.install -d %name-%version/%_arch64
%endif

%libsndfile.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

#to prevent old name SFElibsndfile, library/libsndfile and new name library/gnu/libsndfile
#be installed at the same time
#list *all* old package names here which could be installed on
#user's systems
%actions
depend fmri=SFElibsndfile type=optional
##TODO## check if the same name Solaris library library/libsndfile
#is matched as well, if we don't want this, needs a pkgmogrify rule then!
#we need to put the publisher here: fmri=pkg:/localhost<name>/library/libsndfile 
# depend fmri=sfe_publisher_name_keep_current/library/libsndfile type=optional
depend fmri=library/libsndfile type=optional


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sndfile-convert
%{_bindir}/sndfile-info
%{_bindir}/sndfile-play
%{_bindir}/sndfile-regtest
%{_bindir}/sndfile-cmp
%{_bindir}/sndfile-metadata-set
%{_bindir}/sndfile-metadata-get
%{_bindir}/sndfile-interleave
%{_bindir}/sndfile-salvage
%{_bindir}/sndfile-concat
%{_bindir}/sndfile-deinterleave
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
#%{_datadir}/octave
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/sndfile-convert
%{_bindir}/%{_arch64}/sndfile-info
%{_bindir}/%{_arch64}/sndfile-play
%{_bindir}/%{_arch64}/sndfile-regtest
%{_bindir}/%{_arch64}/sndfile-cmp
%{_bindir}/%{_arch64}/sndfile-metadata-set
%{_bindir}/%{_arch64}/sndfile-metadata-get
%{_bindir}/%{_arch64}/sndfile-interleave
%{_bindir}/%{_arch64}/sndfile-salvage
%{_bindir}/%{_arch64}/sndfile-concat
%{_bindir}/%{_arch64}/sndfile-deinterleave
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif


%changelog
* Sun Dec 11 2016 - Thomas Wagner
- change (Build)Requires to pnm_buildrequires_SUNWogg_vorbis_devel, pnm_buildrequires_SUNWlibms_devel (S12)
* Sun Nov 29 2015 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWflac_devel} SUNWaudh (OIH), %include packagenamemacros.inc
- don't set -features=extensions if cc_is_gcc / g++
* Fri Jul  5 2013 - Thomas Wagner
- add IPS_package_name and include hint to "gnu" location
* Sun Nov  4 2012 - Thomas Wagner
- relocate to /usr/gnu (pulseaudio needs >= 1.0.20 and dist has 1.0.17)
  (version is now 1.0.25 see base-specs/libsndfile.spec)
* Sun Feb 05 2012 - Brian Cameron
- Bump to 1.0.25.
* Wed Mar 23 2011 - Thomas Wagner
- bump to 1.0.24
* Sat May 09 2009 - Thomas Wagner
- submitting changes suggested by Srirama Sharma:
- add log note about removal of obsoleted libsndfile-01-flac-1.1.3.diff (removal on behalf Srirama Sharma)
- add libsndfile-01-common.diff (new) to fix feature with SUNSPRO compiler detection (add patch on behalf Srirama Sharma)
* Wed Apr 29 2009 - Srirama Sharma
- Fix files section to make 1.0.19 build without problems.
- Remove duplicate Requires: SUNWflac entry
* Tue Mar 03 2009 - Thomas Wagner
- bump to 1.0.19  in base-specs/libsndfile.spec
* Sat Aug 16 2008 - nonsea@users.sourceforge.net
- Add BuildRequires: SUNWaudh
* Fri Jun 13 2008 - trisk@acm.jhu.edu
- Allow building with SFEogg-vorbis again
* Mon May 05 2008 - brian.cameron@sun.com
- Now that we are building 64-bit libraries in SUNWogg-vorbis, remove
  dependency of SFEogg-vorbis and add SUNWogg-vorbis.
* Thu Jan 24 2007 - Thomas Wagner
- remove %{_mandir}/man1/* from the -devel package
* Sun Aug 12 2007 - dougs@truemail.co.th
- Converted to build 64bit
* Mon Apr 30 2007 - laca@sun.com
- bump to 1.0.17
- add gentoo patch that makes it build with flac 1.1.3
- add patch that fixes the cpp_test test program when built with sun studio
* Mon Jun 12 2006 - laca@sun.com
- rename to SFElibsndfile
- change to root:bin to follow other JDS pkgs.
- get rid of -share pkg
- move stuff around between base and -devel
- add missing deps
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
