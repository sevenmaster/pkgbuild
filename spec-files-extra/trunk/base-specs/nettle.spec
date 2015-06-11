
#
Name:     	nettle
Version: 	3.1
##TODO##License:	LGPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Source:         http://ftp.gnu.org/gnu/nettle/nettle-%{version}.tar.gz
Summary:        Nettle is a cryptographic library that is designed to fit easily in more or less any context: In crypto toolkits for object-oriented languages (C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in kernel space.  (/usr/gnu)

%description
Nettle is a cryptographic library that is designed to fit easily in more or less any context: In crypto toolkits for object-oriented languages (C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in kernel space.

This package installs into /usr/gnu path.


%prep
%setup  -q -n %{name}-%{version}

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

##CC=gcc
##CXX=g++
export CFLAGS="%optflags -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%{_ldflags} %{gnu_lib_path}"


./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --mandir=%{_mandir}         \
            --infodir=%{_infodir}       \
            --disable-assembler         \
            --disable-static            \
            --enable-shared



make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
#find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
#find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Jun 11 2015 - Thomas Wagner
- initial spec
- make it 32/64-bit
