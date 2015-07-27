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

#osdistro.inc is included --- NOTE: this variable is primarily for internal use by osdistro.inc
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
# 20150330 = Iso Snapshot
# 20141010 = Iso Snapshot
# 20140701 = Iso Snapshot
%if %( uname -v | egrep '^illumos-' > /dev/null && echo 1 || echo 0 )
%define osbuild 151
%endif

#quick and dirty hack, only works on OmniOS - uname -v prints on 151008j: omnios-6de5e81
%if %( uname -v | egrep '^omnios-[0-9a-f]' > /dev/null && echo 1 || echo 0 )
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
%define oih20150330 0
%define oih20141010 0
%define oih20140701 0

#OpenIndiana
# could be oi201009 and oi201100 or something, the first development release and following
##TODO## replace oi201100
%define oi201100 0
%define oi201009 0

#Solaris 12
#always defined on 12.0 and all subsequent 12.xx versions. build 00.
%define s120000 0
#12.0 build 24
%define s120024 0

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
%define osdistrelnumber $( grep "OmniOS v[0-9]* r[0-9]*" /etc/release | sed -e 's?^.*OmniOS v[0-9]* *r??' )
#                                below: subject to change!
%define osdistrelname   "OmniOS"
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
%if %( egrep 'OpenIndiana Development' /etc/release > /dev/null && echo 1 || echo 0 )
# Detect if hipsterish
%if %( uname -v | egrep '^illumos-' > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
#below: subject to change!
%define oihipster 1
# Find date of osnet-incorporation and change to ISO date format
# Not sure how this will go with pre-iso snapshot updated to post-iso packages
%define osbuilddate %(pkg info osnet-incorporation | grep 'Packaging Date' | cut -d' ' -f 3,4,5 | date --date=- +%Y%m%d)

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
%if %( egrep 'OpenIndiana Development' /etc/release > /dev/null && echo 1 || echo 0 )
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

#NOTE: s121200 <- 1200 - 12.00 - nothing is released, all is speculative. Later Updates, e.g. 12.1 -> 1201
%if %{osdet299999}
%if %( expr %{osbuild} '>=' 24 )
%if %( egrep 'Oracle Solaris 12' /etc/release > /dev/null && echo 1 || echo 0 )
#we are on an IPS based OS distro
%define os2nnn   1
#below: subject to change!
%define s120000 1
%define s120024 1
%define solaris12 1
%define osdistrelnumber 24
#                                below: subject to change!
%define osdistrelname   "Solaris 12"
#this was the last check, skip all others
%define osdet299999 0
%else
%endif
%else
%endif
%else
%endif
##END


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


# if we are on a IPS based system, hopefully the package entire
# is installed. record the output for later use to detect e.g. SRUs, build numbers
# we could ask for entire, but if someone decided to uninstall that for a reason?
# lets use this and hope no one ever uninstalls this package
#    FMRI: pkg://solaris/release/name@5.12-5.12.0.0.0.63.1:20141215T141436Z
# could use as well: system/core-os or system/kernel
%if %{os2nnn}
#%define osdistro_entire %( pkg info entire | grep "FMRI:" | sed -e 's/FMRI:.*entire@//' -e s'/.*-//' -e s'/:.*//' )
%define osdistro_entire %( pkg info release/name | grep "FMRI:" | sed -e 's?FMRI:.*release/name@??' -e s'/.*-//' -e s'/:.*//' )
#echo 5.12.0.0.0.63.0 | awk -F'.' '{printf "%.4d%.4d%.4d%.4d%.4d%.4d%.4d", $1, $2, $3, $4, $5, $6, $7}'
#0005001200000000000000630000
#%define osdistro_entire_padded_number4 %( echo %{osdistro_entire} | awk -F'.' '{printf "%.4d%.4d%.4d%.4d%.4d%.4d%.4d", $1, $2, $3, $4, $5, $6, $7}' )
#%define osdistro_entire_padded_number4 %( echo %{osdistro_entire} | awk -F'.' '{printf "\%.4d\%.4d\%.4d\%.4d\%.4d\%.4d\%.4d", $1, $2, $3, $4, $5, $6, $7}' )
#note:  %% results in a % to awk
%define osdistro_entire_padded_number4 %( echo %{osdistro_entire} | awk -F'.' '{printf "%%.4d%%.4d%%.4d%%.4d%%.4d%%.4d%%.4d", $1, $2, $3, $4, $5, $6, $7}' )
%else
%define osdistro_entire 0
%endif



### bail out, detection of the os2... distribution failed!
###%if %{osdet299999}
###echo "Error. Detection of OS Distribution failed in osdistro.inc"
###exit 1
###%endif


%changelog
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
- initial - drafting the idea, bugs are the only feature of this include file
