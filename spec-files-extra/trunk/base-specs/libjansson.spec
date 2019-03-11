
Name:         libjansson
Version:      2.12
Summary:      Jansson is a C library for encoding, decoding and manipulating JSON data
URL:          http://www.digip.org/jansson
Source:       http://www.digip.org/jansson/releases/jansson-%{version}.tar.bz2
##TODO## Patch1: CVE
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
jansson is a C library for encoding, decoding and manipulating JSON data. It features:

    Simple and intuitive API and data model
    Comprehensive documentation
    No dependencies on other libraries
    Full Unicode support (UTF-8)
    Extensive test suite


%prep
%setup -q -c -n jansson-%{version}

##TODO## %patch1 -p1      CVE

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

cd jansson-%{version}
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir}         \
            --mandir=%{_mandir}                 \
            --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info          \
	    --disable-static			\
            --includedir=%{_includedir}/jansson   \


gmake -j$CPUS

%install
cd jansson-%{version}

#from Makefile Solaris Userland: remove jansson_config.h
rm -f src/jansson_config.h

gmake -i install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sun Mar  3 2019 - Thomas Wagner
- initial spec version 2.12 based on Solaris Userland library/jasson
