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




%changelog
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
