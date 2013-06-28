# owner: tom68 - please ask/discuss if you want non-trivial changes

# NOTE: The NAME of this include file is currently subject to change

#
# Macro definitions for setting available features
#
# especially provide flags for features depending on osbuild / distro version
#

#this file is to be included in the spec file or is included in other
#e.g. with 
#   %include osdistro.inc
#   %include osdistrofeatures.inc

#osdistrofeatures.inc is included --- NOTE: this variable is primarily for internal use by osdistrofeatures.inc
%define osdistrofeatures 1

#Feature/Flags depending on the osbuild and distro version

#Solaris 12, SolarisExpress, Solaris 11 and OpenIndiana, SXCE, not S10
#defaults to off, e.g. on Solaris 10
%define etc_security_directorylayout 0
#%if %{?SXCE}%{?solaris11express}%{?solaris12}%{?openindiana}
%if %{?os2nnn}%{?SXCE}
#we have /etc/security/ *.d directories
%define etc_security_directorylayout 1
%endif
#END >= 151

%changelog
* Fri Jun 21 2013 - Thomas Wagner
- fix logic, test with SXCE, S11, S12, openindiana
* Thu Jun 20 2013 - Thomas Wagner
- add feature flag etc_security_directorylayout (>=151)
