



Summary:	Open Source multimedia framework
Version:	%{version}
#Source:         http://openjpeg.googlecode.com/files/openjpeg-%{version}.tar.gz
Source:         %{src_url}/version.%{version}.tar.gz?openjpeg-%{version}.tar.gz



%prep
#openjpeg-version.1.5.2/
#%setup -q -n %{src_name}-%{version}
%setup -q -n %{src_name}-version.%{version}


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%{optflags} -I%{gnu_inc}"
export CXXFLAGS="%{cxx_optflags} -I%{gnu_inc}"
export LDFLAGS="%{gnu_lib_path} %{_ldflags}"

#for SFElcms2-gnu
#note: %{_libdir} already contains current %{_arch64}
#export PKG_CONFIG_PATH="/usr/gnu/lib/%{_arch64}/pkgconfig:%{_libdir}/pkgconfig"
%if %{opt_arch64}
  export PKG_CONFIG_PATH=/usr/gnu/lib/%{_arch64}/pkgconfig
%else
  export PKG_CONFIG_PATH=/usr/gnu/lib/pkgconfig
%endif

set

mkdir -p builds/unix
cd builds/unix

#prefix=@CMAKE_INSTALL_PREFIX@
#libdir=@OPENJPEG_INSTALL_LIB_DIR@
#includedir=@OPENJPEG_INSTALL_INCLUDE_DIR@

cmake -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DOPENJPEG_INSTALL_LIB_DIR:PATH=%{_libdir} \
      -DOPENJPEG_INSTALL_BIN_DIR:PATH=%{_bindir} \
%if %{opt_arch64}
      -DLCMS2_LIBRARY:FILEPATH=/usr/gnu/lib/%{_arch64}/liblcms2.so \
%else
      -DLCMS2_LIBRARY:FILEPATH=/usr/gnu/lib/liblcms2.so \
%endif
      ../..
make VERBOSE=1 -j$CPUS


%install

cd builds/unix
make install DESTDIR=${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_pkg_config_path}
[ -f ${RPM_BUILD_ROOT}%{_datadir}/pkgconfig/libopenjpeg1.pc ] && mv  ${RPM_BUILD_ROOT}%{_datadir}/pkgconfig/libopenjpeg1.pc  ${RPM_BUILD_ROOT}%{_pkg_config_path}/libopenjpeg1.pc 
[ -d ${RPM_BUILD_ROOT}%{_datadir}/pkgconfig ] && rmdir ${RPM_BUILD_ROOT}%{_datadir}/pkgconfig 

#1.5.0 rm -f %{buildroot}/%{_includedir}/openjpeg.h
#1.5.0 ln -s openjpeg-%{major_minor_version}/openjpeg.h %{buildroot}/%{_includedir}/openjpeg.h


%changelog
* Mon Nov 21 2014 - Thomas Wagner
- bump to 1.5.2
- make download-file contain the source name (stupid github setup! "version.1.5.2.tar.gz" is not a valid download-filename!)
* Sun Jan 03 2016 - reneelg
- align Source definition with SFEopenjpeg.spec to prevent build error of SFEopenjpeg
* Sat May 22 2015 - pjama
- update download URL
* Sat Mar 22 2014 - Thomas Wagner
- Workaround broken search for liblcms2.so in configure.
  On some OS and installed package mix, the amd64 build traps over /usr/gnu/lib/lcms2.so (=32bit)
* Mon Jan  6 2014 - Thomas Wagner
- bump to 1.5.1
- fix %files
* Fri Jan  3 2014 - Thomas Wagner
- change (Build)Requires to SFElcms2-gnu, update CFLAGS/LDFLAGS to first search gnu_inc / gnu_lib_path
* Wed Jan 01 2014 - Thomas Wagner
- add (Build)Requires: SFElcms2
- update 32/64-bit support
* Sun Nov 17 2013 - Thomas Wagner
- add 32/64-bit support
