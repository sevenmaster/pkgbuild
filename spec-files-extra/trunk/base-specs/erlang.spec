# base spec for erlang
#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define pkg_src_name     otp_src
%define src_name         erlang
%define src_ver          R15B03
%define major            15
%define minor            3

Name:                    SFEerlang 
Summary:                 erlang - Erlang programming language and OTP libraries (g++-built)
Version:                 %{major}.%{minor}
Release:                 1
License:                 ERLANG PUBLIC LICENSE
Group:                   Development/Languages/Erlang
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://www.erlang.org
Source:                  http://erlang.org/download/%{pkg_src_name}_%{src_ver}-1.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{src_name}_%{src_ver}

%prep
%setup -q -n %{pkg_src_name}_%{src_ver}

chmod 0755 configure

#sed -i -e 's,WX_LIBS=`$WX_CONFIG_WITH_ARGS --libs`,WX_LIBS="`$WX_CONFIG_WITH_ARGS --libs` -lGLU",' lib/wx/configure lib/wx/configure.in
#sed -i -e '/SSL_DYNAMIC_ONLY=/s:no:yes:' erts/configure erts/configure.in

#sed -i -e 's,$rdir/include,$rdir/include/odbc,g' lib/odbc/configure lib/odbc/configure.in
#sed -i -e 's,${libdir}/64,${libdir}/%{_arch64},g' lib/odbc/configure lib/odbc/configure.in

export CC=gcc
export CXX=g++
export CPPFLAGS="-D_LARGEFILE64_SOURCE -I%{gnu_inc} -I%{gnu_inc}/wx-2.8 -I%{_includedir}/gd2 -I%{xorg_inc}"
export LDFLAGS="%{_ldflags} %{gnu_lib_path} %{xorg_lib_path}"
%if %{is64}
export CPPFLAGS="${CPPFLAGS} -DSIZEOF_VOID_P=8 -DSIZEOF_LONG=8"
export CFLAGS="%{gcc_optflags64}"
export CXXFLAGS="%{gcc_cxx_optflags64}"
export LDFLAGS="-m64 ${LDFLAGS}"
%else
export CFLAGS="%{gcc_optflags}"
export CXXFLAGS="%{gcc_cxx_optflags}"
%endif

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}	\
            --libdir=%{_libdir}	\
            --libexecdir=%{_libexecdir}	\
            --includedir=%{_includedir} \
            --mandir=%{_mandir} \
            --enable-static=no \
	    --localstatedir=/var \
 	    --disable-static \
 	    --disable-rpath \
 	    --enable-smp-support \
 	    --enable-threads \
 	    --enable-hipe \
 	    --with-ssl \
%if %{is64}
            --enable-m64-build \
%endif
 	    --enable-dynamic-ssl-lib

%build
export CC=gcc
export CXX=g++
export CPPFLAGS="-D_LARGEFILE64_SOURCE -I%{gnu_inc} -I%{gnu_inc}/wx-2.8 -I%{_includedir}/gd2 -I%{xorg_inc}"
export LDFLAGS="%{gnu_lib_path} %{xorg_lib_path}"
%if %{is64}
export CPPFLAGS="${CPPFLAGS} -DSIZEOF_VOID_P=8 -DSIZEOF_LONG=8"
export CFLAGS="%{gcc_optflags64}"
export CXXFLAGS="%{gcc_cxx_optflags64}"
export LDFLAGS="-64 ${LDFLAGS}"

# Exporting DED_LD doesn't seem to cover all the cases so force it for now
# export DED_LD=/usr/ccs/bin/ld
gsed -i 's|DED_LD = ld|DED_LD = /usr/ccs/bin/ld|g' make/*/otp_ded.mk
%else
export CFLAGS="%{gcc_optflags}"
export CXXFLAGS="%{gcc_cxx_optflags}"
%endif

export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
${MAKE}

%install
export CC=gcc
export CXX=g++
export CPPFLAGS="-D_LARGEFILE64_SOURCE -I%{gnu_inc} -I%{gnu_inc}/wx-2.8 -I%{_includedir}/gd2 -I%{xorg_inc}"
export LDFLAGS="%{_ldflags} %{gnu_lib_path} %{xorg_lib_path}"
%if %{is64}
export CPPFLAGS="${CPPFLAGS} -DSIZEOF_VOID_P=8 -DSIZEOF_LONG=8"
export CFLAGS="%{gcc_optflags64}"
export CXXFLAGS="%{gcc_cxx_optflags64}"
export LDFLAGS="-m64 ${LDFLAGS}"
%else
export CFLAGS="%{gcc_optflags}"
export CXXFLAGS="%{gcc_cxx_optflags}"
%endif

export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

$MAKE install DESTDIR=${RPM_BUILD_ROOT}

# if [ ! -f ${RPM_BUILD_ROOT}/usr/lib/%{_arch64}/erlang/lib/tools-2.6.5.1/emacs/erlang-skels.el ]
# then
#     # These files are not installed by make install in the R13B04 Erlang/OTP release
#     install -m 0644 lib/tools/emacs/erlang-skels.el ${RPM_BUILD_ROOT}/usr/lib/%{_arch64}/erlang/lib/tools-2.6.5.1/emacs
#     install -m 0644 lib/tools/emacs/erlang-skels-old.el ${RPM_BUILD_ROOT}/usr/lib/%{_arch64}/erlang/lib/tools-2.6.5.1/emacs
# fi

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Jan 18 2013- Logan Bruns <logan@gedanken.org>
- Updated to R15B03
- Added IPS name
* Sun Jun 6 2010 - markwright@internode.on.net
- create
