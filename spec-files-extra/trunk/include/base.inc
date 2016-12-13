#
# Base (32-bit) platform settings for Solaris packages
#
# Solaris.inc must be included before this file

%define opt_arch64 0

%ifarch sparc
%define bld_arch        "sparc"
%else
%define bld_arch	"i386"
%endif

# use --without-gtk-doc to disable building gtk-docs (it takes quite
# a while to build them)
# default: build gtk-doc API docs
%define gtk_doc_option %{?!_without_gtk_doc:--enable-gtk-doc}%{?_without_gtk_doc:--disable-gtk-doc}

%define arch_ldadd -m32

%if %debug_build
%define pkgbuild_postprocess /bin/true
%define _gcc_opt_level     -g
%define _gxx_opt_level     -g
%define _cc_opt_level      -g
%define _cxx_opt_level     -g
%else
%define _gcc_opt_level     -O3
%define _gxx_opt_level     -O3
%define _cc_opt_level      -xO4 -xspace
%define _cxx_opt_level     -xO3 -xspace
%endif

%ifarch sparc
%define gcc_optflags           %_gcc_opt_level -m32 -mv8plus -Xlinker -i
%define gcc_cxx_optflags       %_gxx_opt_level -m32 -mv8plus -Xlinker -i
%define suncc_optflags         %_cc_opt_level  -m32 -xarch=v8plusa -i -mr
%define suncc_cxx_optflags     %_cxx_opt_level -m32 -xarch=v8plusa -i -mr
%endif

%ifarch i386
%define gcc_optflags           %_gcc_opt_level -m32 -march=i686 -Xlinker -i -fno-omit-frame-pointer -mincoming-stack-boundary=2
%define gcc_cxx_optflags       %_gxx_opt_level -m32 -march=i686 -Xlinker -i -fno-omit-frame-pointer -mincoming-stack-boundary=2
%define suncc_optflags         %_cc_opt_level  -m32 -xarch=pentium_pro -i -mr -xregs=no%%frameptr
%define suncc_cxx_optflags     %_cxx_opt_level -m32 -xarch=pentium_pro -i -mr -xregs=no%%frameptr
%endif

%if %cc_is_gcc
# optflags get picflags added to them for gcc but not Sun CC. This inconsistency
# should be eliminated; unfortunately however, because so many specs using gcc 
# rely upon this, correcting it is impractical without a concerted effort.

%define picflags %gcc_picflags
%define optflags %gcc_optflags %gcc_picflags
%define cxx_optflags %gcc_cxx_optflags %gcc_picflags
%define _gpp_version %(%{?_gpp:%_gpp}%{!?_gpp:g++} --version | head -1 | cut -f3 -d' ')
%define _cxx_libdir	   %{_prefix}/lib/g++/%{_gpp_version}

%else
# cc is not gcc

%define picflags %suncc_picflags
%define optflags %suncc_optflags ${EXTRA_CFLAGS}
%define cxx_optflags %suncc_cxx_optflags ${EXTRA_CXXFLAGS}
%define _cxx_libdir %{_prefix}/lib

%endif

%define _bindir		%{_prefix}/bin
%define _libdir		%{_prefix}/lib
%define _libexecdir	%{_prefix}/lib
%define _pkg_config_path %{_libdir}/pkgconfig
%define _sysconfdir	/etc

# Define some standard directories
%define gnu_bin		/usr/gnu/bin
%define gnu_inc		/usr/gnu/include
%define gnu_lib		/usr/gnu/lib
%define gnu_lib_path	-L%{gnu_lib} -R%{gnu_lib}
%define gpp_bin		/usr/g++/bin
%define gpp_inc		/usr/g++/include
%define gpp_lib		/usr/g++/lib
%define gpp_lib_path	-L%{gpp_lib} -R%{gpp_lib}
%define sfw_bin		/usr/sfw/bin
%define sfw_inc		/usr/sfw/include
%define sfw_lib		/usr/sfw/lib
%define sfw_lib_path	-L%{sfw_lib} -R%{sfw_lib}
%define xorg_bin	/usr/X11/bin
%define xorg_lib	/usr/X11/lib
%define xorg_inc	/usr/X11/include
%define xorg_lib_path	-L%{xorg_lib} -R%{xorg_lib}

%changelog
* Sun Dec 11 2016 - Thomas Wagner
- remove vom c++ "-norunpath" or run with developerstudio into e.g. "ld.so.1: conftest: fatal: libstatomic.so.1: open failed: No such file or directory" (S12/SunCC 5.14)
- LDFLAGS -> set arch_ldadd -m32 to get ld invoked correctly in 32-bit with brand new compilers (or get wrong ELFCLASS when linking)
* Sun Dec 11 2016 - Thomas Wagner
- compilers start to default to -m64, so explicitly require -m32 for all non-64-bit compile runs (base.inc, x86_sse2.inc
* Thu Oct  6 2016 - Thomas Wagner
- add to gcc_optflags/cxx_optflags "-mincoming-stack-boundary=2" (needed for gcc 4.8 on x86 for 32-bit targets to avoid segfaults with -O3)
* Sun Okt 11 2015 - Thomas Wagner
- add gpp_lib to base.inc, arch64.inc and x86_sse2.inc
- still try to keep changes to this include files to a minumum please
# 2013-10-28  Alex Viskovatoff
# - do not add gcc_picflags to gcc_optflags: in the case of gcc, add them to
#   optflags instead, so that users can access the standard gcc_optflags
#   without their containing picflags, which are only needed for libraries.
# - clean up
# 2011-10-21  Alex Viskovatoff
# - %define opt_arch64 0, since it is %defined 1 in arch64.inc
# 2011-03-18  Milan Jurik
# - move minimal x86 CPU to pentium_pro/i686
# - move minimal SPARC CPU to UltraSPARC
# 2008-05-09  Laszlo (Laca) Peter  <laca@sun.com>
# - use %_gpp instead of g++ when checking the version of g++
# 2008-02-17  Laszlo (Laca) Peter  <laca@sun.com>
# - define _cxx_libdir and _gpp_version for building C++ libs
# 2007-06-09  Laszlo (Laca) Peter  <laca@sun.com>
# - delete cc_is_gcc conditional when setting _gcc_opt_level,
#   because we want this set anyway so it can be used in spec
#   files that force gcc
# 2007-04-05  Laszlo (Laca) Peter  <laca@sun.com>
# - fix cxx_optflags: use EXTRA_CXXFLAGS and not EXTRA_LDFLAGS
# 2007-03-20  Doug Scott  <dougs@truemail.co.th>
# added standard directories definitions
# 2007-03-19  Doug Scott  <dougs@truemail.co.th>
# - Fixed -fno-omit-frame-pointer flag
# 2007-03-15  Laszlo (Laca) Peter  <laca@sun.com>
# - copied from x86_sse2.inc
# - new include file that resets macros to their default (32-bit build)
#   values
# 2007-03-12  Doug Scott  <dougs@truemail.co.th>
