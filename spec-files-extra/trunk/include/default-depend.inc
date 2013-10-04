#
# Default system dependencies for GNOME packages on Solaris
#
# Copyright (c) 2003 Sun Microsystems, Inc.
#

##TODO## need a solution for distinguishing build numbers, include S12 ...
%if %{?os2nnn:%{os2nnn}}%{?!os2nnn:0}
Requires: system/library 
Requires: system/kernel 
Requires: system/core-os
%else
Requires: SUNWcsr
Requires: SUNWcsu
Requires: SUNWcsd
Requires: SUNWcsl
%endif

* Fri Oct  4 2013 - Thomas Wagner
- try making package name resolve faster on IPS systems
