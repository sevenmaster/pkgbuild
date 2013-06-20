# owner: tom68 - please ask/discuss if you want non-trivial changes

# Note: Name of this include file is currently subject to change

#
# Macro definitions for Solaris OS build version and distribution detection
#
# especially provide flags for features depending on osbuild / distro version
#

#this file is to be included in the spec file or is included in other
#include files

#Feature/Flags depending on the osbuild and distro version
#defaults, e.g. SXCE, Solaris 10
%define etc_security_directorylayout 0

#osdistrofeatures.inc is included --- NOTE: this variable is primarily for internal use by osdistrofeatures.inc
%define osdistrofeatures 1

#SolarisExpress, Solaris 11 and OpenIndiana >= 151
%if %( expr %{osbuild} '>=' 151 )
#we have /etc/security/ *.d directories
%define etc_security_directorylayout 1
%endif
#END >= 151


%changelog
* Thu Jun 20 2013 - Thomas Wagner
- add feature flag etc_security_directorylayout (>=151)
