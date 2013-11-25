#
# spec file for package SFEpkgtree
#

%define _use_internal_dependency_generator 0

%include Solaris.inc
%include packagenamemacros.inc

#description of this download method:
#https://fedorahosted.org/fpc/attachment/ticket/233/slask

#pkgtree
%define githubowner1  quattor
%define githubproject1 pkgtree
#for github commits see link on the right with the shortened commitid on the Webpage
#  -> https://github.com/quattor/pkgtree/commit/261c60c12323bc97975192823c5c3de1c32bb49f
%define commit1 261c60c12323bc97975192823c5c3de1c32bb49f
#remember to increas with every changed commit1 value
%define increment_version_helper 4
%define shortcommit1 %(c=%{commit1}; echo ${c:0:7})
#

Name:                    SFEpkgtree
IPS_Package_Name:        package/pkgtree
Group:                   System/Packaging
Summary:                 Display and query IPS package dependency tree (github version %{commit1})
Version:          0.0.0.0.0.%{increment_version_helper}
Source:           http://github.com/%{githubowner1}/%{githubproject1}/archive/%{shortcommit1}/%{githubproject1}-%{commit1}.tar.gz
URL:                     https://github.com/quattor/pkgtree
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{src_version}-build


%include default-depend.inc


%description
pkgtree displays the IPS package dependency tree on IPS based Systems. It takes package information from the running system, caches it, then displays dependency information for all packages or for an individual package selected by a full or partial FMRI.

There are three main views that can be obtained from pkgtree. The first is a list of packages and what they depend on (the 'depends' command). The second is a list of packages and what depends on them (the 'dependants' command). The third is a list of packages on which no other package depends ('no-dependants').

Each view may be affected by applying a variety of filters. See 'pkgtree -h' for more information.

Perl libraries are also available in this distribution providing APIs for obtaining and manipulating information about IPS packages from within a Perl script.

example:
pkgtree depends pkgtree
  |------(    require)--pkg://localhosts11/package/pkgtree@0.0.0.0.0.4,5.11-0.0.175.0.0.0.2.0:20131125T224942Z
  | pkg://solaris/system/library@0.5.11-0.175.0.0.0.2.1
  | pkg://solaris/system/kernel@0.5.11-0.175.0.0.0.2.1


%prep
%setup -q -n %{githubproject1}-%{commit1}

#%build

#dummy - nothing to make

#think on running the perl test routines in t/*


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp -p bin/pkgtree $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}
cp -pr lib/perl5/* $RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, bin)
%doc README.md
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%{_prefix}/%{perl_path_vendor_perl_version}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}



%changelog
* Mon Nov 25 2013 - Thomas Wagner
- fix install location for perl modules (tested: S11, S12, oi151a8)
- fix datadir/docdir owner/group
* Fri Nov 22 2013 - Thomas Wagner
- Initial spec
