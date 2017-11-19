



#make renamed-to-package
#set name=pkg.fmri value=pkg://openindiana.org/library/perl-5/archive-zip@1.37,5.11-2016.0.1.0:20161010T194403Z
#set name=userland.info.git-remote value=git://github.com/OpenIndiana/oi-userland.git
#set name=com.oracle.info.name value=Archive-Zip
#set name=userland.info.git-branch value=HEAD
#set name=userland.info.git-rev value=8e98cf6711528c2fc323d44108126e30e03cb496
#set name=pkg.summary value="Provide an interface to ZIP archive files"
#set name=info.classification value=org.opensolaris.category.2008:Development/Perl
#set name=info.source-url value=http://search.cpan.org/CPAN/authors/id/P/PH/PHRED/Archive-Zip-1.37.tar.gz
#set name=info.upstream-url value=http://search.cpan.org/dist/Archive-Zip/
#set name=org.opensolaris.consolidation value=userland
#set name=com.oracle.info.version value=1.37
#set name=variant.arch value=i386
#depend fmri=library/perl-5/archive-zip-516@1.37,5.11-2016.0.1.0 predicate=runtime/perl-516 type=conditional
#depend fmri=library/perl-5/archive-zip-522@1.37,5.11-2016.0.1.0 predicate=runtime/perl-522 type=conditional
#
#library/perl-5/archive-zip@1.37-2015.0.2.0
#
#





#
# spec file for package: SFEperl-archive-zip
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

%define tarball_version 1.30
%define tarball_name    Archive-Zip


%define deliver_files 1
%define deliver_no_files 0

#generate only the renamed package: --define 'perl_archive_zip_renamed_package 1'
#%if %{!?perl_archive_zipz_renamed_package:1}
%if %{?perl_archive_zip_renamed_package:1}0
%define deliver_files 0
%define deliver_no_files 1
%else
%define perl_archive_zip_renamed_package 0
%endif

%define _use_internal_dependency_generator 0

Name:		SFEperl-archive-zip
IPS_package_name: library/perl-5/archive-zip
Version:	%{tarball_version}
%if %{deliver_no_files}
IPS_Component_Version:   %{tarball_version}.0.1
%endif
Summary:	Provides an interface to ZIP archive files
License:	Artistic
Url:		http://search.cpan.org/~adamk/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
SUNW_Copyright: %{name}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Archive-Zip-%{tarball_version}.tar.gz

BuildRequires:	%pnm_buildrequires_perl_default
Requires:	%pnm_requires_perl_default

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Adam Kennedy <adamk@cpan.org>
Meta(info.upstream_url):        http://search.cpan.org/~adamk/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%if %{deliver_no_files}
#this tries to obsolete the package on the target OSdistro version, as it now has its own package
%if %(expr %{openindiana} '+' %{solaris12} '>=' 1 )

#START automatic renamed package  (remember to add as well %actions)
# create automatic package with old name and "renamed=true" in it
%include pkg-renamed.inc
#exception, as we don't deliver files on certain osdistro build versions, then our package is empty and is not allowed to have a (default: unknown) license file
Meta(pkg.renamed): true
PkgBuild_Make_Empty_Package: true
ips_legacy: false
%endif
#END openindiana hipster 2016

%package noinst-1
%define renamed_from_oldname      library/perl-5/archive-zip
#%define renamed_to_newnameversion library/zlib = *
#                   library/perl-5/archive-zip = 1.37-2015.0.2.0
%define renamed_to_newnameversion library/perl-5/archive-zip = 1.37-2015.0.2.0
%endif
#END deliver_no_files

%include pkg-renamed-package.inc

#list all the old published package name wich need to go away with upgrade to our new package name/location
#special case here, as we want the renamed part only be effective on S12 build 87 and up, we need to put a dependency on that release/name@5.12,5.12-5.12.0.0.0.87
#release/name can be "optional" as it is normally present and then it needs to have at least this revision
%actions
depend fmri=library/perl-5/archive-zip@%{version} type=optional

%endif
#END deliver_no_files





%description
Provides an interface to ZIP archive files
%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build
perl Makefile.PL PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT LIB=%{_prefix}/%{perl_path_vendor_perl_version}
make

%install
rm -rf $RPM_BUILD_ROOT
make pure_install
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_datadir}/man/man3 $RPM_BUILD_ROOT%{_datadir}/man/man3perl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_prefix}/perl%{perl_major_version}
%dir %attr(0755,root,sys) %{_datadir}
%{_mandir}
%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*

%changelog
* Sun Oct  8 2017 - Thomas Wagner
- add renamed-to package for removal (OIH, S12)
* Mon Sep 9 2011 - Thomas Wagner
- initial spec
