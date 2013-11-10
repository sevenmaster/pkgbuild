


%if %{pkgbuild_ips_legacy}
%if %( test -n "%{renamed_to_newnameversion_1}"; echo $? )

%package -n %{renamed_from_oldname_1}-renamed-noinst
Summary:                 %{summary} - was renamed to terminal/urxvt

#STRONG NOTE: put the old name which is going away into IPS_Package_Name !!!
#this might be SFEurxvt -> terminal/urxvt then use pkg:/"SFEurxvt"
#example: IPS_package_name:	 SFEurxvt
IPS_package_name:	 %{renamed_from_oldname_1}

#make it faster
%define _use_internal_dependency_generator 0

IPS_legacy: false
#example: SUNW_Pkg: SFEurxvt
SUNW_Pkg: %{renamed_from_oldname_1}

Meta(pkg.renamed): true

#NOTE: need a version rule, or get ignored. >= 1.1.1 or = * 
#example: renamed_to: terminal/urxvt >= %{version}
#example: Renamed_To: terminal/urxvt = *
Renamed_To: %{renamed_to_newnameversion_1}

#not allowed to place a depend into a obsoleted package! #Meta(pkg.obsolete): true
Meta(variant.opensolaris.zone): global, nonglobal
PkgBuild_Make_Empty_Package: true

%endif
#END renamed_to_newnameversion_1
%endif
#END pkgbuild_ips_legacy





#example manifest:
#calling spec file sets:
#
#%define renamed_to_newnameversion_1 'terminal/urxvt = *'
#%include pkg-renamed.inc


#this results in a manifest like this: (this is the last in the series names pkg://SFEurxvt
#set name=pkg.fmri value=SFEurxvt@9.18,5.11-0.0.175.0.0.0.2.0
#set name=variant.opensolaris.zone value="global" value="nonglobal"
#depend fmri=terminal/urxvt type=require
#set name=pkg.renamed value="true"

#and a note in the target package terminal/urxvt
#set name=pkg.fmri value=terminal/urxvt@9.18,5.11-0.0.175.0.0.0.2.0
#depend fmri=pkg://localhosts11/SFEurxvt@9.18,5.11 type=optional

#thats broken! set name=pkg.depend value="'fmri=pkg://localhosts11/SFEurxvt@9.18" value="5.11 type=require'"

#depend fmri=pkg://localhosts11/SFEurxvt@9.18,5.11-0.0.175.0.0.0.2.0:20131106T114822Z type=optional


%changelog
* Sat Nov  9 2013 - Thomas Wagner
- initial include file

