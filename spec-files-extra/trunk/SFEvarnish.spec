  # pkg install library/pcre                                                                                                                                             
  # pkg install gnu-gettext                                                                                                                                              
  # wget http://repo.varnish-cache.org/source/varnish-3.0.5.tar.gz                                                                                                       
  # tar xzf varnish-3.0.5.tar.gz                                                                                                                                         
  # cd varnish-3.0.5                                                                                                                                                     
  # ./configure CFLAGS=-m64 PCRE_LIBS="-L/usr/lib -lpcre" PCRE_CFLAGS=-I/usr/include/pcre                                                                                
  # make                                                                                                                                                                 
  # make install                             

##
# spec file for package: varnish
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

##TODO## make SMF manifest more nice, check for /etc/varnish.cfg present

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%include packagenamemacros.inc

%define src_name varnish

# /var/svc/manifest/..l1../..l2..
%define svcdirl1 application
%define svcdirl2 proxy

Name:           SFEvarnish
IPS_Package_Name: web/proxy/varnish
Group:		WebServices/ApplicationandWebServers
Summary:        Varnish
Version:        3.0.6
License:        FreeBSD
URL:            http://www.varnish-cache.org
Source:         http://repo.varnish-cache.org/source/varnish-%{version}.tar.gz
Source1:	%{src_name}.xml
Source2:	%{src_name}.cfg

Meta(info.upstream): varnish-misc@varnish-cache.org
Meta(info.classification): org.opensolaris.category.2008:Applications/Internet


BuildRoot:      %{_tmppath}/%{src_name}-%{version}-build
SUNW_Basedir:   /
SUNW_Copyright: %{src_name}.copyright


#####################################
##  Package Requirements Section   ##
#####################################

%include default-depend.inc
BuildRequires:	SFEgcc
Requires:	SFEgccruntime
BuildRequires:	%{pnm_buildrequires_SUNWopenssl}
Requires:	%{pnm_requires_SUNWopenssl}
BuildRequires:	%{pnm_buildrequires_SUNWlibms}
Requires:	%{pnm_requires_SUNWlibms}
BuildRequires:	%{pnm_buildrequires_library_pcre}
Requires: 	%{pnm_requires_library_pcre}
BuildRequires:	%{pnm_buildrequires_SUNWzlib}
Requires:	%{pnm_requires_SUNWzlib}
BuildRequires:	%{pnm_buildrequires_SUNWbzip}
Requires:	%{pnm_requires_SUNWbzip}


%description
Varnish cache accellerates web applications by caching.
See the website %{URL} for all details.

%prep
%setup -q -n %{src_name}-%{version}


%build
#/usr/gnu/bin/gcc or /usr/gcc/bin/gcc
export CC=gcc
export LDFLAGS="%_ldflags -lmtmalloc"
export CFLAGS="%{optflags} -I/usr/include/pcre"

./configure --prefix=%{_prefix} \
            --sysconfdir=%{_sysconfdir} \
	    --localstatedir=%{_localstatedir} \



%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#Install example config file
#cp "%{SOURCE2}" "${RPM_BUILD_ROOT}/etc/varnish.cfg.example"

#Install manifest
mkdir -p ${RPM_BUILD_ROOT}/%{_localstatedir}/svc/manifest/%{svcdirl1}/%{svcdirl2}
cp "%{SOURCE1}" "${RPM_BUILD_ROOT}/%{_localstatedir}/svc/manifest/%{svcdirl1}/%{svcdirl2}/%{src_name}.xml"

find ${RPM_BUILD_ROOT}/%{_prefix} -name \*la -exec rm {} \;


%clean
rm -rf %{buildroot}

%if %(test -f /usr/sadm/install/scripts/i.manifest && echo 0 || echo 1)
%iclass manifest -f i.manifest
%endif


%files
%defattr(-,root,sys)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*
%{_libdir}/varnish*
%dir %attr(0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr(0755, root, bin) %{_mandir}/man7
%{_mandir}/man7/*

%dir %attr(755,root,sys) /etc
#%config(noreplace) %attr(644,root,root) /etc/*
%{_sysconfdir}/*

%defattr(-,root,sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/%{src_name}
%class(manifest) %attr (0444, root, sys) %{_localstatedir}/svc/manifest/%{svcdirl1}/%{svcdirl2}



%changelog
* Wed Feb 15 2015 - Thomas Wagner
- bump to 3.0.5
* Fri Oct 28 2011 - Thomas Wagner
- initial version
