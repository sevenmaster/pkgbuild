# /* vim: set filetype=spec : */ 



#not defined on OmniOS, so we must go without it
%define pnm_buildrequires_SUNWpostrun	system/core-os
%define pnm_requires_SUNWpostrun	system/core-os

#OmniOS has no package (below), so use the SFE replacement
%define pnm_buildrequires_image_library_libexif	SFElibexif-gnu
%define pnm_requires_image_library_libexif	SFElibexif-gnu
%define pnm_buildrequires_SUNWlibexif_devel	SFElibexif-gnu
%define pnm_buildrequires_SUNWlibexif		SFElibexif-gnu
%define pnm_requires_SUNWlibexif		SFElibexif-gnu
%define pnm_buildrequires_libexif		SFElibexif-gnu
%define pnm_requires_libexif			SFElibexif-gnu


#not defined on OmniOS >= r151006, so we must use our own libpopt

%if %( expr %{osdistrelnumber} '>=' '151006' )
%define pnm_buildrequires_library_popt		SFElibpopt-devel
%define pnm_requires_library_popt		SFElibpopt
%define pnm_buildrequires_SUNWlibpopt_devel	SFElibpopt-devel
%define pnm_buildrequires_SUNWlibpopt		SFElibpopt-devel
%define pnm_requires_SUNWlibpopt		SFElibpopt
%define pnm_buildrequires_libpopt		SFElibpopt-devel
%define pnm_requires_libpopt			SFElibpopt
%endif


%changelog
* Thu Jul 25 2015 - Thomas Wagner
- use SFElibpopt (OM >= 151006)
* Wed Mar  4 2015 - Thomas Wagner
- add pnm_requires_image_library_libexif -> SFElibexif-gnu (OM)
* Mon Apr 21 2014 - Thomas Wagner
- handle pnm_buildrequires_SUNWpostrun, OmniOS has no SUNWpostrun (OOS151008)
