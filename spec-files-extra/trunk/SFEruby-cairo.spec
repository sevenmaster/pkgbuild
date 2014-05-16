#
# spec file for package SFEruby-gnome2.spec
#
# includes module(s): ruby-gnome2
#
%include Solaris.inc

%define src_name	rcairo

Name:                   SFEruby-cairo
IPS_package_name:		library/ruby-2/cairo
Summary:                Ruby cairo bindings
Version:                1.12.9
Source:                 https://github.com/%{src_name}/%{src_name}/archive/v%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEruby
BuildRequires: SFEruby-pkgconfig
Requires: SFEruby

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
ruby extconf.rb --vendor
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%changelog
* Thu May 15 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial version
