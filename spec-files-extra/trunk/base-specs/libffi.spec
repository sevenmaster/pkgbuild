# spec file for package libffi
#

Name:		libffi
#License:	
Version:	3.2.1
Source:         ftp://sourceware.org/pub/libffi/libffi-%{version}.tar.gz

Patch1:		libffi-01-1_raw_api.patch

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')  

export CFLAGS="%{optflags}"
export CFLAGS="${CFLAGS} -DFFI_MMAP_EXEC_WRIT=1"

export LDLAGS="%{_ldflags}"




./configure --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --disable-raw-api \
	--enable-shared \
        --disable-static

gmake -j$CPUS V=2

%install
gmake install DESTDIR=$RPM_BUILD_ROOT

# Clean up unpackaged files.
rm $RPM_BUILD_ROOT%{_libdir}/*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Dec 23 2016 - Thomas Wagner
- initial spec version 3.2.1
