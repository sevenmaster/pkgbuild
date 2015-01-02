#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name ddrescue

Name:                SFEddrescue
IPS_Package_Name:	storage/ddrescue
Summary:             Data recovery tool
Version:             1.19
License:             GPLv3+
Source:              http://ftp.gnu.org/gnu/ddrescue/%{src_name}-%{version}.tar.lz
URL:                 http://www.gnu.org/software/ddrescue/ddrescue.html

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElzip-gnu

%prep
#don't unpack please
%setup -q -c -T -n %{src_name}-%{version}
lzip -dc %SOURCE0 | (cd ${RPM_BUILD_DIR}; tar xf -)

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    CXX="$CXX"			\
	    CFLAGS="$CFLAGS"		\
	    CXXFLAGS="$CXXFLAGS"	\
	    LDFLAGS="$LDFLAGS"

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Wed Dec 17 2014 - Thomas Wagner
- bump to 1.19
- unpack sources with "lz" (lzip)
- use gcc/g++, function snprintf not in (older) studio compiler available
* Sun Mar 11 2012 - Milan Jurik
- bump to 1.15
* Tue Mar 10 2011 - Thomas Wagner
- bump to 1.14
* Sun Apr 18 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec
