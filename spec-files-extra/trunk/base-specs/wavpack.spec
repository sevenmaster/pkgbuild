#
# spec file for package libwavpack
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#


Name:         wavpack
Summary:        WavPack audio compression
Version:	4.70.0
Source:         http://www.wavpack.com/wavpack-%{version}.tar.bz2
Patch1:         wavpack-01-include-glob_t.diff
URL:            http://www.wavpack.com
BuildRoot:    %{_tmppath}/%{name}-%{version}-build


%prep
%setup -q -n %name-%version

%patch1 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}			\
	    --datadir=%{_datadir}		\
	    --mandir=%{_mandir}			\
	    --enable-shared			\
	    --disable-static 			\

gmake -j$CPUS

%install
gmake DESTDIR=$RPM_BUILD_ROOT install

rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Mar 29 2014 - Thomas Wagner
- initial spec derived from opus.spec
