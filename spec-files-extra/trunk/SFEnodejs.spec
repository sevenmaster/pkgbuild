#
# spec file for package SFEnodejs
#
# includes module(s): nodejs
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%include packagenamemacros.inc

Summary:	Asynchronous JavaScript Engine  
Name:		SFEnodejs  
IPS_Package_Name:	runtime/javascript/nodejs
Version:	0.12.0
License:	BSD  
Group:		System/Libraries  
URL:		http://nodejs.org/  
Source:		http://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz  
#probably we want mdb, need libproc.h (ONbld)
Patch1:		nodejs-01-configure-disable-mdb-is-this-sad.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

BuildRequires: SFEgcc
Requires: SFEgccruntime

%if %( expr %{solaris11} '|' %{solaris12} )
#get ec.h
##TODO## for SVR4 create and change this to pnm_buildrequires_SUNWopenssl_fips_140_include
BuildRequires: library/security/openssl/openssl-fips-140
Requires:      library/security/openssl/openssl-fips-140
%else
BuildRequires: %{pnm_buildrequires_SUNWopenssl}
Requires:      %{pnm_requires_SUNWopenssl}
%endif

%description  
Node's goal is to provide an easy way to build scalable network  
programs. In the above example, the two second delay does not prevent  
the server from handling new requests. Node tells the operating system  
(through epoll, kqueue, /dev/poll, or select) that it should be  
notified when the 2 seconds are up or if a new connection is made --  
then it goes to sleep. If someone new connects, then it executes the  
callback, if the timeout expires, it executes the inner callback. Each  
connection is only a small heap allocation.  

mdb is disabled
ssl3 is disabled

%package devel  
Summary:	Development headers for nodejs  
Group:		Development/Libraries  

%description devel  
Development headers for nodejs.  

%prep  
%setup -q -n node-v%{version}  

%patch1 -p1



%build  
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export LDFLAGS="%{_ldflags} -R/lib/openssl/fips-140/ -L/lib/openssl/fips-140/"

./configure --prefix=%{_prefix} \
        --shared-openssl        \
%if %( expr %{solaris11} '|' %{solaris12} )
        --shared-openssl-includes=/usr/include/openssl/fips-140 \
        --shared-openssl-libpath=/lib/openssl/fips-140          \
%endif

# --gdb

#trick missing CXXFLAGS/CPPFLAGS in build system systems with ec.h in fips-140 location
#illumos finds ec.h in /usr/include/openssl/ec.h, Solaris in /usr/include/openssl/fips-140/openssl/ec.h
export CFLAGS="%{optflags}"
%if %( expr %{solaris11} '|' %{solaris12} )
[ -d src ] || mkdir src
[ -s src/openssl ] || ln -s /usr/include/openssl/fips-140/openssl src/openssl
%endif

gmake -j$CPUS

%install  
rm -rf $RPM_BUILD_ROOT  
export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

gmake install DESTDIR=$RPM_BUILD_ROOT

%clean  
rm -rf $RPM_BUILD_ROOT  
  
%files  
%defattr(-, root, bin)
%doc AUTHORS ChangeLog LICENSE
%{_bindir}/node
%{_bindir}/npm
%dir %attr (0755, root, sys) %{_datadir}
#well, remove that in %install?
%{_datadir}/systemtap/*
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}
#dir is gone %{_libdir}/node
%{_libdir}/node_modules
%{_libdir}/dtrace/node.d

%files devel  
%defattr(-, root, bin)  
#file is gone %{_bindir}/node-waf
%{_includedir}/node  

%changelog  
* Sun Feb  8 2015 - Thomas Wagner
- bump to 0.12.0
- add patch nodejs-01-configure-disable-mdb-is-this-sad.diff
- add (Build)Requires library/security/openssl/openssl-fips-14 (S11, S12)
- find fips-140/openssl/ec.h headers via local symlink in src/openssl (S11, S12)
- add Build)Requires %{pnm_buildrequires_SUNWopenssl}, include packagenamemacros.inc
* Sun Jan  4 2015 - Thomas Wagner
- fix %files for %{_bindir}/node-waf
* Sat Jan  3 2015 - Thomas Wagner
- bump to 0.10.35
- fix %files for %{_libdir}/node
* Wed Aug 20 2014 - Thomas Wagner
- bump to 0.10.31
* Mon Jun 16 2014 - Thomas Wagner
- bump to 0.10.29 - #Node v0.8.27 (maint) and v0.10.29 (stable) released updating OpenSSL and fixing a UTF-8 issue with a breaking change
* Wed Jan  1 2014 - Thomas Wagner
- bump to 0.10.24
* Sun May 26 2013 - Thomas Wagner
- bump to 0.10.8
* Wed Mar 06 2013 - Thomas Wagner
- bump to 0.8.21
* Wed Feb 06 2013 - Thomas Wagner
- bump to 0.8.19
* Fri Jan 11 2013 - Thomas Wagner
- bump to 0.8.17
* Sun Dec 30 2012 - Thomas Wagner
- bump to 0.8.16
* Thu Aug 30 2012 - Milan Jurik
- bump to 0.8.8
* Fri Jul 27 2012 - Milan Jurik
- bump to 0.8.4
* Wed May 16 2012 - Milan Jurik
- bump to 0.6.18
* Sat Dec 31 2011 - Milan Jurik
- bump to 0.6.6
* Sat Nov 19 2011 - Milan Jurik
- bump to 0.6.2
* Thu Jun 30 2011 - Milan Jurik
- bump to 0.4.9
* Thu Mar 24 2011 - Thomas Wagner
- bump to 0.4.3
* Sat Mar 05 2011 - Milan Jurik
- bump to 0.4.2, use internal libev
* Wed Jan 05 2011 - Milan Jurik
- bump to 0.2.6
* Sun Nov 28 2010 - Milan Jurik
- bump to 0.2.5
* Fri Nov 12 2010 - Milan Jurik
- bump to 0.2.4
* Sat Oct 16 2010 - Milan Jurik
- bump to 0.2.3
* Thu Sep 07 2010 - Milan Jurik
- initial spec
