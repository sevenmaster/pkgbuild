#
# spec file for package SFEthrift-gpp
#
# includes module(s): thrift
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%define _basedir /usr/g++
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define srcname thrift

Name:                    SFEthrift-gpp
IPS_Package_Name:	 library/network/g++/thrift
Summary:                 thrift - Apache Thrift networking stack
Group:                   Utility
Version:                 0.9.0
URL:		         http://thrift.apache.org
Source:		         http://www.us.apache.org/dist/thrift/%{version}/thrift-%{version}.tar.gz
Patch1:        	thrift-01-pkgconfig.diff
License: 		 Apache 2.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SFEboost-gpp-devel
Requires:	SFEboost-gpp

%description
The Apache Thrift software framework, for scalable cross-language
services development, combines a software stack with a code generation
engine to build services that work efficiently and seamlessly between
C++, Java, Python, PHP, Ruby, Erlang, Perl, Haskell, C#, Cocoa,
JavaScript, Node.js, Smalltalk, OCaml and Delphi and other languages.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}                 \
            --with-boost=%{_prefix}             \
            --without-csharp                    \
            --without-erlang                    \
            --without-java                      \
            --without-python                    \
            --without-perl                      \
            --without-php                       \
            --without-php_extension             \
            --without-ruby                      \
            --without-haskell                   \
            --without-go                        \
            --without-d
# Note: there aren't any known problems with any of these languages
# I'm just not sure they are needed for this package and rather then
# add all the dependencies I've left them off although perhaps a
# better approach would be to use subpackages.

#make -j$CPUS
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libthrift*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/thrift
%{_includedir}/thrift/*

%changelog
* Mon Nov 5 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
