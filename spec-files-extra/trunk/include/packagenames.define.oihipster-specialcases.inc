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

#oihipster has its own cmake with almost the same package name. we want ours with ^sfe/
%define pnm_buildrequires_developer_build_cmake sfe/developer/build/cmake
%define pnm_requires_developer_build_cmake sfe/developer/build/cmake

#Hipster has zlib with zlib.pc since 2014
%define pnm_buildrequires_SFEzlib_pkgconfig	library/zlib
%define pnm_requires_SFEzlib_pkgconfig		library/zlib


%changelog
* Sun Feb  5 2017 - Thomas Wagner
- fix pnm_macro for zlib / zlib.pc (OIH)
* Thu Nov 24 2016 - Thomas Wagner
- handle pnm_buildrequires_developer_build_cmake to be our ^sfe/ package (OIH)
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
