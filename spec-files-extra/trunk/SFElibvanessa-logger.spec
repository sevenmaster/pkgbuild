
# spec file for package SFElibvanessa-logger
# used by at least SFEperdition pop3/imap proxy

##TODO## check if changing the tarball name "_" to a "-" makes any problems

#note: "_" instead of "-" for later package name
%define src_name vanessa_logger
%include perditionparentversion.inc

%include Solaris.inc

Name:                    SFElibvanessa-logger
IPS_Package_Name:	library/vanessa/logger
Summary:                 vanessa-logger - logging functions library to support perdition imap/pop3 proxy/loadbalancer
URL:                     http://www.vergenet.net/linux/perdition/
#Version:                 n.m.o
Version:		%{libvanessa_logger_version}
Source:                  http://www.vergenet.net/linux/perdition/download/%{perditionparentversion}/vanessa_logger-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc


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
%{_libdir}/pkgconfig/*
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
* Sun Feb  2 2012 - Thomas Wagner
- fix %files for pkgconfig/ not included
* Mon Aug 02 2010 - Thomas Wagner
- export Version to include/perditionparentversion.inc and detect automaticly 
  libraries version
- bump to 0.0.10 (in file include/perditionparentversion.inc)
* Fri Jul  9 2010 - Thomas Wagner
- %include perditionparentversion.inc
- bump to 0.0.8
* Sat Jul 18 2009 - Thomas Wagner
- Initial spec
