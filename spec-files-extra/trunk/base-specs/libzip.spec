#
# spec file for package SFElibzip
#
# includes module(s): libzip
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#


Name:		SFElibzip
License:	BSD
Version:	1.0.1
Summary:        C library for reading, creating, and modifying zip archives
URL:            http://www.nih.at/libzip/index.html
Source:         http://www.nih.at/libzip/libzip-%{version}.tar.xz


%description
libzip is a C library for reading, creating, and modifying zip archives. Files
can be added from data buffers, files, or compressed data copied directly from 
other zip archives. Changes made without closing the archive can be reverted. 
The API is documented by man pages.

%prep
%setup -q -n libzip-%{version}

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="%{cxx_optflags} -D_FILE_OFFSET_BITS=64"
export LDFLAGS="%{_ldflags} -D_FILE_OFFSET_BITS=64"

./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir}         \
            --mandir=%{_mandir}                 \
            --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info          \
	    --disable-static			

gmake -j $CPUS

%install
gmake install DESTDIR=$RPM_BUILD_ROOT

# Clean up unpackaged files.
rm $RPM_BUILD_ROOT%{_libdir}/*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Feb 10 2013 - Thomas Wagner
- initial spec
