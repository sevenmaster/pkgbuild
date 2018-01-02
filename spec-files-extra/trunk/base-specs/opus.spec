#
# spec file for package libopus
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#


Name:         opus
Version:      1.1.5
Summary:      The Opus Audio Codec Library
Source:       http://downloads.xiph.org/releases/opus/opus-%{version}.tar.gz
BuildRoot:    %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n %name-%version

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}			\
	    --datadir=%{_datadir}		\
	    --mandir=%{_mandir}			\
	    --enable-shared			\
	    --disable-static \
    --disable-silent-rules \
    --disable-doc \
    --enable-custom-modes

gmake -j$CPUS

%install
gmake DESTDIR=$RPM_BUILD_ROOT install

rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Nov 27 2017 - Thomas Wagner
- bump to 1.1.5
* Sat May 25 2013 - Thomas Wagner
- initial spec derived form libvorbis.spec
