Name:                    popt
Version:                 1.16
Source:                  http://rpm5.org/files/popt/popt-%{version}.tar.gz

%prep
%setup  -q -n %{name}-%{version}

%patch1 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%{_ldflags}"

echo "CFLAGS=$CFLAGS"
echo "CXXLAGS=$CXXFLAGS"
echo "LDLAGS=$LDFLAGS"
echo "CC=$CC"
echo "CXX=$CXX"


./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --mandir=%{_mandir}         \
            --infodir=%{_infodir}       \
            --disable-assembler         \
            --disable-nls               \
            --libexecdir=%{_libexecdir}/%{_arch64}  \
            --sysconfdir=%{_sysconfdir}/%{_arch64}  \
            --enable-shared


make -j $CPUS



%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Thu Jul 25 2015 - Thomas Wagner
- initial spec, based on spec-files/specs/SUNWlibpopt.spec .. Omnios lost libpopt
