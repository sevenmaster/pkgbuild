



Summary:	Open Source multimedia framework
Version:	%{version}
Source:		http://openjpeg.googlecode.com/files/openjpeg-%{version}.tar.gz



%prep
%setup -q -n %{src_name}-%{version}


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

mkdir -p builds/unix
cd builds/unix

#prefix=@CMAKE_INSTALL_PREFIX@
#libdir=@OPENJPEG_INSTALL_LIB_DIR@
#includedir=@OPENJPEG_INSTALL_INCLUDE_DIR@

cmake -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
      -DOPENJPEG_INSTALL_LIB_DIR:PATH=%{_libdir} \
      -DOPENJPEG_INSTALL_BIN_DIR:PATH=%{_bindir} \
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

