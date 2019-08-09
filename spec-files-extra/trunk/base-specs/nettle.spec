
#
Name:     	nettle
Version: 	3.5.1
##TODO##License:	LGPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Source:         http://ftp.gnu.org/gnu/nettle/nettle-%{version}.tar.gz
Patch1:         nettle-01-build.patch
Patch3:         nettle-03-patch-aa.diff
Summary:        Nettle is a cryptographic library that is designed to fit easily in more or less any context: In crypto toolkits for object-oriented languages (C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in kernel space.  (/usr/gnu)

%description
Nettle is a cryptographic library that is designed to fit easily in more or less any context: In crypto toolkits for object-oriented languages (C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in kernel space.

This package installs into /usr/gnu path.


%prep
%setup  -q -n %{name}-%{version}

%patch1 -p1
%patch3 -p0

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

##CC=gcc
##CXX=g++
export CFLAGS="%optflags -I%{_std_includedir}/openssl/fips-140 -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc}"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
   export LDFLAGS="%{_ldflags} -R/lib/openssl/fips-140/%{_arch64} -L/lib/openssl/fips-140/%{_arch64} %{gnu_lib_path}"
else
   export LDFLAGS="%{_ldflags} -R/lib/openssl/fips-140 -L/lib/openssl/fips-140 %{gnu_lib_path}"
fi



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
            --enable-shared             \
            --enable-public-key         \
            --disable-openssl           \
%if %{omnios}
            --enable-mini-gmp           \
%endif

##PAUSE##            --enable-public-key         \
##PAUSE##            --enable-mini-gmp           \
##PAUSE##            --disable-static            \


#we have htobe64 but bswap64 is only in libs, missing headers
#could define the function though
gsed -i.bak -e '/#define HAVE_BUILTIN_BSWAP64 1/ s?^?// disabled, missing header ?' config.h

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Aug  8 2019 - Thomas Wagner
- bump to 3.5.1, patches from OI and pkgsrv
* Fri Jul 26 2019 - Thomas Wagner
- bump to 3.4.1
- for gnutls --enable-public-key
* Sat Okt 10 2015 - Thomas Wagner
- bump to 3.1.1 for new gnutls 3.4.4
* Mon Jun 15 2015 - Thomas Wagner
- downgrade to 2.7.1 (to suit gnutls)
- fix _arch64 build
- downgrade version to suit gnutls
* Thu Jun 11 2015 - Thomas Wagner
- initial spec
- make it 32/64-bit
