#
# spec file for package SFEruby-pkgconfig
#
# includes module(s): ruby-pkgconfig
#
%include Solaris.inc

%define src_name	ruby-pkgconfig

Name:                   SFEruby-pkgconfig
IPS_package_name:		library/ruby-2/pkgconfig
Summary:                Implementation of pkg-config in Ruby
Version:                1.1.5
Source0:                http://gems.rubyforge.org/gems/pkg-config-%{version}.gem
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEruby
Requires: SFEruby

%prep
if [ ! -d %{_builddir}/%{src_name}-%{version} ]; then
	mkdir %{_builddir}/%{src_name}-%{version}
fi
cp %SOURCE0 %{_builddir}/%{src_name}-%{version}/

%install
cd %{_builddir}/%{src_name}-%{version}
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/`ruby -rubygems -e'puts Gem.default_dir'`
gem install \
	--no-user-install \
	--ignore-dependencies \
	-i "$RPM_BUILD_ROOT/`ruby -rubygems -e'puts Gem.default_dir'`" \
	pkg-config-%{version}.gem

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%changelog
* Tue Apr 29 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial version 1.1.5
