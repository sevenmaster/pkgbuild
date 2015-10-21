#
# spec file for package libyaml
#
# includes module(s): libyaml
#
%include Solaris.inc
%include packagenamemacros.inc

%define _prefix /usr
%define	tarball_version	0.1.6
%define	tarball_name yaml
%define	src_url	http://pyyaml.org/download/libyaml

Name:		SFElibyaml
Summary:	LibYAML is a YAML 1.1 parser and emitter written in C. 
Version:	%{tarball_version}
IPS_package_name:  library/text/yaml
License:	MIT license
Source:		%{src_url}/%{tarball_name}-%{tarball_version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

#Meta(info.maintainer_url):      http://pyyaml.org/wiki/LibYAML
Meta(info.upstream_url):        http://pyyaml.org/wiki/LibYAML
#Meta(info.classification):      org.opensolaris.category.2011:Media

%prep
%setup -c -n %{name}-%{version}

%ifarch amd64 sparcv9
rm -rf %{tarball_name}-%{tarball_version}-64
cp -rp %{tarball_name}-%{tarball_version} %{tarball_name}-%{tarball_version}-64
%endif

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

cd %{tarball_name}-%{tarball_version}
%ifarch sparc
%define target sparc-sun-solaris
%else
%define target i386-sun-solaris
%endif

export CFLAGS="-i -xO4 -xspace -xstrconst -fast -Kpic -xregs=no%frameptr -xCC"

./configure --prefix=%_prefix

make -j$CPUS

%ifarch amd64 sparcv9
cd ../%{tarball_name}-%{tarball_version}-64

export CFLAGS="-m64 -i -xO4 -xspace -xstrconst -fast -Kpic -xregs=no%frameptr -xCC"

./configure\
 --prefix=%{_prefix}\
 --exec-prefix=%{_prefix}\
 --libdir=%{_libdir}/%{_arch64} \
 --includedir=%{_includedir} \
 --mandir=%{_mandir}

gmake -j$CPUS
%endif

%install
cd %{tarball_name}-%{tarball_version}
make install DESTDIR=$RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd ../%{tarball_name}-%{tarball_version}-64
make install DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr(0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*
%endif
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Wed Oct 21 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Remove errant backslash in configure line in :46
* Thu Aug 27 2015 - Alex Viskovatoff <herzen@imap.cc>
- bump to 0.1.6
* Fri Dec 21 2012 - Logan Bruns <logan@gedanken.org>
- fixed some permissions.
* Sat Jun 25 JST 2011 TAKI, Yasushi <taki@justplayer.com>
- Initial Revision

