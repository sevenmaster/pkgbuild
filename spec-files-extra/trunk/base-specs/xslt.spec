# base-specs/xslt.spec for SFExslt.spec

# owner: tom68

Name:                    SFExslt-gnu
Version:                 1.1.28
Summary:                 The XML library (gnu)
Source:                  ftp://xmlsoft.org/libxslt/libxslt-%{version}.tar.gz
URL:                     http://xmlsoft.org
Patch1:                  libxslt-01-disable-version-script.diff

%prep
%setup -q -n %{src_name}-%{version}

%patch1 -p1

mkdir bin
ln -s /usr/gnu/bin/%{bld_arch}/xml2-config bin/

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%{optflags} -I%{gnu_inc}"
export CXXFLAGS="%{cxx_optflags} -I%{gnu_inc}"
export LDFLAGS="%{_ldflags} %{gnu_lib_path}"

#need this to find symlinked xml2-config of correct _arch
export PATH=`pwd`/bin:$PATH


#note: --with-libxml-prefix=`pwd` makes configure find bin/xml2-config
./configure --prefix=%{_prefix} \
                                    --sysconfdir=%{_sysconfdir} \
				    --bindir=%{_bindir} \
				    --libdir=%{_libdir} \
				    --libexecdir=%{_libexecdir} \
                                    --includedir=%{_includedir} \
                                    --with-libxml-include-prefix=%{_includedir}/%{src_name} \
%if %{opt_arch64}
                                    --without-python \
%endif
                                    --mandir=%{_mandir} \
                                    --disable-static

gmake -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

echo "remove statics lib files:"
find $RPM_BUILD_ROOT%{_libdir}/ -name "*.a" -exec rm {} \; -print -o -name  "*.la" -exec rm {} \; -print


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Jan 13 2013 - Thomas Wagner
- fix Name: SFExslt-gnu -> SFElxsl-gnu
- fix isaexec (hardlink)
- fix %hard %files %_bindir for multiarch
- add (Build)Requires: SFElxml-gnu(-devel) SUNWzlib
- add dependencies
* Thu Jan 10 2013 - Thomas Wagner
- rename SVR4 package from SFExslt-gnu to SFElxsl-gnu
* Mon Jan  8 2013 - Thomas Wagner
- initial spec, copied from libxml2 (lxml.spec)
