# /* vim: set filetype=spec : */ 

##TODO## check added leading "0." for branch with different versions of pkgbuild!

##NOTE## -- include this spec file into the package by specifying %include pkg-renamed.inc
#           and adding the sessions accoding to the other examples like SFEurxvt.spec

##NOTE## testing this inclulde file with e.g.: spectool --define 'version 3' eval %{ips_version_release_renamedbranch} include/pkg-renamed.inc


# include file to help creating packages with the
# "renamed=true" flag in case a package name has
# changed.
# e.g. SFEurxvt               renamed to terminal/urxvt
# e.g. sfe/library/libsndfile renamed to sfe/library/gnu/libsndfile
#
# on pkg update  or  on pkg install terminal/urxvt  you get
# automaticly removed the old package name then installed the package newname.
# on pkg install oldname you automaticly get installed the  package newname.

#STRONG NOTE:
#remember to set in the new spec file the %action which
#adds the depend rule in the new package. The new
#package then requests the oldname package in a slightly 
#higher IPS_vendor_version (aka branch version) with
#the renamed=true tag in it. A depend rule requesting the
#newname package then puts the newname package into the
#plan while uninstalling the oldname package at that time.
#
#note: the ips_version_release_renamedbranch from this include
#file has the last number incremented by one.
#That makes the renamed package #always more fresh then any
#other regular oldname package.
#This tells IPS to upgrade the oldname package, that one
#has renamed=true in it and a dependency on the newname
#package to be installed.
#
#example for the calling spec file, seciton %packages
# -> see SFEurxvt.spec for now
#example for the calling spec file, section %action
#%actions
#depend fmri=%{name}@%{ips_version_release_renamedbranch} type=optional
#results in e.g.:
#depend fmri=SFEurxvt@9.18,5.11-0.0.175.0.0.0.2.1 type=optional
#depend fmri=SFEurxvt@9.18,5.12-5.12.0.0.0.32.3 type=optional



#already included before?
%if %{?osdistro:%{osdistro}}%{?!osdistro:0}
#yes, osdistro.inc is already included
%else
%include osdistro.inc
%endif

#already included before?
%if %{?pkgbuild_features:%{pkgbuild_features}}%{?!pkgbuild_features:0}
#yes, pkgbuild-features.inc is already included
%else
%include pkgbuild-features.inc
%endif



#calculate an incemented-by-one IPS_Vendor_version (aka branch number)
#based on what the currently running OS prints in "pkg info release/name | grep Branch"

%if %{pkgbuild_ips_legacy}
#we are always on a IPS based system here
##TODO## check if all pkgbuild versions work with branches of 
##TODO## check if all IPS based systems work with a usable content in Branch field
#type "0.0.175.x.x.x.x.x" or "5.12.x.x.x.x.x"
#what about OmniOS, other IPS based osdistro?

#calculate a branch version which is always higher then the
#one from the osbuild / parent spec file

#pkg update "*"            #works with same branch
#pkg update oldpkg         #works with same branch
#pkg install oldpkg newpkg #works with same branch
#pkg install newpkg        #fails w conflicting files, except the oldpkg has higher branch!
#this is why we do that magic below!

# LC_ALL=C pkg info release/name | grep Branch                 
#uname -r  5.11
#        Branch: 0.175.0.0.0.2.0
#uname -r  5.12 
#        Branch: 5.12.0.0.0.32.2
#set a high default of 999999 in case we can't calculate
#test! (echo 0.175.0.0.0.1.0; echo 5.12.0.0.0.32.2) | egrep "^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$"; echo $? 
#test! (echo 0.175.0.0.0.1.0; echo 5.12.0.0.0.32.2) | awk -F'.' '{ print $1"."$2"."$3"."$4"."$5"."$6"."1+$7 }' 

# calculating the left hand side so it is ever matching this equation afterwards:
# oldpkg....(higher branch then any other oldpkg with content)       newpkg.....(lower branch)
# package_renamed_true@version-buildrelease,branch_renamed_package > package@version-buildrelease,branch

%define ips_branch_renamed_package 999999

#ATTENTION# we are editing 0.175 -> 0.0.175 for Solaris 11 (to match what pkgtool/pkgbuild does internally)
%define ips_branch_raw %( LC_ALL=C pkg info release/name | grep Branch | sed -e 's?.* ??' -e 's?^0\.175?0.0.175?' )

#case: 7 numbers branch sanity check
%if %( echo %{ips_branch_raw} | egrep "^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$" > /dev/null && echo 1 || echo 0 )
#add plus one on the last/seventh digit
%define ips_branch_renamed_package %( echo %{ips_branch_raw} | awk -F'.' '{ print $1"."$2"."$3"."$4"."$5"."$6"."1+$7 }' )
%endif
#END %{ips_branch_raw} sanity check e.g. 5.12.0.0.0.32.2

#case: 8 numbers branch sanity check
%if %( echo %{ips_branch_raw} | egrep "^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$" > /dev/null && echo 1 || echo 0 )
#add plus one on the last/eighth digit
%define ips_branch_renamed_package %( echo %{ips_branch_raw} | awk -F'.' '{ print $1"."$2"."$3"."$4"."$5"."$6"."$7"."1+$8 }' )
%endif
#END %{ips_branch_raw} sanity check 0.0.175.0.0.0.1.0

#case: 4 (5) numbers branch sanity check (OI: 0.0.151.1.4 or 0.0.151.1.8)
# oi151a8:  LC_ALL=C pkg info release/name | grep Branch
#        Branch: 0.151.1.8
##TODO## Hipster support! might be 0.151.1.8.1 ??
%if %{openindiana}
#we have 4 or 5 numbers, add the leading zero by awk, add trailing numbers by awk including increment
%if %( echo %{ips_branch_raw} | egrep "^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.{0,1}[0-9]*+$" > /dev/null && echo 1 || echo 0 )
#add plus one on the last number. As Hipster added randomly another .number to branch,
# we show that we can do even worse. We simply append .0.0.0.1 in any case!
# 0.151.1.8 -> 0.0.151.1.8.0.0.0.1   0.151.1.8.1 -> 0.0.151.1.8.1.0.0.0.1 (note more numbers!)
%define ips_branch_renamed_package %( echo %{ips_branch_raw} | awk -F'.' '{ print "0."$1"."$2"."$3"."$4"."0+$5"."0+$6"."0+$7"."1+$8 }' )
%else
%endif
#END %{ips_branch_raw} sanity check ....151.1.8....
%else
%endif
#END %{openindiana}

#example: uname -r 5.11  0.175.0.0.0.1.0 or uname -r 5.12  5.12.0.0.0.32.2
#-->>        9.18,5.11-0.0.175.0.0.0.1.1         9.18,5.12-5.12.0.0.0.32.3
%define ips_release_renamedbranch %( uname -r)-%{ips_branch_renamed_package}
#again, but prefixed with current package version
%define ips_version_release_renamedbranch %{version},%ips_release_renamedbranch
%else
%endif
#END pkgbuild_ips_legacy




%changelog
* Wed Nov 14 2013 - Thomas Wagner
- fixed branch calculation
- fixed detection which renamed_<n> set is defined by the calling spec file
- split out section %package into extra include file, because it can't be wrapped
  by %if and must always be in the calling spec file
* Wed Nov 13 2013 - Thomas Wagner
- fix logic that checks if %{renamed_to_newnameversion_1} is set to a package name
- add calculation to get an always higher IPS_Vendor_version (aka branch) for the renamed=true package
- add suport for up to three old package names / %{renamed_to_newnameversion_2} and %{renamed_to_newnameversion_3}
* Sat Nov  9 2013 - Thomas Wagner
- initial include file
