#
#
#   STRONG note: this is an early stage, logic and variable names *might* change
#
#

# owner: Thomas Wagner (tom68) - please ask/discuss if you want non-trivial changes

# TODO1: test logic for correctness
# TODO2: extend rules to match Solaris 10 / SVR4
# TODO3: add copyright (CDDL?)

# TODO4: Add fine granularity for version/branch of entire@ package


#
# Macro definitions for Solaris OS build version and distribution detection
#

# note for new OS releases: Follow the marks NEWRELEASE in his include file
# to add new code for detection these new releases
# hint: use the search function of your editor with the pattern NEWRELEASE
#       and copy an old block, then edit. Keep the order to not break the logic

# note this fails havily if you are "BFU"ing your box
# (if you don't use BFU / don't know what BFU is, you don't need to take care of)


# detect OS distro and os build version if possible
# distinguish between SXCE and os20nn.nn, set distro numbers for "osbuild > nnn" logic
# try to detect the distro release in example of os20nn.nn
# and provide boolean flags e.g. %os200902  <0|1>
# and provide test numbers with a distro releasenumber %osdistrelnumber  201003
# and provide test strings with a short distro releasename %osdistrelname  "os2010.03"

# see also the include file "packagenamemakros.inc" for
# already predefined "BuildRequires" and "Requires" depending
# on the distro and build number, leveraging the detection from 
# this osversion.inc include file
# should simplify sharing spec files between SXCE and os20nn.nn


# usage/examples:
# if you depend on a package which for instance got some day a rename:
# (or dissapeared, newly introduced, merged into another package
# this is not limited to these examples (think of switching off SVR4 package
# scripting, ...).
#
# %if %( expr %{osbuild} '>=' 100 )
# BuildRequires: SUNWnewname
# %else
# BuildRequires: SUNWoldname
# %endif

#TO BE CHECKED # *if* we are on os20nn.nn *and* build is younger|equal then 118
#TO BE CHECKED # %if %os2nnn %( expr %osbuild '>=' 118 )
#TO BE CHECKED # BuildRequires: newpackagename
#TO BE CHECKED # %else
#TO BE CHECKED # BuildRequires: SUNWoldname
#TO BE CHECKED # %endif

#TO BE CHECKED # same as above but based on the os20nn.nn distro, example os2009.06 and above
#TO BE CHECKED # %if %( expr %os2nnndistro '>=' 200906 && echo 1 || echo 0 )
#TO BE CHECKED # BuildRequires: newpackagename
#TO BE CHECKED # %else
#TO BE CHECKED # BuildRequires: SUNWoldname
#TO BE CHECKED # %endif

### end of examples
### rules below need extensions with every major distro release

##overall the include file - we are already included
%if %{?osdistro:%{osdistro}}%{?!osdistro:0}
#osdistro.inc is ALREADY included
%else
#osdistro.inc is NOT YET included --- NOTE: this variable is primarily for internal use by osdistro.inc
%define osdistro 1

%define osbuild %(uname -v | sed -e 's/^[A-z_]*//' -e 's/[A-z_].*//')
#special handling for release builds: uname -v prints 11.0 or similar 
#which might correspond to build 175 (needs refinement)
%if %( uname -v | egrep '^11\.[0-9]' > /dev/null && echo 1 || echo 0 )
##TODO## be more precise later, for build 173 and 174 and later SRU
%define osbuild 175
%endif 

%if %( uname -v | egrep '^s12_[0-9]' > /dev/null && echo 1 || echo 0 )
%define osbuild %( uname -v | sed -e 's/s12_//' )
%endif

#quick and dirty hack, only works on OI hipster printing "illumos" with "uname -v". DON'T USE ON ANY OTHER OSDISTRO PLEASE!
# For want of a line in the sand between different "versions", I'm using the date of significant milestones like 
# iso snapshot date (per http://dlc.openindiana.org/isos/hipster/) or significant update dates between snapshots if needs be.
# To determine date I'll use the "Packaging Date" of the package consolidation/osnet/osnet-incorporation.
# Dates of last iso snapshots. eg
# 20160421 = Iso Snapshot
# 20151003 = Iso Snapshot
# 20150330 = Iso Snapshot
# 20141010 = Iso Snapshot
# 20140701 = Iso Snapshot
%if %( uname -v | egrep '^illumos-' > /dev/null && echo 1 || echo 0 )
%define osbuild 151
%endif

#new for 151030 or so,
#https://github.com/omniosorg/omnios-build/blob/master/build/release/build.sh#L33
#calculation to get from two letter to one digit.
##TODO## use the above if it is available
#r151028ef would be 5*26 + 6
#quick and dirty hack, only works on OmniOS - uname -v prints on 151008j: omnios-6de5e81
#quick and dirty hack, only works on OmniOS - uname -v prints on 151022y: omnios-r151022-eb9d5cb557
%if %( uname -v | egrep '^omnios-[0-9a-f]' > /dev/null && echo 1 || echo 0 )
%define osbuild 151
%endif
%if %( uname -v | egrep '^omnios-r151[0-9]*-[0-9a-f]*' > /dev/null && echo 1 || echo 0 )
%define osbuild 151
%endif


# see if we are on old SVR4 release
%define SXCE %( egrep "Solaris Express Community Edition" /etc/release > /dev/null 2>&1 && echo 1 || echo 0 )


#switches for major distro releases
# os2nnn is defined 1 if we can detect the OpenSolaris (IPS based) distro
# 
# an estimate is done to tell which distro release is present
#NEWRELEASE add to the table    (OpenSolaris releases as os2......)
# os2008.11    os2009.06    os2009.11    os2010.03    os2010.05  
# corresponds to:
# os200811     os200906     os200911     os201003     os201005   
#
# Solaris11Express_firstrelease Solaris11Express_following OpenIndiana147 OpenIndiana151
##TODO## replace the "*00" to be the real release month
# s11ex201011                   s11ex201000                oi201009       oi201100

#numbers for each major distro release are stored in %os2nnnversion

#Flags - who knows what that's worth for
#set defaults to null - reverse order to catch youngest distro first 
#and then used to skip the other detection rules for older releases
#NEWRELEASE add to the table

#boolean flags for major osdistro names
#no versioning here
%define oihipster 0
%define openindiana 0
%define solaris11express 0
%define solaris11 0
%define solaris12 0
%define omnios 0


#boolean flags for major osdistro names - *with* versioning the releases
#use osbuild in addition to finer granularity, e.g. osbuild >= 148
#OpenSolaris and Solaris11Express below. We need something to tell the release as well
#Solaris11Express gets its own name prefix though it's close to what OpenSolaris was

#OI/Hipster
#has most C++ stuff compiled with GCC
#:r!grep oih20 %
%define oih20140701    0
%define oih20141010    0
%define oih20150330    0
%define oih20151003    0
%define oih20151128    0
%define oih20160421    0
%define oih20160926    0

#OpenIndiana
# could be oi201009 and oi201100 or something, the first development release and following
##TODO## replace oi201100
%define oi201100 0
%define oi201009 0

#Solaris 12 - NOTE: This is now named "11.4" ... these variables deprecated. for transition they'll be defined on s11.4 as it it where s12 at the time of development
#always defined on 12.0 and all subsequent 12.xx versions. build 00.
%define s120000 0
#12.0 build 24
%define s120024 0
#superceded by: s110400 see below

#Solaris 11
#always defined on 11.0 and all subsequent 11.xx versions.
#11.0 build ??
%define s110000 0
#11.1 build ??
%define s110100 0
#11.2 build ??
%define s110200 0
#11.3 build ??
%define s110300 0
#11.4 build ??
%define s110400 0

#Solaris 11 Express and OpenSolaris
##TODO## replace s11ex201100
%define s11ex201100 0
%define s11ex201011 0
#OpenSolaris
%define os201005 0
#never apperared: (this variable might go away some day)
%define os201003 0
%define os200906 0
%define os200902 0
%define os200811 0


# one of the IPS style OpenSolaris distro releases is present if os2nnn set to "1"
# set default to "0" which is good
# includes OI
%define os2nnn        0

# make your logic work with the major distro number  %if %( expr %os2nnndistro '>=' 200906 )
# set default to "0" which is good
# includes OI
%define osdistrelnumber 0

# set readable name for this os distribution  (not for SXCE)
%define osdistrelname   "not detected"

# Note osdet299999 is a helper variable. Specs should use %if %os2nnn ... and %os2nnndistro
# Make default to "1" to enable the os20nn.nn detection steps below.
# for readability see separated %if where a present %SXCE resets this switch to "0" and disables all remaining checks
# which makes this file skip any following checks
%define osdet299999 1

# we are on SXCE, so skip the all other os2nnn detection rules and leave %os**** defaults at "0"
%if %SXCE
#no more work to do
%define osdet299999 0
%define osdistrelname   "SXCE"
%endif

# try detecting the distro release we are on
# might need more fine grained rules some day?

#(os2010.03)
#e.g. OpenSolaris 2010.03 snv_134 X86

#NEWRELEASE carefull: add new releases *always* on top of the predecessor version.
#NEWRELEASE for that, copy the example from below (START to END) and change numbers
#NEWRELEASE you might need *many* places in the block edited. be *carefull* please and double-check and 
#NEWRELEASE do not forget to change the variables names too!

#NEWRELEASE *add* new version  *here* (below)



#note: build 166 (maybe earlier) does read "Oracle Solaris 11 snv_166 X86"
#note: build 160 (2010.11++) does read "Oracle Solaris 11 Express snv_160 X86"
#note: build 151a 2010.11 does read "Oracle Solaris 11 Express snv_156 X86"
#note: build 140 does read "Solaris Next Development"
#note: build 134 does read "OpenSolaris Development"
#below probably release of 2010.05 (was 2010.03 or whatever name)


#root@host:~# cat /etc/release | grep OmniOS
#  OmniOS v11 r151006
#root@host:~# cat /etc/release | grep OmniOS
#  OmniOS v11 r151008
# cat /etc/release | grep OmniOS
#  OmniOS v11 r151010
# cat /etc/release | grep OmniOS
#  OmniOS v11 r151012

#OpenIndiana Hipster 2015
#/etc/release 
#             OpenIndiana Development oi_151.1.8 X86 (powered by illumos)
#        Copyright 2011 Oracle and/or its affiliates. All rights reserved.
#                        Use is subject to license terms.
#                           Assembled 19 February 2013

#when it switched to name Hipster is not known
#OpenIndiana Hipster 2016.04
#/etc/release
#             OpenIndiana Hipster 2016.04 (powered by illumos)
#        OpenIndiana Project, part of The Illumos Foundation (C) 2010-2016
#                        Use is subject to license terms.
#                           Assembled 17 August 

#release/name@0.5.11,5.11-2017.0.0.5:20171030T214925Z
#gzip -d < /tmp/hipster-2017-10-etc-release-3be5012aa181a5e70a1ba26138c5e0f5c76c8249 
#             OpenIndiana Hipster 2017.10 (powered by illumos)
#        OpenIndiana Project, part of The Illumos Foundation (C) 2010-2017
#                        Use is subject to license terms.
#                           Assembled 30 October 2017




##START build 151 006 and 008 and up , OmniOS
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 151 )
#  OmniOS v11 r151006
#  OmniOS v11 r151008
%if %( egrep 'OmniOS ' /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
#below: subject to change!
%define omnios 1
#OmniTI: r151022
#OmniOSce: r151022y
#%define osdistrelnumber %( grep "OmniOS v[0-9]* r[0-9]*" /etc/release | sed -e 's?^.*OmniOS v[0-9]* *r??' )
#%define osdistrelnumber %( grep "OmniOS v[0-9]* r[0-9]*" /etc/release | sed -e 's?^.*OmniOS v[0-9]* *r??' -e 's?[a-z]*$??' )
#%define osdistrelnumber %( egrep "OmniOS v[0-9]* r[0-9]*[a-z]{0,1}$" /etc/release | sed -e 's?^.*OmniOS v[0-9]* *r??' -e 's?[a-z]*$??' )
%define osdistrelnumber %( egrep "OmniOS v[0-9]* r[0-9a-z]" /etc/release | sed -e 's?^.*OmniOS v[0-9]* *r??' -e 's?[a-z]*$??' )
#                                below: subject to change!
#Please note: if you need a fine grained relese, use osdistro_entire_padded_number4
%define osdistrelname   OmniOS
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END

##START build 151 circa 20150330 and up, OI/Hipster
# but still flags ealier versions although not dealt with as such.
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 151 )
#%if %( egrep 'OpenIndiana (Development|Hipster)' /etc/release > /dev/null && echo 1 || echo 0 )
%if %( egrep 'OpenIndiana Development|OpenIndiana Hipster' /etc/release > /dev/null && echo 1 || echo 0 )
# Detect if hipsterish
%if %( uname -v | egrep '^illumos-' > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
#below: subject to change!
%define oihipster 1
# Find date of osnet-incorporation and change to ISO date format
# Not sure how this will go with pre-iso snapshot updated to post-iso packages
##TODO## check if this can hardened against situation with same content but (re-)packaged at a newer date, that would more secure detection
##       the price of supporting a development OS, being a moving target.
#DEBUG %define marker1 %( echo marker1 >> /tmp/pkg_wrapper_log )
%define osbuilddate %(pkg info osnet-incorporation | grep 'Packaging Date' | cut -d' ' -f 3,4,5 | date +%Y%m%d )

# Post 20140701
%if %( expr %{osbuilddate} '>=' 20140701 )
%define oih20140701    1
#may be overwritten later
%define osdistrelnumber 20140701
%endif
# Post 20141010
%if %( expr %{osbuilddate} '>=' 20141010 )
%define oih20141010    1
%define osdistrelnumber 20141010
%endif
# Post 20150330
%if %( expr %{osbuilddate} '>=' 20150330 )
%define oih20150330    1
%define osdistrelnumber 20150330
%endif
# Post 20151003
%if %( expr %{osbuilddate} '>=' 20151003 )
%define oih20151003    1
%define osdistrelnumber 20151003
%endif
# Post 20151128
%if %( expr %{osbuilddate} '>=' 20151128 )
%define oih20151128    1
%define osdistrelnumber 20151128
%endif
# Post 20160421
%if %( expr %{osbuilddate} '>=' 20160421 )
%define oih20160421    1
%define osdistrelnumber 20160421
%endif
# Post 20160926
%if %( expr %{osbuilddate} '>=' 20160926 )
%define oih20160926    1
%define osdistrelnumber 20160926
%endif
#                                below: subject to change!
%define osdistrelname   "OIHipster"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
%else
%endif
##END

##START build 151 and up, OpenIndiana
#NOTE: we try to set a resonable opensolaris/solaris express release
# name as well, they should behave similar. Remaining issues to be fixed
# in consuming spec file!
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 151 )
#%if %( egrep 'OpenIndiana (Development|Hipster)' /etc/release > /dev/null && echo 1 || echo 0 )
%if %( egrep 'OpenIndiana Development|OpenIndiana Hipster' /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
#below: subject to change!
%define openindiana 1
##TODO## replace oi201100
%define oi201100    1
%define osdistrelnumber 151
#                                below: subject to change!
%define osdistrelname   "OpenIndiana"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END


##START build 147 and up, OpenIndiana
#NOTE: we try to set a resonable opensolaris/solaris express release
# name as well, they should behave similar. Remaining issues to be fixed
# in consuming spec file!
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 147 )
%if %( egrep 'OpenIndiana Development' /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
#below: subject to change!
%define openindiana 1
%define oi201009    1
%define osdistrelnumber 147
#                                below: subject to change!
%define osdistrelname   "OpenIndiana"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END

#s11.4 ~ cat /etc/release 
#                            Oracle Solaris Trunk X86
#  Copyright (c) 1983, 2018, Oracle and/or its affiliates.  All rights reserved.
#                            Assembled 17 January 2018
#uname -v
#11.4.0.12.0

#NOTE: development s12 is now s11.4 - old references to "s12" will eventually go away on some day
#NOTE: Use for new develeoped spec files the variable s110400 to identify Solaris 11.4 (former Solaris 12 in development)
%if %{osdet299999}
#%if %( expr %{osbuild} '>=' 24 )
#%if %( egrep 'Oracle Solaris Trunk' /etc/release > /dev/null && echo 1 || echo 0 )
%if %( egrep 'Oracle Solaris 11\.4|Oracle Solaris Trunk' /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
#below: subject to change!
%define s120000 1
%define s120024 1
%define s110100 1
%define s110200 1
%define s110300 1
%define s110400 1
%define solaris12 1
##TODO##!! which number do we want here?
%define osdistrelnumber 201104
#                                below: subject to change!
%define osdistrelname   "Solaris 11.4"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
#%else
#%endif
%else
%endif
##END

#s11.4 ~ cat /etc/release 
#                            Oracle Solaris Trunk X86
#  Copyright (c) 1983, 2018, Oracle and/or its affiliates.  All rights reserved.
#                            Assembled 17 January 2018
#uname -v
#11.4.0.12.0

#s12 sfe ~  cat /etc/release
#                             Oracle Solaris 11.4 X86
#  Copyright (c) 1983, 2018, Oracle and/or its affiliates.  All rights reserved.
#                            Assembled 16 August 2018
#uname -v
#11.4.0.15.0
#pkg info entire osnet-incorporation
#s12 sfe ~ pkg info entire osnet-incorporation name | grep FMRI
#             FMRI: pkg://solaris/consolidation/osnet/osnet-incorporation@11.4-11.4.0.0.1.15.0:20180817T002336Z
#             FMRI: pkg://solaris/entire@11.4-11.4.0.0.1.15.0:20180817T004203Z
#             FMRI: pkg://solaris/release/name@11.4-11.4.0.0.1.15.0:20180817T003543Z




##START build *greater then* 151, this is 152 and up, detect "Oracle Solaris 11 snv_166 X86" aka 2011.00 as s11ex201100
#NOTE: s11ex201100 <- 00 - nothing is released, to use "00" as placeholder in year 2011
#NOTE: we try to set a resonable release number in %osdistrelnumber
# name as well, they should behave similar. Remaining issues to be fixed
# in consuming spec file!
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 152 )
%if %( egrep 'Oracle Solaris 11' /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
#below: subject to change!
##TODO## replace s11ex201100
%define s11ex201100 1
%define solaris11express 1
%define osdistrelnumber 201100
%define solaris11 1
%define s110000 1
#11.1 build ??
%if %( uname -v | egrep '^11\.1$' > /dev/null && echo 1 || echo 0 )
#additive
%define s110100 1
%define osdistrelnumber 201101
%else
%endif
#11.2 build ??
%if %( uname -v | egrep '^11\.2$' > /dev/null && echo 1 || echo 0 )
#additive
%define s110100 1
%define s110200 1
%define osdistrelnumber 201102
%else
%endif
#11.3 build ??
%if %( uname -v | egrep '^11\.3$' > /dev/null && echo 1 || echo 0 )
#additive
%define s110100 1
%define s110200 1
%define s110300 1
%define osdistrelnumber 201103
%else
%endif
#11.4 build ??
%if %( uname -v | egrep '^11\.4$' > /dev/null && echo 1 || echo 0 )
#additive
%define s110100 1
%define s110200 1
%define s110300 1
%define s110400 1
%define osdistrelnumber 201104
%else
%endif
%define osdistrelname   "Solaris 11"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END


##START build 151 and up, detect "Oracle Solaris 11 Express snv_151a X86" aka 2010.11 as s11ex201011
#NOTE: we try to set a resonable release number in %osdistrelnumber
# name as well, they should behave similar. Remaining issues to be fixed
# in consuming spec file!
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 151 )
%if %( egrep 'Oracle Solaris 11 Express' /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
#below: subject to change!
%define s11ex201011 1
%define solaris11express 1
%define osdistrelnumber 201011
#                                below: subject to change!
%define osdistrelname   "Solaris 11 Express"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END


##START build 134 and up, os2010.05 as os201005
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 134 )
%if %( egrep 'Solaris Develop|Solaris Next Develop' /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
%define os201005 1
%define osdistrelnumber 201005
%define osdistrelname   "os2010.05"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END


##START build 111 and up, os2009.06 as os200906
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 111 )
%if %( egrep "OpenSolaris 2[0-9][0-9][0-9]" /etc/release > /dev/null  && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os200906 1
%define osdistrelnumber 200906
%define osdistrelname   "os2009.06"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END



##START build 101 and up, os2008.11 as os200811
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 101 )
%if %( egrep "OpenSolaris Develop" /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os200911 1
%define osdistrelnumber 200811
%define osdistrelname   "os2008.11"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END

#hipster sfe ~ pkg list | egrep "osnet|entire|/name"
#consolidation/osnet/osnet-incorporation           0.5.11-2015.0.2.15619      i--
#entire                                            0.5.11-2015.0.2.0          i--
#release/name                                      0.5.11-2013.0.0.0          i--
#hipster sfe ~ uname -a -v -r
#SunOS hipster 5.11 illumos-380fd67 i86pc i386 i86pc
 
#OpenIndiana 2017.10
#pkg info entire name osnet-incorporation | grep FMRI
#             FMRI: pkg://openindiana.org/consolidation/osnet/osnet-incorporation@0.5.11-2017.0.0.16838:20171118T005255Z
#             FMRI: pkg://openindiana.org/entire@0.5.11-2015.0.2.0:20151027T090547Z
#             FMRI: pkg://openindiana.org/release/name@0.5.11-2017.0.0.5:20171030T214925Z
#uname -a -r
#SunOS hipster 5.11 illumos-a3b2868063 i86pc i386 i86pc



# if we are on a IPS based system, hopefully the package entire
# is installed. record the output for later use to detect e.g. SRUs, build numbers
# we could ask for entire, but if someone decided to uninstall that for a reason?
# lets use this and hope no one ever uninstalls this package
#    FMRI: pkg://solaris/release/name@5.12-5.12.0.0.0.63.1:20141215T141436Z
# could use as well: system/core-os or system/kernel
#Update: sometimes we may see "name" and "entire" diverting in version numbers. That is a SRU might not necessarily update the "name" package.
#Now we collect from more packages and just use the one with the highest version
#testing: (echo 0.5.11,5.11-0.175.3.19.0.5.0; echo 0.5.11,5.11-0.175.3.11.0.4.0; echo 0.5.11,5.11-0.175.3.19.0.5.0) | sort -n -t'.' | tail -1

%if %{os2nnn}
#entire might be uninstalled, so use release/name instead. You don't uninstall it! If you do, then don't blame us if pnm_macros get confused.
#DEBUG %define marker2_not_defined_osdistro_entire %( echo marker2 >> /tmp/pkg_wrapper_log )

#could be made a bit better atomic stile!
#works %define osdistro_entire_cache_helper %( test -f /tmp/pkg_info_release_name_entire_consolidation_osnet_osnet_incorporation || pkg info release/name entire consolidation/osnet/osnet-incorporation > /tmp/pkg_info_release_name_entire_consolidation_osnet_osnet_incorporation )
%define osdistro_entire_cache_helper %( test -f /tmp/pkg_info_release_name_entire_consolidation_osnet_osnet_incorporation -a /tmp/pkg_info_release_name_entire_consolidation_osnet_osnet_incorporation -nt %{buildroot} || pkg info release/name entire consolidation/osnet/osnet-incorporation > /tmp/pkg_info_release_name_entire_consolidation_osnet_osnet_incorporation )

%define osdistro_entire %( cat /tmp/pkg_info_release_name_entire_consolidation_osnet_osnet_incorporation | grep "FMRI:" | sed -e 's?FMRI:.*release/name@??' -e s'/.*-//' -e s'/:.*//' | sort -n -t'.' | tail -1 )

#original %define osdistro_entire %( pkg info release/name entire consolidation/osnet/osnet-incorporation | grep "FMRI:" | sed -e 's?FMRI:.*release/name@??' -e s'/.*-//' -e s'/:.*//' | sort -n -t'.' | tail -1 )
%endif

#older hipster doesn't match entire and release/name version packages. People! Don't uninstall entire on a OIHipster machine please!
#release/name 0.151.1.8 
#entire 2015.0.1.1
##TODO## make version detection more robust, entire package might have been uninstalled, which packages to use for version detection in that case?
## PJAMA *puts hand up as having uninstalled "entire"*
## perhaps osnet-incorporation is a better option for the moment (or release/name? or the most fresh of both?)
# pkg info name osnet-incorporation entire | grep FMRI                                                                                                                                       
#           FMRI: pkg://openindiana.org/consolidation/osnet/osnet-incorporation@0.5.11-2017.0.0.16838:20171118T005255Z
#           FMRI: pkg://openindiana.org/entire@0.5.11-2015.0.2.0:20151027T090547Z
#           FMRI: pkg://openindiana.org/release/name@0.5.11-2017.0.0.5:20171030T214925Z
%if %{oihipster}
#%define osdistro_entire %( pkg info entire | grep "FMRI:" | sed -e 's/FMRI:.*entire@//' -e s'/.*-//' -e s'/:.*//' )
#DEBUG %define marker3 %( echo marker3 >> /tmp/pkg_wrapper_log )
%define osdistro_entire %( pkg info osnet-incorporation | grep "FMRI:" | sed -e 's/FMRI:.*osnet-incorporation@//' -e s'/.*-//' -e s'/:.*//' )
%endif

%if %{os2nnn}
#echo 5.12.0.0.0.63.0 | awk -F'.' '{printf "%.4d%.4d%.4d%.4d%.4d%.4d%.4d", $1, $2, $3, $4, $5, $6, $7}'
#0005001200000000000000630000
#%define osdistro_entire_padded_number4 %( echo %{osdistro_entire} | awk -F'.' '{printf "%.4d%.4d%.4d%.4d%.4d%.4d%.4d", $1, $2, $3, $4, $5, $6, $7}' )
#%define osdistro_entire_padded_number4 %( echo %{osdistro_entire} | awk -F'.' '{printf "\%.4d\%.4d\%.4d\%.4d\%.4d\%.4d\%.4d", $1, $2, $3, $4, $5, $6, $7}' )
#note:  %% results in a % to awk
%define osdistro_entire_padded_number4 %( echo %{osdistro_entire} | awk -F'.' '{printf "%%.4d%%.4d%%.4d%%.4d%%.4d%%.4d%%.4d", $1, $2, $3, $4, $5, $6, $7}' )
%else
%define osdistro_entire 0
%endif

#add a workaround to distinguish the "letter" releases like r151022h and r151022y
#make the latter a number and add it to osdistro_entire_padded_number4 
#0000151022 0000 0008 000000000000   is r151022h
#0000151022 0000 0025 000000000000   is r151022y
#0000151022 0001 0020 000000000000   is r151022at
#
#pnm: osdistro_entire    151030.3
#pnm: osdistro_entire_padded_number4 1510300003-0096-0096000000000000 (wrong!)
#pnm: osdistro_entire_padded_number4 1510300003-0000-0003000000000000 (correct!)

%if %( expr %{omnios} '=' 1 '&' %{osdistro_entire} '<' 151028  )
#get char if any
#shift to the right in case of one letter release - test:  (echo a; echo yz) | /usr/gnu/bin/sed -e 's?^[a-z]$? &?'
%define osdistrelnumber_letterrelease_char_all %( /usr/gnu/bin/egrep "OmniOS v[0-9]* r[0-9]*[a-z]{0,2}$" /etc/release | /usr/gnu/bin/sed -e 's?^.*[0-9][0-9][0-9][0-9][0-9][0-9]??' | /usr/gnu/bin/egrep "^[a-z][a-z]*$" | /usr/gnu/bin/sed -e 's?^[a-z]$? &?' )
%define osdistrelnumber_letterrelease_char_1 %( echo %{osdistrelnumber_letterrelease_char_all} |  /usr/gnu/bin/sed -e 's?.$??'  -e 's?^?\o134\o134\o047?' )
%define osdistrelnumber_letterrelease_char_2 %( echo %{osdistrelnumber_letterrelease_char_all} |  /usr/gnu/bin/sed -e 's?^.??'  -e 's?^?\o134\o134\o047?' )
#make char a number, note! \o047 puts an >\'< before the letter in the sed command above (without the > <)
%define osdistrelnumber_letterrelease_number_1 %( expr -96 '+' `/usr/bin/printf "%%d" \\%{osdistrelnumber_letterrelease_char_1}` )
%define osdistrelnumber_letterrelease_number_2 %( expr -96 '+' `/usr/bin/printf "%%d" \\%{osdistrelnumber_letterrelease_char_2}` )
%define osdistro_entire_padded_number4 %( echo %{osdistro_entire} | awk -F'.' '{printf "%%.4d%%.4d%%.4d%%.4d%%.4d%%.4d%%.4d", $1, $2, %{osdistrelnumber_letterrelease_number_1}, %{osdistrelnumber_letterrelease_number_2}, $5, $6, $7}' )
%endif


#OmniOSce from 151028 on has the number extention xxxxxx.<n>
%if %( expr %{omnios} '=' 1 '&' %{osdistro_entire} '>=' 151028  )
#add calc to make .3 -> 0000.0003
#add calc to make .55 -> 0002.0003
# expr 52 '/' 26
#2
# expr 51 '/' 26
#1
# expr 51 '%' 26
#25
%define osdistrelnumber_letterrelease_number_full %( echo %{osdistro_entire} | awk -F'.' '{print $2}' )
%define osdistrelnumber_letterrelease_number_1 %( expr %{osdistrelnumber_letterrelease_number_full} '/' 26 )
%define osdistrelnumber_letterrelease_number_2 %( expr %{osdistrelnumber_letterrelease_number_full} '%%' 26 )
%define osdistro_entire_padded_number4 %( echo %{osdistro_entire} | awk -F'.' '{printf "%%.4d%%.4d%%.4d%%.4d%%.4d%%.4d%%.4d", 0, $1, %{osdistrelnumber_letterrelease_number_1}, %{osdistrelnumber_letterrelease_number_2}, $5, $6, $7}' )
# 151030             .3
# 151030 0000 0000 0003 000000000000
#        ^reserved
#             ^modulo 26
#                  ^div 26
%endif

### bail out, detection of the os2... distribution failed!
###%if %{osdet299999}
###echo "Error. Detection of OS Distribution failed in osdistro.inc"
###exit 1
###%endif

##overall the include file - we are already included
%endif 


%changelog
* Tue Sep 17 2019 - Thomas Wagner
- enhance defines for Solaris 11.4 to propperly detect GA release (S11.4 S12)
* Thr Jul 25 2019 - Thomas Wagner
- cache the output of "pkg info entire ...osnet-incorp..." to speed up overly re-processed osdistro.inc (annoying pkgbuild oddity)
* Tue Jun 25 2019 - Thomas Wagner
- OmniOSce has changed version numbers of entire package, release/name shows 0.5.11-151030.3, entire shows 0.5.11-151030.0, affects osdistro_entire_padded_number4
  rewrite detection of sub-releases formerly represented by one or two letters (OM >= 151028, 151030 LTS)
* Sun Dec 23 2018 - <me@tsundoku.ne.jp>
- add defines for Solaris 11.4
* Fri Mar  2 2018 - Thomas Wagner
- support two letter OS revisions for OmniOSce (OM)
* Fri Dec 15 2017 - Thomas Wagner
- avoid "(" and ")" in egrep regex, some pkgbuild versions can't escape these propperly
* Fri Dec  8 2017 - Thomas Wagner
- spec full path to /usr/bin/printf
* Sat Dec  2 2017 - Thomas Wagner
- improve detection for OmniOSce with two letters as sub release e.g. r151022aa (OM)
* Tue Nov  7 2017 - Thomas Wagner
- detect OmniOSce with new pattern in uname -v .... omnios-r151022-eb9d5cb557
* Sun Oct  8 2017 - Thomas Wagner
- harden release detection for S11 and use most recent version of release/name | entire | consolidation/osnet/osnet-incorporation
* Mon Oct 31 2016 - Thomas Wagner
- add / detect oih20160926 with changed name in /etc/release: OpenIndiana Hipster 2016.04 / Assembled 17 August 2016 pkg info osnet-incorporation -> 2016.0.1.15945:20161028T005445Z
* Thu Oct 13 2016 - Thomas Wagner
- merged in & commit pjama's changes. 1,$s/20160423/20160421/ (OIH)
* Sat Oct  8 2016 - pjama
- add later OIHipster snapshots oih20160421 oih20151003
- use pkg name "osnet-incorporation" instead of "entire" to test for OIHipster version
* Tue May 24 2016 - Thomas Wagner
- remove --date from date command (OIH) 
* Sat Nov 28 2015 - Thomas Wagner
- add more OIHipster switches
- fix osdistro_entire_padded_number4 by using entire@version (OIH)
* Wed Aug  5 2015 - Thomas Wagner
- typo $->% in %define osdistrelnumber (OOS/OM)
* Mon Jul 27 2015 - Thomas Wagner
- verify/merge hipster integration (thanks to pjama)
* Mon May 25 2015 - pjama
- add config for hipster
* Fri Jan 23 2015 - Thomas Wagner
- add experimental version of osdistro_entire_padded_number4 (IPS based Systems),
  enables compares, e.g. expr %{osdistro_entire_padded_number4} '>=' 0005001200000000000000610000
* Thu Jan 22 2015 - Thomas Wagner
- add a first experimental version of osdistro_entire
* Sun Dec 14 2014 - Thomas Wagner
- add s11 11.3 support, define s110300 and distrelnumber 201103 (S11.3)
* Sat Apr 12 2014 - Thomas Wagner
- re-add OpenIndiana (was edit error)
* Sat Apr 12 2014 - Thomas Wagner
- add omnios OmniOS v11 r151008 support (OOS151008)
* Sun Mar 23 2014 - Thomas Wagner
- add s11 11.2 support, define s110200 and distrelnumber 201102 (S11.2)
- fix osdistrelnumber (S11.1)
- add solaris11 1 to Solaris 11 releases
* Wed Feb 12 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- typo in egrep regex to define s110100 for S11.1
* Mon Jan  6 2014 - Thomas Wagner
- typo in define osbuild for S12
* Sat Sep 28 2013 - Thomas Wagner
- quick solution to workaound differen uname -v output on OI hipster
* Thu Sep 19 2013 - Ian Johnson
- fix egrep "Oracle Solaris 11" to really detect (S11.1)
* Mon Jul  1 2013 - Thomas Wagner
- add s11 11.1 support
* Thu Jun 27 2013 - Thomas Wagner
- renamed s12 variables
* Sun Jun 22 2013 - Thomas Wagner
- start prelimiary support for S12
* Thu Jun 21 2012 - Thomas Wagner
- osbuild needs to work with 151a4, should print 151 and not 151a4,
  change sed pattern
* Mon Nov  7 2011 - Thomas Wagner
- add Support for builds (173)(174) as osbuild=175 Oracle Solaris 11 11/11
* Fri Jun 17 2011 - Thomas Wagner
- changed osdistrelname "OI147" to read "OpenIndiana", "os2010.11" to read "Solaris11Express"
- added boolean flags for: openindiana solaris11express oi201009 oi201100 s11ex201011 s11ex201100
- removed boolean flags for: os201011 (renamed to s11ex201011), oi147 (renamed to oi201009)
- added OpenIndiana development release with build 151 number, faked distreleasenumber to oi201100 (00 to be changed later)
- make grep on /etc/release more relaxed on "Oracle Solaris 11 "
* Wed Mar 16 2011 - Thomas Wagner
- add Oracle Solaris 11 Express to the mix
* Sat Oct 20 2010 - Thomas Wagner
- add OI 147 to the mix
* May 31 2010 - Thomas Wagner
- rename 201003/2010.03 to 201005/2010.05 (speculative)
- change egrep for builds >=134 to match OpenSolaris Development and Solaris Next Development
- remove typo os2distrelname -> osdistrelname
- for SXCE %define osdistrelname   "SXCE"
* May  5 2010 - Thomas Wagner
- fix ifs to give echo 0 | echo 1 and not strings or exitcodes
- lot's of fixes over time, especially %if logic is non standard in spec files...
-i initial - drafting the idea, bugs are the only feature of this include file
