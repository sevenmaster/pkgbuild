# /* vim: set filetype=spec : */ 

#note: one piece of the include files is generated automaticly:
#      generate the file packagenames.defines.inc by fetching the
#      attached file "attachment (id=3635) / The final new package
#      names sorted by new name"
#      from the bug (see script) and then run packagenames-convert.pl
#      http://defect.opensolaris.org/bz/show_bug.cgi?id=6186 
#      ./packagenames-convert.pl < attachment_id_3635 > packagenames.define-133.inc

# http://hub.opensolaris.org/bin/view/Project+indiana/Renamed+Packages+in+Build+133


#already included before?
%if %{?osdistro:%{osdistro}}%{?!osdistro:0}
#yes, osdistro.inc is already included
%else
%include osdistro.inc
%endif

#already included before?
%if %{?osdistrofeatures:%{osdistrofeatures}}%{?!osdistrofeatures:0}
#yes, osdistrofeatures.inc is already included
%else
%include osdistrofeatures.inc
%endif

#use for testing:    pkgbuild --interactive base-specs/packagenamemacros.spec
#you may want to edit your test cases into the base-specs/packagenamemacros.spec

#packagenamemacros.inc is included --- NOTE: this variable is primarily 
# for internal use by packagenamemacros.inc
%define packagenamemacros 1

# inially including a general file with definitions. Later on, some of
# those definitions get overwritten if needed

%include packagenames.define.initial.inc

# order in this include file: OLDEST build on top, ascending
# 81
# 111
# newer/including 133
#    the reason for this order is: you might easily overwrite
#    an old definition with a new one starting with a specific build number!
#    e.g. from 81 to 111 the package was named hugo
#         from 133 on up to today the package was named freshhugo
#    the only exception is, you can't delete a define if a pacakge name is gone
#    completely (that is: merged into another one / obsoleted) - then set the
#    replacement beginning with the build number to the merged name or a well-known
#    package name which is required anyways and let pkgbuild sort that douplicates out

# more complicated combinations should be handled in the spec files itself, to make
# this include file not too complex.

# next list all build versions ascending (build version)
# BIG NOTE: OS distribution specific cases (SVR4/SXCE and IPS, but not S10) are 
# handled *inside* the blocks' includes # this is to make this only decide on build numbers!
# see for special cases the files packagenames.define-specialcases-NNN.inc (build NNN and up)
# NOTE: a later include file may overwrite a define from same or previous block
#       and might be overwritten or set to empty string in a later includefile /and build/ as well

#normal packages in IPS did get theyer -devel name stripped off and the files flagged
#as "devel" instead
#in the end packages on IPS combine regular and devel parts into one single package
%if %( expr %{osbuild} '>=' 81 '|' %{solaris12} '=' 0 )
%if %( expr %{osbuild} '<' 133 '|' %{solaris12} '=' 0 )
%include packagenames.define-81.inc
%include packagenames.define-specialcases-81.inc
#<133
%endif
#>=81
%endif

#huge package rename actions took place with build 133 (including)
#http://defect.opensolaris.org/bz/show_bug.cgi?id=6186
%if %( expr %{osbuild} '>=' 133  '|' %{solaris12} '>=' 1 '|' %{omnios} '>=' 1 )
%include packagenames.define-133.inc
%include packagenames.define-specialcases-133.inc
#>=133
%endif

#NOTE: cumulative, this includes the settings from builds before
#package rename actions took place with build 134 (including)
#http://defect.opensolaris.org/bz/show_bug.cgi?id=6186
%if %( expr %{osbuild} '>=' 134  '|' %{solaris12} '>=' 1 '|' %{omnios} '>=' 1 )
%include packagenames.define-134.inc
%include packagenames.define-specialcases-134.inc
#>=133
%endif

#NOTE: cumulative
#OmniOS unfortunatly removed (all?) legacy package names. Therefore we 
#need to add pnm_macros for translate those from e.g. SUNWzlib to library/zlib
%if %{omnios}
%include packagenames.define.omnios.inc
%include packagenames.define.omnios-specialcases.inc
#>=133
%endif


# finally including a general file with definitions, to overwrite possible
# special cases (and eventually overriding content which got defined above)

%include packagenames.define.allbuilds.inc

%changelog
* Fri May 16 2014 - Thomas Wagner
- %include packagenames.define.initial.inc to pre-load defaults
- add Support for OmniOS with packagenames.define.omnios.inc / packagenames.define.omnios-specialcases.inc
* Mon Nov  4 2013 - Thomas Wagner
- make check for osdistrofeatures.inc robust against non-defined %{osdistrofeatures} variable
* Fri Jun 28 2013 - Thomas Wagner
- first s12 support
* Thu Jun 20 2013 - Thomas Wagner
- include osdistrofeatures.inc
* Wed Mar 16 2011 - Thomas Wagner
- add missing changelog
- change include order to include packagenames.define.allbuilds.inc at the 
  very end, instead at the top
