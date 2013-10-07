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
%define pkgbuild_ver %( grep "^pkgbuild_dir" `which pkgbuild` | head -1 | sed -e '/pkgbuild/ s?.*pkgbuild-??' -e 's?[^0-9\.]??g' )


%if %( echo %{pkgbuild_ver} | grep -w "1.3.103" >/dev/null && echo 1 || echo 0 )
%define pkgbuild_ver_1_3_103 1
%define pkgbuild_ver_numeric 001003103
#features suported:
%define pkgbuild_ips_legacy  0
%endif
#1.3.103

%if %( echo %{pkgbuild_ver} | grep -w "1.3.104" >/dev/null && echo 1 || echo 0 )
%define pkgbuild_ver_1_3_104 1
%define pkgbuild_ver_numeric 001003104
#features suported:
%define pkgbuild_ips_legacy  1
%endif
#1.3.104

%if %( echo %{pkgbuild_ver} | grep -w "1.3.105" >/dev/null && echo 1 || echo 0 )
%define pkgbuild_ver_1_3_105 1
%define pkgbuild_ver_numeric 001003105
#features suported:
%define pkgbuild_ips_legacy  1
%endif
#1.3.105


#add more sections of new pkgbuild version add new feature
#so they can be excluded in case older pkgbuild version is active


%changelog
* Mon Oct  7 2013 - Thomas Wagner
- add faster version detection for pkgbuild
* Sat Oct  6 2013 - Thomas Wagner
- initial spec
