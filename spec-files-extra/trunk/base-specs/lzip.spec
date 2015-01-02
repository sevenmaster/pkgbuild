

Name:		SFElzip-gnu
Version:	1.16
Summary:	LZMA utils
URL:            http://www.nongnu.org/lzip/lzip.html
Source:         http://download.savannah.gnu.org/releases/lzip/lzip-%{version}.tar.gz


%prep
%setup -q -c -n lzip-%{version}


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

cd lzip-%{version}

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}    \
            --bindir=%{_bindir}    \
            --mandir=%{_mandir}    \
            --datarootdir=%{_datadir}   \
            --infodir=%{_datadir}/info  \
            CXX="${CXX}"           \
            CPPFLAGS="${CPPFLAGS}" \
            CXXFLAGS="${CXXFLAGS}" \
            LDFLAGS="${LDFLAGS}"   \

gmake -j$CPUS

%install
cd lzip-%{version}
gmake install DESTDIR=${RPM_BUILD_ROOT}

%clean
rm -rf ${RPM_BUILD_ROOT}


%changelog
* Fri Jan  1 2014 - Thomas Wagner
- initial spec version 1.16
- derived from SFExz-gnu.spec
- build 64-bit only, bindir is /usr/gnu/bin/
- fix build for 64-bit only
- rename to SFElzip-gnu.spec
