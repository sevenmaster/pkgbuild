#
# spec file for package: SFEperl-yaml-libyaml
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%include packagenamemacros.inc

%define srcname YAML-LibYAML

Name:		SFEperl-yaml-libyaml
IPS_package_name: library/perl-5/yaml-libyaml
Version:	0.62
Group:          Development/Libraries                    
Summary:	Perl YAML Serialization using XS and libyaml
License:	Artistic
Url:		http://github.com/ingydotnet/yaml-libyaml-pm
Source0:	http://search.cpan.org/CPAN/authors/id/T/TI/TINITA/%srcname-%version.tar.gz

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}
BuildRequires:	SFElibyaml
Requires:	SFElibyaml

%description
Kirill Siminov's libyaml is arguably the best YAML implementation. The C library
is written precisely to the YAML 1.1 specification. It was originally bound to
Python and was later bound to Ruby.  This module is a Perl XS binding to libyaml
which offers Perl the best YAML support to date.

%prep
%setup -q -n %srcname-%version

%build

if test -f Makefile.PL
  then
  # style "Makefile.PL"
  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    LIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLARCHLIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3

  make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC
else
  # style "Build.PL"
  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Build.PL \
    --installdirs vendor --makefile_env_macros 1 \
    --install_path lib=%{_prefix}/%{perl_path_vendor_perl_version} \
    --install_path arch=%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    --install_path libdoc=%{_mandir}/man3 \
    --destdir $RPM_BUILD_ROOT

  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Build build
fi

%install
rm -rf $RPM_BUILD_ROOT
if test -f Makefile.PL
   then
   # style "Makefile.PL"
   make install
else
   # style "Build.PL"
   %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Build install
fi

find $RPM_BUILD_ROOT -name .packlist -exec %{__rm} {} \; -o -name perllocal.pod  -exec %{__rm} {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%{_prefix}/%{perl_path_vendor_perl_version}/*
%dir %attr(0755,root,sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Tue Mar  1 2016 - Alex Viskovatoff <herzen@imap.cc>
- Generate new spec using make_perl_cpan_settings.pl
