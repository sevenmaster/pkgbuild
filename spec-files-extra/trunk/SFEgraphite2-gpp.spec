#
# spec file for package SFEgraphite2
#
# includes module: graphite2
#

%include Solaris.inc
%include usr-g++.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc
%define _use_internal_dependency_generator 0

%define	src_name	graphite2

Name:			SFEgraphite2-gpp
IPS_Package_Name:	library/g++/graphite2
Summary:		SILgraphite - rendering engine for complex scripts
Group:			System/Libraries
Version:		1.2.4
URL:			http://silgraphite.sourceforge.net/
License:		LGPLv2
SUNW_Copyright:		%{license}.copyright
#http://sourceforge.net/projects/silgraphite/files/graphite2/graphite2-1.2.4.tgz/download
Source:			%{sf_download}/silgraphite/%{version}/%{src_name}-%{version}.tgz
#imported from OI userland, thanks much!
Patch1:			graphite2-01-install-paths.patch
Patch2:			graphite2-02-examples-libstdc++.patch
Patch3:			graphite2-debian-01-include-and-libraries.patch
Patch4:			graphite2-debian-02-no-icons.patch
Patch5:			graphite2-debian-03-no-specific-nunit-version.patch
Patch6:			graphite2-debian-04-non-linux.patch

SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%name-%version-build

%include default-depend.inc

%description
Graphite is a project within SIL's scripts and software dev groups to provide cross-platform rendering for complex writing systems.

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name



%prep
%setup -q -n %{src_name}-%{version}

%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I/usr/g++/include"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"

mkdir build
cd build

#same cmake options as in OI userland

cmake .. \
       -DCMAKE_INSTALL_PREFIX=%{_prefix} \
       -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Release \
    -DGRAPHITE2_ASAN=OFF \
    -DGRAPHITE2_COMPARE_RENDERER=OFF \
    -DGRAPHITE2_DOXYGEN_CONFIG=public \
    -DGRAPHITE2_NFILEFACE=OFF \
    -DGRAPHITE2_NSEGCACHE=OFF \
    -DGRAPHITE2_NTRACING=ON \
    -DGRAPHITE2_TELEMETRY=OFF \
    -DGRAPHITE2_VM_TYPE=auto \
    -DLATEX=/usr/bin/latex

gmake -j$CPUS
gmake test

%install
rm -rf $RPM_BUILD_ROOT
cd build
gmake install DESTDIR=$RPM_BUILD_ROOT

%if %{cc_is_gcc}
#libstdc++.so.6 defines the missing symbols
#ldd -r /usr/g++/lib/libgraphite2.so.3.0.1                                                                             
#[...]
#        symbol not found: _ZTVN10__cxxabiv120__si_class_type_infoE              (/usr/g++/lib/libgraphite2.so.3.0.1)
#[...]

#get missing symbols, e.g. ffmpeg testing libass, then fail with unresolved symbols for libgraphite2.so
#in ffmpeg configure when testing for libass you see:
#Undefined                       first referenced
# symbol                             in file
#vtable for __cxxabiv1::__si_class_type_info /usr/g++/lib/libgraphite2.so.3
#__cxa_call_unexpected               /usr/g++/lib/libgraphite2.so.3
#vtable for __cxxabiv1::__class_type_info /usr/g++/lib/libgraphite2.so.3
#__gxx_personality_v0                /usr/g++/lib/libgraphite2.so.3
#ld: fatal: symbol referencing errors. No output written to /tmp/ffconf.zexGdUP4

echo "editing into elf-header of src/libgraphite2.so:   NEEDED libstdc++.so.6"
/usr/bin/elfdump -d src/libgraphite2.so > elf-header.before
/usr/bin/elfedit -e 'dyn:value -add -s NEEDED libstdc++.so.6' src/libgraphite2.so
/usr/bin/elfdump -d src/libgraphite2.so > elf-header.after
echo "Diff of elf-header"
if gdiff -u0 elf-header.before elf-header.after ;
  then
   echo "ERROR: editing in the libstdc++.so.6 as a NEEDED library in libgraphite2.so has failed"
  else
   #gdiff tells us there is a difference, which is what we want to see
   echo "ok"
fi
%endif

find $RPM_BUILD_ROOT -name '*.la' -exec rm {} \; -o -name '*.a'  -exec rm {} \;


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %_bindir
%_bindir/*

%dir %attr (0755, root, bin) %_libdir
%_libdir/*.so*

%dir %attr (0755, root, sys) %_datadir
%_datadir/%src_name/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/%src_name.pc
%dir %attr (0755, root, bin) %_includedir
%dir %_includedir/%src_name
%_includedir/%src_name/*


%changelog
* Sat Feb 27 2016 - Thomas Wagner
- link in libstdc++.so.6 to fix ffmpeg build failing when probing for libass which
  uses libgraphite2 which then has unresolved symbols (missing libstdc++.so.6)
* Fri Feb 26 2016 - Thomas Wagner
- change back SVR4 name to SFEgraphite-gpp or this breakes automatic solve for dependcies (regression from rev 6136)
* Sat Jan  2 2016 - Alex Viskovatoff <herzen@imap.cc>
- Change SVr4 name to maintain consistency with IPS name
* Mon Aug 10 2015 - Thomas Wagner
- initial spec, obsoletes older SFEsilgraphite.spec
##TODO## make a 32/64 bit package
