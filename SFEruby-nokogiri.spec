#
# spec file for package SFEruby-nokogiri
#
# includes module(s): ruby-nokogiri
#
%include Solaris.inc

%define src_name	nokogiri

Name:                   SFEruby-nokogiri
IPS_package_name:		library/ruby-2/nokogiri
Summary:                HTML, XML, SAX, and Reader parser
Version:                1.6.6.2
Source0:                http://rubygems.global.ssl.fastly.net/gems/%{src_name}-%{version}.gem
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEruby
BuildRequires: SFEruby-mini-portile
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
- Initial version 1.6.6.2
