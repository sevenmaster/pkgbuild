##TODO##


##TODO## from publlic channel #illumos on irc.freenode.org
 
# 20:25 < richlowe> I'm trying to keep myself in the state where he's convinced me it's right.
# 20:25 < richlowe> otherwise I'll start doubting it again :)
# 20:28 < pmooney> richlowe: Would it make sense to include a little test program which exercise this?
# 20:30 < jeffpc> richlowe: btw, I haven't noticed any badness with your latest aslr changes
# 20:30 < jeffpc> latest = month or so old
# 20:46 < richlowe> pmooney: all I could do is what the problem app is doing, and I'm not sure there's any real chance 
#                   at re-breaking.
# 20:46 < pmooney> richlowe: roger that
# 20:46 < pmooney> I'm checking one last thing...
# 20:48 < richlowe> pmooney: if you can think of ways that'll have some variance?
# 20:48 < pmooney> richlowe: No, how gcc behaves in the face of AVX.  The newer psABI doc makes reference to 32-byte 
#                  alignment for that.
# 20:53 < nbjoerg> gcc since around 4.6 can finally properly realign the stcak on demand
# 20:53 < nbjoerg> so all the excuses for breaking the sysv abi as done by linux are just that, excuses
# 21:00 < pmooney> richlowe: I'm satisfied.  Ship it.
# 21:09 < richlowe> nbjoerg: 5.x with SSE ops in init functions sure does crash unless you align the stack 
#                   sufficiently on entry for it.
# 21:15 < richlowe> nbjoerg: though the alignment reqs don't _break_ the ABI exactly, they're back compatible but not 
#                   forward
# 21:23 < richlowe> jeffpc: that's next, unless something else breaks in the interim.
# 21:38 < alanc> I thought rainer was fixing that in 5.3 or 5.4
# 21:40 < leoric> I tested with 5.3
# 21:40 < richlowe> the other test was 5.4
# 21:41 < richlowe> though I suppose that was of the init_array stuff.
# 21:55 < richlowe> alanc: and it's not obvious when his fix got backported, but yeah, he seems to have somehow fixed 
#                   it only for Solaris 9 in the past.
# 21:55 < richlowe> and then realized it was a generic problem.
# 22:05 < daleg> I thought you were referring to SunOS versions there for a second
# 22:08 < anniz> wasnt 5.3 kinda rare? iirc people didnt really start switching over from sunos 4 until 5.4-5.5
# 22:09 < alanc> gcc 5.3, not SunOS 5.3
# 22:10 < alanc> ah, found the mail from him after I hacked userland to do -mincoming-stack-boundary=2
# 22:10 < alanc> he said "The fix (effectively defaulting to -mstackrealign on 32-bit Solaris/x86)
# 22:10 < alanc> Ihttps://gcc.gnu.org/ml/gcc-patches/2016-03/msg00461.html
# 22:10 < alanc> went into GCC 4.9.4 (not yet released), 5.4 (released a few days ago)
# 22:10 < alanc> and 6.1.  Either cherry-picking that fix or upgrading GCC could be
# 22:10 < alanc> options."
# 22:11 < alanc> and the gcc upstream bug was https://gcc.gnu.org/bugzilla/show_bug.cgi?id=62281
# 22:16 < alanc> fortunately, now that gcc is doing annual major releases, the odds of ever seeing gcc 5.11 are slim
# 22:16 < richlowe> "fortunately, now that gcc is doing annual major releases"
# 22:17  * alanc starts humming "Always look on the bright side of life, doo doo..."
# 22:17 < richlowe> wash your mouth out.
# 22:17 < alanc> lol
# 
# 
# 
# 
# 
# 
# https://gcc.gnu.org/ml/gcc-patches/2016-03/msg00461.html
# 
# 
# Only assume 4-byte stack alignment on 32-bit Solaris/x86 (PR target/62281)
# 
# 


#
# spec file for package SFEgcc
#
# includes module(s): GNU gcc
#

# owner:  Thomas Wagner
#

##TODO## test sparc version of gcc-05-LINK_LIBGCC_SPEC-sparcv9.diff

%include Solaris.inc
%include osdistro.inc
%include buildparameter.inc
%if %( expr %{solaris12} '|' %{oihipster} '|' %{omnios} )
%define cc_is_gcc 1
%endif
%include base.inc

%define _use_internal_dependency_generator 0

#provide symbolic links in places define below:
#start the paths with a leading "/"

#IMPORTANT! READ ON BELOW and set switches and paths accordingly

#hack for the %files section. use define for each directory from above
#to control the non scriptable %files section
#1 = enabled    0 = disabled
#and special<n>path point to one of the paths noted in %{gccsymlinks}
%define symlinktarget1enabled      1
%define symlinktarget1path /usr/gcc-sfe

%define symlinktarget2enabled      1
%define symlinktarget2path /usr/gnu

#spare
%define symlinktarget3enabled      0
%define symlinktarget3path /usr

#overwrite
%if %{omnios}
%define symlinktarget3enabled      1
%define symlinktarget3path /usr/sfw
#mediators?
%define create_gcc_3_dummypackage  1
%endif

#construct used targets into one variable
%if %{symlinktarget1enabled}
%define gccsymlinks1 %{symlinktarget1path}
%else 
%define gccsymlinks1
%endif

%if %{symlinktarget2enabled}
%define gccsymlinks2 %{symlinktarget2path}
%else 
%define gccsymlinks2
%endif

%if %{symlinktarget3enabled}
%define gccsymlinks3 %{symlinktarget3path}
%else 
%define gccsymlinks3
%endif

%define gccsymlinks %{gccsymlinks1} %{gccsymlinks2} %{gccsymlinks3}

# check for /usr/gnu/bin/cc and bail out
# CR 7031722 (Solaris)
# Bug-ID <TBD> (OI)
%define compat_link_usr_gnu_bin_cc %( test -r /usr/gnu/bin/cc && echo 1 || echo 0 )

# to more widely test if this change causes regressions, by default off:
# want this? compile with: --with-handle_pragma_pack_push_pop
%define with_handle_pragma_pack_push_pop %{?_with_handle_pragma_pack_push_pop:1}%{?!_with_handle_pragma_pack_push_pop:0}

##TODO## should include/arch64.inc consider setting _arch64 that way?
#        gcc builds 64-bit libs/binaries even on 32-bit CPUs/Kernels (e.g. ATOM CPU)
%ifarch amd64 i386
%define _arch64 amd64
%else
%define _arch64 sparcv9
%endif


#default to SUNWbinutils
%define SUNWbinutils 0
##TODO## if necessary add osbuild numbers to decide SUNW/SFE version
%define SFEbinutils_gpp     %(/usr/bin/pkginfo -q SFEbinutils-gpp  2>/dev/null && echo 1 || echo 0)

##TODO## check binutils version in OIH, if sufficiently new, then set SUNWbinutils 1, SFEbinutils_gpp  0
#overwrite the default for specific OS
#name on omnios would be developer/gnu-binutils (check if that can be used, then deal with package names)
%if %{omnios}
%define SUNWbinutils 0
%define SFEbinutils_gpp  0
#using /usr/bin/gld from developer/gnu-binutils@2.24
%endif

#see below, older builds then 126 have too old gmp / mpfr to gcc version around 4.4.4
#%define SFEgmp          %(/usr/bin/pkginfo -q SFEgmp  2>/dev/null  && echo 1 || echo 0)
##TODO## to be replaced by packagenamemacros, selecting SFEgmp on specific osbuilds where
#it is too old for fresh gcc builds
%define SFEgmp          1
#%define SFEmpfr         %(/usr/bin/pkginfo -q SFEmpfr 2>/dev/null  && echo 1 || echo 0)
##TODO## to be replaced by packagenamemacros, selecting SFEmpfr on specific osbuilds where
#it is too old for fresh gcc builds
%define SFEmpfr         1

# force using gmp | mpfr
#if SFEgmp is not present, force them as required by the commandline switch --with_SFEgmp
%define with_SFEgmp %{?_with_SFEgmp:1}%{?!_with_SFEgmp:0}
#if build is lower then 126 then force it (update to gmp see CR 6863696)
%if %(expr %{osbuild} '<' 126)
%define with_SFEgmp 1
%endif

%if %with_SFEgmp
%define SFEgmp 1
%endif

#if SFEgmp is not present, force them as required by the commandline switch --with_SFEmpfr
%define with_SFEmpfr %{?_with_SFEmpfr:1}%{?!_with_SFEmpfr:0}
#if build is lower then 126 then force it (update to gmp see CR 6863684)
%if %(expr %{osbuild} '<' 126)
%define with_SFEmpfr 1
%endif

%if %with_SFEmpfr
%define SFEmpfr 1
%endif

#if SFElibmpc is not present, force them as required by the commandline switch --with-SFElibmpc
#future OS versins might include a libmpc, leave code commented until then
%define with_SFElibmpc %{?_with_SFElibmpc:1}%{?!_with_SFElibmpc:0}
#parked #if build is lower then 126 then force it (update to gmp see CR 6863684)
#parked %if %(expr %{osbuild} '<' 126)
#for *now* require SFElibmpc in any case
%define with_SFElibmpc 1
#parked %endif

%if %with_SFElibmpc
%define SFElibmpc 1
%endif

#set default gcc version
%define default_version 4.9.4

#set more defaults
%define build_gcc_with_gnu_ld 0

%if %{solaris12}
%define default_version 4.9.4
#%define build_gcc_with_gnu_ld 0
#try with gnu_ld to avoid having -fno-exception passed to the linker which only accepts this for dynamic objects
%define build_gcc_with_gnu_ld 1
#END solaris12
%endif

%if %{omnios}
%define default_version 4.9.4
#test %define build_gcc_with_gnu_ld 0
%define build_gcc_with_gnu_ld 1
#END OmniOS
%endif

#temporary setting, 4.9.4 testing on OI151a8 OI151a9
%if %( expr %{openindiana} '&' %{oihipster} '=' 0 )
%define default_version 4.9.4
%define build_gcc_with_gnu_ld 1
#END openindiana
%endif

#transform full version to short version: 4.6.2 -> 4.6  or  4.7.1 -> 4.7
%if %{oihipster}
%define default_version 4.9.4
%define build_gcc_with_gnu_ld 1
#END OIHipster
%endif

#if you want a specific version of gcc be built, then change the default setting
#below *or* specify the number on the command line (gcc_version), example see below

# To set a specific gcc version to be build, do this from *outside*
# pkgtool build SFEgcc --define 'gcc_version 4.7.2'

%if 0%{!?gcc_version:1}
#make version bump *here* - this is the default version being built
%define version %{default_version}
%else
#gcc version is already defined from *outside*, from the pkgtool command line
%define version %{gcc_version}
%endif
#special handling of version / gcc_version

#transform full version to short version: 4.6.2 -> 4.6  or  4.7.1 -> 4.7
#%define major_minor %( echo %{version} | sed -e 's/\([0-9]*\)\.\([0-9]*\)\..*/\1.\2/' )
#below is a workaround for pkgbuild 1.3.104 failing to parse the escaped \( and \)
%define major_minor %( echo %{version} |  sed -e 's/\.[0-9]*$//' )
# make 4.9.3 -> 4
# make 5.4.0 -> 5
%define major_version %( echo %{version} |  sed -e 's/\..*$//' )

#for package or path names we need the version number _without_ the dots:
#transform dottet version number to non-dotted:  4.6 -> 46
%define majorminornumber %( echo %{major_minor} | sed -e 's/\.//g' )

##TODO## check if this works with gcc5 version numbers works (shorter)
#for comparisons we need the verison number major-minor-micro
#example echo 4.9.4 | awk -F'.' '{printf "%.4d%.4d%.4d", $1, $2, $3}'
#mind escaping % by using %%
#000400090004
%define majorminormicro_padded_number4 %( echo %{version} | awk -F'.' '{printf "%%.4d%%.4d%%.4d", $1, $2, $3}' )

# new filesystem location /usr/gcc-sfe/ for SFEgcc.spec is now *on* by default, 
# you may choose to switch this back # to the previous location: /usr/gcc/
# example: pkgtool --with-old-path-usr-gcc
# note: creation is automatic for compatibility symlinks from /usr/gcc/lib and /usr/gcc/bin to /usr/gcc-sfe/lib and /usr/gcc-sfe/bin
%define old_path_usr_gcc %{?_with_old_path_usr_gcc:1}%{?!_with_old_path_usr_gcc:0}


%if %( expr %{major_minor} '<' 4.8 '|' %{major_minor} '>=' 5.0)
#gcc is too old or is at gcc 5.0 or higher
%define old_path_usr_gcc 0
%if %{?_with_old_path_usr_gcc:1}
%define old_path_usr_gcc 1
%endif
%else
#build with old_path_usr_gcc directory /usr/gcc/lib 
%define old_path_usr_gcc 1
%if 0%{?_without_old_path_usr_gcc:1}
%define old_path_usr_gcc 0
%endif
%endif


%define _prefix_original %{_basedir}

##TODO## make new gcc home configurable from the command line!

%if %( expr %{major_minor} '<=' 4.7 )
#OLD path
%define gccdir gcc
%define _prefix_usr_gcc %{_basedir}/gcc
%else
#NEW path, this is the default
%define gccdir gcc-sfe
%define _prefix_usr_gcc %{_basedir}/gcc-sfe
%endif
#END old_path_usr_gcc 


%if %( expr %{major_minor} '>=' 5.0 )
#NEW with gcc 5.x the only remaining version strong in directory path is: major (e.g. "5")
%define _prefix_usr_gcc_version %{_prefix_usr_gcc}/%{major_version}
%else
#OLD with gcc 4.x have longer version numbers in in directory path: major_minor (e.g. "4.9")
%define _prefix_usr_gcc_version %{_prefix_usr_gcc}/%{major_minor}
%endif
#END

%define _prefix		%{_prefix_usr_gcc_version}
%define _infodir	%{_prefix}/info

# Supported languages are: c,c,c++,fortran,go,java,lto,objc,obj-c++
%define gcc_enable_languages c,c++,fortran,objc

#enable java compiler --with-gcj or disable --without-gcj
#is default on with majorminor = 4.9, on 4.9 currently this is always on, regardless of --without-gcj is used
%define gcj %{?_with_gcj:1}%{?!_with_gcj:0}

#enable compiling java gcj
##TODO## see if this works also for gcc 5.x
%if %( expr %{major_minor} '=' 4.9 )
%define gcj 1
%endif

%if %{gcj}
#%define ecj_jar_abs_path  %{topdir}/gcc-%{version}/ecj.jar
%define ecj_jar_abs_path  %_builddir/%name-%version/ecj.jar
%define gcc_configure_java --with-java --with-ecj-jar=%{ecj_jar_abs_path} --enable-libgcj
%define gcc_enable_languages_java ,java
%define gcc_symlinks_pattern bin/ecj bin/aot-compile bin/gappletviewer bin/gc-analyze bin/gcj bin/gcj-dbtool bin/gcjh bin/gij bin/gjar bin/gjarsigner bin/gjavah bin/gkeytool bin/gnative2ascii bin/gorbd bin/grmic bin/grmid bin/grmiregistry bin/gserialver bin/gtnameserv bin/jcf-dump bin/jv-convert bin/rebuild-gcj-db lib/gcj-%{version}-15 lib/libgcj-tools.so lib/libgcj-tools.so.15 lib/libgcj-tools.so.15.0.0 lib/libgcj.so lib/libgcj.so.15 lib/libgcj.so.15.0.0 lib/libgcj.spec lib/libgij.so lib/libgij.so.15 lib/libgij.so.15.0.0 lib/logging.properties lib/pkgconfig/libgcj-%{major_minor}.pc lib/security/classpath.security
%define gcc_symlinks_pattern_arch64 lib/%{_arch64}/gcj-%{version}-15 lib/%{_arch64}/libgcj-tools.so lib/%{_arch64}/libgcj-tools.so.15 lib/%{_arch64}/libgcj-tools.so.15.0.0 lib/%{_arch64}/libgcj.so lib/%{_arch64}/libgcj.so.15 lib/%{_arch64}/libgcj.so.15.0.0 lib/%{_arch64}/libgij.so lib/%{_arch64}/libgij.so.15 lib/%{_arch64}/libgij.so.15.0.0 lib/%{_arch64}/logging.properties lib/%{_arch64}/pkgconfig/libgcj-%{major_minor}.pc lib/%{_arch64}/security/classpath.security
%else
#no java
%define gcc_configure_java
%define gcc_enable_languages_java
%define gcc_symlinks_pattern
%define gcc_symlinks_pattern_arch64
%endif


#`--with-ecj-jar=FILENAME'
#     This option can be used to specify the location of an external jar
#     file containing the Eclipse Java compiler.  A specially modified
#     version of this compiler is used by `gcj' to parse `.java' source
#     files.  If this option is given, the `libjava' build will create
#     and install an `ecj1' executable which uses this jar file at
#     runtime.
#
#     If this option is not given, but an `ecj.jar' file is found in the
#     topmost source tree at configure time, then the `libgcj' build
#     will create and install `ecj1', and will also install the
#     discovered `ecj.jar' into a suitable place in the install tree.
#
#     If `ecj1' is not installed, then the user will have to supply one
#     on his path in order for `gcj' to properly parse `.java' source
#     files.  A suitable jar is available from
#     `ftp://sourceware.org/pub/java/'.



# force using SFEbinutils_gpp from the pkgtool/pkgbuild command line - for testing purpose
#if SFEbinutils_gpp is not present, force it by the commandline switch --with_SFEbinutils_gpp
%define with_SFEbinutils_gpp %{?_with_SFEbinutils_gpp:1}%{?!_with_SFEbinutils_gpp:0}
%if %with_SFEbinutils_gpp
%define SFEbinutils_gpp 1
%define SUNWbinutils 0
%endif

#if building gcc 4.7 or up force the use of SFEbinutils_gpp since OI's binutils is too old
#S11.0    developer/gnu-binutils@2.21.1,5.11-0.175.1.0.0.24.0
#S11.2                           2.23.1
#oi151a9  developer/gnu-binutils@2.19,5.11-0.151.1.9
##TODO## what do we need on OI hipster?
#%if %( expr %{openindiana} '+' %{oihipster} '>=' 1 '&' %{major_minor} '>=' 4.7 )
%if %( expr %{openindiana} '>=' 1 '&' %{major_minor} '>=' 4.7 )
%define SFEbinutils_gpp 1
%define SUNWbinutils 0
%endif

# This "Name:" SFEgcc and SFEgccruntime is a compatibility layer,
# and delivering only symbolic links to corresponding versioned
# directories with real files delivered in sub packages like 
# SFEgcc-%majorminornumber and SFEgccruntime-%majorminornumber

##TODO## make symlinks mediated symlinks for machine-local configured,
#preferred versions. Not as flexible as we want (want: user selectable
#gcc variant, but we get only whole machine defaults)

Name:		SFEgcc
#https://gcc.gnu.org/develop.html#num_scheme
IPS_package_name:	sfe/developer/gcc
Summary:	GNU gcc compiler (%{_prefix}) - metapackage with symbolic links to version %{major_minor} compiler files available in %{gccsymlinks}
#Version:	see above, %{version} is set elsewhere
Version:	%{version}
License:             GPLv3+
Group:		Development/C
SUNW_BaseDir:	%{_basedir}
SUNW_Copyright:      gcc.copyright
Source:              ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.gz
#%define version_ecj  -latest
%define version_ecj  %{major_minor}
%define version_ecj  4.9
Source2:             ftp://sourceware.org/pub/java/ecj-%{version_ecj}.jar
Patch1:              gcc-01-libtool-rpath.diff

%if %with_handle_pragma_pack_push_pop
Patch2:              gcc-02-handle_pragma_pack_push_pop.diff
%else
%endif

##TODO## temporarily paused for >=4.9
%if %( expr %{major_minor} '>=' 4.7 '&' %{major_minor} '<=' 4.8 )
Patch3:              gcc-03-gnulib-47.diff
%else
Patch3:              gcc-03-gnulib.diff
%endif

#changes in version -> see %prep as well for re-editing of the sol2.h file
%if  %( expr %{major_minor} '>=' 4.8 '&' %{major_minor} '<' 5.0 )
#                    ^^^^^
#LINK_LIBGCC_SPEC
#gcc-05 in reworked version now supports both, AMD64 and SPARC from the same patch
#NOTE: once sol2.h changes too much, we might need to rework the patch
Patch5:              gcc-05-LINK_LIBGCC_SPEC-%{majorminornumber}.diff
#                                                   ^^^^^^^^^^^ e.g. 49
%endif
#END %{major_minor} >= 4.8 & %{major_minor} < 5.0 

#changes in version -> see %prep as well for re-editing of the sol2.h file
%if  %( expr %{major_minor} '>=' 5.0 )
#                    ^^^^^
#LINK_LIBGCC_SPEC
#gcc-05 now supports both, AMD64 and SPARC from the same patch
#NOTE: once sol2.h changes too much, we might need to rework the patch
Patch5:              gcc-05-LINK_LIBGCC_SPEC-%{major_version}.diff
#                                                    ^^^^^^^
%endif
#END %{major_minor} >= 5.0

# http://gcc.gnu.org/bugzilla/show_bug.cgi?id=49347
# if clause to apply only on specific gcc versions, see %prep
Patch10:	gcc-10-spawn.diff

#SFElibx264.spec https://gcc.gnu.org/viewcvs/gcc?view=revision&revision=230249
# -> bug problem of gcc with -fstack-check https://gcc.gnu.org/bugzilla/show_bug.cgi?id=67265
#https://gcc.gnu.org/viewcvs/gcc?view=revision&revision=230249
Patch11: gcc-11-remove-obsolete-assertion-on-the-CFA-register-_ported_to_4.8.x_gcc_bug_230249.diff

#For gcc 4.8.5 on Solaris 11 and Solaris 12 (already have updated/fixed header files)
%if %( expr %{solaris11} '+' %{solaris12} '>=' 1 '&' %{major_minor} '=' 4.8 )
Patch12: gcc-12-fixinc.in.patch
%endif

##TODO## enhance: use padded numbers eventually - same in %prep
%if %( expr %{solaris11} '+' %{solaris12} '>=' 1 '&' %{major_minor} '=' 4.8 )
#Patch100: 000-userlandgate-gcc-Makefile.in.patch
Patch101: 001-userlandgate-fixinc.in.patch
Patch102: 002-userlandgate-inclhack.def.patch
Patch103: 003-userlandgate-libgomp-omp_h-multilib.patch
Patch104: 004-userlandgate-libitm-configure.patch
Patch105: 005-userlandgate-libitm-rwlock.patch
Patch106: 006-userlandgate-fixincludes-check.tpl.patch
#careful please when updating patch, we've removed the runpath part! (this is in our own gcc-05-LINK_LIBGCC_SPEC-**)
Patch107: 007-userlandgate-gcc-sol2.h.patch.modified.diff
Patch108: 008-userlandgate-c99_classification_macros.patch
##TODO## already applied? verify! Patch109: 009-userlandgate-CVE-2014-5044.patch
Patch110: 010-userlandgate-studio-as-comdat.patch
#END %{solaris11} '+' %{solaris12} '>=' 1 '&' %{major_minor} '=' 4.8
%endif


#patches thanks to solaris userland gate
%if %( expr %{solaris11} '+' %{solaris12} '>=' 1 '&' %{major_minor} '=' 4.9 )
#Careful please when updating patch, we've removed the runpath part in gcc49-000-sol2.h.patch! (this is in our own gcc-05-LINK_LIBGCC_SPEC-**)
#This time we apply patch5 for gcc 4.9 *after* using the userland gate patch. This should make maintenance a bit easier as gcc49-000-sol2.h.patch stays unmodified.
Patch200: gcc49-000-sol2.h.patch
Patch201: gcc49-001-Makefile.in.patch
Patch202: gcc49-002-omp-lock.h.patch
Patch203: gcc49-003-ptrlock.h.patch
Patch204: gcc49-004-sem.h.patch
#got you, there is no 005
Patch206: gcc49-006-omp.h.in.patch
Patch207: gcc49-007-libgomp.exp.patch
Patch208: gcc49-008-fixincludes-check.tpl.patch
Patch209: gcc49-009-configure.patch
Patch210: gcc49-010-c99_classification_macros_c++0x.cc.patch
Patch211: gcc49-011-libstdc++.configure.patch
Patch212: gcc49-012-fixinc.in.patch
Patch213: gcc49-013-libcpp-Makefile.in.patch
Patch214: gcc49-014-libiberty-Makefile.in.patch
Patch215: gcc49-015-configure-largefile.patch
Patch216: gcc49-016-022-gthr-posix.h.patch
Patch217: gcc49-017-libstdc++-src-Makefile.in.patch
Patch218: gcc49-018-libcilkrts-Makefile.in.patch
Patch219: gcc49-019-libcilkrts-sysdep-unix.c.patch
Patch220: gcc49-020-libcilkrts-configure.tgt.patch
Patch221: gcc49-021-libcilkrts-cilk-abi-vla.c.patch
Patch222: gcc49-022-libcilkrts-os-unix-sysdep.c.patch
Patch223: gcc49-023-libcilkrts-tests.patch
Patch224: gcc49-024-configure.patch
Patch225: gcc49-025-libgcc-Makefile.in.patch
Patch226: gcc49-026-basic_string.patch
%if %( expr %{majorminormicro_padded_number4}.0 '<=' 000400090003.0 )
Patch227: gcc49-027-cmath_c99.patch
%endif
#END %{solaris11} '+' %{solaris12} '>=' 1 '&' %{major_minor} '=' 4.8
%endif

#patches thanks to solaris userland gate
%if %( expr %{solaris11} '+' %{solaris12} '>=' 1 '&' %{major_minor} '>=' 5.3 )
Patch301: gcc53-001-multilib-sparc.patch
Patch302: gcc53-002-libc-values.patch
Patch303: gcc53-003-cilk-sparc.patch
Patch304: gcc53-004-alignment.patch
Patch306: gcc53-006-fixincludes.patch
%if %( expr %{major_minor} '<' 5.4 )
Patch308: gcc53-008-c99_classification_macros_c++0x.cc.patch
%endif
#END %{solaris11} '+' %{solaris12} '>=' 1 '&' %{major_minor} '=' 4.8
%endif

##TODO## temporary fix, probably needs rework. With java we get boehm-gc/os_dep.c complain about procfs.h not large file aware so we #undef _FILE_OFFSET_BITS
#        and hope, that is only uses procfs stuff where this doesn't matter.
Patch501: gcc49-501-boehmm-gc-os_dep.c-dirty-fix-for-procfs-large-file-env.diff

#gcj with 4.9.4 (and others) doesn't work on s1104, missing old_procfs.h defining PIOCOPENPD that is used in
#older versions of boehm-gc/os_dep.c:3202:41: error: 'PIOCOPENPD' undeclared (first use in this function)
#     GC_proc_fd = syscall(SYS_ioctl, fd, PIOCOPENPD, 0);
#s1104 stopped providing old_procfs.h, need to use new interface
Patch502: gcc49-502-boehm-gc-os_dep.c-avoid-procfs-ioctl.diff


BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#Attention - this is the dependency chain for the compiler:
#      SFEgcc -needs-> SFEgcc-46,SFEgccruntime-46
# this is an example for a program which can have this
# dependency chain (most common case)
#      SFEapplication -needs-> SFEgccruntime 
# *OR* in special cases
#      SFEapplication -needs-> SFEgccruntime-46
#
# today we want exactly 4.6. later on if we can ask a minimum revision,
# then a "Requires:" can be changed to request the minimum version which
# is needed to e.g. >= 4.6
Requires:      SFEgcc-%{majorminornumber},SFEgccruntime-%{majorminornumber}
#cosmetic:
Requires:      SFEgccruntime

#try libc iconv by setting --without-libiconv-prefix
#BuildRequires: SFElibiconv-devel
#Requires:      SFElibiconv
%if %{is_s10}
BuildRequires:  SUNWbash
%endif

#need something to start compiling with
%if %( expr %{solaris11} '|' %{oihipster} '|' %{openindiana} )   
BuildRequires: developer/gcc-3
##TODO## check if required: Requires: developer/gcc-3-runtime
%endif

%if %( expr %{s110400} )
BuildRequires: developer/gcc-5
%endif

#OmniOS R151012 has no gcc-3 any more, request OmniOS's gcc-48
#as a replacement and in %build, point the CC and CXX variable to this compiler
%if %{omnios}
#mind the modification of the CC and CXX variables in %build
BuildRequires: developer/gcc48
BuildRequires: developer/gnu-binutils
%endif

%if %SFEgmp
BuildRequires: SFEgmp-devel
Requires: SFEgmp
#workaround on IPS which is wrong with BASEdir as "/" -> then assume /usr/gnu
%define SFEgmpbasedir %(pkgparam SFEgmp BASEDIR 2>/dev/null | sed -e 's+^/$+/usr/gnu+')
%else
BuildRequires: SUNWgnu-mp
Requires: SUNWgnu-mp
%endif

#OmniOS R151012 has no gcc-3 any more, request OmniOS's gcc-48
#as a replacement and in %build, point the CC and CXX variable to this compiler
%if %{omnios}
#mind the modification of the CC and CXX variables in %build
BuildRequires: developer/gcc48
BuildRequires: developer/gnu-binutils
%endif

%if %SFEgmp
BuildRequires: SFEgmp-devel
Requires: SFEgmp
#workaround on IPS which is wrong with BASEdir as "/" -> then assume /usr/gnu
%define SFEgmpbasedir %(pkgparam SFEgmp BASEDIR 2>/dev/null | sed -e 's+^/$+/usr/gnu+')
%else
BuildRequires: SUNWgnu-mp
Requires: SUNWgnu-mp
%endif

%if %SFEmpfr
BuildRequires: SFEmpfr-devel
Requires: SFEmpfr
#workaround on IPS which is wrong with BASEdir as "/" -> then assume /usr/gnu
%define SFEmpfrbasedir %(pkgparam SFEmpfr BASEDIR 2>/dev/null | sed -e 's+^/$+/usr/gnu+')
%else
BuildRequires: SUNWgnu-mpfr
Requires: SUNWgnu-mpfr
%endif

%if %SFElibmpc
BuildRequires: SFElibmpc-devel
Requires: SFElibmpc
#workaround on IPS which is wrong with BASEdir as "/" -> then assume /usr/gnu
%define SFElibmpcbasedir %(pkgparam SFElibmpc BASEDIR 2>/dev/null | sed -e 's+^/$+/usr/gnu+')
%else
#BuildRequires: empty
#Requires: empty
%endif

%if %SFEbinutils_gpp
BuildRequires: SFEbinutils-gpp
Requires: SFEbinutils-gpp
%endif

%if %( expr %SUNWbinutils '&' %{os2nnn} '=' 0 '&' %{SFEbinutils_gpp} '=' 0 )
#old non IPS systems:
BuildRequires: SUNWbinutils
Requires: SUNWbinutils
%endif

%if %( expr %SUNWbinutils '&' %{os2nnn} '=' 1 '&' %{SFEbinutils_gpp} '=' 0 )
#on an IPS based system
BuildRequires: developer/gnu-binutils
Requires: developer/gnu-binutils
%endif

%if %{os2nnn}
#no need for postrun
%else
BuildRequires: SUNWpostrun
Requires: SUNWpostrun
%endif

%package -n SFEgcc-%{majorminornumber}
IPS_package_name:        sfe/developer/gcc-%{majorminornumber}
Summary:                 GNU gcc compiler (%{_prefix}) - version %{major_minor} compiler files
Version:                 %{version}
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}runtime-%{majorminornumber}

%package -n SFEgccruntime
IPS_package_name:        sfe/system/library/gcc-runtime
Summary:                 GNU gcc runtime libraries for applications (%{_prefix}) - metapackage with symbolic links to version %{major_minor} runtime available in %{gccsymlinks}
Version:                 %{version}
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}runtime-%{majorminornumber}

%package -n SFEgccruntime-%{majorminornumber}
IPS_package_name:        sfe/system/library/gcc-%{majorminornumber}-runtime        
Summary:                 GNU gcc runtime libraries for applications (%{_prefix}) - version %{version} runtime library files
Version:                 %{version}
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
#not apropriate Requires: %{name}

%if %SFEgmp
BuildRequires: SFEgmp-devel
Requires: SFEgmp
%else
BuildRequires: SUNWgnu-mp
Requires: SUNWgnu-mp
%endif

%if %SFEmpfr
BuildRequires: SFEmpfr-devel
Requires: SFEmpfr
%else
BuildRequires: SUNWgnu-mpfr
Requires: SUNWgnu-mpfr
%endif

%if %SFElibmpc
BuildRequires: SFElibmpc-devel
Requires: SFElibmpc
%else
#BuildRequires: SUNWthis-package-not-availbale
#Requires: SUNWthis-package-not-availbale
%endif

%if %build_l10n
%package -n SFEgcc-l10n
IPS_package_name: sfe/developer/gcc-%{majorminornumber}/locale
Summary:                 %{summary} (%{_prefix}) - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%description
GCC compiler with special setting to find the own runtime library files in
this path: ...
prefix/lib                %{_prefix}/lib/  ...
_prefix_usr_gcc/lib       %{_prefix_usr_gcc}/lib/  ...
old_compat_libdir         %{old_compat_libdir}  ...
old_path_usr_gcc          %{old_path_usr_gcc}  ...
...
compile options: ...
--enable-languages=%{gcc_enable_languages}%{gcc_enable_languages_java}


%prep

echo "Info:
version:	%{version}
major_minor:	%{major_minor}
major_version:	%{major_version}
"

%if %{compat_link_usr_gnu_bin_cc}
export BAILOUTMESSAGE="\n
\n
***READ THIS***\n
\n
bailing out (%name). Consider removing those symbolic links:\n
  /usr/gnu/bin/cc and /usr/gnu/bin/cpp\n
\n
you can do this with:\n
    pfexec rm /usr/gnu/bin/cc /usr/gnu/bin/cpp\n
\n
or on recent builds, use:\n
    sudo rm /usr/gnu/bin/cc /usr/gnu/bin/cpp\n
\n
that symlink points to the gcc compiler which\n
was an error in the development version of the OS.\n
\n
See also CR 7031722 (Solaris)\n
See also Bug-ID <TBD> (OI)\n
\n
Besides that, remember to initialize your CBE environment\n
before running the pkgtool.\n
Run \"pkgtool\" with these SFE spec files only *after* initializing CBE:\n
   . /opt/dtbld/bin/env.sh\n
   pkgtool build SFEthisspec.spec\n
\n
***READ THIS***\n
\n"

/usr/bin/echo ${BAILOUTMESSAGE}

exit 1
%endif

%setup -q -c -n %{name}-%version


mkdir gcc
#cp -p %{SOURCE2}            gcc/ecj-%{version_ecj}.jar 
#cp -p %{SOURCE2} gcc-%{version}/ecj.jar 
cp -p %{SOURCE2} ecj.jar 

#with 4.3.3 in new directory libjava/classpath/
cd gcc-%{version}/libjava/classpath/
#%patch1 -p1
cd ../../..
cd gcc-%{version}
%if %with_handle_pragma_pack_push_pop
%patch2 -p1
%endif

%if %( expr %{major_minor} '>=' 4.7 '&' %{major_minor} '<=' 4.8 )
%patch3 -p1
%endif

#note: up to gcc 4.7 we apply patch5 here, for higher version we apply patch5 *after* the large batch of solaris userland patches (see below!)
#gcc 4.8, 4.9, 5 is handled after applying userland gate patches below
#we have patch5 in separate patchfiles for each 4.x version
#here: userland patches not yet applied
%if %( expr %{major_minor} '>=' 4.4 '&' %{major_minor} '<' 4.8 )
%patch5 -p1
%endif

##TODO## check versions which apply. bug says 4.3.3 is not, but 4.6.0 is
#fix maybe in 4.7.x
%if %( expr %{major_minor} '>=' 4.4 '&' %{major_minor} '<' 4.7 )
%patch10 -p1
%endif

#only 4.8.5 - gcc-11-remove-obsolete-assertion-on-the-CFA-register-_ported_to_4.8.x_gcc_bug_230249.diff
%if %( expr %{major_minor} '=' 4.8 )
%patch11 -p1
%endif

#For gcc 4.8.5 on Solaris 11 and Solaris 12 (already have updated/fixed header files)
%if %( expr %{solaris11} '+' %{solaris12} '>=' 1 '&' %{major_minor} '=' 4.8 )
%patch12 -p1
%endif

##get rid of these options to (Solaris) LD
#gsed -i.bak -e 's/-fno-exceptions//g' -e 's/-fno-rtti//g' -e 's/-fasynchronous-unwind-tables//g' configure.ac configure

##TODO## enhance: use padded numbers eventually - same in %prep
%if %( expr %{solaris11} '+' %{solaris12} '>=' 1 '&' %{major_minor} '=' 4.8 )
#apply patches imported from userland gate, as S11.2 and S12 need them
#%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
##TODO## see above %patch109 -p1
%patch110 -p1
#%{solaris11} '+' %{solaris12} '&' %{major_minor} '=' 4.8
%endif


%if %( expr %{solaris11} '+' %{solaris12} '>=' 1 '&' %{major_minor} '=' 4.9 )
%patch200 -p0
%patch201 -p0
%patch202 -p0
%patch203 -p0
%patch204 -p0
#there is no 205
%patch206 -p0
%patch207 -p0
%patch208 -p0
%patch209 -p0
%patch210 -p0
%patch211 -p0
%patch212 -p0
%patch213 -p0
%patch214 -p0
%patch215 -p0
%patch216 -p0
%patch217 -p0
%patch218 -p0
%patch219 -p0
%patch220 -p0
%patch221 -p0
%patch222 -p0
%patch223 -p0
%patch224 -p0
%patch225 -p0
%patch226 -p0
%if %( expr %{majorminormicro_padded_number4}.0 '<=' 000400090003.0 )
%patch227 -p0
%endif
#%{solaris11} '+' %{solaris12} '>=' 1 '&' %{major_minor} '=' 4.9
%endif



%if %( expr %{solaris11} '+' %{solaris12} '>=' 1 '&' %{major_minor} '=' 5.3 )
%patch301 -p0
%patch302 -p0
%patch303 -p0
%patch304 -p0
%patch306 -p0
%patch308 -p0
#%{solaris11} '+' %{solaris12} '>=' 1 '&' %{major_minor} '=' 5.3
%endif

#note: up to gcc 4.8 we apply patch5 before the large userland batch, with gcc 4.9 we apply patch5 right *after* the large batch of solaris userland patches
#here: userland patches already applied

##TODO## if in need of 4.8.x series, test if same patch is needed on s1104 / s12
%if %( expr %{major_minor} '>=' 4.9 '&'  %{major_minor} '<' 5.0 )
# gcc49-501-boehmm-gc-os_dep.c-dirty-fix-for-procfs-large-file-env.diff
%patch501 -p1
#s1104 stopped providing old_procfs.h, need to use new interface
# gcc49-502-boehm-gc-os_dep.c-avoid-procfs-ioctl.diff
%patch502 -p1
%endif


##TODO## make a switch for pkgtool kommand line to override _OLD_COMPAT_LIBDIR_ to be enabled or disabled

#adding old compatibility search path to LINK_LIBGCC_SPEC *if* we are below gcc 5.x. 
#By default we have changerd _prefix to /usr/gcc-sfe/ for the compiler+runtime, old binaries use gccruntime in /usr/gcc/lib/
#only if compiler is lower then 5.x, then add the old compat path /usr/gcc/lib to LINK_LIBGCC_SPEC (appears in RPATH / RUNPATH)
#for gcc 4.x the compat switch is by default on, then we get /usr/gcc/lib added to libpath, so new binaries compiled by rebuilt compiler 4.8 or 4.9 so search gcc-runtime in /usr/gcc/lib as well. This rebuilt compiler is stored in /usr/gcc-sfe/lib. Think of a binary compiled on one machine with rebuild gcc in /usr/gcc-sfe/ but target machine has older gccruntime package with gccruntime libs linked from /usr/gcc/lib to /usr/gcc/major.minor/lib and not in /usr/gcc-sfe/lib.
#variable only used if compiler is 4,8, 4.9 or 5.x an later)
#KKKFFJJSSLL
##remove## %if %( expr %{major_minor} '>=' 5.0 )
%if !%{old_path_usr_gcc}
#gcc5 has no old installs, so no compat gcc runtime libdir is necessary _OLD_COMPAT_LIBDIR_="" as gcc5runtime package is necessary
#and all SFE-gcc 5.x will live in /usr/gcc-sfe/ since first appearance, therefore we can't use old gcc runtime files anyways (all below version 5.x)
%define old_compat_libdir 
#_OLD_COMPAT_LIBDIR_=""
%else
#help new binaries built by new/relocated /usr/gcc-sfe/major.minor/bin/gcc of version 4.8 or gcc 4.9 on old target system find old gccruntime 4.8 or 4.9
%define old_compat_libdir :/usr/gcc/lib
#_OLD_COMPAT_LIBDIR_=":/usr/gcc/lib"
%endif
#END KKKFFJJSSLL


#ABABABSGSGSGSHSH
%if %( expr %{major_minor} '>=' 4.8 )
#4.8, 4.9, 5.x has now patch5 reworked to new patching method. 
#we have one patch for AMD64 and SPARC and which adds prepared placeholders for LINK_LIBGCC_SPEC. This is now replaced with locations with gccruntime libdirs.
%patch5 -p1

#                                                         /usr/gcc-sfe /5                /lib/ARCH64_SUBDIR    :/usr/gcc-sfe /lib/ARCH64_SUBDIR    :/usr/gcc/lib            /ARCH64_SUBDIR
#                                                         /usr/gcc-sfe /5                /lib:/usr/gcc-sfe/lib :/usr/gcc/lib
#ARCH64_SUBDIR gets replaced by gcc macros

##TODO## colon                                                                                                 : -->> is now in the variable _OLD_COMPAT_LIBDIR_
  # -e '/LINK_LIBGCC_SPEC/ s?@@_LINK_LIBGCC_SPEC_ARCH64_@@?'%{_prefix}/${_GCCVERSIONPATH_}'/lib/" ARCH64_SUBDIR ":'%{_prefix}'/lib/" ARCH64_SUBDIR "'${_OLD_COMPAT_LIBDIR_}'/" ARCH64_SUBDIR "?g' \
  # -e '/LINK_LIBGCC_SPEC/ s?@@_LINK_LIBGCC_SPEC_ARCH32_@@?'%{_prefix}/${_GCCVERSIONPATH_}'/lib:'%{_prefix}'/lib'${_OLD_COMPAT_LIBDIR_}'?g' \
#      [7]  FINI            0xdf020   
#      [8]  SONAME          0x3c930   libstdc++.so.6
#      [9]  RUNPATH         0x3c9da   /usr/4.9/lib:/lib:/usr/gcc/lib
#     [10]  RPATH           0x3c9da   /usr/4.9/lib:/lib:/usr/gcc/lib

echo "prefix/lib		%{_prefix}/lib/"
echo "_prefix_usr_gcc/lib	%{_prefix_usr_gcc}/lib/"
echo "old_compat_libdir		%{old_compat_libdir}"
echo "old_path_usr_gcc		%{old_path_usr_gcc}"


gsed -i.bak.LINK_LIBGCC_SPEC \
  -e '/LINK_LIBGCC_SPEC/ s?@@_LINK_LIBGCC_SPEC_ARCH64_@@?%{_prefix}/lib/" ARCH64_SUBDIR ":%{_prefix_usr_gcc}/lib/" ARCH64_SUBDIR "'\
%if %{old_path_usr_gcc}
'%{old_compat_libdir}/" ARCH64_SUBDIR "?g'\
%else
'?g'\
%endif
  -e '/LINK_LIBGCC_SPEC/ s?@@_LINK_LIBGCC_SPEC_ARCH32_@@?%{_prefix}/lib:%{_prefix_usr_gcc}/lib%{old_compat_libdir}?g' \
  -e '/define MD_EXEC_PREFIX/ s?/usr/ccs/bin?/usr/bin?' \
  gcc/config/sol2.h




echo "==="
echo "diff -u gcc/config/sol2.h.bak.LINK_LIBGCC_SPEC gcc/config/sol2.h"
diff -u gcc/config/sol2.h.bak.LINK_LIBGCC_SPEC gcc/config/sol2.h || true
echo "==="


%endif
#END ABABABSGSGSGSHSH


%build
CPUS=%{_cpus_memory}

echo "debug _totalmemory: %{_totalmemory}"
echo "debug CPUS: $CPUS"

#perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash -x," `find . -type f -name configure -exec grep -q "^#\!.*/bin/sh" {} \; -print`
#perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash -x," `find . -type f -name configure -exec grep -q "^#\!.*/bin/sh" {} \; -print`

cd gcc

##TODO## fix NLS
%if %( expr %{major_minor} '>=' 5.4 )
%define build_l10n 0
%endif

#gcj / gcjh / libgcj.so don't propperly link agains libiconv. Try iconv from libc. Older OS might need --with-libiconv-prefix=/usr/gnu
%if %build_l10n
nlsopt='--enable-nls --without-libiconv-prefix'
%else
nlsopt='--disable-nls --without-libiconv-prefix'
%endif

#%define build_gcc_with_gnu_ld 0
#saw problems. 134 did compile, OI147 stopped with probably linker errors
##TODO## research which osbuild started to fail, adjust the number below
#%if %( expr %{osbuild} '>=' 1517)
#paused#, use individual setting %define build_gcc_with_gnu_ld 0

##TODO## if ld-wapper is not found ($LD is empty), add one temporarily and specify 
#options like this:  exec /usr/bin/ld -z ignore -Bdirect -z combreloc "${@}"
#build with gnu ld if requested or on OI hipster
%if %build_gcc_with_gnu_ld
echo "build_gcc_with_gnu_ld: %build_gcc_with_gnu_ld"
export LD=/usr/bin/ld
export LD_FOR_BUILD=/usr/bin/gld
export LD_FOR_TARGET=/usr/bin/ld
#%define _ldflags
%else
export LD=/usr/bin/ld
%endif

#around 4.8, configure ignores disabling -fno-exception
#create a filter script to remove -fno-exceptions from linker calls
##cat - > ld_filtered << EOF--
###!/bin/ksh
##/usr/bin/ld \`echo \${@} | sed -e 's/-fno-exceptions//g' -e 's/-fno-rtti//g' -e 's/-fasynchronous-unwind-tables//g\`
##EOF--
##chmod a+rx ld_filtered
##export LD=`pwd`/ld_filtered

%if %SUNWbinutils 
export LD="/usr/bin/ld"
%endif

%define configure_binutils --with-build-time-tools=/usr/sfw --with-as=/usr/sfw/bin/gas --with-gnu-as

%if %SFEbinutils_gpp
#using only at compile time the GNU linker from our binutils
export LD="/usr/g++/bin/ld"
%endif

#defaults:
export CC=cc
export CXX=CC
#maybe needed for stone old studio compilers, commented for reference
#export CPP="cc -E -Xs"
export CPP="cc -E"

%if %( expr %{solaris11} '|' %{oihipster} '|' %{openindiana} )
#using gcc-3 because running into problems with -fno-exception, as the Studio compiler would pass that to Solaris linker which doesn't understand
#export CC=/usr/sfw/bin/gcc
#export CXX=/usr/sfw/bin/g++
export CC=gcc
export CXX=g++
unset CPP
#solaris11 solaris12 oihipster openindiana
%endif

%if %( expr %{s110400} )
export CC=gcc
export CXX=g++
unset CPP
%endif

#R151012 is missing the gcc-3 package, use gcc48 instead
%if %{omnios}
export CC=$( ls -1 /opt/gcc-4.8.*/bin/gcc | tail -1 )
export CXX=$( ls -1 /opt/gcc-4.8.*/bin/g++ | tail -1 )
unset CPP
#OmniOS
%endif

#S11, gcc 3.4.3 is not able to do libiconv for static libstdc++.a
##TODO## try with newer gcc
%if %( expr %{major_minor} '>=' 5.0 )
export CC=gcc
export CXX=g++
unset CPP
#%{major_minor} '>=' 5.0
%endif

#set the bootstrap compiler optionally on the command line
#is 1 if variable is set
%if 0%{?gcc_boot_cc:1}
#yes
export CC=%{gcc_boot_cc}
%if %{!?gcc_boot_cxx:1}
 echo "gcc_boot_cxx needs to be set to C++ compiler!"
 echo "you may need as well need define cc_is_gcc 1 in case of GCC/G++"
 exit 1
%endif
export CXX=%{gcc_boot_cxx}
%else
#no
%endif


export CFLAGS="-O"
export CONFIG_SHELL=/usr/bin/ksh


export BOOT_CFLAGS="-Os %gcc_picflags %gnu_lib_path"

%if %build_gcc_with_gnu_ld
export BOOT_CFLAGS="$BOOT_CFLAGS"
%else
export BOOT_CFLAGS="$BOOT_CFLAGS -Xlinker -i"
%endif

#related: https://gcc.gnu.org/bugzilla/show_bug.cgi?id=59788
#Bug 59788 - Mixing libc and libgcc_s unwinders on 64-bit Solaris 10+/x86 breaks EH (exception handling)
export BOOT_LDFLAGS="-zinterpose %_ldflags -R%{_prefix}/lib %gnu_lib_path"


# for target libraries (built with bootstrapped GCC)
export CFLAGS_FOR_TARGET="-zinterpose -O2 %gcc_picflags"
#export CXXFLAGS_FOR_TARGET=""

%if %build_gcc_with_gnu_ld
%else
export CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET -Xlinker -i"
%endif

##TODO## fix this to be an optional switch: add extra fallback runpath to find gcc_runtime
export LDFLAGS_FOR_TARGET="-zinterpose %_ldflags"
#find mpfr in  %gnu_lib_path
export LDFLAGS="-zinterpose %_ldflags %gnu_lib_path"


#Set this always
export LD_FOR_TARGET=/usr/bin/ld

# For pod2man
export PATH="$PATH:/usr/perl5/bin"

echo "cleanup **CFLAGS/GXXFLAGS/LDFLAGS from -m32 and -m64 switches"
#this came in with include/base.inc changed in case a compiler defaults to creating 64-bit objects
#to fix 32-bit builds, we've added to regular optflags and ldflags "-m32"
export CFLAGS_FOR_TARGET=$(  echo ${CFLAGS_FOR_TARGET}  | sed -e 's/-m32//g' -e 's/-m64//g' )
export LDFLAGS_FOR_TARGET=$( echo ${LDFLAGS_FOR_TARGET} | sed -e 's/-m32//g' -e 's/-m64//g' )
export BOOT_CFLAGS=$(  echo ${BOOT_CFLAGS}  | sed -e 's/-m32//g' -e 's/-m64//g' )
export BOOT_LDFLAGS=$( echo ${BOOT_LDFLAGS} | sed -e 's/-m32//g' -e 's/-m64//g' )

##%if %{omnios}
###disable checks for -fvisibility, as they may fail on KVMed OmniOS guest
##echo "disabling on OmniOS check for -fvisibility attribute. It may fail on KVMed OmniOS guest."
##gsed -i.bak.disable.visibibilty.check.on.omnios -e '/CFLAGS="$CFLAGS -Werror"/ s/CFLAGS/#dont fail on KVMed OmniOS CFLAGS/' ../gcc-%{version}/libstdc++-v3/configure
##gsed -i.bak.disable.visibibilty.check.on.omnios -e '/ -Werror -S conftest.c -o conftest.s/ s/-Werror//' ../gcc-%{version}/libgcc/configure
##%endif

echo "current settings in SFE spec file: (1=yes, 0=no)

version:	%{version}
_prefix:	%{_prefix}
_libdir:	%{_libdir}
_libexecdir:	%{_libexecdir}
_mandir:	%{_mandir}
_infodir:	%{_infodir}

PATH:		$PATH
symlinks in     %{gccsymlinks}

CC:		${CC}
CXX:		${CXX}
CPP:		${CPP}

build java gcj: %{gcj}
languages:      %{gcc_enable_languages}%{gcc_enable_languages_java}
configure options %{gcc_configure_java}
switch cc_is_gcc:	      %{cc_is_gcc}
switch SFEbinutils_gpp:       %SFEbinutils_gpp
switch SUNWbinutils:          %SUNWbinutils
switch build_gcc_with_gnu_ld: %build_gcc_with_gnu_ld
switch SFEgmp:     %SFEgmp    %{SFEgmpbasedir}
switch SFEmpfr:    %SFEmpfr   %{SFEmpfrbasedir}
switch SFElibmpc : %SFElibmpc %{SFElibmpcbasedir}
LD:            ${LD}
LD_FOR_TARGET: ${LD_FOR_TARGET}
" | tee -a SFEgcc.spec.compileinfo

#OmniOS gcc 4.8.1:    ../gcc-4.8.5/configure --prefix=/usr/gcc/4.8 --host i386-pc-solaris2.11 --build i386-pc-solaris2.11 --target i386-pc-solaris2.11 --with-boot-ldflags=-R/usr/gnu/lib --with-gmp=/usr/gnu --with-mpfr=/usr/gnu --with-mpc=/usr/gnu --enable-languages=c,c++ --without-gnu-ld --with-ld=/bin/ld --with-as=/usr/bin/gas --with-gnu-as --with-build-time-tools=/usr/gnu/i386-pc-solaris2.11/bin


../gcc-%{version}/configure			\
	--prefix=%{_prefix}			\
        --libdir=%{_libdir}			\
        --libexecdir=%{_libexecdir}		\
        --mandir=%{_mandir}			\
	--infodir=%{_infodir}			\
        %{configure_binutils}                   \
	--with-ld=$LD_FOR_TARGET                \
	--without-gnu-ld			\
        %{gcc_configure_java} \
	--enable-languages=%{gcc_enable_languages}%{gcc_enable_languages_java} \
	--enable-shared				\
	--disable-static			\
	--enable-decimal-float			\
%if %SFEgmp
	--with-gmp=%{SFEgmpbasedir}             \
%else
        --with-gmp_include=%{_basedir}/include/gmp \
%endif
%if %SFEmpfr
	--with-mpfr=%{SFEmpfrbasedir}           \
%else
        --with-mpfr_include=%{_basedir}/include/mpfr \
%endif
%if %SFElibmpc
	--with-mpc=%{SFElibmpcbasedir}           \
%else
        --with-mpc_include=%{_basedir}/include	\
%endif
%if %omnios
        --target=i386-pc-solaris2.11              \
        --host i386-pc-solaris2.11                \
        --build i386-pc-solaris2.11               \
        --target i386-pc-solaris2.11              \
        --with-boot-ldflags=-R/usr/gnu/lib        \
        --with-build-time-tools=/usr/gnu/i386-pc-solaris2.11/bin \
        --disable-bootstrap                       \
%endif
%if %( expr %{major_minor} '>=' 5.0 )
        --disable-bootstrap                       \
%endif
	$nlsopt                                   \

        #--enable-libstdcxx-visibility            \
        #--target=x86_64-pc-solaris2.1x           \
#g++     -dM -E -x c++ /dev/null 


echo "gmake bootstrap..."
echo "variables:"
echo "		
             BOOT_CFLAGS="$BOOT_CFLAGS"                  \
             BOOT_LDFLAGS="$BOOT_LDFLAGS"                \
             CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET"      \
             CXXFLAGS_FOR_TARGET="$CXXFLAGS_FOR_TARGET"  \
             LDFLAGS_FOR_TARGET="$LDFLAGS_FOR_TARGET"    \
             LD_FOR_BUILD="$LD_FOR_BUILD"                \
             LD_FOR_TARGET="$LD_FOR_TARGET"              \
             LD="$LD"                                    \

"


#on S11, gcc 5.4.0 we run into 
#std::basic_istream<char, std::char_traits<char> >::ignore(int) /localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/src/.libs/libstdc++.a(istream.o)
#std::basic_istream<wchar_t, std::char_traits<wchar_t> >::ignore(int) /localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/src/.libs/libstdc++.a(istream.o)
#try without bootstrap
#try without OSDistro gcc 3.4.3!

#pkgbuild@hipster> LD_LIBRARY_PATH=/localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/src/.libs LD_DEBUG=files /localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/./prev-gcc/xg++ -zinterpose -B/localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/./prev-gcc/ -B/usr/gcc-sfe/5/i386-pc-solaris2.11/bin/ -nostdinc++ -B/localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/src/.libs -B/localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/libsupc++/.libs  -I/localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/include/i386-pc-solaris2.11  -I/localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/include  -I/localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc-5.4.0/libstdc++-v3/libsupc++ -L/localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/src/.libs -L/localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/libsupc++/.libs   -Os -fPIC -DPIC -L/usr/gnu/lib -R/usr/gnu/lib -DIN_GCC    -fno-exceptions -fno-rtti -fasynchronous-unwind-tables -W -Wall -Wno-narrowing -Wwrite-strings -Wcast-qual -Wmissing-format-attribute -Woverloaded-virtual -pedantic -Wno-long-long -Wno-variadic-macros -Wno-overlength-strings   -DHAVE_CONFIG_H -static-libstdc++ -static-libgcc -zinterpose   -Wl,-zignore -Wl,-zcombreloc -Wl,-Bdirect  -R/usr/gcc-sfe/5/lib -L/usr/gnu/lib -R/usr/gnu/lib -o cc1 c/c-lang.o c-family/stub-objc.o attribs.o c/c-errors.o c/c-decl.o c/c-typeck.o c/c-convert.o c/c-aux-info.o c/c-objc-common.o c/c-parser.o c/c-array-notation.o c-family/c-common.o c-family/c-cppbuiltin.o c-family/c-dump.o c-family/c-format.o c-family/c-gimplify.o c-family/c-lex.o c-family/c-omp.o c-family/c-opts.o c-family/c-pch.o c-family/c-ppoutput.o c-family/c-pragma.o c-family/c-pretty-print.o c-family/c-semantics.o c-family/c-ada-spec.o c-family/c-cilkplus.o c-family/array-notation-common.o c-family/cilk.o c-family/c-ubsan.o i386-c.o sol2-c.o default-c.o   cc1-checksum.o libbackend.a main.o  libcommon-target.a libcommon.a ../libcpp/libcpp.a ../libdecnumber/libdecnumber.a libcommon.a ../libcpp/libcpp.a  /usr/gnu/lib/libiconv.so -R/usr/gnu/lib ../libbacktrace/.libs/libbacktrace.a ../libiberty/libiberty.a ../libdecnumber/libdecnumber.a   -L/usr/gnu/lib -L/usr/gnu/lib -L/usr/gnu/lib -lmpc -lmpfr -lgmp   -L../zlib -lz 2>&1 | grep libstd".*"\.so                                                                
#12241: file=libstdc++.so.6;  needed by /packagepool/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-gcc/xg++
#12241: file=/localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/src/.libs/libstdc++.so.6  [ ELF ]; generating link map
#12241: file=/localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/src/.libs/libstdc++.so.6;  analyzing  [ RTLD_LAZY RTLD_GLOBAL RTLD_WORLD RTLD_NODELETE ]
#12241: file=libgcc_s.so.1;  needed by /localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/src/.libs/libstdc++.so.6
#12241: file=libc.so.1;  needed by /localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/src/.libs/libstdc++.so.6
#12243: file=libstdc++.so.6;  needed by /packagepool/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-gcc/collect2
#12243: file=/localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/src/.libs/libstdc++.so.6  [ ELF ]; generating link map
#12243: file=/localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/src/.libs/libstdc++.so.6;  analyzing  [ RTLD_LAZY RTLD_GLOBAL RTLD_WORLD RTLD_NODELETE ]
#12243: file=libgcc_s.so.1;  needed by /localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/src/.libs/libstdc++.so.6
#12243: file=libc.so.1;  needed by /localhomes/sfe/packages/BUILD/SFEgcc-5.4.0/gcc/prev-i386-pc-solaris2.11/libstdc++-v3/src/.libs/libstdc++.so.6
#pkgbuild@hipster> echo $?
#0

# %if %(expr %{omnios} )
%if %(expr %{omnios} '|'  %{major_minor} '>=' 5.0 )
#libgfortran accidentially detects mkostemp and this doesn't exist - gcc 5.4.x
#####mkostemp muss auf gcc/i**/libgfortran/config.h auf 0 gesetzt werden
#####alternativ heruaspatchen aus unix.c
export       CFLAGS_FOR_TARGET="-DHAVE_MKOSTEMP=0 $CFLAGS_FOR_TARGET"
gmake -j$CPUS           \
%else
gmake -j$CPUS bootstrap \
%endif
             BOOT_CFLAGS="$BOOT_CFLAGS"                  \
             BOOT_LDFLAGS="$BOOT_LDFLAGS"                \
             CFLAGS_FOR_TARGET="$CFLAGS_FOR_TARGET"      \
             CXXFLAGS_FOR_TARGET="$CXXFLAGS_FOR_TARGET"  \
             LDFLAGS_FOR_TARGET="$LDFLAGS_FOR_TARGET"    \
             LD_FOR_BUILD="$LD_FOR_BUILD"                \
             LD_FOR_TARGET="$LD_FOR_TARGET"              \
             LD="$LD"                                    \

#sanity check
%if %{omnios}
grep "0" *solaris2*/libstdc++-v3/include/stamp-visibility \
   *solaris2*/amd64/libstdc++-v3/include/stamp-visibility \
   && echo "-fvisibility not enabled. Please investigate" && exit 1
%endif


%install
rm -rf $RPM_BUILD_ROOT

cd gcc
gmake install DESTDIR=$RPM_BUILD_ROOT

cd $RPM_BUILD_ROOT%{_prefix}
ln -s share/man man

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

#link runtime libs, for compatibility
#note: links only "basename_of_lib", then "major"-number version libs
#leaves out "minor" and "micro" version libs, they are normally not
#to be linked by userland binaries (runtime linking, see output of "ldd binaryname")

for SYMLINKTARGET in %{gccsymlinks}
do
  # make from /usr/gcc-sfe this offset ../../
  #OFFSET=$( echo "$SYMLINKTARGET" | sed -e 's?/$??' -e 's?\w*/?../?g' -e 's?\w*$??' -e 's?/$??' )
  OFFSET=$( echo "$SYMLINKTARGET" | sed -e 's?/$??' -e 's?[A-z0-9_-]*/?../?g' -e 's?[A-z0-9_-]*$??' -e 's?/$??' )
  # with CWD /usr/gcc/lib, an example is ../../gcc/%major_minor/lib/libgcc_s.so.1
  mkdir -p $RPM_BUILD_ROOT/$SYMLINKTARGET/lib
  #cd $RPM_BUILD_ROOT/$SYMLINKTARGET/lib
  cd $RPM_BUILD_ROOT/$SYMLINKTARGET
  # gcc_symlinks_pattern includes bin/ and lib/ and directory matched by pattern
  for filepath in %{gcc_symlinks_pattern} lib/libgcc_s.so.1 lib/libgcc_s.so lib/libgfortran.so.3 lib/libgfortran.so lib/libgomp.so.1 lib/libgomp.so lib/libobjc_gc.so.2 lib/libobjc_gc.so lib/libobjc.so.2 lib/libobjc.so lib/libssp.so.0 lib/libssp.so lib/libstdc++.so.6 lib/libstdc++.so lib/libquadmath.so lib/libquadmath.so.0
  do
  DIR=$( dirname $RPM_BUILD_ROOT/$SYMLINKTARGET/$filepath )
  [ -d ${DIR} ] || mkdir -p ${DIR}
  [ -r ${DIR}/$OFFSET/%{gccdir}/%major_minor/$filepath ] && ln -s $OFFSET/%{gccdir}/%major_minor/$filepath $filepath
  done #for file
done #for SYMLINKTARGET

#link arch runtime libs for compatibility
%ifarch amd64 sparcv9
for SYMLINKTARGET in %{gccsymlinks}
do
  # make from /usr/gcc this offset ../../
  #OFFSET=$( echo "$SYMLINKTARGET" | sed -e 's?/$??' -e 's?\w*/?../?g' -e 's?\w*$??' -e 's?/$??' )
  OFFSET=$( echo "$SYMLINKTARGET" | sed -e 's?/$??' -e 's?[A-z0-9_-]*/?../?g' -e 's?[A-z0-9_-]*$??' -e 's?/$??' )
  # with CWD /usr/gcc/lib, an example is ../../gcc/%major_minor/lib/libgcc_s.so.1
  mkdir -p $RPM_BUILD_ROOT/$SYMLINKTARGET/lib/%{_arch64}
  #cd $RPM_BUILD_ROOT/$SYMLINKTARGET/lib/%{_arch64}
  cd $RPM_BUILD_ROOT/$SYMLINKTARGET
  # gcc_symlinks_pattern_arch64 matches e.g. lib/%{_arch64}/libgij.so
  for filepath in %{gcc_symlinks_pattern_arch64} lib/%{_arch64}/libgcc_s.so.1 lib/%{_arch64}/libgcc_s.so lib/%{_arch64}/libgfortran.so.3 lib/%{_arch64}/libgfortran.so lib/%{_arch64}/libgomp.so.1 lib/%{_arch64}/libgomp.so lib/%{_arch64}/libobjc.so.2 lib/%{_arch64}/libobjc.so lib/%{_arch64}/libssp.so.0 lib/%{_arch64}/libssp.so lib/%{_arch64}/libstdc++.so.6 lib/%{_arch64}/libstdc++.so lib/%{_arch64}/libquadmath.so lib/%{_arch64}/libquadmath.so.0
  do
  DIR=$( dirname $RPM_BUILD_ROOT/$SYMLINKTARGET/$filepath )
  [ -d ${DIR} ] || mkdir -p ${DIR}
  #note add one ../ for %{_arch64}
  [ -r ${DIR}/$OFFSET/../%{gccdir}/%major_minor/$filepath ] && ln -s $OFFSET/../%{gccdir}/%major_minor/$filepath $filepath
  done #for file
done #for SYMLINKTARGET
%endif

for SYMLINKTARGET in %{gccsymlinks}
do
  # make from /usr/gcc this offset ../../
  #OFFSET=$( echo "$SYMLINKTARGET" | sed -e 's?/$??' -e 's?[\w-]*/?../?g' -e 's?[\w-]*$??' -e 's?/$??' )
  OFFSET=$( echo "$SYMLINKTARGET" | sed -e 's?/$??' -e 's?[A-z0-9_-]*/?../?g' -e 's?[A-z0-9_-]*$??' -e 's?/$??' )
  # with CWD /usr/gcc/lib, an example is ../../gcc/%major_minor/lib/libgcc_s.so.1
  mkdir -p $RPM_BUILD_ROOT/$SYMLINKTARGET/bin
  #cd $RPM_BUILD_ROOT/$SYMLINKTARGET/bin
  cd $RPM_BUILD_ROOT/$SYMLINKTARGET
# leave out sfw gcc 3.x.x uses this name already ln -s ../../gcc/%major_minor/bin/cpp
  for filepath in bin/c++ bin/g++ bin/gcc bin/cpp bin/gcov bin/gfortran
  do
  DIR=$( dirname $RPM_BUILD_ROOT/$SYMLINKTARGET/$filepath )
  [ -d ${DIR} ] || mkdir -p ${DIR}
  [ -r ${DIR}/$OFFSET/%{gccdir}/%major_minor/$filepath ] && ln -s $OFFSET/%{gccdir}/%major_minor/$filepath $filepath
  done #for file
done #for SYMLINKTARGET

#for a test, keep static files like /usr/gcc/4.8/lib/libssp_nonshared.a libssp.a libitm.a libgomp.a libatomic.a 
#rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
%ifarch amd64 sparcv9
#rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*.la
%endif

#would ldd find the map files for _arch64 even if they are only in %{_libdir} ?
%if %( expr %{major_minor} '>=' 4.9 )
cp -p $RPM_BUILD_ROOT%{_libdir}/clearcap.map $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/clearcap.map
cp -p $RPM_BUILD_ROOT%{_libdir}/libgcc-unwind.map $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/libgcc-unwind.map
%endif

# fix pkgconfig for 64-Bit to show the right libdir
#s11175 sfe /localhomes/tom/spec-files-extra cat /usr/gcc-sfe/4.9/lib/amd64/pkgconfig/libgcj-4.9.pc 
#libdir=/usr/gcc-sfe/4.9/lib
#Description: libgcj
#Version: 4.9.4
#Libs: -L${libdir} -lgcj
#Cflags: -I${includedir}

ls -1 $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/pkgconfig/libgcj-*.pc && \
  gsed -i -e '/^libdir=/ s?$?/%{_arch64}?' \
          -e '/^Description/ s?$? %{_arch64}?' \
          $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/pkgconfig/libgcj-*.pc && \

%clean
rm -rf $RPM_BUILD_ROOT

%post -n SFEgcc
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gcc.info cpp.info gccint.info cppinternals.info gccinstall.info gfortran.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun -n SFEgcc
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gcc.info cpp.info gccint.info cppinternals.info gccinstall.info gfortran.info' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE



#SFEgcc-%{majorminornumber}, other packages see below

%files -n SFEgcc-%{majorminornumber}
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%{_prefix}/man
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gcc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man7
%{_mandir}/man7/*.7
%{_infodir}
%{_includedir}

%dir %attr (0755, root, sys) %{_datadir}/gcc-%{version}
%dir %attr (0755, root, sys) %{_datadir}/gcc-%{version}/python
%dir %attr (0755, root, sys) %{_datadir}/gcc-%{version}/python/libstdcxx
%dir %attr (0755, root, sys) %{_datadir}/gcc-%{version}/python/libstdcxx/v6
%{_datadir}/gcc-%{version}/python/libstdcxx/v6/printers.py
%{_datadir}/gcc-%{version}/python/libstdcxx/v6/__init__.py
%{_datadir}/gcc-%{version}/python/libstdcxx/__init__.py
#%if %( test -f RPM_BUILD_ROOT/%{_datadir}/gcc-%{version}/python/libstdcxx/v6/xmethods.py && echo 1 || echo 0 )
##TODO## which version brought us the file xmethods.py
%if %( expr %{major_minor} '>=' 5.0 )
%{_datadir}/gcc-%{version}/python/libstdcxx/v6/xmethods.py
%endif



%files -n SFEgccruntime-%{majorminornumber}
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.spec
%{_libdir}/lib*.a
%if %( expr %{major_minor} '>=' 4.9 )
%{_libdir}/clearcap.map
%{_libdir}/libgcc-unwind.map
%endif
%if %{gcj}
%{_libdir}/security/classpath.security
%{_libdir}/logging.properties
%{_libdir}/pkgconfig/libgcj-*.pc
%{_libdir}/gcj-*/libjvm.so
%{_libdir}/gcj-*/classmap.db
%{_libdir}/gcj-*/libjvm.la
%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/java/libgcj-4.9.3.jar
#%{_datadir}/java/libgcj-tools-4.9.3.jar
%{_datadir}/java/libgcj-%{version}.jar
%{_datadir}/java/libgcj-tools-%{version}.jar
%dir %attr (0755, root, sys) %{_datadir}/gcc-%{version}
%dir %attr (0755, root, sys) %{_datadir}/gcc-%{version}/python
%{_datadir}/gcc-*/python/libjava/classfile.py
%{_datadir}/gcc-*/python/libjava/aotcompile.py
%endif


%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/lib*.spec
%{_libdir}/%{_arch64}/lib*.a
%if %( expr %{major_minor} '>=' 4.9 )
%{_libdir}/%{_arch64}/clearcap.map
%{_libdir}/%{_arch64}/libgcc-unwind.map
%endif
%if %{gcj}
%{_libdir}/%{_arch64}/pkgconfig/libgcj-*.pc
%{_libdir}/%{_arch64}/security/classpath.security
%{_libdir}/%{_arch64}/logging.properties
%{_libdir}/%{_arch64}/gcj-*/libjvm.la
%{_libdir}/%{_arch64}/gcj-*/libjvm.so
%{_libdir}/%{_arch64}/gcj-*/classmap.db
%endif
%endif


%if %symlinktarget1enabled
%files -n SFEgcc
%defattr (-, root, bin)
%{symlinktarget1path}/bin
%files -n SFEgccruntime
%defattr (-, root, bin)
#avoid catching pkgconfig directory
%{symlinktarget1path}/lib/security
%{symlinktarget1path}/lib/lib*so*
%ifarch amd64 sparcv9
#avoid catching pkgconfig directory
%{symlinktarget1path}/lib/%{_arch64}/security
%{symlinktarget1path}/lib/%{_arch64}/lib*so*
%endif
# amd64 sparcv9
%if %{gcj}
%dir %attr (0755, root, other) %{symlinktarget1path}/lib/pkgconfig
%{symlinktarget1path}/lib/gcj-*
%{symlinktarget1path}/lib/logging.properties
%{symlinktarget1path}/lib/libgcj.spec
%{symlinktarget1path}/bin/gcj
%{symlinktarget1path}/bin/grmic
%{symlinktarget1path}/bin/gkeytool
%{symlinktarget1path}/bin/gorbd
%{symlinktarget1path}/bin/grmid
%{symlinktarget1path}/bin/gjavah
%{symlinktarget1path}/bin/jv-convert
%{symlinktarget1path}/bin/gjar
%{symlinktarget1path}/bin/gserialver
%{symlinktarget1path}/bin/jcf-dump
%{symlinktarget1path}/bin/gij
%{symlinktarget1path}/bin/gtnameserv
%{symlinktarget1path}/bin/gcjh
%{symlinktarget1path}/bin/gnative2ascii
%{symlinktarget1path}/bin/rebuild-gcj-db
%{symlinktarget1path}/bin/gjarsigner
%{symlinktarget1path}/bin/aot-compile
%{symlinktarget1path}/bin/gc-analyze
%{symlinktarget1path}/bin/gappletviewer
%{symlinktarget1path}/bin/grmiregistry
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{symlinktarget1path}/lib/%{_arch64}/pkgconfig
%{symlinktarget1path}/lib/%{_arch64}/gcj-*
%{symlinktarget1path}/lib/%{_arch64}/logging.properties
%endif
# amd64 sparcv9
%endif
# gcj
%endif
# symlinktarget1enabled

%if %symlinktarget2enabled
%files -n SFEgcc
%defattr (-, root, bin)
%{symlinktarget2path}/bin
%files -n SFEgccruntime
%defattr (-, root, bin)
#avoid catching pkgconfig directory
%{symlinktarget2path}/lib/security
%{symlinktarget2path}/lib/lib*so*
%ifarch amd64 sparcv9
#avoid catching pkgconfig directory
%{symlinktarget2path}/lib/%{_arch64}/security
%{symlinktarget2path}/lib/%{_arch64}/lib*so*
%endif
# amd64 sparcv9
%if %{gcj}
%dir %attr (0755, root, other) %{symlinktarget2path}/lib/pkgconfig
%{symlinktarget2path}/lib/gcj-*
%{symlinktarget2path}/lib/logging.properties
%{symlinktarget2path}/lib/libgcj.spec
%{symlinktarget2path}/bin/gcj
%{symlinktarget2path}/bin/grmic
%{symlinktarget2path}/bin/gkeytool
%{symlinktarget2path}/bin/gorbd
%{symlinktarget2path}/bin/grmid
%{symlinktarget2path}/bin/gjavah
%{symlinktarget2path}/bin/jv-convert
%{symlinktarget2path}/bin/gjar
%{symlinktarget2path}/bin/gserialver
%{symlinktarget2path}/bin/jcf-dump
%{symlinktarget2path}/bin/gij
%{symlinktarget2path}/bin/gtnameserv
%{symlinktarget2path}/bin/gcjh
%{symlinktarget2path}/bin/gnative2ascii
%{symlinktarget2path}/bin/rebuild-gcj-db
%{symlinktarget2path}/bin/gjarsigner
%{symlinktarget2path}/bin/aot-compile
%{symlinktarget2path}/bin/gc-analyze
%{symlinktarget2path}/bin/gappletviewer
%{symlinktarget2path}/bin/grmiregistry
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{symlinktarget2path}/lib/%{_arch64}/pkgconfig
%{symlinktarget2path}/lib/%{_arch64}/gcj-*
%{symlinktarget2path}/lib/%{_arch64}/logging.properties
%endif
# amd64 sparcv9
%endif
# gcj
%endif
# symlinktarget2enabled


%if %symlinktarget3enabled
%files -n SFEgcc
%defattr (-, root, bin)
%{symlinktarget3path}/bin
%files -n SFEgccruntime
%defattr (-, root, bin)
#avoid catching pkgconfig directory
%{symlinktarget3path}/lib/security
%{symlinktarget3path}/lib/lib*so*
%ifarch amd64 sparcv9
#avoid catching pkgconfig directory
%{symlinktarget3path}/lib/%{_arch64}/security
%{symlinktarget3path}/lib/%{_arch64}/lib*so*
%endif
# amd64 sparcv9
%if %{gcj}
%dir %attr (0755, root, other) %{symlinktarget3path}/lib/pkgconfig
%{symlinktarget3path}/lib/gcj-*
%{symlinktarget3path}/lib/logging.properties
%{symlinktarget3path}/lib/libgcj.spec
%{symlinktarget3path}/bin/gcj
%{symlinktarget3path}/bin/grmic
%{symlinktarget3path}/bin/gkeytool
%{symlinktarget3path}/bin/gorbd
%{symlinktarget3path}/bin/grmid
%{symlinktarget3path}/bin/gjavah
%{symlinktarget3path}/bin/jv-convert
%{symlinktarget3path}/bin/gjar
%{symlinktarget3path}/bin/gserialver
%{symlinktarget3path}/bin/jcf-dump
%{symlinktarget3path}/bin/gij
%{symlinktarget3path}/bin/gtnameserv
%{symlinktarget3path}/bin/gcjh
%{symlinktarget3path}/bin/gnative2ascii
%{symlinktarget3path}/bin/rebuild-gcj-db
%{symlinktarget3path}/bin/gjarsigner
%{symlinktarget3path}/bin/aot-compile
%{symlinktarget3path}/bin/gc-analyze
%{symlinktarget3path}/bin/gappletviewer
%{symlinktarget3path}/bin/grmiregistry
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{symlinktarget3path}/lib/%{_arch64}/pkgconfig
%{symlinktarget3path}/lib/%{_arch64}/gcj-*
%{symlinktarget3path}/lib/%{_arch64}/logging.properties
%endif
# amd64 sparcv9
%endif
# gcj
%endif
# symlinktarget3enabled


%if %build_l10n
%files -n SFEgcc-l10n
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Apr 17 2018 - Thomas Wagner
- remove (Build)Requires SFElibiconv (especially good for gcj gcjh libgcj-tools.so.15.0.0)
- set CC CXX without full path (now found by $PATH) (S11, OIH, OI)
* Sun Apr  1 2018 - Thomas Wagner
- fix symlink glob for directory gcj-* and libgcj-*.pc
* Fri Mar 16 2018 - Thomas Wagner
- fix typo in symlinktarget3path (s/2/3)
* Sat Feb 18 2018 - Thomas Wagner
- fix directory permissions for /usr/gnu/lib/pkgconfig /usr/gnu/lib/%{_arch64}/pkgconfig
- fix the packaging fix, add gcj supporting files
- improve gsed regex to change /usr/gcc-sfe into ../..
- change symlinktarget1path from /usr/gcc to /usr/gcc-sfe
* Thu Feb 22 2018 - Thomas Wagner
- add Patch502 gcc49-502-boehm-gc-os_dep.c-avoid-procfs-ioctl.diff as s1104 stopped providing old_procfs.h, need to use new interface (S11.4 S12)
* Sun Feb 18 2018 - Thomas Wagner
- set default version 4.9.4 for all osdistro
* Fri Feb 16 2018 - Thomas Wagner
- fix gcj compile/package by using gcj-%{version}-15
- fetch slightly larger .gz file, newer versions only provide .gz or .xz (helps downloads when --define 'version 4.9.4' vs. 7.3.0)
- apply Patch227 gcc49-027-cmath_c99.patch only if =< 4.9.3; - add missing "expr"
- new (Build)Requires for (S11.4) is developer/gcc-5
- new (Build)Requires for (OM) is developer/gcc48 developer/gnu-binutils 
* Mon Jul 31 2017 - Thomas Wagner
- bump to 4.9.4 for OIH
* Sun Feb 27 2017 - Thomas Wagner
- add libgcc-unwind.map, clearcap.map for %{_arch64} into gcc-..-runtime
- fix patch to cmath.h for gcc 4.9.4
* Fri Dec 16 2016 - Thomas Wagner
- fix build of libgomp in 64-bit as change to include/base.inc brought in "-m32" through CFLAGS/LDFLAGS
  filter out any -m32 or -m64 from *FLAGS
* Thu Dec 15 2016 - Thomas Wagner
- add backported fix to 4.8.5 patch11 gcc-11-remove-obsolete-assertion-on-the-CFA-register-_ported_to_4.8.x_gcc_bug_230249.diff
  fixes SFElibx264.spec e.g. version 0.148.0.20160529 -> ./common/osdep.h:261:13: error: 'asm' operand has impossible constraints #define asm __asm__
- add patch12 gcc-12-fixinc.in.patch to stop fixing system headers on S11 and S12 only
* Thu Dec  1 2016 - Thomas Wagner
- fix build libfortran my removing mis-detected HAVE_MKOSTEMP (we have none) (OM)
* Fri Oct 21 2016 - Thomas Wagner
- integrate for gcc 5 series
- relocate compiler to /usr/gcc-sfe/ and provide backwards compatible symlinks only in /usr/gcc/lib and /usr/gcc/bin
- only gcc 4.9 has ecj / gcj
* Fri Apr 22 2016 - Thomas Wagner
- rework patch 007-userlandgate-gcc-sol2.h.patch.modified.diff to no longer interfere with patch5 gcc-05-LINK_LIBGCC_SPEC-4.8.diff
- re-enable patch5 LINK_LIBGCC_SPEC to lookup libgcc_s.so and libstdc++.so.6 in /usr/gcc/<major.minor>/lib first
* Wed Apr  6 2016 - Thomas Wagner
- add java language (default for version >= 4.9)
- add --with-ecj-jar to get ecj1 and wapper
- fetch extra source eclipse java compiler and copy into source tree
* Tue Apr  5 2016 - Thomas Wagner
- add to --enable-languages=java  (only tested on 4.9.3, please test SFEgcc.spec with 4.8.5 as well)
- add patch501 as a temporary fix - gcc49-501-boehmm-gc-os_dep.c-dirty-fix-for-procfs-large-file-env.diff  (probably introduced by adding java)
* Sun Jan  3 2015 - Thomas Wagner
- add support for gcc 4.9.3 
  use: pkgtool --IPS --download  --define 'gcc_version 4.9.3' build-only SFEgcc && pfexec pkg install -v gcc-49 gcc-49-runtime
  ... then export PATH=/usr/gcc/4.9/bin:$PATH to get the new gcc first in the row
- use patch3 only for gcc 4.7 + 4.8 (re-visit later if needed)
- import patches from solaris userland (used for S11 and S12)
- created patch5 for gcc 4.9 (to be applied *after* userland patches)
##TODO## does patch5 work on OI (all) and OmniOS w/ the userland patches not applied?
- changed order for gcc 4.9: patch5 is used *after* the unmodified userland patches (simpler maintenance)
- fix %fies for new linker map files: %{_libdir}/clearcap.map %{_libdir}/libgcc-unwind.map
* Mon Nov 23 2015 - Thomas Wagner
- for a test, keep static files like /usr/gcc/4.8/lib/libssp_nonshared.a libssp.a libitm.a libgomp.a libatomic.a 
* Mon Nov 16 2015 - Thomas Wagner
- import patches from userland gate, as they are needed for S11.2 and S12 with enhanced c++ system headers
  and only apply them on Solaris 11.2 and S12! Patch100 to Patch110, rework patch for sol2.h
- include buildparameter.inc and use CPUS=%{_cpus_memory}
- build with /usr/sfw/bin/gcc on S11 (studio w/ need __STDC__ or get arg-count error getopt_long )
- BuildRequires: developer/gcc-3 (S11 S12 OIH OI)
- BuildRequires: developer/gcc48 developer/gnu-binutils (OM)
- add testing switches to set bootstrap compiler on command line --define 'gcc_boot_cc /usr/usethis/bin/gcc' --define 'gcc_boot_cxx /usr/usethis/bin/g++' 
- lots of switches to compile in OmniOS fine and including visibility-features propperly
- set the distro independent default_version to 4.8.5
* Wed Aug  5 2015 - Thomas Wagner
- add symlink to cpp
* Tue Aug  4 2015 - Thomas Wagner
- initialize gccsymlinks[123] in any case
- BuildRequires: developer/gcc-3 (S12, OIH)
- fix logic for --define 'gcc_version 4.x.y'
* Mon Aug  3 2015 - Thomas Wagner
- bump to 4.8.5 for (S12, OIH, OM) only
- prepare for OIHipster (OIH)
- rework finding a suitable compiler for bootstrapping gcc (S12, OM)
* Fri Feb 27 2015 - Thomas Wagner
- re-introduce for 4.8: patch5 gcc-05-LINK_LIBGCC_SPEC-4.8.diff
  to try avoiding osdistro provided /usr/lib/libgcc_s.so and /usr/lib/libstdc++.so.6
- use OmniOs's binutils (OM)
- use gcc-3 on OmniOS for fix getopt_long (OM)
* Mon Feb  2 2015 - Thomas Wagner
- ld-wrapper is wrong, use --with-ld=/usr/bin/ld
- move defines for binutils to get major_minor defines before, fix expr syntax
* Fri Jan 23 2015 - Thomas Wagner
- set gnu ld to off (again), or get gnu linker called and fail to understand Solaris linker switches
- default to SUNWbinutils
- bump to 4.8.4
- require bash only for S10, set SFEbinutils_gpp 1 for %{openindiana} & %{major_minor} >= 4.7 (OI, TODO: hipster)
- on solaris12 use /usr/sfw/bin/gcc (3.x.x) of get with studio -fno-exceptions passed to the linker (fails)
- fix syntax errors %if around *binutils for configure
* Mon Apr 21 2014 - Thomas Wagner
- exclude BuildRequires SUNWpostrun on OmniOS (OM)
- rename variables SFEbinutils -> SFEbinutils_gpp
- bump to 4.8.3
* Sat Dec  7 2013 - Thomas Wagner
- %include osdistro.inc
* Thu Oct 24 2013 - Thomas Wagner
- add -zinterpose to gcc runtime libraries.
  NOTE: recompile all your libs and binaries working with g++
  code to get this test succeed:
  elfedit -re 'dyn:' yourlib_or_binary  -->> no LAZY for gcc-runtime_libs
  libgcc_s.so and libstdc++.so.6, see setting INTERPOSE for FLAG1
  eliminates binding libc C++ calls *before* gcc runtime, avoids breaking c++
  exception handling for instance
* Sun Nov 10 2013 - Milan Jurik
- fix l10n IPS package name
* Sat Sep 28 2013 - Milan Jurik
- bump to 4.6.4
* Sun Feb 24 2013 - Logan Bruns <logan@gedanken.org>
- switch back to sun ld for gcc 4.7 but require SFEbinutils (for 4.7 only)
* Sat Feb 23 2013 - Logan Bruns <logan@gedanken.org>
- updated some of the patches for gcc 4.7
- use gnu ld by default for gcc 4.7
- updated %build_gcc_with_gnu_ld rules
- use SFEbinutils-gpp if present
* Fri Jun 22 2012 - Thomas Wagner
- back to CC=cc and CXX=CC as solarisstudio is still needed for SFE anyways.
  and that way we don't need gcc-3 installed generally. Maybe the wrong
  symlink /usr/gnu/bin/cc missled to use CC=gcc before.
- changed back CPP to run solarisstudio and not gcc, removed "-Xs" as it looks
  like not longer needed, now it is CPP="cc -E"
- Removed BuildRequires: SUNWgcc  (which is gcc-3 on IPS)
- make a bail-out mechanism if user still has poisonous symlinks /usr/gnu/bin/cc
  and /usr/gnu/bin/cpp. They need to be removed to avoid breakage for some
  build systems ignoring $PATH variable (set by CBE to first find "cc" as
  the solaristudio compiler)
* Thu Jun 21 2012 - Logan Bruns <logan@gedanken.org>
- Replaced CPP="cc -E -Xs" with CPP="gcc -E"
* Wed Jun 20 2012 - Thomas Wagner
- automate transform of version number to string for package names e.g. SFEgcc-46
- apply Patch 10 spawn as well for other versions 4.6 and higher, fixes build 4.5 (no spawn patch)
- prepare fresh patches for LINK_LIBGCC_SPEC for 4.7.x/4.6.x/4.7.x
  use %{majorminornumber} to match the right filename,
  old patch name gcc-05-LINK_LIBGCC_SPEC.diff will remain because external 
  documentation links to this filename!
* Sat Mar 03 2012 - Milan Jurik
- bump to 4.6.3
* Wed Dec 23 2011 - Milan Jurik
- add libquadmath symlinks
* Sun Dec 04 2011 - Milan Jurik
- patch10 for spawn issue
* Sat Oct 29 2011 - Milan Jurik
- bump to 4.6.2
* Thr Oct 13 2011 - Thomas Wagner
- add to LDFLAGS %gnu_lib_path or cc1 can't find libs in bootstrapping the compiler
- remove typo in LDFLAGS_FOR_TARGET="%_ldflags"
* Wed Oct 11 2011 - Thomas Wagner
- add IPS_package_names
- little cleaning up: remove development comments
* Tue Sep 27 2011 - Thomas Wagner
- add version control form outside, so you can build and version
  (if the patches apply cleanly). Note: only one micro version at
  a time is supported by the naming schema: 4.6.1 -> SFEgcc-46
  4.5.3 -> SFEgcc-45, and not at the same time 4.5.2 -> SFEgcc-45.
  Always send to the repo last, what then should be the version
  providing the symlinks in /usr/gnu/<bin|lib>
  e.g. first 4.5.3 then second 4.6.1 -> you get SFEgcc symlinks to 4.6.1 version
* Thu Sep 22 2011 - Thomas Wagner
- automate symlinks to be created in for instance /usr/gnu/bin or /usr/gcc/bin
  as requested at compile time by the configure line --enable-languages=c,c++,fortran,objc
  This works automaticly and independent of number of languages enabled
- reverse package odering, make filename match package SFEgcc, this fixes --autodeps
##TODO## review/verify documentatioin in patch gcc-03-gnulib.diff
- document patch gcc-03-gnulib.diff backgrounds
##TODO## review/verify documentatioin in patch gcc-05-LINK_LIBGCC_SPEC.diff
- add patch gcc-05-LINK_LIBGCC_SPEC.diff (inspired by pkgsrc's gcc variant!)
  to make gcc always know where the gcc compiler runtime lives. Needed to get
  rid of excessive number of directories hardcoded in -R  (patch gcc-03-gnulib.diff
  new version removed them, resultingin libgcc_s.so and libstdc++.so.6 not always
  found). Only downside: if you want a user library then really *do* specify one
  -R/usr/gnu/lib for instance. Else find a clean binary with the correct runpath
- move %gnu_lib_path over from LDFLAGS + LD_OPTIONS to BOOT_CFLAGS, removes 
  excessive number of directories in runpath of binaries, but still finds iconv, 
  mpfr, gmp, mpc in /usr/gnu/lib at compiler bootstrap and when using the compiler 
  itself.
- second draft of a compile time selectable set of target directories where
  gcc symlinks for compiler and runtime are support to going to. Current 
  simplification is that all symlinks go into a single target package SFEgcc 
  respectively SFEgccruntime.
- avoid slipping in gnu-ld with the new consolidation of /usr/sfw/bin/<ld|*> and/or
  /usr/ccs/bin over to /usr/bin which might be accidentially be the first in PATH.
  Set LD=`which ld-wrapper`   -->> NOTE changd again later
- it's actually better to really specify LD=/usr/bin/ld then specifying 
  eventually unavailable ld-wrapper script (in case CBE is not installed)
- make extra matapackages available to be set as "Requires:" in consumer packages
  and add packages which version number in theyr names that can will be pulled 
  in by the metapackages or consumer packages. In selected special cases
  programs can "Requires:" the versioned SFEgccruntime-46 package name.
- first draft patch5 gcc-05-LINK_LIBGCC_SPEC-sparcv9.diff for sparcv9 - needs
  testing, please give feedback
* Tue Aug 16 2011 - Thomas Wagner
- first version of reworked gcc-03-gnulib.diff where user can
  define libdirs everywhere in RUNPATH, e.g. /usr/g++/lib:/usr/gnu/lib:/usr/lib
  please test results with  dump -Lv /usr/g++/lib/libQtNetwork.so | grep RUNPATH
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sun Jul 17 2011 - Alex Viskovatoff
- do not hardcode <majornumber>.<minornumber>
* Sun Jul 17 2011 - Milan Jurik
- bump to 4.6.1
* Tue May 17 2011 - Milan Jurik
- bump to 4.5.3
* Thu Mar 17 2011 - Thomas Wagner
- temporarily force SFEgmp SFEmpfr to have pkgtool --autodeps working in correct build-order
* Wed Mar 16 2011 - Thomas Wagner
- symlinks did not go into package, added %{_gnu_bindir}/* to %files SFEgcc 
* Tue Mar 15 2011 - Thomas Wagner
- add missing %define _gnu_bindir %{_basedir}/gnu/bin
* Sat Mar 12 2011 - Thomas Wagner
- make symlinks to get SFEgcc.spec version 4.x.x to have the gcc 4.x.x
  default compiler accessible by /usr/gnu/bin/gcc and /usr/gnu/bin/g++ 
  and /usr/gnu/bin/gfortran ...
* Fri Mar 04 2011 - Milan Jurik
- RUNPATH enforced to contain /usr/gnu/lib, libs symlinked to /usr/gnu/lib
* Wed Mar 02 2011 - Milan Jurik
- fix NLS build, need to fix linker for g++ still
* Tue Mar 01 2011 - Milan Jurik
- move to /usr/gcc/4.5
* Tue Feb 08 2011 - Thomas Wagner
- interim solution for very old gcc-4.3.3, derived from experimental/SFEgcc-4.5.2.spec
* Sun Jan 30 2011 - Thomas Wagner
- bump to 4.5.2
* Sat Oct 23 2010 - Thomas Wagner
- bump to 4.5.1
- require SFEgmp / SFEmpfr (new version) for builds below 126. may add
  upper limit later if OS contains required version as SUNWgnu-mp / SUNWgnu-mpfr
- finetune BASEDIR detection (SVR4 works, IPS lacks BASEDIR -> emulate)
- merge new logic for (Build)Requires from SFEgcc version 4.4.4 to 4.5.0 spec file
- start with osbuild >= 146 to use gnu ld for linking (build_gcc_with_gnu_ld)
  because looks like linker error
- collect python files from directory based on gcc %version
- make spec bailout if the symlink /usr/gnu/bin/cc exists
- add (Build)Requires SFElibmpc.spec  (SFEMpc might retire, naming)
- add new python files to %files
- add experimental --with-SFEbinutils to force using more fresh SFEbinutils
- don't hard-code ld-wrapper location, use instead `which ld-wrapper`
* Mon Jul 28 2010 - Thomas Wagner
- bump to 4.5.0
* Wed Aug 18 2010 - Thomas Wagner
- try with defaults to SUNWbinutils SUNWgnu-mp SUNWgnu-mpfr
  this might break gcc compile on older osbuild versions
- stop and exit 1 if the link /usr/gnu/bin/cc exists. Give user hint to 
  remove this problematic symlink of gcc to cc
- search ld-wrapper from PATH (e.g. /opt/jdsbld/bin or /opt/dtbld/bin)
- workaround IPS bug that ever prints BASEdir as "/" even if it presents 
  "/usr/gnu" to have configure find SFEgmp and SFEmpfr in case it should 
* Sun Jun  6 2010 - Thomas Wagner
- bump to 4.4.4
- add switches to force SFEgmp and SFEmpfr
- experimenting with gcc related CFLAGS/LDFLAGS
* Fri Feb 05 2010 - Albert Lee <trisk@opensolaris.org>
- Fix bootstrap compiler options
* Sun Aug 09 2009 - Thomas Wagner
- BuildRequires: SUNWbash
* Sat Mar 14 2009 - Thomas Wagner
- change logic to require SFEgmp/SFEmpfr only if *no* SUNWgnu-mp/SUNWgnu-mpfr is present (this is on old OS builds)
- make SFEgcc use of new SUNWgnu-mp/SUNWgnu-mpfr (replacement for SFEgmp/SFEmpfr, SFE-versions still work with SFEgcc)
- detect new location of SFEgmp/SFEmpfr now in /usr/gnu and use them only if missing SUNWgnu-mp/SUNWgnu-mpfr
- add (Build)Requires: SFElibiconv(-devel) (thanks to check-deps.pl)
* Sat Feb 21 2009 - Thomas Wagner
- bump to 4.3.3
- make conditional SFEgmp  / SUNWgnu-mp
- make conditional SFEmpfr / SUNWgnu-mpfr
- add extra configure switch if SUNWgnu-mp and/or SUNWgnu-mpfr is used
* Sun Jan 25 2009 - Thomas Wagner
- make default without HANDLE_PRAGMA_PACK_PUSH_POP. switch on with:
  --with-handle_pragma_pack_push_pop
* Sat Jan 24 2009 - Thomas Wagner
- add HANDLE_PRAGMA_PACK_PUSH_POP (might help wine)
- bump to 4.2.4, version SFEgcc wit %{version}
* Wed Jan  7 2009 - Thomas Wagner
- add conditional SUNWbinutils/SFEbinutils to SFEgcc package
* Sun Dec 28 2008 - Thomas Wagner
- work around %files section on i386/32-bit not finding %{_arch64} binaries because _arch64 is unset ... _arch64 only set if running 64-bit OS in include/arch64.inc
* Sat Dec 27 2008 - Thomas Wagner
- add conditional SUNWbinutils/SFEbinutils to re-enable build on old OS
- add configure-switch for SUNWbinutils otherwise left over SFEbinutils catched by configure/compile. SUNWbinuils not found otherwise.
* Wed Aug 06 2008 - andras.barna@gmail.com
- change SFEbinutils to SUNWbinutils, defaulting to SUN ld
* Mon Mar 10 2008 - laca@sun.com
- add missing defattr
* Sun Mar  2 2008 - Mark Wright <markwright@internode.on.net>
- Add gcc-01-libtool-rpath.diff patch for a problem where
- the old, modified libtool 1.4 in gcc 4.2.3 drops
- -rpath /usr/gnu/lib when building libstdc++.so.6.0.9.
* Fri Feb 29 2008 - Mark Wright <markwright@internode.on.net>
- Bump to 4.2.3.  Remove patch for 32787 as it is upstreamed into gcc 4.2.3.
* Sat Jan 26 2008 - Moinak Ghosh <moinak.ghosh@sun.com>
- Refactor package to have SFEgcc and SFEgccruntime.
* Sun Oct 14 2007 - Mark Wright <markwright@internode.on.net>
- Bump to 4.2.2.
* Wed Aug 15 2007 - Mark Wright <markwright@internode.on.net>
- Change from /usr/ccs/bin/ld to /usr/gnu/bin/ld, this change
  requires SFEbinutils built with binutils-01-bug-2495.diff,
  binutils-02-ld-m-elf_i386.diff and binutils-03-lib-amd64-ld-so-1.diff.
  Add objc to --enable-languages, add --enable-decimal-float.
* Wed Jul 24 2007 - Mark Wright <markwright@internode.on.net>
- Bump to 4.2.1, add patch for gcc bug 32787.
* Wed May 16 2007 - Doug Scott <dougs@truemail.co.th>
- Bump to 4.2.0
* Tue Mar 20 2007 - Doug Scott <dougs@truemail.co.th>
- Added LD_OPTIONS so libs in /usr/gnu/lib will be found
* Sun Mar  7 2007 - Doug Scott <dougs@truemail.co.th>
- change to use GNU as from SFEbinutils
* Sun Mar  7 2007 - Doug Scott <dougs@truemail.co.th>
- Initial spec
