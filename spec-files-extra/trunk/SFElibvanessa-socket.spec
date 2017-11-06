
# spec file for package SFElibvanessa-socket
# used by at least SFEperdition pop3/imap proxy

##TODO## check if changing the tarball name "_" to a "-" makes any problems

#note: "_" instead of "-" for later package name
%define src_name vanessa_socket
%include perditionparentversion.inc

%include Solaris.inc
%include packagenamemacros.inc

Name:                    SFElibvanessa-socket
IPS_Package_Name:	library/vanessa/socket
Summary:                 vanessa-socket - TCP socket interface library to support perdition imap/pop3 proxy/loadbalancer
URL:                     http://www.vergenet.net/linux/perdition/
#Version:                 n.m.o
Version:		%{libvanessa_socket_version}
Source:                  http://horms.net/projects/vanessa/download/vanessa_socket/%{version}/vanessa_socket-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires: %{pnm_buildrequires_SUNWlibpopt_devel}
BuildRequires: SFElibvanessa-logger
Requires: %{pnm_requires_SUNWlibpopt}
Requires: SFElibvanessa-logger

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"

export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --enable-dynamic     \
            --disable-static

gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/*la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/vanessa-socket.pc
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Fri May 22 2015 - Thomas Wagner
- add IPS_Package_Name
- new Download URL
* Thu May 21 2015 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWlibpopt_devel}, %include packagenamacros.inc
* Mon Aug 02 2010 - Thomas Wagner
- add to %files :   /usr/lib/pkgconfig/vanessa-socket.pc
- export Version to include/perditionparentversion.inc and detect automaticly 
  libraries version
- bump to 0.0.12
* Fri Jul  9 2010 - Thomas Wagner
- %include perditionparentversion.inc
- bump to 0.0.10
* Sat Jul 18 2009 - Thomas Wagner
- Initial spec
