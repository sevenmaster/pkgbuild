# /* vim: set filetype=spec : */ 



#not defined on OmniOS, so we must go without it
%define pnm_buildrequires_SUNWpostrun	SUNWcs
%define pnm_requires_SUNWpostrun	SUNWcs
%define pnm_buildrequires_SUNWbash	SUNWcs
%define pnm_requires_SUNWbash		SUNWcs

#OmniOS has no package (below), so use the SFE replacement
%define pnm_buildrequires_image_library_libexif	SFElibexif-gnu
%define pnm_requires_image_library_libexif	SFElibexif-gnu
%define pnm_buildrequires_SUNWlibexif_devel	SFElibexif-gnu
%define pnm_buildrequires_SUNWlibexif		SFElibexif-gnu
%define pnm_requires_SUNWlibexif		SFElibexif-gnu
%define pnm_buildrequires_libexif		SFElibexif-gnu
%define pnm_requires_libexif			SFElibexif-gnu

#OmniOS has  automake 115 1.15
%define pnm_buildrequires_SFEautomake_115	developer/build/automake
%define pnm_requires_SFEautomake_115		developer/build/automake

##TODO## #OmniOS has autoconf 2.69

#OmniOS has no guile, use SFEguile
%define pnm_buildrequires_library_guile		SFEguile
%define pnm_requires_library_guile		SFEguile
%define pnm_buildrequires_SUNWguile_devel	SFEguile
%define pnm_buildrequires_SUNWguile		SFEguile
%define pnm_requires_SUNWguile			SFEguile
%define pnm_buildrequires_guile			SFEguile
%define pnm_requires_guile			SFEguile


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

#add make to onbld
%define pnm_buildrequires_SUNWonbld		developer/build/make,developer/build/onbld

#OmniOS doesn't have it
##%define pnm_buildrequires_SUNWgnupg_devel	SFEgnupg2
##%define pnm_requires_SUNWgnupg			SFEgnupg2
##%define pnm_buildrequires_crypto_gnupg		SFEgnupg2
##%define pnm_requires_crypto_gnupg		SFEgnupg2
##%define pnm_buildrequires_sfe_crypto_gnupg	SFEgnupg2
##%define pnm_requires_sfe_crypto_gnupg		SFEgnupg2
%define pnm_buildrequires_library_pth		SFEpth-gnu
%define pnm_requires_library_pth		SFEpth-gnu
%define pnm_buildrequires_SUNWpth_devel		SFEpth-gnu
%define pnm_buildrequires_SUNWpth		SFEpth-gnu
%define pnm_requires_SUNWpth			SFEpth-gnu

%define pnm_buildrequires_SUNWslang_devel	SFEslang
%define pnm_buildrequires_SUNWslang		SFEslang
%define pnm_requires_SUNWslang			SFEslang

%define pnm_buildrequires_SUNWpng_devel		SFElibpng
%define pnm_buildrequires_SUNWpng		SFElibpng
%define pnm_requires_SUNWpng			SFElibpng

%define pnm_buildrequires_library_file_monitor_gamin	SFEgamin
%define pnm_requires_library_file_monitor_gamin		SFEgamin
%define pnm_buildrequires_SUNWgamin_devel	SFEgamin
%define pnm_buildrequires_SUNWgamin		SFEgamin
%define pnm_requires_SUNWgamin			SFEgamin
%define pnm_buildrequires_gamin			SFEgamin
%define pnm_requires_gamin			SFEgamin

%define pnm_buildrequires_library_database_gdbm SFEgdbm
%define pnm_requires_library_database_gdbm      SFEgdbm
%define pnm_buildrequires_SFEgdbm               SFEgdbm
%define pnm_requires_SFEgdbm                    SFEgdbm
%define pnm_buildrequires_SUNWgnu_dbm           SFEgdbm
%define pnm_requires_SUNWgnu_dbm                SFEgdbm


%changelog
* Fri Nov  1 2019 - Thomas Wagner
- add pnm_buildrequires_library_database_gdbm SFEgdbm on (OM)
* Sun Jun 16 2019 - Thomas Wagner
- add pnm_buildrequires_SUNWbash and map to SUNWcs (OM)
* Sat Nov 18 2017 - Thomas Wagner
- add pnm_buildrequires_SUNWgamin (OM)
* Tue Sep  5 2017 - Thomas Wagner
- use for pnm_buildrequires_SUNWslang_devel SFEslang (OM)
- use for pnm_buildrequires_SUNWpng_devel SFElibpng (OM)
##* Sun Aug 13 2017 - Thomas Wagner
##- add pnm_buildrequires_SUNWgnupg SFEgnupg2 (OM)
* Tue Feb 14 2017 - Thomas Wagner
- add developer/build/make to pnm macro pnm_buildrequires_SUNWonbld (developer/build/onbld) (OM)
* Sun Jul 31 2016 - Thomas Wagner
- use for pnm_buildrequires_SFEautomake_115 Omnios' package developer/build/automake @ 1.15 (OM)
- use for pnm_buildrequires_library_guile SFEguile (OM)
- use for pnm_buildrequires_library_guile SFEguile (OM)
* Thu Jul 25 2015 - Thomas Wagner
- use SFElibpopt (OM >= 151006)
* Wed Mar  4 2015 - Thomas Wagner
- add pnm_requires_image_library_libexif -> SFElibexif-gnu (OM)
* Mon Apr 21 2014 - Thomas Wagner
- handle pnm_buildrequires_SUNWpostrun, OmniOS has no SUNWpostrun (OOS151008)
