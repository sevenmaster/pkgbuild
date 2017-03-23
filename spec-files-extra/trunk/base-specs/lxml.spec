# base-specs/lxml.spec for SFElxml.spec

# owner: tom68


Name:                    SFElxml-gnu
Version:                 2.9.4
Summary:                 The XML library (gnu)
#Source:                  ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
Source:                  http://gd.tuwien.ac.at/gds/languages/html/libxml/libxml2-%{version}.tar.gz
URL:                     http://xmlsoft.org

%prep
%setup -q -n %{src_name}-%{version}


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

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Mar 23 2017 - Thomas Wagner
- bump to 2.9.4
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
