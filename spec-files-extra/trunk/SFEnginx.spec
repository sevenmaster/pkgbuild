#
# spec file for package SFEnginx
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# NOTE: This package will include all normally-optional modules which do not
#       require dependencies. GeoIP, image-filter, xslt have dependencies and
#       therefore do not get built without explicit request.

# Recognized options:
# --define 'nginxuser USERNAME'		specify the system user (Default: webservd)
# --define 'nginxgroup GROUPNAME'	specify the system group (Default: webservd)
# --define 'cpu CPUTYPE'		specify the target CPU
#					Choose target CPU from:
#					pentium, pentiumpro, pentium3,
#					pentium4, athlon, opteron,
#					sparc32, sparc64
# --with-gcc				build with GCC instead of Sun Studio
# --with-geoip				Enable GeoIP module (not done yet)

###
### TODO:
###
### ! Determine if rtsig/select should be included (probably not)
### ! Man Page
### ! Test on SPARC
### ! Verify sanity of default config
### * GeoIP
### 

%include Solaris.inc
%include packagenamemacros.inc

Name:		SFEnginx
IPS_Package_Name:	web/server/nginx
Version:	1.14.1
Summary:	Free, open-source, high-performance HTTP server and reverse proxy
Source:		http://nginx.org/download/%{sname}-%{version}.tar.gz
Source1:	http-nginx
Source2:	http-nginx.xml
URL:		http://nginx.org/
Group:		System/Services
License:	BSD
SUNW_Copyright:	%{sname}.copyright
SUNW_BaseDir:	%{_basedir}
SUNW_Hotline:	http://wiki.nginx.org/NginxFaq
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

# IPS Manifest stuff
Meta(info.upstream):		Igor Sysoev <http://sysoev.ru/en/>

%include default-depend.inc

BuildRequires:	%{pnm_buildrequires_SUNWgsed_devel}
BuildRequires:	%{pnm_buildrequires_SUNWopenssl_include}
Requires:		%{pnm_requires_SUNWopenssl_libraries}
Requires:		%{pnm_requires_SUNWpcre}
Requires:		%{pnm_requires_SUNWzlib}
Requires:		%{pnm_requires_SUNWlxsl}
BuildRequires:	%{pnm_buildrequires_SUNWgd2_devel}
Requires:		%{pnm_requires_SUNWgd2}
Requires:		%{pnm_requires_SUNWlxml}
Requires:		%{pnm_requires_SUNWlxsl}

%package root
Summary:		%{name} - root filesystem files, /
SUNW_BaseDir:		/
Requires: %name

%description
Nginx (pronounced "engine ex") is a free, open-source, high-performance HTTP
server and reverse proxy, as well as an IMAP/POP3 proxy server. Igor Sysoev
started development of Nginx in 2002, with the first public release in 2004.

Nginx is known for its high performance, stability, rich feature set, simple
configuration, and low resource consumption. 

Nginx is one of a handful of servers written to address the C10K problem.
Unlike traditional servers, Nginx doesn't rely on threads to handle requests.
Instead it uses a much more scalable event-driven (asynchronous) architecture.
This architecture uses small, but more importantly, predictable amounts
of memory under load.

Even if you don't expect to handle thousands of simultaneous requests, you can
still benefit from Nginx's high-performance and small memory footprint. Nginx
scales in all directions: from the smallest VPS all the way up to clusters of
servers.

Some configuration guides:
https://www.nginx.com/resources/wiki/start
http://nginx.org/en/docs/beginners_guide.html
http://blog.martinfjordvald.com/2010/07/nginx-primer (updated 2014, wrote a book?)



%prep
%setup -q -n %{sname}-%{version}

#########################
# User-overrideable stuff
#########################

# See above for more information.

# Username to run as
%define nginxuser %{?!nginxuser:webservd}%{?nginxuser}

# Group to run as
%define nginxgroup %{?!nginxgroup:webservd}%{?nginxgroup}

# Whether to enable HTTP image filter module
# (Adds an unspecified dependency; not yet done.)
%define geoip %{?_with_geoip:--with-http_geoip_module}%{!?_with_geoip:}

# Is there a better way to refer to /lib?
%define methodpath /lib/svc/method
%define manifestpath %{_localstatedir}/svc/manifest/network

#############################
# End User-overrideable stuff
#############################

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%if %{?_with_gcc}
# GCC
%define %cc_is_gcc 1
export CC=gcc
export CXX=g++
export LDFLAGS="%{_ldflags}"

%else
# Sun Studio
export LDFLAGS="%{_ldflags}"
export CFLAGS="%{optflags}"

%endif # _with_gcc

# export LD=/usr/ccs/bin/ld

# Define the things we use more than once.
%define statedir %{_localstatedir}/%{sname}
%define logdir %{statedir}/logs
%define confpath %{_sysconfdir}/%{sname}/%{sname}.conf
%define pidpath %{statedir}/nginx.pid
%define sbinpath %{_sbindir}/%{sname}

./configure								\
		--conf-path=%{confpath}					\
		--error-log-path=%{logdir}/error.log			\
		--group=%{nginxgroup}					\
		--http-client-body-temp-path=%{statedir}/client_body_temp \
		--http-fastcgi-temp-path=%{statedir}/fastcgi_temp	\
		--http-log-path=%{logdir}/access.log			\
		--http-proxy-temp-path=%{statedir}/proxy_temp		\
		--http-scgi-temp-path=%{statedir}/scgi_temp		\
		--http-uwsgi-temp-path=%{statedir}/uwsgi_temp		\
		--lock-path=%{statedir}/nginx.lock			\
		--pid-path=%{pidpath}		\
		--prefix=%{statedir}		\
		--sbin-path=%{sbinpath}		\
		--user=%{nginxuser}		\
		--with-http_addition_module	\
		--with-http_dav_module		\
		--with-http_flv_module		\
		--with-http_gzip_static_module	\
		--with-http_random_index_module	\
		--with-http_realip_module	\
		--with-http_secure_link_module	\
		--with-http_ssl_module		\
		--with-http_stub_status_module	\
		--with-http_sub_module		\
		--with-ipv6			\
		--with-select_module		\
		--with-http_xslt_module		\
		%{geoip}

		#no longer valid --with-rtsig_module		\

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{methodpath}
install -d $RPM_BUILD_ROOT%{manifestpath}
install %{SOURCE1} $RPM_BUILD_ROOT%{methodpath} # SMF method
install %{SOURCE2} $RPM_BUILD_ROOT%{manifestpath} # SMF manifest

gsed -i 's~-CONF_PATH-~%{confpath}~' $RPM_BUILD_ROOT%{methodpath}/http-nginx
gsed -i 's~-PID_PATH-~%{pidpath}~' $RPM_BUILD_ROOT%{methodpath}/http-nginx
gsed -i 's~-SBIN_PATH-~%{sbinpath}~' $RPM_BUILD_ROOT%{methodpath}/http-nginx

gsed -i 's~-METHOD_PATH-~%{methodpath}/http-nginx~' $RPM_BUILD_ROOT%{manifestpath}/http-nginx.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_sbindir}

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, bin) %{_sysconfdir}/%{sname}
%config %attr (0644, root, bin) %{_sysconfdir}/%{sname}/*
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, %{nginxuser}, %{nginxgroup}) %{_localstatedir}/%{sname}
%dir %attr (0755, root, bin) %{_localstatedir}/%{sname}/html
%attr (0644, root, bin) %{_localstatedir}/%{sname}/html/*
%dir %attr (0755, %{nginxuser}, %{nginxgroup}) %{_localstatedir}/%{sname}/logs
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0755, root, bin) /lib/svc/method/*
%class(manifest) %attr(0755, root, sys)/var/svc/manifest/*


%changelog
* Sun Nov 11 2018 - Ian Johnson
- bump to 1.14.1
* Wed May 30 2018 - Ian Johnson
- bump to 1.14.0
* Sun Dec 31 2017 - Thomas Wagner
- bump to 1.13.8
* Fri Nov 03 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 1.12.2
* Thu Sep 21 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 1.12.1
* Thu May 18 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 1.12.0
* Thu Feb 02 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 1.10.3
* Wed Jan 25 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 1.10.2
* Sat Apr 23 2016 - Thomas Wagner
- bump to 1.9.15
* Tue Oct 20 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 1.8.0
* Thu Apr 02 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 1.7.11
- add %config to config files
* Fri Apr 18 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- add CFLAGS
* Tue Apr 15 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- fix IPS_package_name to match other web server packages
* Wed Apr 09 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 1.4.7
* Wed Jul 03 2013 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 1.4.1
* Tue Feb 07 2012 - Milan Jurik
- bump to 1.0.12
* Fri Oct 14 2011 - Thomas Wagner
- fix syntax in http-nginx.xml SMF manifest , no functional SMF testing done
* Thr Mar 17 2011 - Thomas Wagner
- fix packaging ownergroup of directories to smf manifest 
- fix directory and files permissions in %files root for /lib/..., method, manifest
* Wed Nov 17 2010 - Matt Lewandowsky <matt@greenviolet.net>
- Added SMF manifest/method.
* Tue Nov 16 2010 - Matt Lewandowsky <matt@greenviolet.net>
- Initial version
