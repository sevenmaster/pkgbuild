# 
# 
# 
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc

%define srcdate 130518

Name:                SFEjd
IPS_Package_Name:	desktop/2ch/jd
License:             GPL
Summary:             2ch browser (gtkmm/GTK+)
Version:             2.8.6
Source:              http://iij.dl.sourceforge.jp/jd4linux/58841/jd-%{version}-%{srcdate}.tgz
Patch0:              jd-timegm.diff
Patch1:              jd-iconv-const.diff
URL:                 http://sourceforge.jp/projects/jd4linux
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
Group:		     Applications/Internet
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEgcc
Requires:      SFEgccruntime
BuildRequires: %{pnm_buildrequires_SUNWopenssl_devel}
Requires:      %{pnm_requires_SUNWopenssl}
BuildRequires: SFEgtkmm-gpp
Requires:      SFEgtkmm-gpp
BuildRequires: SFElibiconv-devel
Requires:      SFElibiconv

%description
Client for 2channel messageboards

%prep
%setup -q -n jd-%{version}-%{srcdate}
%patch0 -p1
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags} -I/usr/g++/include -I%{gnu_inc}"
export CXXFLAGS="%{optflags} -I/usr/g++/include -I%{gnu_inc}"
export LDFLAGS="%{_ldflags} -L/usr/g++/lib -R/usr/g++/lib %{gnu_lib_path} -liconv"
export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig


bash autogen.sh
./configure				\
	--prefix=%{_prefix} \
	--with-openssl

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%changelog
* Thu Nov 14 2013 - Ian Johnson <ianj0h@yahoo.co.jp>
- Use standard CFLAGS / CXXFLAGS / LDFLAGS
- Add %description
- Fix Group
- use bash autogen.sh
* Fri Oct 25 2013 - Ian Johnson <ianj0h@yahoo.co.jp>
- Add BuildRequires: SFEgcc and Requires: SFEgccruntime
- Fix Summary
* Thu Oct 24 2013 - Ian Johnson <ianj0h@yahoo.co.jp>
- Initial spec
