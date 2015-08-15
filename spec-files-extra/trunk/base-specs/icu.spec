# Base SPEC file for SFEicu.spec
#
# Copyright 2009 Stefan Teleman
# Copyright 2010 Adriaan de Groot
#
# This file is released under the terms of an MIT / 1-clause BSD
# license. See the file LICENSE.MIT for details.

%define tarball_name    icu4c

Name:                   icu
Summary:                International Components for Unicode
Version:                55.1
%define tarball_version %( echo %{version} | sed -e 's/\./_/g' )
Source:			http://download.icu-project.org/files/%tarball_name/%version/%tarball_name-%tarball_version-src.tgz

#remove#Patch1: icu-01-qt-bug-7702.diff
#remove#Patch2: icu-02-qt-bug-7702.diff
#remove#from upstream http://bugs.icu-project.org/trac/ticket/7695
#remove#Patch3:	icu-03-Rpath.diff
#remove#Patch4: icu-04-gnu99.diff
#remove# This is executed in the context either of 32- or 64-bit builds.

#imported from OI Userland gate
Patch00: icu-00-patch-common_uposixdefs.h.patch.diff
Patch01: icu-01-source_common_tetdata_conversion.txt.patch.diff
Patch02: icu-02-source_common_ucnv_u7.c.patch.diff
Patch03: icu-03-source_config_mh_solaris.patch.diff
Patch04: icu-04-source_data_mappings_johab.ucm.patch.diff
Patch05: icu-05-source_i18n_decNumber.h.patch.diff
Patch06: icu-06-source_runConfigureICU.patch.diff
Patch07: icu-07-source_test_ccapitst.c.patch.diff


%prep
%setup -q -n %name
#%patch1 -p 1
#%patch3
#removed %patch4 -p 1
# Patch2 applied below

%build

%if %cc_is_gcc
export CC=gcc
export CXX=g++
export CFLAGS="%optflags -D_XPG6"
export CXXFLAGS="%cxx_optflags -std=c99 -D_XPG6"

%if %opt_arch64
 export LDFLAGS="%_ldflags -L/usr/gnu/lib/%bld_arch -R/usr/gnu/lib/%bld_arch"
%else
 export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
%endif

%else
export LD=CC
export CFLAGS="%optflags -D_XPG6"
export CXXFLAGS="%cxx_optflags -D_XPG6"
export CXXFLAGS="%cxx_optflags -library=stdcxx4"
#export LDFLAGS="-library=stdcxx4 %_ldflags"
export LDFLAGS="-library=stdcxx4"
%endif
export LIBS=""
PATH=%{_bindir}:$PATH

# Kind of peculiar, but we need to avoid accidentally linking to the
# already installed icu4c libraries in the system, so we push some
# local directories to the front.
# PWD=`pwd`
# LOCAL_LIB="-L$PWD/source/lib -L$PWD/source/stubdata"
# CXXFLAGS="$LOCAL_LIB $CXXFLAGS"
# CFLAGS="$LOCAL_LIB $CFLAGS"
# LDFLAGS="$LOCAL_LIB $LDFLAGS"
# CPPFLAGS="$LOCAL_LIB $CPPFLAGS"

# arch64.inc defines _bindir etc. but not _sbindir
%if %opt_arch64
%define _sbindir %_prefix/sbin/%bld_arch
%endif

cd source
#./configure \
chmod 0755 ./runConfigureICU
%if %cc_is_gcc
./runConfigureICU Solaris/GCC \
%else
./runConfigureICU Solaris \
%endif
	--prefix=%{_prefix} \
	--bindir=%{_bindir}\
	--sbindir=%{_sbindir} \
	--libexecdir=%{_libexecdir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--disable-warnings \
	--disable-debug \
	--disable-dependency-tracking \
	--disable-strict \
%if %opt_arch64
	--with-library-bits=64 \
%else
	--with-library-bits=32 \
%endif
	--enable-release \
	--enable-draft \
	--disable-renaming \
	--enable-rpath \
	--enable-threads \
	--enable-extras \
	--enable-icuio \
	--enable-layout \
	--enable-tests \
	--disable-samples \
	--enable-shared \
	--disable-static \
        --with-data-packaging=library \
        || { r=$?; cat config.log; exit $r; }

#from Oi Userland Makefile
echo 'CPPFLAGS += -DICU_DATA_DIR=\"%{_prefix}/share/icu/%{version}\"' >> icudefs.mk 

#OI Makefile#  #COMPONENT_POST_UNPACK_ACTION += ( chmod +x $(@D)/source/configure $(@D)/source/runConfigureICU )
#OI Makefile#  # Missing files in build dir for configure without this.
#OI Makefile#  #COMPONENT_PRE_CONFIGURE_ACTION = ($(CLONEY) $(SOURCE_DIR) $(@D) && cd $(@D) && autoconf )
#OI Makefile#  CONFIGURE_SCRIPT = $(SOURCE_DIR)/source/runConfigureICU
#OI Makefile#  CONFIGURE_OPTIONS = Solaris/GCC
#OI Makefile#  CONFIGURE_OPTIONS+= --with-data-packaging=library
#OI Makefile#  CONFIGURE_OPTIONS+= --enable-shared
#OI Makefile#  CONFIGURE_OPTIONS+= --enable-static
#OI Makefile#  CONFIGURE_OPTIONS+= --disable-samples
#OI Makefile#  CONFIGURE_OPTIONS+= --prefix=$(CONFIGURE_PREFIX)
#OI Makefile#  CONFIGURE_OPTIONS+= --libdir=$(CONFIGURE_LIBDIR.$(BITS))
#OI Makefile#  CONFIGURE_OPTIONS+= --bindir=$(CONFIGURE_BINDIR.$(BITS))
#OI Makefile#  CONFIGURE_OPTIONS.32+= --disable-64bit-libs
#OI Makefile#  COMPONENT_POST_CONFIGURE_ACTION = (echo 'CPPFLAGS += -DICU_DATA_DIR=\"$(CONFIGURE_PREFIX)/share/icu/$(COMPONENT_VERSION)\"' >> $(@D)/icudefs.mk )
#OI Makefile#  build: $(BUILD_32_and_64)
#OI Makefile#  install: $(INSTALL_32_and_64)

# That runConfigure wrapper will mess up configure's exit code,
# so also check that Makefile was created.
test -f Makefile || { cat config.log ; exit 1 ; }

# Patch2, but by now we're in the source/ dir; the second patch is already
# relative to that directory.
#%patch2 -p1

[ -z "$MAKE" ] && MAKE=gmake

test -f ./runConfigureICU || cd source
# Parallelism seems to break after a while, so finish single-threaded
${MAKE} ${MAKE_CPUS} || ${MAKE}

%install
[ -z "$MAKE" ] && MAKE=gmake

test -f ./runConfigureICU || cd source
${MAKE} install DESTDIR=${RPM_BUILD_ROOT}


%changelog
* Sat Aug  8 - 2015 Thomas Wagner
- moved %build up before configure step to solve "make" running without our ENV variables (CFLAGS,...)
- bump to 55.1
- imported new patch0 - patch7 from OI Userland
* Wed Dec 21 2011 - James Choi
- manually specify $MAKE if none defined
* Mon Nov 07 2011 - Milan Jurik
- bump to 4.8.1.1
* Mon Apr 11 2011 - Alex Viskovatoff
- Revert the previous change: that breaks the build
- Update to 4.6.1
* Fri Jan 28 2011 - Alex Viskovatoff
- Add %_ldflags to LDFLAGS
* Fri Nov 19 2010 - Alex Viskovatoff
- Adapt kde-solaris base-icu4c.spec, bumping to 4.4.2 from 4.4.1
