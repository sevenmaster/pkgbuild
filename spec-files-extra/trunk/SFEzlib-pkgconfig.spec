#
#  add missing "zlib.pc" files of the osdistro doesn't deliver it
#
#  note: this package may be empty and only deliver a "renamed-to" information
#  telling IPS to go forward and just use the osdistro provided zlib package (.... w/ is updated to contain zlib.pc)
#

%include Solaris.inc
%include osdistro.inc
%include pkgbuild-features.inc

%define deliver_files 1
%define deliver_no_files 0

%if %( expr %{solaris11} '&' %{osdistro_entire_padded_number4}.1 '>=' 0000017500030009000000030000.1 )
%define deliver_files 0
%define deliver_no_files 1
%endif

%if %( expr %{solaris12} '&' %{osdistro_entire_padded_number4}.1 '>=' 0005001200000000000000870000.1 )
%define deliver_files 0
%define deliver_no_files 1
%endif

#generate only the renamed package: --define 'zlib_renamed_package 1'
#%if %{!?zlib_renamed_package:1}
%if %{?zlib_renamed_package:1}0
%define deliver_files 0
%define deliver_no_files 1
%else
%define zlib_renamed_package 0
%endif

%define _use_internal_dependency_generator 0

#this works because library/zlib must be preinstalled, so we can ask for the version that is currently installed
%define version_zlib %( LC_ALL=C pkg info library/zlib | grep Version | awk -F':' '{print $2}' | sed -e 's? *??' )

%if %{deliver_no_files}
IPS_Component_Version:   %{version_zlib}.0.1
%endif

Name:                SFEzlib-pkgconfig
IPS_Package_Name:   library/zlib/pkgconfig/zlib.pc
Version:             %{version_zlib}
Summary:             Add missing zlib.pc for pkg-config

SUNW_BaseDir:        %{_prefix}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

BuildRequires: library/zlib
Requires:      library/zlib

%if %{deliver_no_files}
#this tries to obsolete the helper package delivering the files zlib.pc, as Solaris 12 build 87 and up now have that file in library/zlib package
%if %(expr %{solaris11} '+' %{solaris12} '>=' 1 )
#START automatic renamed package  (remember to add as well %actions)
# create automatic package with old name and "renamed=true" in it
%include pkg-renamed.inc
#exception, as we don't deliver files on certain osdistro build versions, then our package is empty and is not allowed to have a (default: unknown) license file
Meta(pkg.renamed): true
PkgBuild_Make_Empty_Package: true
ips_legacy: false
%endif
####END solaris11 solaris 12
#S11 S12

#                                           '5.12.0.0.0.88.0'
#pnm: osdistro_entire    5.12.0.0.0.87.0
# osdistro_entire_padded_number4 0005001200000000000000870000

# %define obsolete_in_build_entire_release_name 
#   IPS_Component_Version:
#     Sets the component version portion of the IPS package version string,
#     as described in pkg(5).  For example 2.20 in the case of this package:
# 
#     gtk2@2.20.0,5.11-0.133:<timestamp>
# 
#   IPS_Build_Version:
#     Sets the build version portion of the IPS version string.  5.11 in the
#     above example.  See pkg(5).
# 
#   IPS_Vendor_Version:
#     Sets the vendor-specific branch version portion of the IPS version
#     string, 0.133 in the above example.  See pkg(5).
# 
# 
#                #pkg://solaris/entire@5.12-5.12.0.0.0.87.0:20151102T151225Z
#  #pkg://solaris/release/name@5.12-5.12.0.0.0.87.0:20151102T143134Z
# 
# 
# strategy: always build a package renamed-to with the regular name IPS_Package_Name:   library/zlib/pkgconfig/zlib.pc
# it depends on the release/name packages beginning in version 5.12-5.12.0.0.0.87.0
# it redirects with "renamed to" to Solaris12 package:  pkg://solaris/library/zlib
# pkg contents -r -m library/zlib@1.2.8-5.12.0.0.0.87 | grep zlib.pc  -->> YES

#This is specific to Solaris 11
#This is specific to Solaris 12 
%package noinst-1
%define renamed_from_oldname      library/zlib/pkgconfig/zlib.pc
#%define renamed_to_newnameversion library/zlib = *
%if %{solaris11}
Summary:     Solaris 11 up to build 86 has not zlib.pc file, starting with build 87 this packages removes the helper package SFEzlib-pkgconfig or library/zlib/pkgconfig/zlib.pc
#                                      zlib@1.2.8,5.11-0.175.3.9.0.3.0
%define renamed_to_newnameversion library/zlib = 1.2.8-0.175.3.9.0.3.0
#                                   entire@0.5.11,5.11-0.175.3.9.0.4
%endif
%if %{solaris12}
Summary:     Solaris 12 up to build 86 has not zlib.pc file, starting with build 87 this packages removes the helper package SFEzlib-pkgconfig or library/zlib/pkgconfig/zlib.pc
%define renamed_to_newnameversion library/zlib = 1.2.8-5.12.0.0.0.87
%endif

%include pkg-renamed-package.inc

#list all the old published package name wich need to go away with upgrade to our new package name/location
#special case here, as we want the renamed part only be effective on S12 build 87 and up, we need to put a dependency on that release/name@5.12,5.12-5.12.0.0.0.87
#release/name can be "optional" as it is normally present and then it needs to have at least this revision
%actions
depend fmri=library/zlib/pkgconfig/zlib.pc@%{version_zlib} type=optional
%if %{solaris12}
depend fmri=release/name@5.12-5.12.0.0.0.87 type=optional
%endif
%if %{solaris11}
#depend fmri=release/name@5.11-0.175.3.1.0.5.0 type=optional
#depend fmri=entire@0.5.11,5.11-0.175.3.9.0.4 type=optional
#once this package is available, ask to have it in this minimum version
depend fmri=library/zlib@1.2.8-0.175.3.9.0.3 type=optional
%endif

%endif
#END deliver_no_files



%description
Special package to add zlib.pc, the information file for
pkg-config which tells the automatic configuration process
for compiling software where the library zlib is found
and which compiler includes and linker informations are
needed.

Note: This packages determines the zlib version at compile
time of the package. If the OS has an updates zlib library,
then the content of this packge with zlib.pc is most likely
in the need to be updated too.

%if %{solaris12}
This package has been compiled on a system build 87 or later,
it will stop delivering any files. The system zlib contains the
necessary zlib.pc files. The package IPS feature "renamed-to"
ensures that this packages will be uninstalled automatically
if the required conditions are met.
%endif

%prep
%setup -T -c -n %name-%version


%build

%if %{deliver_no_files}
#just to keep the build machine past build 87 running the build without publishing errors
echo "Do not deliver any files in this package on a build machine with recent osdistro, as the OS distro package zlib already has files zlib.pc"
%else 
echo "Do deliver the missing files /usr/lib/pkgconfig/zlib.pc and /usr/lib/<amd64|sparcv9>pkgconfig/zlib.pc"
echo "If you want to build a package with only the renamed-to info, then use pkgtool --define 'zlib_renamed_package 1' build %{name}"
%endif

echo "
switch to deliver files is set to %{deliver_files}
pnm: osdistrelnumber    %{osdistrelnumber}
pnm: osdistrelname      %{osdistrelname}
pnm: osdistro_entire    %{osdistro_entire}
pnm: osdistro_entire_padded_number4 %{osdistro_entire_padded_number4}
selection: zlib_renamed_package	%{zlib_renamed_package}
switch:    deliver_files	%{deliver_files}
switch:    deliver_no_files	%{deliver_no_files}
"

%install
rm -rf $RPM_BUILD_ROOT

echo "
switch to deliver files is set to %{deliver_files}
pnm: osdistrelnumber    %{osdistrelnumber}
pnm: osdistrelname      %{osdistrelname}
pnm: osdistro_entire    %{osdistro_entire}
pnm: osdistro_entire_padded_number4 %{osdistro_entire_padded_number4}
selection: zlib_renamed_package	%{zlib_renamed_package}
switch:    deliver_files	%{deliver_files}
switch:    deliver_no_files	%{deliver_no_files}
"

%if %{deliver_no_files}
#just to keep the build machine past build 87 running the build without publishing errors
echo "Do not deliver any files in this package on a build machine with recent osdistro, as the OS distro package zlib already has files zlib.pc"

%else
echo "Do deliver the missing files /usr/lib/pkgconfig/zlib.pc and /usr/lib/<amd64|sparcv9>pkgconfig/zlib.pc"
#we deliver the missing files. Remember: on certain osdistro this package needs to be a "renamed" package which uninstalles itself if osdistro gets updated beyond a specific build release
mkdir -p $RPM_BUILD_ROOT/usr/lib/pkgconfig
mkdir -p $RPM_BUILD_ROOT/usr/lib/%{_arch64}/pkgconfig

#32-bit
cat - > $RPM_BUILD_ROOT/usr/lib/pkgconfig/zlib.pc << --EOF--
prefix=/usr
exec_prefix=\${prefix}
libdir=\${exec_prefix}/lib
sharedlibdir=\${libdir}
includedir=\${prefix}/include

Name: zlib
Description: zlib compression library
Version: %{version}

Requires:
Libs: -L\${libdir} -L\${sharedlibdir} -lz
Cflags: -I\${includedir}
--EOF--

#64-bit
cat - > $RPM_BUILD_ROOT/usr/lib/%{_arch64}/pkgconfig/zlib.pc << --EOF2--
prefix=/usr
exec_prefix=\${prefix}
libdir=/usr/lib/%{_arch64}/
sharedlibdir=\${libdir}
includedir=\${prefix}/include

Name: zlib
Description: zlib compression library
Version: %{version}

Requires:
Libs: -L\${libdir} -L\${sharedlibdir} -lz
Cflags: -I\${includedir}
--EOF2--
##END all other osdistro. Exception is S12 past build 86, that is 87 and later and this delivers no files any more
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%if %{deliver_files}
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%endif


%changelog
* Wed Jun 08 2016 - Thomas Wagner
- add renamed-to for pkg://solaris/library/zlib@1.2.8,5.11-0.175.3.9.0.3.0 (S11 SRU9)
- add switch to generate the "renamed to" package on any release of the target OS
  --define 
* Sun Apr 24 2016 - Thomas Wagner
- make this package deliver no files and trigger "renamed-to" library/zlib
  if compiled (installed) on a system matching the conditions: S12 build >= 87 (S12)
  specific osdistro and build-number >= high enough to have library/zlib contain zlib.pc files
* Thu Aug 20 2015 - Thomas Wagner
- Initial spec - add missing files "zlib.pc" for platforms which have zlib but are missing zlib.pc for pkg-config
