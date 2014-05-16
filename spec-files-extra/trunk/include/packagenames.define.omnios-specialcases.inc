# /* vim: set filetype=spec : */ 



#not defined on OmniOS, so we must go without it
%define pnm_buildrequires_SUNWpostrun	system/core-os
%define pnm_requires_SUNWpostrun	system/core-os


%changelog
* Mon Apr 21 2014 - Thomas Wagner
- handle pnm_buildrequires_SUNWpostrun, OmniOS has no SUNWpostrun (OOS151008)
