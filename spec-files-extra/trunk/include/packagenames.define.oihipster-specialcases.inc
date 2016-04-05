# /* vim: set filetype=spec : */ 



#only oihipster has openjeg, try this
%define pnm_buildrequires_SFEopenjpeg	image/library/openjpeg
%define pnm_requires_SFEopenjpeg		image/library/openjpeg

#only oihipster has orc, try this
%define pnm_buildrequires_SFEorc_devel	system/library/orc
%define pnm_requires_SFEorc		system/library/orc

#only oihipster has libschroedinger, try this
%define pnm_buildrequires_SFElibschroedinger	library/video/libschroedinger
%define pnm_requires_SFElibschroedinger		library/video/libschroedinger

#only oihipster has libschroedinger, try this
#libyaml is a slowly updated lib, no C++ involved
%define pnm_buildrequires_SFElibyaml		library/libyaml
%define pnm_requires_SFElibyaml			library/libyaml


%changelog
* Thu Mar 17 2016 - Thomas Wagner
- handle pnm_buildrequires_SFElibyaml (only OIH has own libyaml)
* Fri Dec 25 2015 - Thomas Wagner
- moved SUNWxwinc to allbuilds
* Sun Nov 29 2015 - Thomas Wagner
- handle openjeg, default to SFEopenjpeg for all, except (OIH) where we use the osdistro package for the moment
- handle orc / libschroedinger, default to SFEorc / SFElibschroedinger for all, except (OIH) where we use the osdistro package for the moment
- handle lost legacy names SUNWxwinc for (OIH)
* Mon Apr 21 2014 - Thomas Wagner
- handle pnm_buildrequires_SUNWpostrun, OmniOS has no SUNWpostrun (OOS151008)
