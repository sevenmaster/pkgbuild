#
# spec file for package SFEperl-gtk2-sourceview
#
# includes module(s): perl-gtk2-sourceview
#

%include Solaris.inc

%define tarball_version 1.000
%define perl_version 5.8.4

Name:                    SFEperl-gtk2-sourceview
Summary:                 Gtk2-SourceView-%{tarball_version} PERL module for GtkSourceView widget.
Version:                 %{perl_version}.%{tarball_version}
Source:                  http://easynews.dl.sourceforge.net/sourceforge/gtk2-perl/Gtk2-SourceView-%{tarball_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:  SUNWperl584core
Requires:       SUNWperl584core
Requires:		SUNWgnome-base-libs
Requires:		SUNWgnome-gtksourceview
Requires:  		SUNWfreetype2
BuildRequires:	SFEperl-extutils-dep
BuildRequires:	SFEperl-extutils-pkg
Requires:		SFEperl-glib
Requires:		SFEperl-gtk2
Requires:		SFEperl-cairo
Requires:		SFEperl-gnome2-print

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif

%prep
%setup -q	 -c -n %name-%version

%build
cd Gtk2-SourceView-%{tarball_version}
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
    
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd Gtk2-SourceView-%{tarball_version}
make install

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Sun Jan 28 2007 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Updated how version is defined.
* Fri Jan 12 2007 - mike kiedrowski (lakeside-AT-cybrzn-DOT-com)
- Initial spec file
