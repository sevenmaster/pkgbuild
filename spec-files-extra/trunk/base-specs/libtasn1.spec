#
Name:     	libtasn1
Version: 	4.5
License:	LGPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:         %{_datadir}/doc
Source:		http://ftp.gnu.org/gnu/libtasn1/%{name}-%{version}.tar.gz
Summary:	Libtasn is a library written in C for manipulating ASN.1 objects. (/usr/gnu)

%description
Libtasn is a library written in C for manipulating ASN.1 objects including 
DER/BER encoding and DER/BER decoding. Libtasn is used by GnuTLS to manipulate 
X.509 objects and by GNU Shishi to handle Kerberos V5 packets.


%prep
%setup  -q -n %{name}-%{version}

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CXX="$CXX -norunpath"
export CFLAGS="%optflags"
#export CXXFLAGS="%cxx_optflags -staticlib=stlport4"
export CXXFLAGS="%cxx_optflags"
export MSGFMT="/usr/bin/msgfmt"


#aclocal $ACLOCAL_FLAGS -I m4 -I gl/m4
#libtoolize --force --copy
#autoconf
#automake -a -c -f

./configure --prefix=%{_prefix}                        \
            --bindir=%{_bindir}                        \
            --libdir=%{_libdir}                        \
            --sysconfdir=%{_sysconfdir}                \
            --includedir=%{_includedir}        \
            --mandir=%{_mandir}                        \
           --infodir=%{_infodir}               \
           --disable-static                    \
           --enable-shared



make -j$CPUS

%install
#make install DESTDIR=$RPM_BUILD_ROOT mkdir_p="mkdir -p"
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
rm -rf $RPM_BUILD_ROOT%{_datadir}/info
rm -rf $RPM_BUILD_ROOT/usr/local
rm -rf $RPM_BUILD_ROOT%{_mandir}
#would need usr-gnu.inc changed
rm -rf $RPM_BUILD_ROOT/%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Jun  7 2015 - Thomas Wagner
- bump to 4.5
- add IPS_Package_Name, relocate to usr-gnu.inc
* Sun Apr 01 2012 - Pavel Heimlich
- fix download location
* Tue Mar 28 2007 - jeff.cai@sun.com
- Split to two spec files.
