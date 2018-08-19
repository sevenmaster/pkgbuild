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
#retired %define pnm_buildrequires_developer_build_cmake sfe/developer/build/cmake
#retired %define pnm_requires_developer_build_cmake sfe/developer/build/cmake

#Hipster has zlib with zlib.pc since 2014
%define pnm_buildrequires_SFEzlib_pkgconfig	library/zlib
%define pnm_requires_SFEzlib_pkgconfig		library/zlib

#Hipster has opus unfortunatly in the same path
%define pnm_buildrequires_SFEopus		library/opus
%define pnm_requires_SFEopus			library/opus

#set name=pkg.fmri value=pkg://openindiana.org/gnome/gnome-audio@2.30.0,5.11-2015.0.2.0:20180217T085449Z
#set name=pkg.renamed value=true
#depend fmri=library/audio/audiofile@0.2.7,5.11-2015.0.2.0 type=require

%define pnm_buildrequires_gnome_gnome_audio	library/audio/audiofile
%define pnm_requires_gnome_gnome_audio		library/audio/audiofile

##TODO## check if that can be a dummy on oihipster with mate desktop?
#compiling multimedia on oihipster asked for gnome support in the past (e.g. libmms)
%define pnm_buildrequires_SUNWgnome_base_libs	system/kernel
%define pnm_buildrequires_SUNWgnome_base_libs_devel	system/kernel
%define pnm_buildrequires_SUNWgnome_common_devel	system/kernel




%changelog
* Tue Mar 13 2018 - Thomas Wagner
- use opus from hipster for now (OIH)
- use replacement library/audio/audiofile for gnome/audio
* Fri Mar  2 2018 - Thomas Wagner
- remove retired setting for pnm_buildrequires_developer_build_cmake (OIH) - check if newer cmake fomr OIH works with SFE packages
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
