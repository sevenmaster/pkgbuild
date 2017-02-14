#
# NoCopyright 2009 - Gilles Dauphin (from Fedora 10)
#

%include Solaris.inc
%include packagenamemacros.inc

%define osbuild %(uname -v | sed -e 's/[A-z_]//g')

%ifarch x86_64
%define java_arch amd64
%else
%define java_arch %{_arch}
%endif

%define src_version	2.8.1
%define src_name	R

Name:			SFEr
IPS_Package_Name:	math/r
Version:		2.15.0
Summary:		A language for data analysis and graphics
URL:			http://www.r-project.org
License:		GPLv2+
SUNW_Copyright: 	%{name}.copyright
Group:			Applications/Math
Source:			ftp://cran.r-project.org/pub/R/src/base/R-2/R-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{src_version}-build

Requires: library/readline
Requires: SFElapack
Requires: SUNWpng
Requires: SUNWjpg
Requires: SUNWTcl
Requires: SUNWncurses
Requires: SUNWpcre
Requires: SUNWzlib

BuildRequires:  %{pnm_buildrequires_SUNWTk_devel}
Requires:       %{pnm_requires_SUNWTk}

#Requires: SUNWxwrtl
Requires: SUNWbzip
Requires: SUNWgnome-base-libs
Requires: SUNWTiff
# %if %(expr %{osbuild} '>=' 134)
# Requires: developer/sunstudioexpress
# %else
# Requires: SPROcc
# Requires: SPROcmpl
# Requires: SPROf90
# Requires: SPROftool
# # TODO
# #BuildRequires: tetex-latex, texinfo-tex 
# %endif

Meta(info.upstream):		cran.r-projet.org
Meta(info.maintainer):		Gilles Dauphin
Meta(info.repository_url):	ftp://ftp.stat.math.ethz.ch/Software/R

%description
R is a language and environment for statistical computing and graphics. 
R is similar to the award-winning S system, which was developed at 
Bell Laboratories by John Chambers et al. It provides a wide 
variety of statistical and graphical techniques (linear and
nonlinear modelling, statistical tests, time series analysis,
classification, clustering, ...).

R is designed as a true computer language with control-flow
constructions for iteration and alternation, and it allows users to
add additional functionality by defining new functions. For
computationally intensive tasks, C, C++ and Fortran code can be linked
and called at run time.

%prep
%setup -q -n %{src_name}-%{version}
#%patch1 -p1 -b .filter-little-out

%build
# Add PATHS to Renviron for R_LIBS
echo 'R_LIBS=${R_LIBS-'"'%{_libdir}/R/library:%{_datadir}/R/library'"'}' >> etc/Renviron.in

export R_PDFVIEWER="%{_bindir}/xdg-open"
export R_PRINTCMD="lpr"
export R_BROWSER="%{_bindir}/xdg-open"

# because of foreign -Wno-long-long !!! Argh :(
export ac_cv_prog_CC="cc -m32"
export CC="cc -m32"
export CXX="CC -m32"
export CXXFLAGS="-library=stlport4"
export SHLIB_CXXFLAGS="-library=stlport4"
export SHLIB_CXXLD="CC -m32 "
export SHLIB_CXXFLAGS="-library=stlport4"
export SHLIB_CXXLDFLAGS="-G -library=stlport4"
export F77="f95 -m32"
export FC="f95 -m32"

export FCFLAGS="%{optflags}"
export CPPFLAGS="-I/usr/gnu/include"
export LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib"
( ./configure \
--prefix=%{_prefix}                 \
    --libexecdir=%{_libexecdir}         \
    --mandir=%{_mandir}                 \
    --datadir=%{_datadir}               \
    --infodir=%{_datadir}/info          \
    --with-system-zlib --with-system-bzlib --with-system-pcre \
    --with-lapack \
    --with-tcl-config=%{_libdir}/tclConfig.sh \
    --with-tk-config=%{_libdir}/tkConfig.sh \
    --enable-R-shlib \
    --with-tcl-config=/usr/lib/tclConfig.sh \
    --with-tk-config=/usr/lib/tkConfig.sh \
    rdocdir=%{_docdir}/R-%{version} \
    rincludedir=%{_includedir}/R \
    rsharedir=%{_datadir}/R) \
 | grep -A30 'R is now' - > CAPABILITIES
make 
(cd src/nmath/standalone; make)
#make check-all
make pdf
make info

#  TODO
# Convert to UTF-8
#for i in doc/manual/R-intro.info doc/manual/R-FAQ.info-1 doc/FAQ doc/manual/R-exts.info-1; do
#  iconv -f iso-8859-1 -t utf-8 -o $i{.utf8,}
#  mv $i{.utf8,}
#done

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=${RPM_BUILD_ROOT} install install-info install-pdf
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir.old
mkdir -p ${RPM_BUILD_ROOT}%{_docdir}/R-%{version}
install -p CAPABILITIES ${RPM_BUILD_ROOT}%{_docdir}/R-%{version}

#Install libRmath files
(cd src/nmath/standalone; make install DESTDIR=${RPM_BUILD_ROOT})

mkdir -p $RPM_BUILD_ROOT%{_datadir}/R/library

# Fix exec bits
chmod +x $RPM_BUILD_ROOT%{_datadir}/R/sh/echo.sh
chmod -x $RPM_BUILD_ROOT%{_libdir}/R/library/mgcv/CITATION ${RPM_BUILD_ROOT}%{_docdir}/R-%{version}/CAPABILITIES

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/R
%{_libdir}/pkgconfig/*
%{_libdir}/R/*
%{_libdir}/libRmath.*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_datadir}/R/*
%{_datadir}/info/*
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/R/*
%{_includedir}/Rmath.h


%clean
rm -rf ${RPM_BUILD_ROOT};

#%post
# Create directory entries for info files
# (optional doc files, so we must check that they are installed)
#for doc in admin exts FAQ intro lang; do
#   file=%{_infodir}/R-${doc}.info.gz
#   if [ -e $file ]; then
#      /sbin/install-info ${file} %{_infodir}/dir 2>/dev/null || :
#   fi
#done
#/sbin/ldconfig
#R CMD javareconf \
#    JAVA_HOME=%{_jvmdir}/jre \
#    JAVA_CPPFLAGS='-I%{_jvmdir}/java/include\ -I%{_jvmdir}/java/include/linux' \
#    JAVA_LIBS='-L%{_jvmdir}/jre/lib/%{java_arch}/server \
#    -L%{_jvmdir}/jre/lib/%{java_arch}\ -L%{_jvmdir}/java/lib/%{java_arch} \
#    -L/usr/java/packages/lib/%{java_arch}\ -L/lib\ -L/usr/lib\ -ljvm' \
#    JAVA_LD_LIBRARY_PATH=%{_jvmdir}/jre/lib/%{java_arch}/server:%{_jvmdir}/jre/lib/%{java_arch}:%{_jvmdir}/java/lib/%{java_arch}:/usr/java/packages/lib/%{java_arch}:/lib:/usr/lib \
#    > /dev/null 2>&1 || exit 0

# Update package indices
#%__cat %{_libdir}/R/library/*/CONTENTS > %{_docdir}/R-%{version}/html/search/index.txt 2>/dev/null
# Don't use .. based paths, substitute RHOME
#sed -i "s!../../..!%{_libdir}/R!g" %{_docdir}/R-%{version}/html/search/index.txt

# This could fail if there are no noarch R libraries on the system.
#%__cat %{_datadir}/R/library/*/CONTENTS >> %{_docdir}/R-%{version}/html/search/index.txt 2>/dev/null || exit 0
# Don't use .. based paths, substitute /usr/share/R
#sed -i "s!../../..!/usr/share/R!g" %{_docdir}/R-%{version}/html/search/index.txt


#%preun core
#if [ $1 = 0 ]; then
#   # Delete directory entries for info files (if they were installed)
#   for doc in admin exts FAQ intro lang; do
#      file=%{_infodir}/R-${doc}.info.gz
#      if [ -e ${file} ]; then
#         /sbin/install-info --delete R-${doc} %{_infodir}/dir 2>/dev/null || :
#      fi
#   done
#fi
#
#%postun core -p /sbin/ldconfig

#%post java
#R CMD javareconf \
#    JAVA_HOME=%{_jvmdir}/jre \
#    JAVA_CPPFLAGS='-I%{_jvmdir}/java/include\ -I%{_jvmdir}/java/include/linux' \
#    JAVA_LIBS='-L%{_jvmdir}/jre/lib/%{java_arch}/server \
#    -L%{_jvmdir}/jre/lib/%{java_arch}\ -L%{_jvmdir}/java/lib/%{java_arch} \
#    -L/usr/java/packages/lib/%{java_arch}\ -L/lib\ -L/usr/lib\ -ljvm' \
#    JAVA_LD_LIBRARY_PATH=%{_jvmdir}/jre/lib/%{java_arch}/server:%{_jvmdir}/jre/lib/%{java_arch}:%{_jvmdir}/java/lib/%{java_arch}:/usr/java/packages/lib/%{java_arch}:/lib:/usr/lib \
#    > /dev/null 2>&1 || exit 0

#%post java-devel
#R CMD javareconf \
#    JAVA_HOME=%{_jvmdir}/jre \
#    JAVA_CPPFLAGS='-I%{_jvmdir}/java/include\ -I%{_jvmdir}/java/include/linux' \
#    JAVA_LIBS='-L%{_jvmdir}/jre/lib/%{java_arch}/server \
#    -L%{_jvmdir}/jre/lib/%{java_arch}\ -L%{_jvmdir}/java/lib/%{java_arch} \
#    -L/usr/java/packages/lib/%{java_arch}\ -L/lib\ -L/usr/lib\ -ljvm' \
#    JAVA_LD_LIBRARY_PATH=%{_jvmdir}/jre/lib/%{java_arch}/server:%{_jvmdir}/jre/lib/%{java_arch}:%{_jvmdir}/java/lib/%{java_arch}:/usr/java/packages/lib/%{java_arch}:/lib:/usr/lib \
#    > /dev/null 2>&1 || exit 0

%changelog
* Tue Mar 22 2016 - Thomas Wagner
- change (Build)Requires to  %{pnm_buildrequires_SUNWTk_devel}
* Sun Dec  9 2012 - Thomas Wagner
- remove noisy comments
- clean %files
* Sun Jun 24 2012 - Thomas Wagner
- remove Requires: SFEblas (archived, use SFElapack instead)
- rename spec file and Package Name to SFEr.spec (sfe always uses lowercase names)
* Sat Apr 14 2012 - Logan Bruns <logan@gedanken.org>
- bumped to 2.15.0, switched to use gnu iconv since iconv is no longer
  optional, added ips name, various minor fixes
* Thu Apr 16 2009 - Gilles Dauphin
- inital config (from fedora)
