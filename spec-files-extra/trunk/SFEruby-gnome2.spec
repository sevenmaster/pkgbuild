#
# spec file for package SFEruby-gnome2.spec
#
# includes module(s): ruby-gnome2
#
%include Solaris.inc

%define src_name	ruby-gnome2
%define src_url		http://nchc.dl.sourceforge.net/sourceforge/ruby-gnome2

Name:                   SFEruby-gnome2
IPS_package_name:		library/ruby-2/gnome2
Summary:                Ruby gnome2 bindings
Version:                2.2.0
Source:                 %{src_url}/%{src_name}-all-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEruby
BuildRequires: SFEruby-pkgconfig
Requires: SFEruby

%prep
%setup -q -n %{src_name}-all-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
ruby extconf.rb atk gdk_pixbuf2 gio2 glib2 gtk2 pango --vendor
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
* Tue Apr 29 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- Add BuildRequires: SFEruby-pkgconfig
* Tue Apr 29 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 2.2.0
- add IPS_package_name
- specify modules to build on extconf.rb line (gobject-introspection does not work)
- remove %{_bindir} from %files - there are no executables in this package
* Sun May 13 2007 - dougs@truemail.co.th
- Initial version
