#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%include usr-gnu.inc

%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

Name:		SFElibgcrypt-gnu
IPS_Package_Name: system/library/security/gnu/libgcrypt
Summary:	Libgcrypt is a general purpose cryptographic library originally based on code from GnuPG
Version:	1.8.0
Source:		ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.gz
URL:		https://gnupg.org/software/libgcrypt/
License:	GPLv2+
Group:		Development/Libraries
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %{omnios}
%else
BuildRequires:	%{pnm_buildrequires_SUNWtexi}
Requires:	%{pnm_requires_SUNWtexi}
%endif

BuildRequires:  SFElibgpg-error-gnu
Requires:       SFElibgpg-error-gnu

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}

%description


Libgcrypt is a general purpose cryptographic library originally based on code from GnuPG. It provides functions for all cryptograhic building blocks: symmetric cipher algorithms (AES, Arcfour, Blowfish, Camellia, CAST5, ChaCha20 DES, GOST28147, Salsa20, SEED, Serpent, Twofish) and modes (ECB,CFB,CBC,OFB,CTR,CCM,GCM,OCB,POLY1305,AESWRAP), hash algorithms (MD2, MD4, MD5, GOST R 34.11, RIPE-MD160, SHA-1, SHA2-224, SHA2-256, SHA2-384, SHA2-512, SHA3-224, SHA3-256, SHA3-384, SHA3-512, SHAKE-128, SHAKE-256, TIGER-192, Whirlpool), MACs (HMAC for all hash algorithms, CMAC for all cipher algorithms, GMAC-AES, GMAC-CAMELLIA, GMAC-TWOFISH, GMAC-SERPENT, GMAC-SEED, Poly1305, Poly1305-AES, Poly1305-CAMELLIA, Poly1305-TWOFISH, Poly1305-SERPENT, Poly1305-SEED), public key algorithms (RSA, Elgamal, DSA, ECDSA, EdDSA, ECDH), large integer functions, random numbers and a lot of supporting functions.

Libgcrypt works on most POSIX systems and many pre-POSIX systems. It can also be built using a cross-compiler system for Microsoft Windows.

See also its Wikipedia entry.


%prep
%setup -q -n libgcrypt-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++

export CFLAGS="%optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags -lsocket -lnsl %{gnu_lib_path}"


./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info \
            --enable-shared \
            --disable-static

make V=2 -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm ${RPM_BUILD_ROOT}%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT/usr/share/info/dir

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (-, root, bin) %{_datadir}/info
%{_datadir}/info/*
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*/*



%changelog
* Sat Jan 20 2018 - Thomas Wagner
- add (Build)Requires: SFElibgpg-error-gnu
* Mon Aug 14 2017 - Thomas Wagner
- initial spec version 1.8.0
