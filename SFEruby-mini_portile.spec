#
# spec file for package SFEruby-mini_portile
#
# includes module(s): ruby-mini_portile
#
%include Solaris.inc

%define src_name	mini_portile

Name:                   SFEruby-mini-portile
IPS_package_name:		library/ruby-2/mini_portile
Summary:                HTML, XML, SAX, and Reader parser
Version:                0.6.2
Source0:                http://rubygems.global.ssl.fastly.net/gems/%{src_name}-%{version}.gem
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
	%{src_name}-%{version}.gem

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%changelog
* Mon Mar 02 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial version 0.6.2
