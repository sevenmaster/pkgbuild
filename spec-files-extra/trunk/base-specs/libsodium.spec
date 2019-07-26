# base-specs/libsodium.spec for SFExl.spec


Name:		SFElibsodium
Version:	1.0.13
Summary:	A modern, portable, easy to use crypto library
URL:            https://libsodium.org
Source:		https://github.com/jedisct1/libsodium/releases/download/%{version}/libsodium-%{version}.tar.gz


%prep
%setup -q -c -n libsodium-%{version}


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
cd libsodium-%{version}

#export CC=/usr/gcc-sfe/7/bin/gcc
#export CXX=/usr/gcc-sfe/7/bin/g++
export CC=gcc
export CXX=g++

export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"
#export AS=/usr/gnu/bin/as

./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir}         \
            --mandir=%{_mandir}                 \
            --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info          \
	    --disable-static			\
            --disable-asm                       \

gmake -j$CPUS

%install
cd libsodium-%{version}
gmake install DESTDIR=${RPM_BUILD_ROOT}

%if %build_l10n
%else
[ -d $RPM_BUILD_ROOT%{_datadir}/locale ] && rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}


%changelog
* Fri Jul 26 2019 - Thomas Wagner
- fix i386 compile with bash_arch
* Mon Jul  2 2018 - Thomas Wagner
- initial spec 1.0.13
