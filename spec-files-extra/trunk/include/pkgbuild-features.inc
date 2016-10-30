#
# pkgbuild-features.inc
#
#
# make extra features of pkgbuild versions
# easily enabled or disabled in spec files
# reason: pkgbuild 1.3.103 doesn't understand
# tags which pkgbuild 1.3.104 and later do,
# e.g. "Renamed_To:"

# example: if pkgbuild 1.3.104 is used, 
# you may start using IPS_Legacy tags and
# some more
# %if %( expr %{pkgbuild_ver_numeric} >= 001003104 )
# IPS_Legacy: false
# %endif


#examples:
#pkgbuild version 1.3.103
#pkgbuild version 1.3.104
#pkgbuild version 1.3.105
# use the "pkgbuild" tool which is found first by using "$PATH"
# %define pkgbuild_ver %( pkgbuild --version 2>&1 | head -1 | sed -e 's/.* //' )
%define pkgbuild_path %( which pkgbuild )
%define pkgbuild_ver %( egrep "^pkgbuild_dir|-I.*lib/pkgbuild" %{pkgbuild_path} | head -1 | sed -e '/pkgbuild/ s?.*pkgbuild-??' -e 's?/pkgbuild\.pl??'  -e 's?[^0-9\.]??g' )

%define pkgbuild_ver_1_3_103 0
%define pkgbuild_ver_1_3_104 0
%define pkgbuild_ver_1_3_105 0
%define pkgbuild_ver_1_3_106 0
%define pkgbuild_ver_1_3_107 0
%define pkgbuild_ver_1_3_108 0
%define pkgbuild_ver_1_3_109 0
%define pkgbuild_ver_numeric 0
#features suported:
%define pkgbuild_ips_legacy  0
%define pkgbuild_renamed_to  0

%if %( echo %{pkgbuild_ver} | grep -w "1.3.103" >/dev/null && echo 1 || echo 0 )
%define pkgbuild_ver_1_3_103 1
%define pkgbuild_ver_numeric 001003103
#features suported:
%define pkgbuild_ips_legacy  0
%define pkgbuild_renamed_to  0
%endif
#1.3.103

%if %( echo %{pkgbuild_ver} | grep -w "1.3.104" >/dev/null && echo 1 || echo 0 )
%define pkgbuild_ver_1_3_104 1
%define pkgbuild_ver_numeric 001003104
#features suported:
%define pkgbuild_ips_legacy  1
%define pkgbuild_renamed_to  1
%endif
#1.3.104

%if %( echo %{pkgbuild_ver} | grep -w "1.3.105" >/dev/null && echo 1 || echo 0 )
%define pkgbuild_ver_1_3_105 1
%define pkgbuild_ver_numeric 001003105
#features suported:
%define pkgbuild_ips_legacy  1
%define pkgbuild_renamed_to  1
%endif
#1.3.105

%if %( echo %{pkgbuild_ver} | grep -w "1.3.106" >/dev/null && echo 1 || echo 0 )
%define pkgbuild_ver_1_3_106 1
%define pkgbuild_ver_numeric 001003106
#features suported:
%define pkgbuild_ips_legacy  1
%define pkgbuild_renamed_to  1
%endif
#1.3.106

%if %( echo %{pkgbuild_ver} | grep -w "1.3.107" >/dev/null && echo 1 || echo 0 )
%define pkgbuild_ver_1_3_107 1
%define pkgbuild_ver_numeric 001003107
#features suported:
%define pkgbuild_ips_legacy  1
%define pkgbuild_renamed_to  1
%endif
#1.3.107

%if %( echo %{pkgbuild_ver} | grep -w "1.3.108" >/dev/null && echo 1 || echo 0 )
%define pkgbuild_ver_1_3_108 1
%define pkgbuild_ver_numeric 001003108
#features suported:
%define pkgbuild_ips_legacy  1
%define pkgbuild_renamed_to  1
%endif
#1.3.108

%if %( echo %{pkgbuild_ver} | grep -w "1.3.109" >/dev/null && echo 1 || echo 0 )
%define pkgbuild_ver_1_3_109 1
%define pkgbuild_ver_numeric 001003109
#features suported:
%define pkgbuild_ips_legacy  1
%define pkgbuild_renamed_to  1
%endif
#1.3.109


#add more sections of new pkgbuild version add new feature
#so they can be excluded in case older pkgbuild version is active

#bailout, we weren't able to detect the pkgbuild version!
%if %(expr %{pkgbuild_ver_numeric} '=' 0 )
echo not able to detect supported pkgbuild version. fix include/pkgbuild-features.inc
echo do not remove these lines from file include/pkgbuild-features.inc
not able to detect supported pkgbuild version. fix include/pkgbuild-features.inc
do not remove these lines from file include/pkgbuild-features.inc
exit 1
%endif
#END not %{pkgbuild_ver_numeric}

%changelog
* Mon Jan 18 2016 - Thomas Wagner
- bail out in case pkgbuild_ver_numeric is 0
* Fri Jan  2 2015 - Thomas Wagner
- add more versions 1.3.105 .. 1.3.109
* Tue Oct  8 2013 - Thomas Wagner
- add bail-out if pkgbuild version can't be detected or is unknown
* Mon Oct  7 2013 - Thomas Wagner
- add faster version detection for pkgbuild
- fix %define pkgbuild_ver being empty
- add pkgbuild_renamed_to and init all variables with zero
- fix detection of pkgbuild-1.3.105
* Sat Oct  6 2013 - Thomas Wagner
- initial spec
