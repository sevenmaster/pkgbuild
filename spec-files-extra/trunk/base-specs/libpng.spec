# base-specs/libpng.spec for SFElibpng.spec


Name:		SFElibpng
Version:	1.6.34
Summary:      	libpng - reference library for use in applications that create and manipulate PNG (Portable Network Graphics) raster image files
URL:            http://www.libpng.org
Source:         ftp://ftp-osl.osuosl.org/pub/libpng/src/libpng16/libpng-%{version}.tar.gz
##TODO##pause Patch1:         libpng-01-no_ld_version_script.diff


%prep 
%setup -q -c -n libpng-%{version}
##TODO##pause %patch1 -p1


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

cd libpng-%{version}
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
	    --disable-static			\


gmake -j$CPUS

%install
cd libpng-%{version}
gmake install DESTDIR=${RPM_BUILD_ROOT}

%if %build_l10n
%else
[ -d $RPM_BUILD_ROOT%{_datadir}/locale ] && rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean


%changelog

##TODO##
