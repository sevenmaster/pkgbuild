
Name:         libarchive
Version:      3.3.3
Summary:      libarchive - Multi-format archive and compression library
URL:          http://www.libarchive.org/
Source:       http://www.libarchive.org/downloads/libarchive-%{version}.tar.gz

Patch1:       libarchive-01-b64_encode.patch
Patch2:       libarchive-02-fix-man-pages.patch
Patch3:       libarchive-03-libarchive-archive_entry_perms.3.patch
Patch4:       libarchive-04-mkdev-include.patch

BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
Multi-format archive and compression library


%prep
%setup -q -n libarchive-%{version}

#from solaris userland
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CPUS=$( psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}' )

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
	    --enable-shared                     \
            --enable-largefile \
            --with-openssl \
            --with-pic \
            --with-xml2 \
            --with-zlib \

gmake V=2 -j$CPUS

%install


gmake -i install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Thu Mar 14 2019 - Thomas Wagner
- initial spec version 3.3.3 based on Solaris Userland library/libarchive
