# base-specs/lxml.spec for SFElxml.spec

# owner: tom68


Name:                    SFElxml-gnu
Version:                 2.9.4
Summary:                 The XML library (gnu)
#Source:                  ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
Source:                  http://gd.tuwien.ac.at/gds/languages/html/libxml/libxml2-%{version}.tar.gz
URL:                     http://xmlsoft.org

Patch5:	lxml-05-CVE-2016-4658.patch
Patch6:	lxml-06-CVE-2016-5131-1.patch
Patch7:	lxml-07-CVE-2016-5131-2.patch

%prep
%setup -q -n %{src_name}-%{version}

#CVE-2016-4658
%patch5 -p1
#CVE-2016-5131
%patch6 -p1
%patch7 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%{optflags} -I%{gnu_inc}"
export CXXFLAGS="%{cxx_optflags} -I%{gnu_inc}"
##TODO is this right/needed at all? -llzma
export LDFLAGS="%{_ldflags} %{gnu_lib_path} -llzma"

./configure --prefix=%{_prefix} \
                                    --sysconfdir=%{_sysconfdir} \
				    --bindir=%{_bindir} \
				    --libdir=%{_libdir} \
				    --libexecdir=%{_libexecdir} \
                                    --includedir=%{_includedir} \
%if %{opt_arch64}
                                    --without-python \
%endif
                                    --mandir=%{_mandir} \
                                    --disable-static
 
gmake -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT/%{_libdir}/xml2Conf.sh

#pyton modules started to appear in /usr/lib/python2.7/site-packages
echo "%{_libdir}" | grep "/gnu/lib" && ls -1d $RPM_BUILD_ROOT/usr/lib/python*/site-packages && mv $RPM_BUILD_ROOT%{_std_libdir} $RPM_BUILD_ROOT%{_prefix}/

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Jan  7 2018 - Thomas Wagner
- typo missing % for %{_std_libdir} in %install
* Mon Aug 14 2017 - Thomas Wagner
- change BuildRequires pnm macro
- move modules into correct site-packages directory
* Thu Mar 23 2017 - Thomas Wagner
- bump to 2.9.4
- add patch5 patch6 patch7 for CVE-2016-4658 and CVE-2016-5131
* Fri Aug  2 2013 - Thomas Wagner
- bump to 2.9.1 / 2.9.1 (IPS) CVE-2013-2877
- remove now obsolete patch1 libxml2-01-2.9.0-fix-PTHREAD_ONCE_INIT.diff
* Sun Jan 13 2013 - Thomas Wagner
- fix isaexec (hardlink)
- fix %hard %files %_bindir for multiarch
- add patch1 libxml2-01-2.9.0-fix-PTHREAD_ONCE_INIT.diff 
- bump to 2.9.0 / 2.9.0.1 (IPS)
- add dependencies
* Mon Jan  7 2013 - Thomas Wagner
- fix package Name: SFElxml-gnu (not SUNWlxml-gnu), fix deps for sub packages
- Use http mirror for download
* Sun Sep  9 2012 - Thomas Wagner
- fix build
* Sat Sep  8 2012 - Thomas Wagner
- split out base-specs/lxml.spec for proper multiarch
