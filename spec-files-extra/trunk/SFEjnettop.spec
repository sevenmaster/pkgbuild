#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEjnettop
Summary:             Similar to top, but for network traffic
Version:             0.13.0
Source:              http://jnettop.kubs.info/dist/jnettop-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: %{pnm_buildrequires_SUNWncurses_devel}
Requires:      %{pnm_requires_SUNWncurses}
BuildRequires: SFElibpcap-devel
Requires:      SFElibpcap

%prep
%setup -q -n jnettop-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

# Custom CFLAGS settings aren't getting into Makefile, but Studio 
# cc needs -xO not -O, and location of ncurses needs to be specified. 
# Therefore I hacked Makefile.in on-the-fly thusly...
# (TODO: Report this bug upstream.)

perl -i.orig -lpe 's/\-O0/-xO4 -I\/usr\/gnu\/include/ if $. == 90' Makefile.in

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir}
	    
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*.8
%dir %attr (0755, root, other) %{_datadir}/jnettop
%{_datadir}/jnettop/*

%changelog
* Fri Jul  5 2013 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWncurses_devel}, %include packagenamemacros.inc
* Wed Nov 08 2006 - Eric Boutilier
- Initial spec
