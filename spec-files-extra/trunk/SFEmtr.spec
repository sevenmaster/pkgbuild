#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Note: must be root to run /usr/sbin/mtr.

%include Solaris.inc

Name:                SFEmtr
IPS_Package_Name:	network/mtr
Summary:             Ping/Traceroute network diagnostic tool with GTK support
License:             GPLv2
SUNW_Copyright:      mtr.copyright
URL:                 http://www.bitwizard.nl/mtr/
Version:             0.85
Source:              ftp://www.BitWizard.nl/mtr/mtr-%{version}.tar.gz
Patch1:              mtr-01-fionbio.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWncurses
Requires: SUNWncurses

%prep
%setup -q -n mtr-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
# Must omit "-Wl,-zignore" or else GTK support won't work. 
# I'm not sure why though...
export LDFLAGS="-Wl,-zcombreloc -Wl,-Bdirect %{gnu_lib_path} -lncurses"
export CFLAGS="-O4 -fPIC -DPIC -Xlinker -i -fno-omit-frame-pointer %{gnu_lib_path}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
cp mtr   $RPM_BUILD_ROOT%{_sbindir}

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
cp mtr.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%changelog
* Mon Sep 09 2013 - Milan Jurik
- bump to 0.85
* Sun Dec 11 2011 - Milan Jurik
- bump to 0.82
* Sun Jul 24 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Wed Mar 16 2011 - Milan Jurik
- bump to 0.80
* Wed Mar 16 2011 - Thomas Wagner
- linker error unresolved wattr_on wattr_off - use SUNWncurses, add to *FLAGS %{gnu_lib_path} and -lncurses
- (Build)Requires SUNWncurses
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Fri Jan 12 2007 - Eric Boutilier
- Fix missing LDFLAGS and CFLAGS
* Thu Jan 11 2007 - Eric Boutilier
- Initial spec
