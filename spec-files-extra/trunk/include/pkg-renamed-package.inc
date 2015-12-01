# /* vim: set filetype=spec : */ 

#this is set in the calling spec, pkgtool/pkgbuild cannot include this: 
#         %package -n %{package_renamed_noinst}

Summary:                 %{summary} - was renamed to %{renamed_to_newnameversion}

#STRONG NOTE: put the old name which is going away into IPS_Package_Name !!!
#this might be SFEurxvt -> terminal/urxvt then use "SFEurxvt"
IPS_package_name:	 %{renamed_from_oldname}

###make it faster
##%define _use_internal_dependency_generator 0

IPS_legacy: false
#example: SUNW_Pkg: SFEurxvt
%if %( echo %{renamed_from_oldname} | grep "/" >/dev/null && echo 0 || echo 1 )
SUNW_Pkg: %{renamed_from_oldname}
%endif

Meta(pkg.renamed): true

#NOTE: you need a version rule, or get ignored. >= 1.1.1 or = * 
#example_minversion: Renamed_To: terminal/urxvt >= %{version}
#example_allversion: Renamed_To: terminal/urxvt = *
Renamed_To: %{renamed_to_newnameversion}

#not allowed to place a depend into a obsoleted package! #Meta(pkg.obsolete): true
Meta(variant.opensolaris.zone): global, nonglobal
PkgBuild_Make_Empty_Package: true

#this needs to be newer branch (or version) then the alread installed oldname package
IPS_Vendor_Version: %{ips_branch_renamed_package}


%changelog
* Fri Nov  6 2015 - Thomas Wagner
- don't use SUNW_Pkg: if it is an IPS package name with a "/" in it
* Thu Nov 14 2013 - Thomas Wager
- split out from pkg-renamed.inc to be included for every single oldname package
