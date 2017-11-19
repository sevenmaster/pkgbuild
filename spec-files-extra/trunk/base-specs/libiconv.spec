Name:		libiconv
Version:	1.14
Source:		http://ftp.gnu.org/pub/gnu/libiconv/libiconv-%{version}.tar.gz
Patch2:		libiconv-02-646.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup  -q -n %{name}-%{version}
%patch2 -p1


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

./configure \
        --prefix=%{_prefix}	\
        --libdir=%{_libdir}	\
        --datadir=%{_datadir}	\
        --mandir=%{_mandir}	\
        --enable-static=no

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib*.la
rm $RPM_BUILD_ROOT%{_libdir}/charset.alias


%changelog
* Sun Nov 19 2017 - Thomas Wagner
- merge spec files, remove *.la files
* Tue Jun 16 2015 - Thomas Wagner
- make it 32/64-bit
