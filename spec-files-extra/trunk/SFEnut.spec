#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

#for SmartOS global zone specify --with-opt_prefix
#tarball based install
%define with_opt_prefix %{?_with_opt_prefix:1}%{?!_with_opt_prefix:0}

%if %with_opt_prefix
%define _prefix /opt
%include base.inc
%define _sysconfdir /opt/etc
%define _localstatedir /var
%endif


Name:                SFEnut
IPS_Package_Name:	network/ups/nut
Summary:             Network UPS Tools
Version:             2.7.1
#%define major_minor_version %( echo %{version} |  awk -F'.' '{print $1 "." $2}' )
%define major_minor_version 2.7
Source:              http://www.networkupstools.org/source/%{major_minor_version}/nut-%{version}.tar.gz

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n nut-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi


export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"

echo _prefix %{_prefix}
echo _sysconfdir %{_sysconfdir}
echo _mandir %{_mandir}
./configure --prefix=%{_prefix}  \
            --sysconfdir=%{_sysconfdir} \
            --mandir=%{_mandir}  \
%if %with_opt_prefix
            --with-usb=no \
%else
            --with-usb=yes \
%endif
            --with-user=root \
	    --with-group=root \
	    --with-statepath=%{_localstatedir}/ups \


make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/ups

find $RPM_BUILD_ROOT%{_libdir} -type f -name '*.la' -exec rm -f {} \;
find $RPM_BUILD_ROOT%{_libdir} -type f -name '*.a' -exec rm -f {} \;

#%if %with_opt_prefix
#export RPM_BUILD_ROOT
#mkdir -p $RPM_BUILD_ROOT%{_datadir}/nut
##/usr/bin/elfedit -e 'dyn:runpath /opt/lib' $RPM_BUILD_ROOT/ups*
#(cd $RPM_BUILD_ROOT; tar cf $RPM_BUILD_ROOT%{_datadir}/nut-%{version}-opt.tar *)
#%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys)  %{_localstatedir}
%dir %attr (0755, root, sys)  %{_localstatedir}/ups
%{_datadir}/*
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*sample
#%class(renamenew) %{_sysconfdir}/*

%changelog
#* Thu Feb 20 2014 - Thomas Wagner
#- add tarball target for e.g. SmartOS
* Sun Feb  9 2014 - Thomas Wagner
- bump to 2.7.1
- add more %files
* Sat Mar 31 2012 - Pavel Heimlich
- fix download location 
* Sat Sep 30 2006 - Eric Boutilier
- Initial spec
