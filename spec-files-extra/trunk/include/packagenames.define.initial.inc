# /* vim: set filetype=spec : */ 



#pre-load some variables which are very common and only a few OS need variants
%define pnm_buildrequires_SUNWpostrun	SUNWpostrun
%define pnm_requires_SUNWpostrun	SUNWpostrun
%define pnm_buildrequires_SUNWbzip	SUNWbzip
%define pnm_requires_SUNWbzip		SUNWbzip


#S12 has asciidoc, all others need out SFE version
%define pnm_buildrequires_SFEasciidoc	SFEasciidoc
%define pnm_requires_SFEasciidoc	SFEasciidoc

#jam is not on available every osdistro
%define pnm_buildrequires_SFEjam	SFEjam
%define pnm_requires_SFEjam		SFEjam
%define pnm_buildrequires_developer_build_jam	SFEjam
%define pnm_requires_developer_build_jam	SFEjam

#library/libedit@3.0,5.11-0.175.1.0.0.24.0:20120904T172539Z
%define pnm_buildrequires_library_libedit	SFEeditline
%define pnm_requires_library_libedit		SFEeditline
%define pnm_buildrequires_SFEeditline		SFEeditline
%define pnm_requires_SFEeditline		SFEeditline

%define pnm_buildrequires_developer_documentation_tool_xmlto	SFExmlto
%define pnm_requires_developer_documentation_tool_xmlto		SFExmlto
%define pnm_buildrequires_SFExmlto				SFExmlto
%define pnm_requires_SFExmlto					SFExmlto

#only oihipster has openjeg, see packagenames.define.oihipster-specialcases.inc
%define pnm_buildrequires_SFEopenjpeg		SFEopenjpeg
%define pnm_requires_SFEopenjpeg		SFEopenjpeg

#only oihipster has orc, see packagenames.define.oihipster-specialcases.inc
%define pnm_buildrequires_SFEorc_devel  	SFEorc
%define pnm_requires_SFEorc             	SFEorc

#only oihipster has libschroedinger, try this
%define pnm_buildrequires_SFElibschroedinger    SFElibschroedinger
%define pnm_requires_SFElibschroedinger         SFElibschroedinger

#only oihipster has libyaml, try this
%define pnm_buildrequires_SFElibyaml		SFElibyaml
%define pnm_requires_SFElibyaml			SFElibyaml

#oihipster lost SUNWxwinc, try a replacement. Set the default for all other osdistro here
%define pnm_buildrequires_SUNWxwinc_devel	SUNWxwinc
%define pnm_buildrequires_SUNWxwinc		SUNWxwinc
%define pnm_requires_SUNWxwinc			SUNWxwinc

#many osdistro do not delive the file "zlib.pc" for pkgconfig, SFE drops one in until the osdistro has one
#osdistro which have one, can replace this in pnm_macro include file (example: S12)
%define pnm_buildrequires_SFEzlib_pkgconfig	SFEzlib-pkgconfig
%define pnm_requires_SFEzlib_pkgconfig		SFEzlib-pkgconfig

#SFEautomake-115 - may be replaced by an osdistro.
#if you get upgrade contraints, then uninstall the SFE automake-115 package
#starting with S12 (some build) we have developer/build/automake-115
%define pnm_buildrequires_developer_build_automake_115        SFEautomake-115
%define pnm_buildrequires_developer_build_automake_115        SFEautomake-115
%define pnm_buildrequires_SUNWautomake_115            SFEautomake-115
%define pnm_requires_SUNWautomake_115                 SFEautomake-115
%define pnm_buildrequires_SFEautomake_115             SFEautomake-115
%define pnm_requires_SFEautomake_115                  SFEautomake-115

%changelog
* Fri Apr 29 2016 - Thomas Wagner
- handle SFEautomake-115 / automake / pnm_requires_SFEautomake_115 (S12)
* Fri Apr 22 2016 - Thomas Wagner
- handle pnm_buildrequires_SFEzlib_pkgconfig SFEzlib-pkgconfig (see example for replacement with regular zlib for S12b87 in other pnm include file)
* Thu Mar 24 2016 - Thomas Wagner
- handle pnm_requires_developer_documentation_tool_xmlto SFExmlto (older distro don't have it)
* Thu Mar 17 2016 - Thomas Wagner
- handle pnm_buildrequires_SFElibyaml (only OIH has own libyaml)
* Mon Nov 30 2015 - Thomas Wagner
- fix typo SFE_openjpeg -> SFEopenjpeg
* Sun Nov 29 2015 - Thomas Wagner
- handle openjeg, default to SFEopenjpeg for all, except (OIH)
- handle orc / libschroedinger, default to SFEorc / SFElibschroedinger for all, except (OIH) where we use the osdistro package for the moment
- handle lost SUNWxwinc for (OIH)
* Sat Okt 17 2015 - Thomas Wagner
- handle pnm_buildrequires_library_libedit SFEeditline
* Fri Aug  1 2014 - Thomas Wagner
- handle pnm_buildrequires_SUNWbzip
* Thu May 15 2014 - Thomas Wagner
- handle pnm_buildrequires_SFEjam (all, see possible exceptions in other p*inc files)
- handle pnm_buildrequires_SUNWpostrun which OmniOS doesn't have (OOS151008)
* Fri Apr 26 2014 - Thomas Wagner
- handle pnm_buildrequires_SFEasciidoc (all, except S12)
* Mon Apr 21 2014 - Thomas Wagner
- initial load for common cases and variables, mostly common settings
