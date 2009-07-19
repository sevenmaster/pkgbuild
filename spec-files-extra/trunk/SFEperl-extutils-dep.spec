#
# spec file for package SFEperl-extutils-dep
#
# includes module(s): perl-extutils-dep
#

%include Solaris.inc

%define tarball_version 0.302
%define perl_version 5.8.4

Name:                    SFEperl-extutils-dep
Summary:                 ExtUtils-Depends-%{tarball_version} PERL module
Version:                 %{perl_version}.%{tarball_version}
Source:                  %{sf_download}/gtk2-perl/ExtUtils-Depends-%{tarball_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                SUNWperl584core
BuildRequires:           SUNWperl584core

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int
%endif

%prep
%setup -q	-c -n %name-%version

%build
cd ExtUtils-Depends-%{tarball_version}
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd ExtUtils-Depends-%{tarball_version}
make install

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/ExtUtils
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/*
%{_prefix}/perl5/vendor_perl/%{perl_version}/ExtUtils/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Sat Jul 18 2009 - matt@greenviolet.net
- Bump version to 0.302
* Sun Jan 28 2007 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Updated how version is defined.
* Fri Aug 18 2006 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Change name from SUNWperl-extutils-dep.spec to SFEperl-extutils-dep.spec
* Sun Jul 02 2006 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec file
