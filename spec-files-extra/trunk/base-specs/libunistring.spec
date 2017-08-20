#
Name:		libunistring
Version:	0.9.7
Source:		http://ftp.gnu.org/gnu/libunistring/libunistring-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup  -q -n %{name}-%{version}

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc

#find out iconv in gnu_inc / gnu_lib_path
export CFLAGS="%optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags %{gnu_lib_path}"

#disable tests or get u16_is_invariant undefined
#            --disable-silent-rules          \
./configure --prefix=%{_prefix}	\
            --bindir=%{_bindir}             \
            --libdir=%{_libdir}             \
            --sysconfdir=%{_sysconfdir}     \
            --includedir=%{_includedir}     \
            --mandir=%{_mandir}             \
            --infodir=%{_infodir}           \
            --with-libiconv-prefix=/usr/gnu \
	    --disable-static	\
	    --enable-shared

gmake -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la

#%{_std_datadir}/info
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -rf $RPM_BUILD_ROOT%{_datadir}/info

rm -rf $RPM_BUILD_ROOT%{_libdir}/charset.alias

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
#%{_bindir}
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/libunistring/*
#%dir %attr(0755, root, bin) %{_infodir}
#%{_infodir}/*



%defattr (-, root, bin)
%{_includedir}


%changelog
* Sun Aug 20 2017 - Thomas Wagner
- bump to 0.9.7
- relocate to usr-gnu.inc
- make it 32/64-bit (for gnutls being 32/64-bit)
* Fri Apr 15 2016 - Thomas Wagner
- Initial spec
