#
#
Name:     	gnutls
Version: 	3.4.8
Copyright:	LGPL/GPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Docdir:         %{_datadir}/doc
URL:		http://www.gnutls.org
%define        major_minor_version %( echo %{version} |  awk -F'.' '{print $1 "." $2}' )
Source:        ftp://ftp.gnutls.org/gcrypt/gnutls/v%{major_minor_version}/gnutls-%{version}.tar.xz
Patch1:        gnutls-01-ENABLE_PKCS11.diff


%prep
#don't unpack please
%setup -q -c -T -n %{name}-%{version}
xz -dc %SOURCE0 | (cd ..; tar xf -)

%if %( expr %{solaris11} '|' %{solaris12} '|' %{omnios} )
#pkcs11_common
%patch1 -p1 
%endif

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags -I/usr/include/idn -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags -I/usr/include/idn -I%{gnu_inc}"
export LDFLAGS="%{_ldflags} %{gpp_lib_path} %{gnu_lib_path}"

export PKG_CONFIG_PATH=%{_pkg_config_path}

echo "using PKG_CONFIG_PATH=$PKG_CONFIG_PATH"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --bindir=%{_bindir} \
    --sysconfdir=%{_sysconfdir} \
    --mandir=%{_mandir} \
    --infodir=%{_datadir}/info \
    --localstatedir=%{_localstatedir} \
    --without-p11-kit \
    --disable-cxx

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sat Jan 16 2016 - Thomas Wagner
- enable patch1 for disable pkcs11 on (OM)
- fix %files guile for (OM), see if necessary on other OS as well, ##TODO## revisit once SFEguile.spec is 32/64-bit
* Fri Jan  8 2016 - Thomas Wagner
- add patch1 gnutls-01-ENABLE_PKCS11.diff or get unresolved symbol pkcs11_common  tpmtool.o (S11 S12)
- bump to 3.4.8
* Sun Oct 11 2015 - Thomas Wagner
- add to *FLAGS  -I/usr/include/idn to find idna.h
- add BuildRequires SFEicu-gpp SFElibtasn1-gnu pnm_buildrequires_library_guile pnm_buildrequires_library_libidn
* Sat Oct 10 2015 - Thomas Wagner
- bump to 3.4.5
- add BuildRequires SFEunbound
- --without-p11-kit (check later if this makes sense on SunOS)
* Thu Aug 20 2015 - Thomas Wagner
- bump to 3.4.4
* Tue Aug  4 2015 - Thomas Wagner
- remove %{pnm_buildrequires_SUNWlibgcrypt}
- fix Requires for -devel to be SFEgnutls
- bump to 3.3.16
* Thu Jun 18 2015 - Thomas Wagner
- unarchvied
- relocate to /usr/gnu, add IPS_Package_Name
- bump to 3.3.15
