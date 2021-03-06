#
# spec file for package SFElibetpan
#
# includes module(s): libetpan
#
%include Solaris.inc

Name:		SFElibetpan
IPS_Package_Name:	library/mail/libetpan
Summary:	A mail library supporting IMAP, POP3, SMTP, NNTP, and Hotmail
Group:		System/Libraries
Version:	1.1
License:	BSD
SUNW_Copyright:	libetpan.copyright
Source:		%{sf_download}/libetpan/libetpan-%{version}.tar.gz
URL:		http://libetpan.sourceforge.net/libetpan/
SUNW_BaseDir:	%{_basedir}
buildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libetpan-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lsocket -lnsl"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/libetpan-config

%changelog
* Tue Feb 07 2012 - Milan Jurik
- bump to 1.1
* Wed Jul 20 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Thu Jun 10 2010 - pradhap (at) gmail.com
- Bump to 1.0
* Thu Oct 2 2008 - markwright@internode.on.net
- create
