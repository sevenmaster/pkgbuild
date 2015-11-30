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

#oihipster lost SUNWxwinc, try a replacement. Set the default for all other osdistro here
#  usr/include/X11/X.h pkg:/x11/header/xproto@7.0.28-2015.0.1.0
%define pnm_buildrequires_SUNWxwinc_devel	x11/header/xproto
%define pnm_buildrequires_SUNWxwinc		x11/header/xproto
%define pnm_requires_SUNWxwinc			x11/header/xproto


%changelog
* Sun Nov 29 2015 - Thomas Wagner
- handle openjeg, default to SFEopenjpeg for all, except (OIH) where we use the osdistro package for the moment
- handle orc / libschroedinger, default to SFEorc / SFElibschroedinger for all, except (OIH) where we use the osdistro package for the moment
- handle lost legacy names SUNWxwinc for (OIH)
* Mon Apr 21 2014 - Thomas Wagner
- handle pnm_buildrequires_SUNWpostrun, OmniOS has no SUNWpostrun (OOS151008)
