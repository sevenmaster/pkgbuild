#
# spec file for package libexif
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#


Name:         libexif
Version:      0.6.21
Summary:      EXIF Tag Parsing Library
#Source:       http://sourceforge.net/projects/libexif/files/libexif/%{version}/libexif-%{version}.tar.bz2/download
Source:       %{sf_download}/libexif/libexif-%{version}.tar.bz2

BuildRoot:    %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n %name-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}			\
	    --datadir=%{_datadir}		\
	    --mandir=%{_mandir}			\
	    --enable-shared			\
	    --disable-static \

gmake -j$CPUS

%install
gmake DESTDIR=$RPM_BUILD_ROOT install

rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon May 27 2013 - Thomas Wagner
- initial spec version 0.6.21
