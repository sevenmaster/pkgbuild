#functions get version numbers starting with ICU 49
#read: http://userguide.icu-project.org/design paragraph ICU Binary Compatibility: Using ICU as an Operating System Level Library
#if set --disable-renaming then you *need* every consumter be rebuilt to match features / functions of the icu version used at compile time
#pkgtool --with-disable_renaming
%define with_disable_renaming %{?_with_disable_renaming:1}%{?!_with_disable_renaming:0}



# beware! If you recompile this spec file while another, older lib of the same is still 

#         installed on your system, you most likely run into "symbol not found"

#         errors. Try uninstalling the previous icu and its dependents before the new compile run!

#         display one level of the installed dependency chain with "pkg search :depend:require:library/g++/icu"

#         (repeat for each dependency found then uninstall in reverse order)


#         or, if you have, use "cd spec-files-extra; pkgtool-uninstall-recoursive SFEicu-gpp.spec"


#
# spec file for package SFEicu
#
# includes module(s): icu
#

# The reason that SFEicu is required is that library/icu is built against
# libcStd, whereas some libraries such as Boost require ICU but do not
# build against libcStd.

# This package does not conflict with library/icu because its base directory
# is /usr/g++.

%include Solaris.inc
%include buildparameter.inc
%include usr-g++.inc
%define cc_is_gcc 1
%include base.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use icu_64 = icu.spec
%endif

%include usr-g++.inc
%include base.inc
%use icu = icu.spec

Name:			SFEicu-gpp
IPS_Package_Name:	library/g++/icu
Summary:		%icu.summary (/usr/g++)
Version:		%icu.version
URL:			http://site.icu-project.org/
License:		BSD.icu
SUNW_Copyright:		icu.copyright
SUNW_BaseDir:		%_basedir
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#BuildRequires:		SFEgcc
#Requires:		SFEgccruntime

%package devel
Summary:		%{summary} - development files
SUNW_BaseDir:		%{_basedir}
%include default-depend.inc
Requires: %name

%description 
ICU is a mature, widely used set of C/C++ and Java libraries providing 
Unicode and Globalization support for software applications. ICU is widely 
portable and gives applications the same results on all platforms and 
between C/C++ and Java software.

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%icu_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%icu.prep -d %name-%version/%{base_arch}

%build

export MAKE_CPUS=%{_cpus_memory}

%ifarch amd64 sparcv9
%icu_64.build -d %name-%version/%_arch64
%endif

%icu.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%icu_64.install -d %name-%version/%_arch64
%endif

%icu.install -d %name-%version/%base_arch

##TODO## link isaexec

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/derb
%{_bindir}/genbrk
%{_bindir}/gencfu
%{_bindir}/gencnval
#%{_bindir}/genctd
%{_bindir}/gendict
%{_bindir}/genrb
%{_bindir}/icu-config
%{_bindir}/icuinfo
%{_bindir}/makeconv
%{_bindir}/pkgdata
%{_bindir}/uconv
%ifarch amd64 sparcv9
%_bindir/%_arch64
%endif

%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/genccode
%{_sbindir}/gencmn
%{_sbindir}/gennorm2
%{_sbindir}/gensprep
%{_sbindir}/icupkg

%ifarch amd64 sparcv9
%_sbindir/%_arch64
%endif

%dir %attr (0755, root, sys) %{_datadir}
%_datadir/icu/%version
%_mandir/man1
%_mandir/man8

%{_libdir}/lib*.so*
%{_libdir}/icu
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/icu
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %_libdir/pkgconfig 
%_libdir/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %_libdir/%_arch64/pkgconfig 
%_libdir/%_arch64/pkgconfig/*
%endif


%changelog
* Fri Jan  8 2016 - Thomas Wagner
- add back accidentially deleted compile time switch and the explanation
* Sun Oct 11 2015 - Thomas Wagner
- add missing include usr-g++.inc
- add parallel build
* Sun Aug 23 2015 - Thomas Wagner
- remove wrong --disable-renamings, as it causes unkown symbol errors in consuming libaries (e.g. libvisio, libmspub)
- remove unrecognized configure opts: --disable-warnings, --disable-dependency-tracking, --enable-threads
- add switch (default off) to build icu without the function renaming for testing (don't switch that on in normal cases)
* Tue Aug 18 - 2015 Thomas Wagner
- really submit missing patches with propper names and numbering, and apply them
- move -std=c99 to CFLAGS
- fix %files for %{_bindir}/genctd now %{_bindir}/gendict
* Tue Aug 18 2015 - Thomas Wagner
- add missing patches
* Sat Aug  8 - 2015 Thomas Wagner
- moved %build up before configure step to solve "make" running without our ENV variables (CFLAGS,...)
- bump to 55.1
- imported new patch0 - patch7 from OI Userland
* Thu Jun 23 2011 - Alex Viskovatoff
- Fork SFEicu-gpp.spec off SFEicu.spec
* Mon Apr 11 2011 - Alex Viskovatoff
- Package pkgconfig files
* Sat Nov 20 2010 - Alex Viskovatoff
- Create new spec using base spec from kde-solaris modified for SFE, with
  some code taken from FOSSicu4c.spec
