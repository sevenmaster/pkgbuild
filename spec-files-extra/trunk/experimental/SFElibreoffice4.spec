##TODO## check what "git" would be used for. Appears at the end of the buildrun (see logfile)
#mabye add as a BuildRequirement

##TODO## see if harfbuzz could be replaced by a g++/harfbuzz, in that case the dependency on distro icu could vanish

##TODO## look for the automatic update notification URL to see if we have a new SFE built LibeOffice4

##TODO## customize vendorstring by a local file not in SVN, so regular users don't get this set.
%define vendorstring SFE spec-files-extra http://sfe.opencsw.org `date +'%Y%m%d-%H%M'`
#1 = yes  0 = no

#default should be 1, so build all languages and build all myspelldicts
#for testers to save time and scratch diskspace, use pkgtool --without-myspelldicts --without-myspelldicts

#%define buildlanguages %{?_without_buildlanguages:0}%{?!_without_buildlanguages:1}
%define buildlanguages   1

#%define withmyspelldicts %{?_without_myspelldicts:0}%{?!_without_myspelldicts:1}
%define withmyspelldicts 1


##TODO## NEED a programme able to re-program the access of the process structures, see below for filenames.
#S12 retired an 20+years deprecated interface, so need to use new proc interface now

#notes S12pkgbuild@s12> S=/s12pool/sfe/packages/BUILD/SFElibreoffice4-4.4.5.2/libreoffice-4.4.5.2 && I=$S/instdir && W=$S/workdir &&  mkdir -p $W/CxxObject/sal/osl/unx/ $W/Dep/CxxObject/sal/osl/unx/ && cd /s12pool/sfe/packages/BUILD/SFElibreoffice4-4.4.5.2/libreoffice-4.4.5.2 &&   g++ -DCPPU_ENV=gcc3 -DINTEL -DLIBO_INTERNAL_ONLY -DNDEBUG -DOPTIMIZE -DOSL_DEBUG_LEVEL=0 -DSOLARIS -DSUN -DSUN4 -DSYSV -DUNIX -DUNX -D_POSIX_PTHREAD_SEMANTICS -D_PTHREADS -D_REENTRANT    -D_FILE_OFFSET_BITS=64 -DSAL_DLLIMPLEMENTATION -DRTL_OS="\"Solaris"\" -DRTL_ARCH="\"x86"\" -DSRCDIR="\"/s12pool/sfe/packages/BUILD/SFElibreoffice4-4.4.5.2/libreoffice-4.4.5.2\""   -DHAVE_GCC_VISIBILITY_FEATURE -fvisibility=hidden   -Wall -Wnon-virtual-dtor -Wendif-labels -Wextra -Wundef -Wunused-macros -fmessage-length=0 -fno-common -pipe  -fvisibility-inlines-hidden -fPIC -Wshadow -Woverloaded-virtual -std=gpp++11    -DEXCEPTIONS_ON -fexceptions -fno-enforce-eh-specs -O2  -c $S/sal/osl/unx/process.cxx -o $W/CxxObject/sal/osl/unx/process.o -MMD -MT $W/CxxObject/sal/osl/unx/process.o -MP -MF $W/Dep/CxxObject/sal/osl/unx/process.d_ -I$S/sal/osl/unx/  -I$S/include  -I/usr/local/include  -I$S/config_host  -I$S/sal/inc  -I/usr/g++/include   && mv $W/Dep/CxxObject/sal/osl/unx/process.d_ $W/Dep/CxxObject/sal/osl/unx/process.d
#notes S12/s12pool/sfe/packages/BUILD/SFElibreoffice4-4.4.5.2/libreoffice-4.4.5.2/sal/osl/unx/process.cxx: In function 'oslProcessError osl_getProcessInfo(oslProcess, oslProcessData, oslProcessInfo*)':
#notes S12/s12pool/sfe/packages/BUILD/SFElibreoffice4-4.4.5.2/libreoffice-4.4.5.2/sal/osl/unx/process.cxx:1035:53: warning: format '%u' expects argument of type 'unsigned int', but argument 4 has type 'pid_t {aka long int}' [-Wformat=]
#notes S12         snprintf(name, sizeof(name), "/proc/%u", pid);
#notes S12                                                     ^
#notes S12/s12pool/sfe/packages/BUILD/SFElibreoffice4-4.4.5.2/libreoffice-4.4.5.2/sal/osl/unx/process.cxx:1039:13: error: 'prstatus_t' was not declared in this scope
#notes S12             prstatus_t prstatus;
#notes S12             ^
#notes S12/s12pool/sfe/packages/BUILD/SFElibreoffice4-4.4.5.2/libreoffice-4.4.5.2/sal/osl/unx/process.cxx:1039:24: error: expected ';' before 'prstatus'
#notes S12             prstatus_t prstatus;
#notes S12                        ^
#notes S12/s12pool/sfe/packages/BUILD/SFElibreoffice4-4.4.5.2/libreoffice-4.4.5.2/sal/osl/unx/process.cxx:1041:27: error: 'PIOCSTATUS' was not declared in this scope
#notes S12             if (ioctl(fd, PIOCSTATUS, &prstatus) >= 0)
#notes S12                           ^
#notes S12/s12pool/sfe/packages/BUILD/SFElibreoffice4-4.4.5.2/libreoffice-4.4.5.2/sal/osl/unx/process.cxx:1041:40: error: 'prstatus' was not declared in this scope
#notes S12             if (ioctl(fd, PIOCSTATUS, &prstatus) >= 0)
#notes S12                                        ^
#notes S12




#hipster
#checking for ldap_set_option in -lldap... yes
#checking which TLS/SSL and cryptographic implementation to use... NSS
#checking which nss to use... external
#checking for NSS... no
#configure: error: Package requirements (nss >= 3.9.3 nspr >= 4.8) were not met:
#
#No package 'nss' found
#No package 'nspr' found
#
#Consider adjusting the PKG_CONFIG_PATH environment variable if you
#installed software in a non-standard prefix.
#
#Alternatively, you may set the environment variables NSS_CFLAGS
#and NSS_LIBS to avoid the need to call pkg-config.
#See the pkg-config man page for more details.
#Error running configure at ./autogen.sh line 266.



# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

## TODO pjama ##
# what's the Solaris makefile edits?
# Could/would/should use gcc 4.7.4 ? we can... and did. 4.8.5 on OI151a9 and 4.7.4 on hipster (I think bundled 4.8.5 works as well)
#   Release 4.8.5 for OIa9 or go back to 4.6.4?
# Need to tidy up python requirements, ie use lcd python 2.6 for all or %if nightmare?
# python2x.pc SFEpkg that just ads links to existing python2.pc for python2.x, 2-x, -2x etc
# Hunspell is looking for dictionaries?
#    they're NOT in the configure default directory
#      checking whether to include MySpell dictionaries... yes
#      checking whether to use dicts from external paths... yes
#      checking for spelling dictionary directory... file:///usr/share/hunspell
#      checking for hyphenation patterns directory... file:///usr/share/hyphen
#      checking for thesaurus directory... file:///usr/share/mythes
# Look at Apache Portable Runtime (apr) inclusion. It's included as system but I don't think it finds/uses it
#  it's pc path is /usr/apr(/1.3 on OI)/lib/pkgconfig and /usr/apr-util
#  What is it, do we need it? Also include Requires:
# change from --without-help to --with-help for final build
#	revisit --without-fonts at the same time
# Investigate --with-external-dict-dir and frinds... do we need to specify them?
# Fortran? Who needs it? Looked for in configure and warded that missing but subsequent configures don't find F77. Investigate
# Look at name/path for required SFE*.spec files... g++ stuff
# gpp_lib and friends in includes or just local?
# Theres a bunch of Reqs to pnm
##DONE## # See note below re cppunit used needs to be compiled with gcc. (necessitates cppunit-gpp?)
# See notes below re poppler. Consequences?
# Languages?
# what are translations and do we need them?
#   turns out setting --enable-lang=ALL (instead of leaving blank and defaulting to en-US) downloads and presumably install translations
# Move to version 5.0.1 ?
# Re possible java patch http://sfe.opencsw.org/comment/23#comment-23
#    i think we disabled java???
# Languages? en-US is default


# Notes 20150729 
# This spec file compiles and creates a package (I created svr4 so as not to polute my IPS repo) that runs* under hipster circa mid 201507
# It obviously needs a lot more work to refine hence it's submission to SFE/experimental but here's what I've done so far.
# It's based on Peter Tribble's work at http://ptribble.blogspot.co.uk/2015/06/building-libreoffice-on-tribblix.html
# Thanks Peter :)
# See various notes throughout spec file.
# * runs as in will start up and open an existing docx file. I haven't tested beyond that. I've also since exported to pdf and re read same.
# This seems to mainly be a hipster problem because of it's current state with all the multiple versions of pkgs like perl and python etc
#  but you'll need to compile some(all?) pkgs with --define "_use_internal_dependency_generator 0" (edit: now defined in spec)
# Some of the dependancies, eg libmsbub and friends link to .so. files by version which obviously breaks when things get updated.
#  An example of this is linking to boost 1.55 vs later 1.58

# A common theme with the SFE pkges written and included in requires area is that they link to versioned .so files which break
# when said .so files are updated. eg for ldd /usr/lib/liborcus-0.8.so lists "libboost_iostreams.so.1.55.0 =>  (file not found)"
# because when it was compiled libboost was 1.55 but after update went to 1.58 and broke shit. Probably responsible for a lot of
# the cppunit tests failing... maybe. There is no libboost_iostreams.so.1 or libboost_iostreams.so

#Notes 20150810: Let's see how much of those trouble can be avoided with a timely
#propagation of binary packages with corresponding library versions.
#This binary packages should be at hand each time the osdistro updates such
#a versioned library file.
#But in the long-term, in case a library is upgrade compatible, then it is
#preferred to link to library with as few version digits as possible.

# Notes 20150914
# With a number of updates that are benificial to all distros, this now compiles and runs (*very basic tests) on Openindiana 151a9 as well as Hipster
# There's still more to do but I think it's nearly at the stage to release for testing


%include Solaris.inc
# Compile with either iodistgcc or SFEgcc4.7 but runpath problem persistes with either.
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc
%include buildparameter.inc
%include pkgbuild-features.inc

# Stop the internal dpendancy checker from crashing and burning.
%define _use_internal_dependency_generator 0

##TODO## see which is already in include/*inc - can something like usr-g++.inc be include w/o altering $PREFIX?
# Define some useful paths. These should relly go in base.inc but LO is the only one to use them so far.
# Should also do arch64.inc equivalents
%define gnu_sbin /usr/gnu/sbin
%define gpp_bin /usr/g++/bin
%define gpp_sbin /usr/g++/sbin
%define gpp_inc /usr/g++/include
%define gpp_lib /usr/g++/lib
%define gpp_lib_path -L%{gpp_lib} -R%{gpp_lib}


%define major_version   4.4.7
%define minor_version   2

%define src_name	libreoffice
%define src_url		http://download.documentfoundation.org/libreoffice/src/%{major_version}


##TODO## put a top package libreoffice ontop and use mediators to symlink to the locally preferred office
Name:			SFElibreoffice4
IPS_Package_Name:	desktop/application/libreoffice4
Summary:		LibreOffice is a powerful office suite
Version:		%{major_version}.%{minor_version}
URL:			http://www.libreoffice.org
Source:			%{src_url}/%{src_name}-%{version}.tar.xz
Patch1:			libreoffice-01-python-mk.diff
Patch2:			libreoffice-02-config-01-python.diff
Patch3:			libreoffice-03-config-CPUs.patch
Patch4:			libreoffice-04-no-symbols-ld-complains.diff
Patch5:			libreoffice-05-process.cxx-new-procfs.diff
Patch6:			libreoffice-06-hypot-cast-args.diff
Patch7:			libreoffice4-07-libwps04.diff
SUNW_BaseDir:  		%{_basedir}
BuildRoot:     		%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires:	SFEgcc
Requires:	SFEgccruntime

%if %{oihipster}
#currently not in a PNMs
## TODO ## PNM this
BuildRequires:	library/perl-5/archive-zip
Requires:	library/perl-5/archive-zip
%else
BuildRequires:	SFEperl-archive-zip
Requires:	SFEperl-archive-zip
%endif

BuildRequires:	%{pnm_buildrequires_bzip}
Requires:	%{pnm_requires_bzip}

BuildRequires:	%{pnm_buildrequires_gnome_media}
Requires:	%{pnm_requires_gnome_media}

# Requires library/audio/gstreamer/plugin/base bu no PNM yet
# IIRC hipster split off the gtreamer plugins (base, goodd)
## TODO ## PNM  this
%if %{oihipster}
BuildRequires:	library/audio/gstreamer/plugin/base
Requires:	library/audio/gstreamer/plugin/base
%else
BuildRequires:	%{pnm_buildrequires_gnome_media}
Requires:	%{pnm_requires_gnome_media}
%endif

BuildRequires:	%{pnm_buildrequires_cups_libs}
Requires:	%{pnm_requires_cups_libs}

BuildRequires:	%{pnm_buildrequires_library_libxml2}
Requires:	%{pnm_requires_library_libxml2}

BuildRequires:	%{pnm_buildrequires_library_libxslt}
Requires:	%{pnm_requires_library_libxslt}

BuildRequires:	%{pnm_buildrequires_system_library_fontconfig}
Requires:	%{pnm_requires_system_library_fontconfig}

BuildRequires:	%{pnm_buildrequires_system_library_libdbus_glib}
Requires:	%{pnm_requires_system_library_libdbus_glib}

BuildRequires:	%{pnm_buildrequires_system_library_math}
Requires:	%{pnm_requires_system_library_math}

BuildRequires:  %{pnm_buildrequires_developer_gperf}
Requires:       %{pnm_requires_developer_gperf}

# NOTE OIa9 seems to require cppunit compiled with gcc. It failed with SStudio install with udef symbols
# Also cppunit version should probably be bumped from 1.12.1 at SF to 1.13.2 now hosted at Libreoffice
BuildRequires:  %{pnm_buildrequires_developer_cppunit}
Requires:       %{pnm_requires_developer_cppunit}

BuildRequires:	%{pnm_buildrequires_SUNWzlib}
Requires:	%{pnm_buildrequires_SUNWzlib}

BuildRequires:	%{pnm_buildrequires_SUNWfreetype2}
Requires:	%{pnm_buildrequires_SUNWfreetype2}

BuildRequires:  %{pnm_buildrequires_SUNWlxml_devel}
Requires:       %{pnm_requires_SUNWlxml}

# Required if there's issues with cppunit tests
BuildRequires:	%{pnm_buildrequires_gdb}

#git

# Requires python, ideally 2.7 but scripts don't seem to recognse 2.7, fall back to 2.6 and break. Fixed with very hacky patch
# also have vague recollection of having to add backported module to 2.6 that's in 2.7 by default (yes SFEpython-importlib)

##TODO## try if ENV variables can point to the right python. 
#Other untested idea: provide a local python.pc which is in fact a copy of (osdistro) python-2.7.pc
#BuildRequires:	runtime/python-26
##TODO## make python depenencies better, solve python extra module suitable for the python version
BuildRequires:	%{pnm_buildrequires_python_default}

##TODO## verify solaris 11 older version if python-27 importlib is present
##TODO## Could be a pnm macro one day %{pnm_buildrequires_python27_library_python_importlib}
#solaris 11 1.0.2-0.175.3.0.0.18.0
#solaris 12 1.0.2-5.12.0.0.0.70.0

# Should fix pnm after discussion with Tomww re what distros have importlib. It *should* be included in python 2.7. 
%if !%{openindiana}
BuildRequires:    %{pnm_buildrequires_library_python_importlib}
Requires:         %{pnm_requires_library_python_importlib}
%else
BuildRequires:    library/python-2/importlib-26
Requires:         library/python-2/importlib-26
%endif

BuildRequires:	%{pnm_buildrequires_SUNWcurl}
Requires:	%{pnm_requires_SUNWcurl}

BuildRequires:	SFEicu-gpp
Requires:	SFEicu-gpp

BuildRequires:  %{pnm_buildrequires_boost_gpp_default}
Requires:       %{pnm_requires_boost_gpp_default}
BuildRequires:	%{pnm_buildrequires_icu_gpp_default}
Requires:	%{pnm_requires_icu_gpp_default}


# who uses LDAP for office docs? Sheesh.
# ^^ sending email and asking for the email addresses or maybe querying printer queues? I don't know
##TODO## switch or pnm macro - we need at runtime the client libs only? no Server? at build time we need headers?
##TODO##paused## BuildRequires:	library/openldap
##TODO##paused## Requires:	library/openldap
#on S11, problems compiling --without-openldap is doesn't find nssutil.h and other stuff
#now: try --with-system-openldap=/usr/gnu and see if it is found and nss3 / nspr goes away
%define SFEopenldap 1
%if %( expr %{solaris12} '|' %{oihipster} )
#try system openldap for now
%define SFEopenldap 0
%endif
%if %{SFEopenldap}
BuildRequires:  SFEopenldap-gnu
Requires:       SFEopenldap-gnu
%else
BuildRequires:  library/openldap
Requires:       library/openldap
%endif

#we want the libs and for compiling add the headers
BuildRequires:	%{pnm_buildrequires_system_library_mozilla_nss_header_nss}
Requires:	%{pnm_requires_system_library_mozilla_nss}

BuildRequires:	%{pnm_buildrequires_library_nspr_header_nspr}
Requires:	%{pnm_requires_library_nspr}


# This should be PNMd? or just use SFE
%if %{oihipster}
BuildRequires:	library/c++/graphite2
Requires:	library/c++/graphite2

BuildRequires:	library/c++/harfbuzz
Requires:	library/c++/harfbuzz
%else
#all other osdistro currently
BuildRequires:	SFEgraphite2-gpp
Requires:	SFEgraphite2-gpp

BuildRequires:	SFEharfbuzz-gpp
Requires:	SFEharfbuzz-gpp
%endif
#END oihipster

BuildRequires:	%{pnm_buildrequires_library_neon}
Requires:	%{pnm_requires_library_neon}

BuildRequires:  %{pnm_buildrequires_SUNWopenssl_include}
Requires:       %{pnm_requires_SUNWopenssl_libraries}


BuildRequires:	%{pnm_buildrequires_bison}
#pkgtool can't resolve this, then enable this line Requires:	%{pnm_requires_bison}

BuildRequires:	%{pnm_buildrequires_image_library_libpng}
Requires:	%{pnm_requires_image_library_libpng}

BuildRequires:	%{pnm_buildrequires_library_expat}
Requires:	%{pnm_requires_library_expat}

##TODO## PNM this?
BuildRequires:  x11/library/libpthread-stubs
Requires:       x11/library/libpthread-stubs


#start with the defaults we can take from pnm, later overwrite for special cases not suiting into pnm
%define		lo_buildrequires_jdk	%{pnm_buildrequires_jdk_default}
%define		lo_requires_jdk		%{pnm_requires_jdk_default}

##TODO## most of this should go into pnm macro
##TODO## Re-Visit this section once LibreOffice builds in 64-bit, then use Java 8
##TODO## which ones do we need at build time, which at runtime
##TODO## 32-bit LO wants 32-bit jdk - check if jdk-8 only comes in 64-bit on which osdistro
##TODO## might need to set JAVA_HOME or JDK_HOME (?) - else get 32/64 bit warings from autogen.sh
%if %( expr %{solaris11} '+' %{solaris12} '>=' 1 )
%define		lo_buildrequires_jdk	developer/java/jdk-7
%define		lo_requires_jdk		developer/java/jdk-7
%endif

#apply the JDK dependencies
##PASED## TAKE THIS OUT ## BuildRequires:  %{lo_buildrequires_jdk}
##PASED## TAKE THIS OUT ## Requires:       %{lo_requires_jdk}

# library/librevenge
BuildRequires:	SFElibrevenge
Requires:	SFElibrevenge

# library/libmspub
BuildRequires:	SFElibmspub
Requires:	SFElibmspub

# library/libvisio
BuildRequires:	SFElibvisio
Requires:	SFElibvisio

# library/libwpd
BuildRequires:	SFElibwpd
Requires:	SFElibwpd

# library/libwps
BuildRequires:	SFElibwps
Requires:	SFElibwps

# library/libwpg
BuildRequires:	SFElibwpg
Requires:	SFElibwpg

# library/mdds
BuildRequires:	SFEmdds	
Requires:	SFEmdds

# library/libixion
BuildRequires:	SFElibixion
Requires:	SFElibixion

# library/liborcus
BuildRequires:	SFEliborcus
Requires:	SFEliborcus


# library/glm
BuildRequires:	SFEglm
Requires:	SFEglm

# library/libodfgen
BuildRequires:	SFElibodfgen
Requires:	SFElibodfgen

# OI requires Info Zip Version 3.0 as osdistro version is 2.32
##TODO##paused# does osdistro zip suffice if zlib.pc is present? %if %(expr %{openindiana})
##TODO##paused# does osdistro zip suffice if zlib.pc is present? BuildRequires:	SFEzip-gnu
##TODO##paused# does osdistro zip suffice if zlib.pc is present? Requires:	SFEzip-gnu
##TODO##paused# does osdistro zip suffice if zlib.pc is present? %else
##TODO##paused# does osdistro zip suffice if zlib.pc is present? BuildRequires:	%{pnm_buildrequires_zip}
##TODO##paused# does osdistro zip suffice if zlib.pc is present? Requires:	%{pnm_requires_zip}
##TODO##paused# does osdistro zip suffice if zlib.pc is present? %endif

%if %( expr %{solaris11} '+' %{solaris12} '>=' 1 )
#S11 S12 need zlib.pc
BuildRequires:  %{pnm_buildrequires_SFEzlib_pkgconfig}
#for pkgtool's dependency resolution
Requires:       %{pnm_requires_SFEzlib_pkgconfig}

%endif

# OI (Build)Requires poppler. OI seems to have partial install, LO config looks for cpp/poppler-version.h
# May need to update. Confirmed. Current SFE version 0.24.3 does not have GfxState.h, v 0.32.0 on hipster does
# poppler couldn't find libopenjpeg.pc. Required linking libopenjpeg.pc to SFEpkged libopenjpeg1.pc. Should prob add to SFEopenjpeg.spec
# Also had to add --enable-xpdf-headers to poppler to get header files... could probably just install xpdf? but we only need the header files.
# LO has dumped xpdf in the past in favour of poppler with xpdf-headers.
%if %( expr %{solaris11} '|' %{solaris12} '|' %{openindiana} )
BuildRequires:  SFEpoppler-gpp
Requires:       SFEpoppler-gpp
%endif

# If only I could get it to compile... done
# Horrible hacks on hipster: glew requires glu (via glu.pc) which is only in usr/lib/mesa/amd64/pkgconfig/glu.pc (ie no non-amd64)
# created usr/lib/mesa/pkgconfig/glu.pc and created links to both .pc files in /usr/lib/(amd64/)pkgconfig
# Could just set GLEW vars to overcom but have alsked alp to fix in chat... and he's done that 20150914 :)

# for %{oihipster}:
# somehow package x11/library/glu doesn't unpack glu.pc into /usr/lib/pkgconfig/glu.pc
# maybe it is package entire not yet permitting an updates glu package in oihipster 2015
#  pkg contents -r -m x11/library/glu | grep \.pc
#  take the first hash for the file and put that onto the URL:
#  wget pkg.openindiana.org/hipster-2015/file/1/a2bafccc7eefb0fd1b3b969a0194107cafea635d
#  sudo bash
#  gzip -d < a2bafccc7eefb0fd1b3b969a0194107cafea635d > /usr/lib/pkgconfig/glu.pc

BuildRequires:	SFElibglew-devel
Requires:	SFElibglew
# Warning, on hipster, glew.pc, requires glu.pc which requires something, which requires xcb.pc, which requires
# x11/library/libpthread-stubs which isn't installed by default. But configure tells you glew failed.

# Other dependencies discoverd OIH but not catered for yet
# OIH split x11 up so likely differnt names on other distos
# pkgbuild:   dependency discovered: x11/library/glu@9.0.0-2015.0.0.0
# pkgbuild:   dependency discovered: x11/library/libice@1.0.6-0.151.1.8
# pkgbuild:   dependency discovered: x11/library/libsm@1.0.3-0.151.1.8
# pkgbuild:   dependency discovered: x11/library/libx11@1.6.2-2015.0.0.1
# pkgbuild:   dependency discovered: x11/library/libxext@1.1.2-0.151.1.8
# pkgbuild:   dependency discovered: x11/library/libxrandr@1.3.0-0.151.1.8
# pkgbuild:   dependency discovered: x11/library/libxrender@0.9.6-0.151.1.8
# pkgbuild:   dependency discovered: x11/library/toolkit/libxt@1.0.8-0.151.1.8


%description
LibreOffice is a powerful office suite; its clean interface and powerful tools
let you unleash your creativity and grow your productivity. LibreOffice embeds
several applications that make it the most powerful Free & Open Source Office
suite on the market: Writer, the word processor, Calc, the spreadsheet application,
Impress, the presentation engine, Draw, our drawing and flowcharting application,
Base, our database and database frontend, and Math for editing mathematics.

fixed CVEs (only recent) for more, see https://www.libreoffice.org/about-us/security/advisories/
CVE-2015-5214 DOC Bookmark Status Memory Corruption (fixed in 4.4.6)

Remember to install package libreoffice4-desktop-int to get the
Links for LibreOffice in your Desktop Menu.

%package desktop-int
IPS_Package_Name:	desktop/application/libreoffice4-desktop-int
Summary:		%summary - Desktop integration
Version:		%{version}
SUNW_BaseDir:		%_basedir
%include default-depend.inc
Requires: %name

%description desktop-int
This package integrates desktop menu items and symbolic links /usr/bin/loffice

#targets sfe.opencsw.org produced binaries. make our old SFElibreoffice4 package go away
%if %{oihipster}
#START automatic renamed package  (remember to add as well %actions)
# create automatic package with old name and "renamed=true" in it
%include pkg-renamed.inc

#STRONG NOTE:
#remember to set in this spec file the %action which
#adds the depend rule in a way that the new package 
#depends on the old package in a slightly updated branch
#version and has the flag "renamed=true" in it

#This is specific to OpenIndiana Hipster only as this got a SFElibreoffice4 package in the beginning
%package noinst-1
Summary:     renamed to desktop/application/libreoffice4-desktop-int 
#if oldname is same as the "Name:"-tag in this spec file:
#use the SFExyz package name, it is only a dummy!
#example_ab# %define renamed_from_oldname      %{name}
#example_ab# %define renamed_from_oldname      SFEstoneoldpkgname
#
#example_a#  %define renamed_to_newnameversion category/newpackagename = *
#or
#example_b#  %define renamed_to_newnameversion category/newpackagename >= 1.1.1
#
#do not omit version equation!
%define renamed_from_oldname      SFElibreoffice4
%define renamed_to_newnameversion desktop/application/libreoffice4-desktop-int = *
%include pkg-renamed-package.inc

#%description noinst-1
#there has been a problem for gnome-terminal with libvte.so which loads
#our cairo library from /usr/gnu/lib/ in error. Our cairo is now
#relocated to /usr/g++/lib where libvte doesnt search for cairo.

#END automatic renamed package  (remember to add as well %actions)


#list *all* old package names here which could be installed on
#user's systems
#stay in sync with section above controlling the "renamed" packages
#example: SFEurxvt@9.18-5.11,0.0.175.0.0.0.2.1 (note: last digit is incremented calculated
#on the branch version printed by pkg info release/name

#list all the old published package name wich need to go away with upgrade to our new package name/location
#SFElibreoffice4@4.4.5.2,5.11-0.0.151.1.8:20150811T165634Z

%actions
depend fmri=SFElibreoffice4 type=optional
#depend fmri=SFEotheroldnamesgohere@%{ips_version_release_renamedbranch} type=optional

%endif
##END oihipster


%prep
%setup -q -c -T -n %name-%version
xz -dc  %{SOURCE} | tar xf -
cd %{src_name}-%{version}

# patch external/python3/ExternalPackage_python3.mk for different/unresolvedVAR paths
# might not need any more now that I've updated hipster to version with later python
%patch1 -p1

# Theres something horribly wrong with configure.ac/autogen.sh/aclocal.m4 such that _AM_PYTHON_INTERPRETER_LIST is set to only list python 2.*
# Here I've set configure to only test for 2.6 but it should test for 3.3 but I can't find where to expand _AM_PYTHON_INTERPRETER_LIST
# might not need any more now that I've updated hipster to version with later python
%patch2 -p1

# Patch configure.ac to have it detect number of CPUs to apply to parallelism IF gmake version is > 3.81
%if %{openindiana}
%patch3 -p1
%endif

#make Solaris linker happy, solve for ooopathutils
#ld: elf error  elf_getarsym
%patch4 -p1


#new procfs.h the only one on S12 remaining. (introduction in S2.6)
%patch5 -p1

%patch6 -p1

# Patch writerperfect/source/writer/MSWorksImportFilter.cxx to use libwps v0.4
%patch7 -p1

# and hack configure.ac to look for libwps-0.4 insteaf of 0.3
gsed -i.prelibwps -e 's/libwps-0.3/libwps-0.4/'	\
	configure.ac	\
	;

# should probably do this with a patch but sed would be more reselient
# Swap LINUX for SOLARIS in a number of .mk files
gsed -i -e 's/LINUX/SOLARIS/' \
	svx/Executable_gengal.mk	\
	sw/Executable_tiledrendering.mk	\
	vcl/Executable_ui-previewer.mk	\
	desktop/Library_sofficeapp.mk	\
	vcl/Library_vcl.mk	\
	;

# Change 'pow' to 'std::pow' in a coupla files
gsed -i -e 's/pow(/std::pow(/'	\
	sc/source/core/tool/interpr1.cxx \
	sal/qa/inc/valueequal.hxx	\
	;

## Start gratuitous hacks to disable cppunit tests. These really should be resolved for a production pkg
#  but disable for now so someone smarter than I am can debug
# The error can be reproduced during interactive build by going into the build directory
# (for me /var/tmp/SFElibreoffice-4.4.5.2/libreoffice-4.4.5.2) and doing
# 'make <name of test that was deleted>' (eg for first one 'make CppunitTest_dbaccess_macros_test')
# but the build system tells you that anyways.
# Update: these failures are in some cases, random in that I can run the spec and get a pass then run
# again with no changes and get a fail... Suspect it's file system resources and order of compiles of parallel compiles.
# same randomness running make tests manually.

# also, there's probably a better way to disable specific test but....

# Disabled dbaccess_macro & dbaccess_hsqldb cppunit tests as they fail
# see http://nabble.documentfoundation.org/another-cppunit-test-core-dump-java-this-time-building-on-xstreamos-illumos-td4141539.html
# ie remove the following lines in dbaccess/Module_dbaccess.mk
#         CppunitTest_dbaccess_macros_test \
#    CppunitTest_dbaccess_hsqldb_test \
# disable CppunitTest_dbaccess_empty_stdlib_save as well
# Most of the failed test seem to involve libsclo.so. Coincidence?
cp -p dbaccess/Module_dbaccess.mk dbaccess/Module_dbaccess.mk.orig
gsed -i -e '/CppunitTest_dbaccess_macros_test/d' \
	-e '/CppunitTest_dbaccess_hsqldb_test/d' \
	-e '/CppunitTest_dbaccess_empty_stdlib_save/d' \
	dbaccess/Module_dbaccess.mk	\
	;

# Disable CppunitTest_sc_filters_test
cp -p sc/Module_sc.mk sc/Module_sc.mk.orig
#gsed -i -e '/CppunitTest_sc_filters_test/d'	\
#	-e '/CppunitTest_sc_subsequent_filters_test/d'	\
#	-e '/CppunitTest_sc_subsequent_export_test/d'	\
#	-e '/CppunitTest_sc_html_export_test/d'	\
#	sc/Module_sc.mk	\
#	;
gsed -i -e '/CppunitTest_sc_subsequent_filters_test/d'	\
	-e '/CppunitTest_sc_subsequent_export_test/d'	\
	sc/Module_sc.mk	\
	;

# Disable CppunitTest_sw_filters_test plus...
cp -p sw/Module_sw.mk sw/Module_sw.mk.orig
gsed -i -e '/CppunitTest_sw_filters_test/d' \
	-e '/CppunitTest_sw_globalfilter/d' \
	-e '/CppunitTest_sw_ooxmlsdrexport/d' \
	-e '/CppunitTest_sw_ooxmlexport/d' \
	-e '/CppunitTest_sw_macros_test/d' \
        -e '/CppunitTest_sw_ooxmlimport/d' \
	sw/Module_sw.mk	\
	;

## Disable CppunitTest_services
cp -p postprocess/Module_postprocess.mk postprocess/Module_postprocess.mk.orig
gsed -i -e '/CppunitTest_services/d' \
	postprocess/Module_postprocess.mk	\
	;

## Disable CppunitTest_writerperfect_draw
cp -p writerperfect/Module_writerperfect.mk writerperfect/Module_writerperfect.mk.orig
gsed -i -e '/CppunitTest_writerperfect_draw/d'	\
	-e '/CppunitTest_writerperfect_writer/d'\
	writerperfect/Module_writerperfect.mk	\
	;

## End (these) gratuitous hacks

# mess with stuff in solaris.mk so we can find libs in /usr/g++/libs
# Needs review as "-fPIC" should be used instead of -mimpure-text no as well as.
# https://www.illumos.org/issues/3336
# Include -L/usr/g++/lib earlier in the command to have an effect of actually including /usr/g++/lib in the path
# -fPIC required to for Postion Independant Code... "-fPIC" should be used instead of -mimpure-text not as well as.
# -Wl,-z,textwarn to warn about Text relocation errors still so some guru can look at in the furure. Code does not seem to conform to PIC
cp -p solenv/gbuild/platform/solaris.mk	solenv/gbuild/platform/solaris.mk.orig
gsed -i -e 's|gb_Library_TARGETTYPEFLAGS := -shared -Wl,-M/usr/lib/ld/map.noexstk -mimpure-text|gb_Library_TARGETTYPEFLAGS := -shared -Wl,-M/usr/lib/ld/map.noexstk -mimpure-text -fPIC -Wl,-z,textwarn %{gpp_lib_path} %{gnu_lib_path} |'	\
	-e '/-L$(SYSBASE)\/lib \\/i \\t%{gpp_lib_path} %{gnu_lib_path} \\'	\
	solenv/gbuild/platform/solaris.mk	\
	;

#gsed -i -e 's|gb_Library_TARGETTYPEFLAGS := -shared -Wl,-M/usr/lib/ld/map.noexstk -mimpure-text|gb_Library_TARGETTYPEFLAGS := -shared -Wl,-M/usr/lib/ld/map.noexstk -mimpure-text -fPIC -Wl,-z,textwarn -L/usr/g++/lib -R/usr/g++/lib -L/usr/gnu/lib -R /usr/gnu/lib|'	\
#	-e '/-L$(SYSBASE)\/lib \\/i \\t-L$(SYSBASE)/usr/g++/lib -R/usr/g++/lib -L/usr/gnu/lib -R/usr/gnu/lib \\'	\


# And you'll need to create a compilation symlink:
# No longer required with external libglew pkg
#mkdir -p  instdir/program
#ln -s libGLEW.so.1.10 instdir/program/libGLEW.so

# #define MAX_FALLBACK 16 is missing for $S/vcl/source/fontsubset/ttcr.cxx
#bad idea to name a project local file "magic.h". And have another one in /usr/gnu/include/magic.h (sfe package "file/file"). And then on the g++ command line have -I/usr/gnu/include ordered before -I$S/vcl/inc 
[ -f vcl/inc/magic.h ] && mv vcl/inc/magic.h vcl/inc/local.magic.h
#ggrep -r "^#include .*\"magic\.h\""  vcl/     -->> prints files with old name magic.h below directory vcl/
#gsed -i.bak -e '/^#include "magic.h"/ s?magic.h?local.magic.h?' vcl/
gsed -i.bak -e '/^#include "magic.h"/ s?magic.h?local.magic.h?' `ggrep -l -r "^#include .*\"magic\.h\""  vcl/`

#typo "?" ? I think yes!
# export PARALLELISM?=@PARALLELISM@
gsed -i.bak.parallelism -e '/export PARALLELISM/ s/PARALLELISM\?=/PARALLELISM=/' config_host.mk.in

#maybe some "make" doesn't accept "make -j 4" compared to "make -j4"
#Makefile.in:PARALLELISM_OPTION := $(if $(filter-out 0,$(PARALLELISM)),-j $(PARALLELISM),)
gsed -i.bak.make_-j -e '/^PARALLELISM_OPTION/ s/-j /-j/' Makefile.in

#sanity check if file /usr/include/GL/gl.h is present & readable
#usually a symlink pointing to ../../../system/volatile/opengl/include/gl.h to
#let svc:/application/opengl/ogl-select:default at boot time select if "mesa"
#or the nvidia provided opengl is to be used.
head /usr/include/GL/gl.h > /dev/null || (echo "file /usr/include/GL/gl.h is not readable, check svc:/application/opengl/ogl-select:default"; echo "and your nvidia driver. The nvidia driver as SVR4 package does *not* provide the"; echo "include files, so non-IPS install of nvdia needs manual correction to get the"; echo "include files back. You could copy gl.h from older ZFS snapshot:"; echo "cp -pr /.zfs/snapshot/the_snapshot_name/usr/X11/include/NVIDIA to /usr/X11/include/"; exit 1)


%build
cd %{src_name}-%{version}

# CPUS managed with --with-parallelism default option in configure (and patch)
export CPUS=%{_cpus_memory}

# Add /usr/gnu to the pkg-config path to include SFE additions
export PKG_CONFIG_PATH=%{gpp_lib}/pkgconfig:%{gnu_lib}/pkgconfig:$PKG_CONFIG_PATH

export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:%{_basedir}/%{apr_default_basedir}/lib/pkgconfig:%{_basedir}/%{apr_util_default_basedir}/lib/pkgconfig

export JAVA_HOME="/usr/java"

export CC="gcc"
export CXX="g++"

## TODO ## Check if fortran is really used now that it's found in configure
export F77=gfortran
export FC=gfortran

#pnm says: %define boost_gpp_default_prefix      /usr/g++
#pnm says: %define boost_gpp_default_includedir  /usr/g++/include
#pnm says: %define boost_gpp_default_libdir      /usr/g++/lib
#pnm says: %define boost_gpp_default_prefix      /usr
#pnm says: %define boost_gpp_default_includedir  /usr/include
#pnm says: %define boost_gpp_default_libdir      /usr/lib
export BOOSTPREFIX="%{boost_gpp_default_prefix}"
#this is imporant, or get lots of boring linker errors with unresolved symbols (e.g. module pdfunzip)
#for whatever reason this variable is empty in config_host.mk
export BOOST_SYSTEM_LIB="-lboost_system"

#make log more nice by removing boost warning if installed in /usr/g++
if [ "$BOOSTPREFIX" = "/usr/g++" ]; then
export ADD_TO_CFLAGS="-isystem"
fi

export CFLAGS="%{optflags} ${ADD_TO_CFLAGS} %{gpp_inc} -I%{gnu_inc}"
export CXXFLAGS="%{cxx_optflags} ${ADD_TO_CFLAGS} %{gpp_inc} -I%{gnu_inc}"
export CPPFLAGS="-I%{gpp_inc} -I%{gnu_inc}"
%if %( expr %{solaris11} '|' %{oihipster} )
#
#-pthreads helps getting over boost complaining missing -pthreads support (stupid bcs it's there on Solarish). e.g. libcdr
export CFLAGS="$CFLAGS -pthreads"
##REMOVE_IF_IT_WORKS## #glm configure detection doesn't use CXXFLAGS, only CFLAGS CPPFLAGS
#using CPPFLAGS here breakes workdir/UnpackedTarball/exttextcat as it injects CPPFLAGS to regular gcc command line as well
export CXXFLAGS="$CXXFLAGS -std=c++11 -D_GLIBCXX_USE_C99_MATH -pthreads"
%endif
%if %{solaris12}
#
#-pthreads helps getting over boost complaining missing -pthreads support (stupid bcs it's there on Solarish). e.g. libcdr
export CFLAGS="$CFLAGS -pthreads"
##REMOVE_IF_IT_WORKS## #glm configure detection doesn't use CXXFLAGS, only CFLAGS CPPFLAGS
#using CPPFLAGS here breakes workdir/UnpackedTarball/exttextcat as it injects CPPFLAGS to regular gcc command line as well
export CXXFLAGS="$CXXFLAGS -std=c++11                         -pthreads"
%endif

# Do we need /usr/lib 'cuase it should just find that.
# Removing /usr/lib/mps becuase pkg-config should set that correctly  using nss.pc
export LDFLAGS="%{_ldflags} %{gpp_lib_path} %{gnu_lib_path}"

#add more osdistro if needed (config.log may not list 'grep -- "-z.*help" config.log'
%if %{solaris12}
#or get gcc linking fail on options only the Solaris linker understands (see config.log)
LD=/usr/bin/ld
%endif

#paused#remove-if-compile-still-works# #same as with SFEliborcus.spec, if there is no zlib.pc info file, then this helps:
#paused#remove-if-compile-still-works# export MSPUB_CFLAGS="-I/usr/include/libmspub-0.1"
#paused#remove-if-compile-still-works# export MSPUB_LIBS="-lmspub-0.1"

#seems that between 4.4.5.2 and  4.4.7.2 the Makefile sets PKG_CONFIG_PATH to "" - so workdir/UnpackedTarball/libetonyek configure can't find librevenge
#export REVENGE_CFLAGS=$( pkg-config --cflags librevenge-0.0 librevenge-generators-0.0 librevenge-stream-0.0 )
#export REVENGE_LIBS=$( pkg-config --libs librevenge-0.0 librevenge-generators-0.0 librevenge-stream-0.0 )


# Need to manually set NSS_LIBS to include -R<lib_path> as pkg-config nss doens't provide it (only -L<lib_path>)
%if %{solaris11}
#no NSS, nssuti.h no longer present
%else
export NSS_LIBS="$(pkg-config nss --libs-only-L | sed -e 's/-L/-R/') $(pkg-config nss --libs)"
%endif

# Looks like we need to set $PATH to find prefered genbrk and icu-config
# and we need *sbin because that's where we keep icu genccode
export PATH=%{gpp_bin}:%{gpp_sbin}:%{gnu_bin}:%{gnu_sbin}:$PATH


## TODO ##
# compile system odfgen LO version 1.3. Later versions 1.3.1 and 1.4 available (done)
# libpagemaker could by done on system but same version as LO
# Others to look at:
# --with-system-libgltf
# --with-system-opencollada
# DBs, maria, mysql, etc
# .... and more

# Define and Create directory in SOURCES for configure to download external tarballs to.
exttarballdir="${RPM_SOURCE_DIR}/libreoffice-external-tarballs"
if [ ! -d ${exttarballdir} ]; then
	mkdir -p ${exttarballdir}
        ln -s /dev/null ${exttarballdir}/fetch.log
        #touch /tmp/libreoffice-external-tarballs-fetch.log || /bin/true
        #ln -s  /tmp/libreoffice-external-tarballs-fetch.log ${exttarballdir}/fetch.log || /bin/true
fi

# Make bin/unpack-sources executable so it can unpack the likes of dicionaries etc
chmod ug+x bin/unpack-sources

# Options for OI
# 	no --with-parallelism=${CPUS}	# because parrallelism is broken under gmake 3.81
#		leave out.... maybe if gmake >= it sets ?
#	no --with-system-openldap	# because we ain't got it
#	--with-boost=/usr/g++		# because we have SFEboost installed. May apply to other distros as well
#	--disable-gltf			# because it doesn't compile on OI151a9...yet.. one day
#	--x-includes=/usr/X11/include	\
#	--x-libraries=/usr/X11/lib	\
#	--disable-cups		\	# We'll want to print at some point.

# CXXFLAGS="$CXXFLAGS $BOOST_CPPFLAGS $CXXFLAGS_CXX11" inject -std=<...> what makes on S12 boost complain about redefining functions

perl -w -pi.remove_cxxflags_cxx11_from_boost_test -e 's/\$CXXFLAGS_CXX11// if /CXXFLAGS="\$CXXFLAGS \$BOOST_CPPFLAGS \$CXXFLAGS_CXX11"/' \
   configure.ac \
   configure

cp -p configure configure.remove_cxxflags_cxx11_from_boost_test
#autoconf
echo "Debug: diff -u configure.ac.remove_cxxflags_cxx11_from_boost_test configure.ac"
diff -u configure.ac.remove_cxxflags_cxx11_from_boost_test configure.ac || true
echo "Debug: diff -u configure.remove_cxxflags_cxx11_from_boost_test configure"
diff -u configure.remove_cxxflags_cxx11_from_boost_test configure || true
echo "Debug end."

./autogen.sh \
	--prefix=%{_prefix}	\
	--x-includes=/usr/X11/include	\
	--x-libraries=/usr/X11/lib	\
	--enable-verbose	\
	--with-external-tar=${exttarballdir}	\
%if %{withmyspelldicts}
	--with-myspell-dicts	\
%endif
	--with-help=common	\
	--enable-release-build	\
	--disable-gstreamer-1-0	\
	--enable-gstreamer-0-10	\
	--disable-odk		\
	--with-system-cairo	\
	--with-system-expat	\
	--with-system-libxml	\
	--with-system-icu	\
	--with-system-poppler	\
	--with-system-curl	\
	--with-system-boost	\
	--with-boost=${BOOSTPREFIX}	\
        --with-boost-system="-lboost_system" \
	--with-system-glm	\
	--with-system-glew	\
	--with-system-nss	\
	--with-system-apr	\
	--with-system-neon	\
	--with-system-openssl	\
	--with-system-libpng	\
	--with-system-harfbuzz	\
	--with-system-graphite	\
	--with-system-cppunit	\
	--with-system-dicts	\
	--with-system-libwps	\
	--with-system-libwpg	\
	--with-system-libwpd	\
	--with-system-libmspub	\
	--with-system-librevenge \
	--with-system-libodfgen	\
	--with-system-orcus \
	--with-system-mdds \
	--with-system-libvisio \
	--enable-gio		\
	--disable-gnome-vfs	\
%if %{buildlanguages}
	--with-lang=ALL		\
%else
	--with-lang=    	\
%endif
	--disable-collada \
	--disable-firebird-sdbc	\
	--disable-postgresql-sdbc	\
	--enable-python=system	\
	--with-java=no		\
	--without-help		\
	--without-fonts		\
	--disable-gconf		\
	--disable-gltf		\
	--enable-cups		\
	--with-epm=internal	\
	--with-package-format=installed	   \
        --with-vendor="%{vendorstring}"    \
        --with-parallelism=%{_cpus_memory} \
        --with-tls="openssl" \
	--with-system-openldap	\
	;

##paused##	--with-system-openldap	\

#%if %{SFEopenldap}
#	--with-system-openldap	\
#%else
#	--without-system-openldap	\
#%endif

#s11175 sfe ~/packages/BUILD/SFElibreoffice4-4.4.7.2/libreoffice-4.4.7.2 ggrep -r 'export PKG_CONFIG=""' 
#external/libabw/ExternalProject_libabw.mk:              export PKG_CONFIG="" \
#external/libfreehand/ExternalProject_libfreehand.mk:            export PKG_CONFIG="" \
#external/libetonyek/ExternalProject_libetonyek.mk.bak_librevenge_cppunit_not_found_PKG_CONFIG_PATH_empty_error:         export PKG_CONFIG="" \
#external/libpagemaker/ExternalProject_libpagemaker.mk:          export PKG_CONFIG="" \
#external/libeot/ExternalProject_libeot.mk:              && export PKG_CONFIG="" \
#external/libmwaw/ExternalProject_libmwaw.mk:            export PKG_CONFIG="" \
#external/firebird/ExternalProject_firebird.mk:          && export PKG_CONFIG="" \
#external/libebook/ExternalProject_libebook.mk:          export PKG_CONFIG="" \
#external/libodfgen/ExternalProject_libodfgen.mk:                export PKG_CONFIG="" \
#external/libgltf/ExternalProject_libgltf.mk:            export PKG_CONFIG="" \
#external/librevenge/ExternalProject_librevenge.mk:              export PKG_CONFIG="" \
#external/libvisio/ExternalProject_libvisio.mk:          export PKG_CONFIG="" \
#external/libmspub/ExternalProject_libmspub.mk:          export PKG_CONFIG="" \
#external/libwps/ExternalProject_libwps.mk:              export PKG_CONFIG="" \
#external/libwpg/ExternalProject_libwpg.mk:              export PKG_CONFIG="" \
#external/libcdr/ExternalProject_libcdr.mk:              export PKG_CONFIG="" \
#external/libwpd/ExternalProject_libwpd.mk:              export PKG_CONFIG="" \

#it started with libetonyek and then ended up in a loooooooooooooog list.
#I mean, those are external libs, and many of them live in SFE in /usr/g++ and not /usr
#fix for external/libetonyek/UnpackedTarball_libetonyek.mk: which in error sets PKG_CONFIG_PATH=""
#makes it no longer find librevenge, cppunit and so on
#Solution: replace the line from the Makefile: export PKG_CONFIG="" will be /usr/bin/true
gsed -i.bak_lib_not_found_PKG_CONFIG_PATH_empty_error \
   -e 's,export PKG_CONFIG="",/usr/bin/true,'             \
   external/libetonyek/ExternalProject_libetonyek.mk \
   external/libabw/ExternalProject_libabw.mk \
   external/libfreehand/ExternalProject_libfreehand.mk \
   external/libpagemaker/ExternalProject_libpagemaker.mk \
   external/libeot/ExternalProject_libeot.mk \
   external/libmwaw/ExternalProject_libmwaw.mk \
   external/firebird/ExternalProject_firebird.mk \
   external/libebook/ExternalProject_libebook.mk \
   external/libodfgen/ExternalProject_libodfgen.mk \
   external/libgltf/ExternalProject_libgltf.mk \
   external/librevenge/ExternalProject_librevenge.mk \
   external/libvisio/ExternalProject_libvisio.mk \
   external/libmspub/ExternalProject_libmspub.mk \
   external/libwps/ExternalProject_libwps.mk \
   external/libwpg/ExternalProject_libwpg.mk \
   external/libcdr/ExternalProject_libcdr.mk \
   external/libwpd/ExternalProject_libwpd.mk \


#please! don't loose the CXXFLAGS setting from us! pleasepleasplease!
#libabw overwrites it, so boost in /usr/g++ is no longer found and probably other stuff too!

#[...]
#                        $(if $(VERBOSE)$(verbose),--disable-silent-rules,--enable-silent-rules) \
#                        CXXFLAGS="$(if $(SYSTEM_BOOST),$(BOOST_CPPFLAGS),\
#                                -I$(call gb_UnpackedTarball_get_dir,boost))" \
#                        $(if $(CROSS_COMPILING),--build=$(BUILD_PLATFORM) --host=$(HOST_PLATFORM)) \
#[...]

#this should be better: CXXFLAGS="$CXXFLAGS $(if $(SYSTEM_BOOST),$(BOOST_CPPFLAGS),\
#                                 ^^^^^^^^^ inserted
#this is what happens, if project copy misstakes in makefiles for reuse
#other external project correctly preserve or incorporate existing CXXFLAGS settings. Chapeau!
#the only godd thing with stupidly copying errors is, the then all look the very same
#and I can fix that with a stupidly simple gsed regex.

gsed -i.bak_not_reset_CXXFLAGS \
   -e 's,CXXFLAGS=",CXXFLAGS="$(CXXFLAGS) ,' \
   external/libabw/ExternalProject_libabw.mk \
   external/firebird/ExternalProject_firebird.mk \
   external/libcdr/ExternalProject_libcdr.mk \
   external/libebook/ExternalProject_libebook.mk \
   external/libmspub/ExternalProject_libmspub.mk \
   external/libmwaw/ExternalProject_libmwaw.mk \
   external/libodfgen/ExternalProject_libodfgen.mk \
   external/libpagemaker/ExternalProject_libpagemaker.mk \
   external/librevenge/ExternalProject_librevenge.mk \
   external/libvisio/ExternalProject_libvisio.mk \
   external/libwps/ExternalProject_libwps.mk \
 
#test only external
#/opt/dtbld/bin/make -j1  -r -f /s11poolkvm/sfe/packages/BUILD/SFElibreoffice4-4.4.7.2/libreoffice-4.4.7.2/Makefile.gbuild V=2 external


##replaced by BOOST_LDFLAGS## removethis line ## #some project miss to include libraries, so getting unresolve symbols
##replaced by BOOST_LDFLAGS## removethis line ## # example pdfunzip misses boost_system
##replaced by BOOST_LDFLAGS## removethis line ## # we look for gb_ExternalProject_use_externals,pdfunzip and insert
##replaced by BOOST_LDFLAGS## removethis line ## # before the link info to boost_system
##replaced by BOOST_LDFLAGS## removethis line ## 
#possibly wrong see below#gsed -i.bak_missing_boost_system_LDFLAG \
#possibly wrong see below#    -e '/call gb_Executable_use_static_libraries,pdfunzip,/ i\
#possibly wrong see below#$(eval $(call gb_ExternalProject_use_externals,pdfunzip,\\\
#possibly wrong see below#    boost_system \\\
#possibly wrong see below#))\
#possibly wrong see below#       ' \
#possibly wrong see below#   sdext/Executable_pdfunzip.mk \
##replaced by BOOST_LDFLAGS## removethis line ## 
##replaced by BOOST_LDFLAGS## removethis line ## #variant of the above
##replaced by BOOST_LDFLAGS## removethis line ## #$(eval $(call gb_Library_use_libraries,svgfilter,\
##replaced by BOOST_LDFLAGS## removethis line ## #        sal \
##replaced by BOOST_LDFLAGS## removethis line ## 
##replaced by BOOST_LDFLAGS## removethis line ## #inject new section with boost_system
##replaced by BOOST_LDFLAGS## removethis line ## #gsed -i.bak_missing_boost_system_LDFLAG \
##replaced by BOOST_LDFLAGS## removethis line ##     #-e '/call gb_Library_use_libraries/ i\
##replaced by BOOST_LDFLAGS## removethis line ## #$(eval $(call gb_ExternalProject_use_externals,svgfilterlo,\\\
##replaced by BOOST_LDFLAGS## removethis line ##     #boost_system \\\
##replaced by BOOST_LDFLAGS## removethis line ## #))\
##replaced by BOOST_LDFLAGS## removethis line ##        #' \
##replaced by BOOST_LDFLAGS## removethis line ##    #filter/Library_svgfilter.mk \
##replaced by BOOST_LDFLAGS## removethis line ## 
##replaced by BOOST_LDFLAGS## removethis line ## #gb_Executable_use_libraries,svg2odf
##replaced by BOOST_LDFLAGS## removethis line ## gsed -i.bak_missing_boost_system_LDFLAG \
##replaced by BOOST_LDFLAGS## removethis line ##     -e '/call gb_Executable_use_libraries/ i\
##replaced by BOOST_LDFLAGS## removethis line ## $(eval $(call gb_Executable_use_externals,svg2odf,\\\
##replaced by BOOST_LDFLAGS## removethis line ##     boost_system \\\
##replaced by BOOST_LDFLAGS## removethis line ## ))\
##replaced by BOOST_LDFLAGS## removethis line ##        ' \
##replaced by BOOST_LDFLAGS## removethis line ##    filter/Executable_svg2odf.mk \

#$(eval $(call gb_Library_use_externals,svgfilter,\
#        boost_headers \
#        libxml2 \
#))
#./filter/Library_svgfilter.mk
gsed -i.bak_missing_boost_system \
     -e '/call gb_.*_use_externals,.*,/ a\
        boost_system \\' \
     -e '/boost_header/ a\
        boost_system \\' \
    filter/Library_svgfilter.mk \
    sdext/Library_pdfimport.mk \
    sdext/StaticLibrary_pdfimport_s.mk \
    sdext/Executable_pdfunzip.mk \
    external/libebook/ExternalProject_libebook.mk \
    external/libabw/ExternalProject_libabw.mk \
    writerperfect/Library_wpftwriter.mk \


#boots
#todo
#

gsed -i.bak_missing_boost_system \
     -e '/call gb_Executable_use_externals,cppunittester/ a\
        boost_system \\' \
    sal/Executable_cppunittester.mk \


#remove_if_works_on_hipster# #ldd -r instdir/program/libwpftwriterlo.so  -lboost_system fehlt!
#remove_if_works_on_hipster# #hipster sfe ~/packages/BUILD/SFElibreoffice4-4.4.7.2/libreoffice-4.4.7.2 find . -name libwpftwriterlo.so -ls
#remove_if_works_on_hipster# #hipster sfe ~/packages/BUILD/SFElibreoffice4-4.4.7.2/libreoffice-4.4.7.2 rm ./workdir/Headers/Library/libwpftwriterlo.so ./instdir/program/libwpftwriterlo.so
#remove_if_works_on_hipster# #hipster sfe ~/packages/BUILD/SFElibreoffice4-4.4.7.2/libreoffice-4.4.7.2 gmake CC=$CC POPT= Library_wpftwriter
#remove_if_works_on_hipster# #hipster sfe ~/packages/BUILD/SFElibreoffice4-4.4.7.2/libreoffice-4.4.7.2 elfdump -d ./instdir/program/libwpftwriterlo.so| grep boost
#remove_if_works_on_hipster# #       [1]  NEEDED            0x2bfac             libboost_system.so.1.59.0
#remove_if_works_on_hipster# # make CppunitTest_sd_export_tests
#remove_if_works_on_hipster# 
#remove_if_works_on_hipster# #/opt/dtbld/bin/make -j6 -r -f /oihpool/sfe/packages/BUILD/SFElibreoffice4-4.4.7.2/libreoffice-4.4.7.2/Makefile.gbuild Library_wpftwriter
#remove_if_works_on_hipster# 
#remove_if_works_on_hipster# #OPEN# $(eval $(call gb_Library_use_externals,wpftwriter,\
#remove_if_works_on_hipster# #OPEN#         abw \
#remove_if_works_on_hipster# #OPEN#         boost_headers \
#remove_if_works_on_hipster# #OPEN#         boost_system \
#remove_if_works_on_hipster# #OPEN# [...]
#remove_if_works_on_hipster# #OPEN# "./writerperfect/Library_wpftwriter.mk" [Modified] line 50 of 73 --68%-- col 22
#remove_if_works_on_hipster# #OPEN# 
#remove_if_works_on_hipster# 
#remove_if_works_on_hipster# 
#remove_if_works_on_hipster# #OPEN# S=/oihpool/sfe/packages/BUILD/SFElibreoffice4-4.4.7.2/libreoffice-4.4.7.2 && I=$S/instdir && W=$S/workdir &&  mkdir -p $W/CppunitTest/ && rm -fr $W/CppunitTest/vcl_filters_test.test.user && mkdir $W/CppunitTest/vcl_filters_test.test.user &&   rm -fr $W/CppunitTest/vcl_filters_test.test.core && mkdir $W/CppunitTest/vcl_filters_test.test.core && cd $W/CppunitTest/vcl_filters_test.test.core && (LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}"$I/ure/lib:$I/program":$W/UnpackedTarball/cppunit/src/cppunit/.libs        $W/LinkTarget/Executable/cppunittester $W/LinkTarget/CppunitTest/libtest_vcl_filters_test.so --headless "-env:BRAND_BASE_DIR=file://$S/instdir" "-env:BRAND_SHARE_SUBDIR=share" "-env:UserInstallation=file://$W/CppunitTest/vcl_filters_test.test.user"   "-env:CONFIGURATION_LAYERS=xcsxcu:file://$I/share/registry xcsxcu:file://$W/unittest/registry"  "-env:UNO_TYPES=file://$I/ure/share/misc/types.rdb file://$I/program/types/offapi.rdb"  "-env:UNO_SERVICES=file://$W/Rdb/ure/services.rdb file://$W/ComponentTarget/configmgr/source/configmgr.component file://$W/ComponentTarget/i18npool/util/i18npool.component file://$W/ComponentTarget/ucb/source/core/ucb1.component file://$W/ComponentTarget/ucb/source/ucp/file/ucpfile1.component"  -env:URE_INTERNAL_LIB_DIR=file://$I/ure/lib -env:LO_LIB_DIR=file://$I/program -env:LO_JAVA_DIR=file://$I/program/classes --protector $W/LinkTarget/Library/unoexceptionprotector.so unoexceptionprotector --protector $W/LinkTarget/Library/unobootstrapprotector.so unobootstrapprotector   --protector $W/LinkTarget/Library/libvclbootstrapprotector.so vclbootstrapprotector    > $W/CppunitTest/vcl_filters_test.test.log 2>&1 || ( RET=$?; $S/solenv/bin/gdb-core-bt.sh $W/LinkTarget/Executable/cppunittester $W/CppunitTest/vcl_filters_test.test.core $RET >> $W/CppunitTest/vcl_filters_test.test.log 2>&1; cat $W/CppunitTest/vcl_filters_test.test.log; $S/solenv/bin/unittest-failed.sh Cppunit vcl_filters_test))
#remove_if_works_on_hipster# #OPEN# [build CUT] vcl_outdev
#remove_if_works_on_hipster# #OPEN# /bin/sh: line 1: 18685: Killed
#remove_if_works_on_hipster# #OPEN# ld.so.1: cppunittester: fatal: relocation error: file /oihpool/sfe/packages/BUILD/SFElibreoffice4-4.4.7.2/libreoffice-4.4.7.2/instdir/program/libwpftwriterlo.so: symbol _ZN5boost6system16generic_categoryEv: referenced symbol not found
#remove_if_works_on_hipster# #OPEN# 
#remove_if_works_on_hipster# #OPEN# No core file identified in directory /oihpool/sfe/packages/BUILD/SFElibreoffice4-4.4.7.2/libreoffice-4.4.7.2/workdir/CppunitTest/sd_export_tests.test.core
#remove_if_works_on_hipster# #OPEN# To show backtraces for crashes during test execution,
#remove_if_works_on_hipster# #OPEN# enable core files with:
#remove_if_works_on_hipster# #OPEN# 
#remove_if_works_on_hipster# #OPEN#    ulimit -c unlimited
#remove_if_works_on_hipster# #OPEN# 
#remove_if_works_on_hipster# #OPEN# 
#remove_if_works_on_hipster# #OPEN# Error: a unit test failed, please do one of:
#remove_if_works_on_hipster# #OPEN# 
#remove_if_works_on_hipster# #OPEN# export DEBUGCPPUNIT=TRUE            # for exception catching
#remove_if_works_on_hipster# #OPEN# export CPPUNITTRACE="gdb --args"    # for interactive debugging on Linux
#remove_if_works_on_hipster# #OPEN# export CPPUNITTRACE="\"[full path to devenv.exe]\" /debugexe" # for interactive debugging in Visual Studio
#remove_if_works_on_hipster# #OPEN# export VALGRIND=memcheck            # for memory checking
#remove_if_works_on_hipster# #OPEN# 
#remove_if_works_on_hipster# #OPEN# and retry using: make CppunitTest_sd_export_tests
#remove_if_works_on_hipster# #OPEN# 
#remove_if_works_on_hipster# #OPEN# make[1]: *** [/oihpool/sfe/packages/BUILD/SFElibreoffice4-4.4.7.2/libreoffice-4.4.7.2/workdir/CppunitTest/sd_export_tests.test] Error 1
#remove_if_works_on_hipster# #OPEN# make[1]: *** Waiting for unfinished jobs....
#remove_if_works_on_hipster# #OPEN# make[1]: Leaving directory `/oihpool/sfe/packages/BUILD/SFElibreoffice4-4.4.7.2/libreoffice-4.4.7.2'
#remove_if_works_on_hipster# #OPEN#

#delete if it works# only boost_system missing? or boost_header as well?
#delete if it works# #hm. trying boost_header as well:
#delete if it works# #/usr/g++/include/boost/config/requires_threads.hpp:47:5: error: #error "Compiler threading support is not turned on. Please set the correct command line options for threading: -pthread (Linux), -pthreads (Solaris) or -mthreads (Mingw32)"
#delete if it works# # external/libcdr/UnpackedTarball_libcdr.mk# $(eval $(call gb_UnpackedTarball_UnpackedTarball,libcdr))
#delete if it works# # external/libcdr/UnpackedTarball_libcdr.mk# $(eval $(call gb_UnpackedTarball_set_tarball,libcdr,$(CDR_TARBALL)))
#delete if it works# #gsed -i.bak_missing_boost_system_boost_header \
#delete if it works# #     -e '/gb_UnpackedTarball/ i\



#OPEN

#$(eval $(call gb_Library_use_externals,pdfimport,\
        #boost_system \
    #zlib \
    #$(if $(filter-out WNT MACOSX,$(OS)),fontconfig) \
#))
#sdext/Library_pdfimport.mk

##better add, not replace! #names boost_header instead of boost_system
##better add, not replace! #solution: replace it
##better add, not replace! gsed -i.bak_missing_boost_system_remove_boost_header \
    ##better add, not replace! -e '/boost_headers/ s/boost_headers/boost_system/' \
    ##better add, not replace! -e '/boost_header/ s/boost_header/boost_system/' \
   ##better add, not replace! sdext/Library_pdfimport.mk \
   ##better add, not replace! sdext/StaticLibrary_pdfimport_s.mk \
   ##better add, not replace! sdext/Executable_pdfunzip.mk \

#add boost_system in case there is boost_header


%if %(expr %{solaris11} '|' %{solaris12} '|' %{oihipster} )
###REMOVE IF IT WORKS ON OIHIPSTER#   hipster is _ex_cluded here, as it would as well need "-fpermissive" when using "decltype" - but it can take typeof here instead, so don't patch at all
###REMOVE IF IT WORKS ON OIHIPSTER#   might be no problem with the unescaped >"< in the "warning"

#fix build for coinmp by preparing a patch which gets applied later in the regular "gmake" as it
#loads all the extra tarballs, unpacks them, runs configure && make
#Solution: we inject another patch to coinmp here as a file 
#and add that patch file into the Makefile which applies LibreOffice supplied patches: 
#     external/coinmp/UnpackedTarball_coinmp.mk
## the experimental sed pattern on file workdir/UnpackedTarball/coinmp/CoinUtils/src/CoinSignal.hpp
##            -e '/warning.*extern \"C\"/ s?\"C\"?\\"C\\"?' \
##            -e '/typedef typeof(SIG_DFL) CoinSighandler_t;/ s?typedef typeof(SIG_DFL) CoinSighandler_t;?typedef decltype(SIG_DFL) CoinSighandler_t;?' \

#$(eval $(call gb_UnpackedTarball_add_patches,coinmp,\
#        external/coinmp/android.build.patch.1 \
#        external/coinmp/no-binaries.patch.1 \
#        external/coinmp/werror-format-security.patch.0 \
#        external/coinmp/werror-undef.patch.0 \
#        external/coinmp/coinmp-msvc-disable-sse2.patch.1 \
#        $(if $(filter MSC,$(COM)),external/coinmp/windows.build.patch.1 \
#                $(if $(filter 120,$(VCVER)),external/coinmp/coinmp-vs2013.patch.1) \
#        ) \
#        $(if $(filter MACOSX,$(OS)),external/coinmp/macosx.build.patch.1) \
#))

gsed -i.bak_coinsignal.hpp_patch \
   -e '/external\/coinmp\/coinmp-msvc-disable-sse2.patch/a\
\texternal/coinmp/coinsignal.hpp--escape-doublequote-in-warning--change-typeof-to-decltype.diff.0 \\' \
   external/coinmp/UnpackedTarball_coinmp.mk 


##TODO## verify if substituting typeof with decltype is the right thing to do!
## who can verify this?

# if OS has new headers regarding c++1, then it looks like the following is the case:
# in a warning, >"< must be escaped:  warning("extern "C" {")  -->>  warning("extern \"C\" {")  line 107 in CoinSignal.hpp

#NOTE about the name of the patch. A suffix .0 gets your patch -p0 and a suffix .1 gets you patch -p1
cat - > external/coinmp/coinsignal.hpp--escape-doublequote-in-warning--change-typeof-to-decltype.diff.0 << COINMPPATCH
--- CoinUtils/src/CoinSignal.hpp.orig 2011-01-04 00:31:00.000000000 +0100
+++ CoinUtils/src/CoinSignal.hpp      2016-01-04 18:45:54.741167853 +0100
@@ -88,7 +88,7 @@
 #     define CoinSighandler_t_defined
 #  endif
 #  if defined(__GNUC__)
-      typedef typeof(SIG_DFL) CoinSighandler_t;
+      typedef decltype(SIG_DFL) CoinSighandler_t;
 #     define CoinSighandler_t_defined
 #  endif
 #endif
@@ -104,7 +104,7 @@

 #ifndef CoinSighandler_t_defined
 #  warning("OS and/or compiler is not recognized. Defaulting to:");
-#  warning("extern "C" {")
+#  warning("extern \"C\" {")
 #  warning("   typedef void (*CoinSighandler_t) (int);")
 #  warning("}")
    extern "C" {

COINMPPATCH

#END %{solaris11} '|' %{solaris12}
%endif


# Define LD_LIBRARY_PATH to:
# 1) prevent gcc4.7 being in path before 4.8 for libstd++. Probably a function of dependancy libs being compled with gcc4.7 (or something osdistro)
# 2) find nss and friends under /usr/lib/mps
# 3) find local libs in current build
export LD_LIBRARY_PATH=%{gpp_lib}:%{gnu_lib}:/usr/gcc/lib:`pwd`/instdir/ure/lib:`pwd`/instdir/sdk/lib:`pwd`/instdir/program:/usr/lib


#fix the compiler, it tries cc which we don't want to have
#erors seen in /glew/ at minimum
# edit pja: on OI, we're already in %{src_name}-%{version}
# and don't have UnpackedTarball till we run make...
#( cd %{src_name}-%{version}
#perl -w -pi.bak -e "s,CC=cc,CC=gcc," ./config_host.mk ./odk/settings/settings.mk ./solenv/gbuild/platform/com_GCC_defs.mk ./solenv/gbuild/platform/mingw.mk workdir/UnpackedTarball/glew/config/Makefile.solaris workdir/UnpackedTarball/glew/config/Makefile.solaris
# pjama created glew spec so no need for internal glew any more
#perl -w -pi.bak2 -e "s,-xO2,," workdir/UnpackedTarball/glew/config/Makefile.solaris
#)

#get "cc" be found as gcc
export PATH=`pwd`/bin:$PATH
echo "gcc \$*" > bin/cc
chmod a+rx bin/cc

# Remove -jCPUs because it's broken with OI's gmake 3.81
# use --with-parallelism=${CPUS} in configure as autogen will disable if gmake <= v3.81
# somehow define BOOST_PP_VARIADICS_MSVC just to shut warnings up.
# 
#try: all except OI, use --with-parallelism=%{_cpus_memory}
#     for OI, enable patch3 (above)

compiletry=""
for compiletry in 5 4 3 2 1 0
 do
 #we are done, if exit == 0, else continue and hack the ....
 gmake CC=$CC POPT= && break || /usr/bin/true

 ###pdfunzip
   #don't delete it [ -r `pwd`/workdir/LinkTarget/Executable/pdfunzip ] && rm `pwd`/workdir/LinkTarget/Executable/pdfunzip
   if [ ! -f `pwd`/workdir/LinkTarget/Executable/pdfunzip ] ; 
    then
     echo "====================== compiletry $compiletry"
     echo "recompile pdfunzip ourselves, with added \"-lboost_system\""
     gmake CC=$CC POPT= Executable_pdfunzip || /usr/bin/true
     S=`pwd` && I=$S/instdir && W=$S/workdir && g++    -Wl,-z,origin '-Wl,-rpath,$ORIGIN/../Library' -L$I/ure/lib -L$I/program -L/usr/g++/lib -R/usr/g++/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/lib -L/usr/lib -Wl,-z,combreloc  -L$W/LinkTarget/StaticLibrary -L$I/sdk/lib  -L$I/ure/lib  -L$I/program  -L$W/LinkTarget/Library -Wl,-zignore -Wl,-zcombreloc -Wl,-Bdirect  -L/usr/g++/lib -R/usr/g++/lib -L/usr/gnu/lib -R/usr/gnu/lib   -L/usr/X11/lib -R/usr/X11/lib -L/usr/g++/lib   $W/CxxObject/sdext/source/pdfimport/test/pdfunzip.o     -Wl,--start-group  $W/LinkTarget/StaticLibrary/libpdfimport_s.a  -lm -lnsl -lsocket   -lz -Wl,--end-group -Wl,-zrecord -luno_sal -lboost_system -o $W/LinkTarget/Executable/pdfunzip
     gmake CC=$CC POPT= Executable_pdfunzip || /usr/bin/true
   fi #pdfunzip

 ###pdf2xml
   #don't delete it [ -r`pwd`/workdir/LinkTarget/Executable/pdf2xml ] && rm `pwd`/workdir/LinkTarget/Executable/pdf2xml
   if [ ! -f `pwd`/workdir/LinkTarget/Executable/pdf2xml ] ; 
    then
     echo "====================== compiletry $compiletry"
     echo "recompile pdf2xml ourselves, with added \"-lboost_system\""
     gmake CC=$CC POPT= Executable_pdf2xml || /usr/bin/true
     S=`pwd` && I=$S/instdir && W=$S/workdir &&  g++    -Wl,-z,origin '-Wl,-rpath,$ORIGIN/../Library' -L$I/ure/lib -L$I/program -L/usr/g++/lib -R/usr/g++/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/lib -L/usr/lib -Wl,-z,combreloc  -L$W/LinkTarget/StaticLibrary -L$I/sdk/lib  -L$I/ure/lib  -L$I/program  -L$W/LinkTarget/Library -Wl,-zignore -Wl,-zcombreloc -Wl,-Bdirect  -L/usr/g++/lib -R/usr/g++/lib -L/usr/gnu/lib -R/usr/gnu/lib   -L/usr/X11/lib -R/usr/X11/lib  $W/CxxObject/sdext/source/pdfimport/test/pdf2xml.o     -Wl,--start-group  $W/LinkTarget/StaticLibrary/libpdfimport_s.a  -lm -lnsl -lsocket  -L/usr/g++/lib -lcppunit    -lz -Wl,--end-group -Wl,-zrecord -lbasegfxlo -lvcllo -lcomphelper -luno_cppu -lunotest -ltest -luno_cppuhelpergcc3 -luno_sal -lboost_system -o $W/LinkTarget/Executable/pdf2xml
     gmake CC=$CC POPT= Executable_pdf2xml || /usr/bin/true
   fi #pdf2xml

 ###pdfimport.so
 #the build system didn't link against libboost_system.so, so we edit this into the binary ourselves
 if [ -f workdir/LinkTarget/CppunitTest/libtest_sdext_pdfimport.so ]
   then
   if elfdump -d workdir/LinkTarget/CppunitTest/libtest_sdext_pdfimport.so | grep boost_system.so
     then
      echo "workdir/LinkTarget/CppunitTest/libtest_sdext_pdfimport.so alread links to the boost_system library"
    else
      echo "Fixing link list of file libtest_sdext_pdfimport.so which misses the libboost_system.so library"
      echo "====================== compiletry $compiletry"
      echo "OLD: elfdump -d workdir/LinkTarget/CppunitTest/libtest_sdext_pdfimport.so"
      elfdump -d workdir/LinkTarget/CppunitTest/libtest_sdext_pdfimport.so       

      echo "====================== compiletry $compiletry"
      
      echo "elfedit needed libboost_system.so into weird static/dynmic mixed library file workdir/LinkTarget/CppunitTest/libtest_sdext_pdfimport.so"
      echo "the macro compiling libtest_sdext_pdfimport.so was not able to link against boost_system, so we edit this into the header ourselves"
      /usr/bin/elfedit -e 'dyn:value -add -s NEEDED libboost_system.so' workdir/LinkTarget/CppunitTest/libtest_sdext_pdfimport.so
      
      
      echo "====================== compiletry $compiletry"
      echo "NEW: elfdump -d workdir/LinkTarget/CppunitTest/libtest_sdext_pdfimport.so"
      elfdump -d workdir/LinkTarget/CppunitTest/libtest_sdext_pdfimport.so       
    fi #elfdump -d libtest_sdext_pdfimport.so | grep boost_system
   
   echo "====================== compiletry $compiletry"
 fi # -f libtest_sdext_pdfimport.so


done #compiletry

if [ "$compiletry" == "0" ] ; then
 echo "Error: did not build successfully!"
 exit 1
fi


echo "Sanity checks for boost (boost_system)"
for lib in `find . -name \*.so  -print`
  do 
  ldd -r $lib 2>/dev/null| grep boost \
     && echo found: $lib
  done \
  | grep "symbol not found" && exit 111
 
%install
## TODO ##
# Create some links in /usr/bin to wherever libreoffice is located. eg /usr/bin/soffice -> /usr/local/lib/libreoffice/soffice
# but don't conflict with openoffice if installed
#
cd %{src_name}-%{version}
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT

# Change RPATH for list of files. There's got to be a better way but do this for now.
# For some reason they have the buld directory in the RPATH and no $ORIGIN like all the others
# Gotcha will be compiler flavour used in the future as now I'm using gcc 4.8.5
# Manipulate this string from gcc -dumpspecs to get gcc path to include:
#"%{m64:-R /usr/gcc/4.8/lib/amd64:/usr/gcc/lib/amd64 %D}%{!m64:-R /usr/gcc/4.8/lib:/usr/gcc/lib %D}"
# remove "\!" in sed regex to get amd64 version for later 64 bit LO :)
gccrpath=`gcc -dumpspecs | grep 'm64:-R' | sed -e 's/^.*{\!m64:-R //;s/ \%D.*$//'`
#%define rpath '%{gpp_lib}:%{gnu_lib}:%{gccrpath}:$ORIGIN:$ORIGIN/../ure-link/lib'
%define rpath '%{gpp_lib}:%{gnu_lib}:'"$gccrpath"':$ORIGIN:$ORIGIN/../ure-link/lib'

pushd $RPM_BUILD_ROOT%{_libexecdir}/libreoffice/program
for file in libCbc.so.3 libCbcSolver.so.3 libCgl.so.1 libClp.so.1 libCoinMP.so.1 libOsi.so.1 libOsiClp.so.1 librdf-lo.so.0 librasqal-lo.so.3
  do
  /usr/bin/elfedit -e 'dyn:runpath '%{rpath}' ' $file
done
popd

# Gratuitously remove all the gid_Module_* files as ATM I have no idea what they are for.
# Something to do with splitting up files into different packages/modules
# http://lists.freedesktop.org/archives/libreoffice/2013-June/053667.html
rm $RPM_BUILD_ROOT/gid_Module_*


##TODO## see if a pkg mediator could be useful to have a default "loffice" but can have another symlink named "soffice"
## TODO ## Desktop integration
# /usr/bin/loffice (so as not to conflict with Openoffice soffice
mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -s ../lib/libreoffice/program/soffice $RPM_BUILD_ROOT%{_bindir}/loffice

# Create /usr/bin/libreoffice4.4 executable script
# f none usr/bin/libreoffice4.4=/var/tmp/SFElibreoffice4-4.4.5.2/libreoffice-4.4.5.2/workdir/CustomTarget/sysui/share/libreoffice/openoffice.sh 0755 root bin
# Note if we copy and use above file, the path will need editing
cat << "EOF" > $RPM_BUILD_ROOT%{_bindir}/libreoffice4.4
#!/bin/sh
exec /usr/lib/libreoffice/program/soffice "$@"
EOF
chmod 0555 $RPM_BUILD_ROOT%{_bindir}/libreoffice4.4

#f none usr/share/mime/packages/libreoffice4.4.xml=/var/tmp/SFElibreoffice4-4.4.5.2/libreoffice-4.4.5.2/workdir/CustomTarget/sysui/share/libreoffice/openoffice.org.xml
install -D ./workdir/CustomTarget/sysui/share/libreoffice/openoffice.org.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages/libreoffice4.4.xml

#f none usr/share/application-registry/libreoffice4.4.applications=/var/tmp/SFElibreoffice4-4.4.5.2/libreoffice-4.4.5.2/workdir/CustomTarget/sysui/share/libreoffice/openoffice.applications
install -D ./workdir/CustomTarget/sysui/share/libreoffice/openoffice.applications $RPM_BUILD_ROOT%{_datadir}/application-registry/libreoffice4.4.applications

# Menu items
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
ln -s ../../lib/libreoffice/share/xdg/startcenter.desktop $RPM_BUILD_ROOT%{_datadir}/applications/libreoffice4-startcenter.desktop
ln -s ../../lib/libreoffice/share/xdg/base.desktop $RPM_BUILD_ROOT%{_datadir}/applications/libreoffice4-base.desktop
ln -s ../../lib/libreoffice/share/xdg/calc.desktop $RPM_BUILD_ROOT%{_datadir}/applications/libreoffice4-calc.desktop
ln -s ../../lib/libreoffice/share/xdg/draw.desktop $RPM_BUILD_ROOT%{_datadir}/applications/libreoffice4-draw.desktop
ln -s ../../lib/libreoffice/share/xdg/impress.desktop $RPM_BUILD_ROOT%{_datadir}/applications/libreoffice4-impress.desktop
ln -s ../../lib/libreoffice/share/xdg/math.desktop $RPM_BUILD_ROOT%{_datadir}/applications/libreoffice4-math.desktop
ln -s ../../lib/libreoffice/share/xdg/qstart.desktop $RPM_BUILD_ROOT%{_datadir}/applications/libreoffice4-qstart.desktop
ln -s ../../lib/libreoffice/share/xdg/writer.desktop $RPM_BUILD_ROOT%{_datadir}/applications/libreoffice4-writer.desktop
ln -s ../../lib/libreoffice/share/xdg/xsltfilter.desktop $RPM_BUILD_ROOT%{_datadir}/applications/libreoffice4-xsltfilter.desktop

install -D ./workdir/CustomTarget/sysui/share/libreoffice/openoffice.keys $RPM_BUILD_ROOT%{_datadir}/mime-info/libreoffice4.4.keys
install -D ./workdir/CustomTarget/sysui/share/libreoffice/openoffice.keys $RPM_BUILD_ROOT%{_datadir}/mime-info/libreoffice4.4.mime

install -D ./sysui/desktop/icons/hicolor/48x48/apps/writer.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-writer.png
install -D ./sysui/desktop/icons/hicolor/48x48/apps/calc.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-calc.png
install -D ./sysui/desktop/icons/hicolor/48x48/apps/draw.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-draw.png
install -D ./sysui/desktop/icons/hicolor/48x48/apps/impress.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-impress.png
install -D ./sysui/desktop/icons/hicolor/48x48/apps/math.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-math.png
install -D ./sysui/desktop/icons/hicolor/48x48/apps/base.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-base.png
install -D ./sysui/desktop/icons/hicolor/48x48/apps/startcenter.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-startcenter.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/text.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-text.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/text-template.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-text-template.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/spreadsheet.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-spreadsheet.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/spreadsheet-template.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-spreadsheet-template.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/drawing.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-drawing.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/drawing-template.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-drawing-template.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/presentation.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-presentation.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/presentation-template.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-presentation-template.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/master-document.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-master-document.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/formula.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-formula.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/database.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-database.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/extension.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-extension.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/oasis-text.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-oasis-text.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/oasis-text-template.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-oasis-text-template.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/oasis-spreadsheet.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-oasis-spreadsheet.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/oasis-spreadsheet-template.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-oasis-spreadsheet-template.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/oasis-drawing.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-oasis-drawing.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/oasis-drawing-template.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-oasis-drawing-template.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/oasis-presentation.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-oasis-presentation.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/oasis-presentation-template.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-oasis-presentation-template.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/oasis-master-document.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-oasis-master-document.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/oasis-formula.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-oasis-formula.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/oasis-database.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-oasis-database.png
install -D ./sysui/desktop/icons/hicolor/48x48/mimetypes/oasis-web-template.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/libreoffice4.4-oasis-web-template.png

# Have a good hard look at ./workdir/CustomTarget/sysui/solaris/libreoffice sysvr4 pkg files


%clean
rm -rf $RPM_BUILD_ROOT

##TODO## place the new icons and stuff into apropriate directory and get auto-refresh on the target system
#above ^^:  verify if that is true (:

%post desktop-int
( echo '# check whether /usr is writable';
  echo 'tiptoe="${PKG_INSTALL_ROOT}/usr/_.$$"';
  echo 'touch "$tiptoe" >/dev/null 2>&1';
  echo 'if [ $? -ne 0 ]; then';
  echo '  exit 0';
  echo 'fi';
  echo 'rm -f "$tiptoe"';
  echo '# update shared mime database';
  echo 'if [ -x /usr/bin/update-mime-database ]; then';
  echo '  update-mime-database ${PKG_INSTALL_ROOT}/usr/share/mime';
  echo 'fi';
  echo 'if [ -x /usr/bin/update-desktop-database ]; then';
  echo '  /usr/bin/update-desktop-database -q';
  echo 'elif (which update-desktop-database); then';
  echo '  update-desktop-database -q /usr/share/applications';
  echo 'fi';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u -c SFE


%postun desktop-int
( echo '# check whether /usr is writable';
  echo 'tiptoe="${PKG_INSTALL_ROOT}/usr/_.$$"';
  echo 'touch "$tiptoe" >/dev/null 2>&1';
  echo 'if [ $? -ne 0 ]; then';
  echo '  exit 0';
  echo 'fi';
  echo 'rm -f "$tiptoe"';
  echo '# update shared mime database';
  echo 'if [ -x /usr/bin/update-mime-database ]; then';
  echo '  update-mime-database ${PKG_INSTALL_ROOT}/usr/share/mime';
  echo 'fi';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -u -c SFE


  
%files
# TODO ##
# There's a whole lot of work to do here once the final includes/excludes and possibilities are finalised above but for now
# I've just pkged the main LO output of above excluding a bunch of gid_Module_* files in the root directory that I have
# no idea what to do with ATM
%defattr (-,root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libreoffice/


%files desktop-int
%defattr (-,root, bin)
%dir %attr (0755, root, bin) %_bindir
%attr (0755, root, bin) %ips_tag (mediator=libreoffice mediator-version=4.4) %{_bindir}/libreoffice4.4
%attr (0755, root, bin) %ips_tag (mediator=libreoffice mediator-version=4.4) %{_bindir}/loffice

%dir %attr(0755, root, root) %_datadir/mime
%dir %attr(0755, root, root) %_datadir/mime/packages
%attr (0644, root, bin) %ips_tag (mediator=libreoffice mediator-version=4.4) %{_datadir}/mime/packages/libreoffice4.4.xml

%dir %attr (0755, root, other) %{_datadir}/application-registry
#%{_datadir}/application-registry/libreoffice4.4.applications
%attr (0644, root, bin) %ips_tag (mediator=libreoffice mediator-version=4.4) %{_datadir}/application-registry/libreoffice4.4.applications

%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/applications
#%{_datadir}/applications/*.desktop
%attr (0644, root, other) %ips_tag (mediator=libreoffice mediator-version=4.4) %{_datadir}/applications/*.desktop

%dir %attr(0755, root, other) %{_datadir}/mime-info
#%{_datadir}/mime-info/libreoffice4.4.keys
#%{_datadir}/mime-info/libreoffice4.4.mime
%attr (0644, root, bin) %ips_tag (mediator=libreoffice mediator-version=4.4) %{_datadir}/mime-info/libreoffice4.4.keys
%attr (0644, root, bin) %ips_tag (mediator=libreoffice mediator-version=4.4) %{_datadir}/mime-info/libreoffice4.4.mime

%dir %attr (0755, root, other) %{_datadir}/pixmaps
#%{_datadir}/pixmaps/*.png
%attr (0644, root, other) %ips_tag (mediator=libreoffice mediator-version=4.4) %{_datadir}/pixmaps/*.png


%changelog
* Sat Sep 24 2016 - pjama
- add patch to enable update of libwps from 0.3.x to 0.4.x
- gsed hack of configure.ac to look for and use libwps-0.4
- set openindiana OI151a[89] to require library/python-2/importlib-26 to go with it's dirty old python 2.6
- fix (?) path to files it looked for in compiletry (ie prepend "/workdir" to path) because I think typo. Tomww please confirm.
- Add tags in the %files area to enable mediated versions for libreoffice4-desktop-int package
* Sat Apr 23 2016 - Thomas Wagner
- add patch6 libreoffice-06-hypot-cast-args.diff first seen on (S12)
  error: call of overloaded 'hypot(long int, long int)' is ambiguous
* Fri Apr 22 2016 - Thomas Wagner
- remove -D_GLIBCXX_USE_C99_MATH for (S12)
- change (Build)Requires to SFEharfbuzz-gpp SFEgraphite2-gpp (added -gpp)
* Thu Apr 21 2016 - Thomas Wagner
- add patch5 new procfs.h (S12) contributed by Jaffar
* Mon Jan  4 2016 - Thomas Wagner
- add to CXXFLAGS -D_GLIBCXX_USE_C99_MATH to avoid std::isnan and isnan conflicting (S11 S12)
- add patch to coinmp as it uses unquoted >"< in a warning macro and uses typeof in wrong context
  inject this patch into external/coinmp/UnpackedTarball_coinmp.mk
* Sun Jan  3 2016 - Thomas Wagner
- bump to 4.4.7.2 to get fix for CVE-2015-5214 DOC Bookmark Status Memory Corruption (fixed in 4.4.6)
- escape >"< in the warning macro CoinSignal.hpp:107
- remove  '/CppunitTest_sw_ooxmlimport/d' from sw/Module_sw.mk (pjama)
* Sun Nov 29 2015 - Thomas Wagner
- make automatic renamed packge to remove old SFElibreoffice4 in case we are on (OIH)


- use pnm_macros for (Build)Requires pnm_buildrequires_library_python_importlib pnm_buildrequires_icu_gpp_default pnm_requires_library_nspr pnm_buildrequires_library_neon pnm_buildrequires_SUNWopenssl_include pnm_buildrequires_bison pnm_buildrequires_image_library_libpng pnm_buildrequires_library_expat pnm_buildrequires_jdk_default
- on S11 S12 (Build)Require our SFEpoppler-gpp wich is newer
- add renamed-to SFElibreoffice4 -> libreoffice4
- make solaris.mk find libs in /usr/g++/libs
- use calculated cpu/memory value for number of parallel build processes $CPUS / $PARALELLISM_OPTION
- point PKG_CONFIG_PATH to apr location
- use pnm %{boost_gpp_default_prefix} to set BOOSTPREFIX
- add -std=c++11 -D_GLIBCXX_USE_C99_MATH -pthreads in case we are on (S11, S12)
- set LD=/usr/bin/ld on (S12)
- set variables MSPUB_CFLAGS MSPUB_LIBS NSS_LIBS and PATCH to find genbrk and icu-config
- fix variable exttarballdir to cache downloaded tarfiles locally
- remove from configure.ac/ CXXFLAGS which might inject too many -std=<...> on (S12)
- elfedit runpath for LO libraries
*     Oct 29 2015
- add patches libreoffice-03-config-CPUs.patch libreoffice-04-no-symbols-ld-complains.diff
- (date unknown) add (Build)Requires bzip, gnome_media, gstreamer/plugin/base, cups_libs, library_libxml2, system_library_fontconfig system_library_libdbus_glib, system_library_math
- special (Build)Requires pnm_buildrequires_gdb  (cppunit tests)
* Sun Sep 20 2015 - pjama
- Remove /usr/lib from LDFLAGS as shouldn't be required
- Made SFEgcc a requirement. There's issues with the hipster gcc. Gcc version needs to be different to hipter's.
-  although it does "run" with hipster gcc 4.8.5 even if compiled with SFE gcc 4.7.4
- added ALL to launguages instead of blank which defaults to en-US
- add --with-myspell-dicts to include LO Dictionaries
- add --with-help=common to include common help
- included apr in pkg-config path
- added gfortan vars... not sure why yet apart from configure looks for it
- much desktop integration
- add --enable-cups so we find printers
* Thu Sep 20 2015 - pjama
- Many changes to support OI151a9
- PNM package Reqs and add many more Reqs (still not complete)
- Changes to include /usr/g++/lib and /usr/gnu/lib early in RPATH
- mods to fix '-j CPUS' vs parallelism. Patch configure.ac so configure sets right paralleism only when/where ok (ie not make 3.81)
- find and elfedit all .so files with dodgey RPATHs (included build directory)
- add --enable-release-build option to conf as it seems to fix RPATH issues
- remove xorg from FLAGS and include in configure options so it's only included in RPATH only where needed. Seems that everything but a few anyway.
- Added basic desktop integration files
* Thu Aug 20 2015 - Thomas Wagner
- add BuildRequires SFEzlib-pkgconfig, remove variables pointing to ZLIB
- use --with-boost=%{boost_gpp_default_prefix} for e.g. /usr/g++ (S11 S12 OI)
* Wed Aug 12 2015 - Thomas Wagner
- change (Build)Requires to %{pnm_requires_SUNWopenssl_include}, %include packagenamemacros.inc
* Tue Aug 11 2015 - Thomas Wagner
- initial submit 4.4.5.2
- add IPS_Package_Name
- thanks to all contributors, especially pjama, tribblix and all those who have not lost interest in a office on solarish OS (Hi Ken! You tried it in 2013!)
* Mon Aug 10 2015 - Thomas Wagner
- renamed the ugly initial experimental spec to SFElibreoffice4.spec
- add IPS_Package_Name for the beginning as libreoffice4, should probably be accomanied by a top-level unversioned package name providing mediators to different office implementations
- add (Build)Requires developer_gperf
#####- change to (Build)Requires %{pnm_buildrequires_SUNWzlib}, %{pnm_buildrequires_boost_gpp_default}, developer_icu, library_math_header_math, add SFExz_gnu
* Wed Jul 29 2015 - pjama
- ugly initial experimental spec
