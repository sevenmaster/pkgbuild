# /* vim: set filetype=spec : */ 
# 
# place defines to match older packages here - this include file is the first of a series
# 
##TODO## list see at the end, shortly before %changelog

# there are very old build out there, we might not need
# to write special logic for builds older then build 81
# at least we should have logic for build 111 (or 101)
# and younger (there are lots of installs out there)

# normally packages are not too much fragmented into
# subpackages. (exception: openssl where we simply
# require all sub packages to keep things easy)

# in general:
#    pnm_buildrequires_packagenames     packagename-devel (on this special range of builds, -devel 
#                                                          if that exists, else just the package name)
#         pnm_requires_packagenames     packagename (on this special range of builds)

# note: the right hand side changes depending on the range of the build number where the include
# file is intended for. the left hand side always lists the package names in currently three
# variants: old SVR4 from SolarisExpress/early or OS2008/OS2009 the early OpenSolaris IPS based
# then the names on OpenSolaris IPS-base without the SUNW prefix and before the big renaming
# around build 133/134


# below this section will be overwritten by the include files for the later builds
# it is there so support build machines with osbuild < 133 or < 134
# but the spec file shave been written with package names presen on
# machines with newer osbuild / after the big package renaming bang

#note defines below will be overwritten with a new target package name
#because it got renamed by the two big renaming projects, 
#starting with build ??? and build 133/134 
#openssl is always a special case since sub packages got combined
#below: our target system is an IPS based OS2008/OS2009/OS2010 
#         *before the big package renaming party*
##TODO## check osbuilds 129 .. 135 to be fully covered! Else run
# pkgtool --interactive prep base-specs/packagenamemacros.spec
# and mail us the output
#note name aliasing the package on build say "< 133" should work
#cases os2nnn
%if %{os2nnn}
%define pnm_buildrequires_SUNWopenssl			SUNWopenssl
%define pnm_buildrequires_SUNWopenssl_include           SUNWopenssl
#handy alias based on typo
%define pnm_buildrequires_SUNWopenssl_includes		SUNWopenssl
%define pnm_buildrequires_SUNWopenssl_commands		SUNWopenssl
%define pnm_buildrequires_SUNWopenssl_libraries		SUNWopenssl
%define pnm_buildrequires_SUNWopensslr			SUNWopenssl

%define pnm_requires_SUNWopenssl			SUNWopenssl
%define pnm_requires_SUNWopenssl_include		SUNWopenssl
#handy alias based on typo
%define pnm_requires_SUNWopenssl_includes		SUNWopenssl
%define pnm_requires_SUNWopenssl_commands		SUNWopenssl
%define pnm_requires_SUNWopenssl_libraries		SUNWopenssl
%define pnm_requires_SUNWopensslr			SUNWopenssl

%define pnm_buildrequires_openssl			SUNWopenssl
%define pnm_requires_openssl				SUNWopenssl

%define pnm_buildrequires_library_security_openssl	SUNWopenssl
%define pnm_requires_library_security_openssl		SUNWopenssl

#SUNWwgetu/SUNWwgetr/SUNWwget wget web/wget
%define pnm_buildrequires_web_wget			SUNWwget
%define pnm_requires_web_wget				SUNWwget
%define pnm_buildrequires_wget				SUNWwget
%define pnm_requires_wget				SUNWwget
%define pnm_buildrequires_SUNWwgetu			SUNWwget
%define pnm_requires_SUNWwgetu				SUNWwget
%define pnm_buildrequires_SUNWwgetr			SUNWwget
%define pnm_requires_SUNWwgetr				SUNWwget
%define pnm_buildrequires_SUNWwget			SUNWwget
%define pnm_requires_SUNWwget				SUNWwget

#SUNWGtku/SUNWGtkr/SUNWGtk Gtk library/desktop/gtk1
%define pnm_buildrequires_library_desktop_gtk1		SUNWGtk
%define pnm_requires_library_desktop_gtk1		SUNWGtk
%define pnm_buildrequires_SUNWGtk_devel			SUNWGtk
%define pnm_buildrequires_SUNWGtk			SUNWGtk
%define pnm_requires_SUNWGtk				SUNWGtk
%define pnm_buildrequires_Gtk				SUNWGtk
%define pnm_requires_Gtk				SUNWGtk

%define pnm_requires_SUNWGtku				SUNWGtk
%define pnm_requires_SUNWGtkr				SUNWGtk

#kerberos
%define pnm_buildrequires_service_security_kerberos_5  SUNWkrb
%define pnm_requires_service_security_kerberos_5       SUNWkrb

%define pnm_buildrequires_SUNWkrb 		SUNWkrb
%define pnm_buildrequires_SUNWkrbr		SUNWkrb
%define pnm_buildrequires_SUNWkrbu		SUNWkrb
%define pnm_requires_SUNWkrb                    SUNWkrb
%define pnm_requires_SUNWkrbr 			SUNWkrb
%define pnm_requires_SUNWkrbu 			SUNWkrb

#note: pkg search -l SUNWsmba 
#returns nothing. So use the very old names SUNWsmbau/SUNWsmbar instead.
#samba service/network/samba
%define pnm_buildrequires_service_network_samba	SUNWsmbau
%define pnm_requires_service_network_samba	SUNWsmbau
%define pnm_buildrequires_SUNWsmba_devel 	SUNWsmbau
%define pnm_buildrequires_SUNWsmba		SUNWsmbau
%define pnm_buildrequires_SUNWsmbar		SUNWsmbar
%define pnm_buildrequires_SUNWsmbau		SUNWsmbau
%define pnm_requires_SUNWsmba			SUNWsmbau
%define pnm_requires_SUNWsmbar			SUNWsmbar
%define pnm_requires_SUNWsmbau			SUNWsmbau
%define pnm_buildrequires_smba			SUNWsmbau
%define pnm_requires_smba			SUNWsmbau


%define pnm_buildrequires_library_ncurses 			library/ncurses
%define pnm_requires_library_ncurses			 	library/ncurses
%define pnm_buildrequires_SUNWncurses_devel 			library/ncurses
%define pnm_buildrequires_SUNWncurses 				library/ncurses
%define pnm_requires_SUNWncurses 				library/ncurses
%define pnm_buildrequires_ncurses 				library/ncurses
%define pnm_requires_ncurses 					library/ncurses
#pre build 100 we're missing ncurses and use SFEncurses instead
#but we are >>>>100 here
%define pnm_buildrequires_SFEncurses_devel 			library/ncurses
%define pnm_buildrequires_SFEncurses 				library/ncurses
%define pnm_requires_SFEncurses 				library/ncurses



#SFElibsndfile/SUNWlibsndfile
#for now, we always default to the SFE version 1.0.25 located in /usr/gnu
#for every platform
#SFElibsndfile/SFElibsndfile-devel or SUNWlibsndfile (no -devel)
%define pnm_buildrequires_library_gnu_libsndfile		SFElibsndfile
%define pnm_requires_library_gnu_libsndfile			SFElibsndfile
%define pnm_buildrequires_SFElibsndfile_devel			SFElibsndfile
%define pnm_buildrequires_SFElibsndfile				SFElibsndfile
%define pnm_requires_SFElibsndfile				SFElibsndfile
#Devel-Package SUNWlibsndfile_devel doesn't really exist, but define it anyways:
%define pnm_buildrequires_library_libsndfile			SFElibsndfile
%define pnm_requires_library_libsndfile				SFElibsndfile
%define pnm_buildrequires_libsndfile				SFElibsndfile
%define pnm_requires_libsndfile					SFElibsndfile
%define pnm_buildrequires_SUNWlibsndfile_devel			SFElibsndfile
%define pnm_buildrequires_SUNWlibsndfile			SFElibsndfile
%define pnm_requires_SUNWlibsndfile				SFElibsndfile

#Nvidia driver names
#for the moment, just make a file require, as this matches driver/graphics/nvidia and NVDAgraphics
#/usr/X11/include/NVIDIA/vdpau/vdpau.h
#users might have installed the SVR4 package directly from nvidia
#%define pnm_buildrequires_driver_graphics_nvidia		driver/graphics/nvidiadriver/graphics/nvidia
#%define pnm_requires_driver_graphics_nvidia			driver/graphics/nvidia
%define pnm_buildrequires_driver_graphics_nvidia		/usr/X11/include/NVIDIA/vdpau/vdpau.h
%define pnm_requires_driver_graphics_nvidia			/usr/X11/include/NVIDIA/vdpau/vdpau.h

##TODO## Add your packages here in case you specify an old

%endif
#END os2nnn

#IPS has a problem: pkg info SUNWopenssl says *not installed* but at the same
#time pkg info openssl (or library/security/openssl) says installed.
#this is problematic, since based on the SUNWopenssl alias name it is still
#tobe seen as *installed* - every package prerequisite check by the old
#compatibilty/alias name *is* *failing* then
#below: our target system is an IPS based OS2010++ ... incl. Oracle Solaris 11 Express
#         *AFTER the big package renaming party*
#note: target is "openssl" which is understood by 133/134++ releases as installed
#and still works with early opensolaris builds as well
##TODO## this is accumulative (see above %if %{os2nnn} w/o osbuild detection

#cases >=133 AND os2nnn
%if %{os2nnn}
##TODO## Re-visit this buildnumber, was this 133 or 134 ? (pkg info SUNWopenssl says not installed)
%if %( expr %{osbuild} '>=' 133 '|' %{solaris12} '>=' 1 )
%define pnm_buildrequires_SUNWopenssl			library/security/openssl
%define pnm_buildrequires_SUNWopenssl_include           library/security/openssl
#handy alias based on typo
%define pnm_buildrequires_SUNWopenssl_includes		library/security/openssl
%define pnm_buildrequires_SUNWopenssl_commands		library/security/openssl
%define pnm_buildrequires_SUNWopenssl_libraries		library/security/openssl
%define pnm_buildrequires_SUNWopensslr			library/security/openssl

%define pnm_requires_SUNWopenssl			library/security/openssl
%define pnm_requires_SUNWopenssl_include		library/security/openssl
#handy alias based on typo
%define pnm_requires_SUNWopenssl_includes		library/security/openssl
%define pnm_requires_SUNWopenssl_commands		library/security/openssl
%define pnm_requires_SUNWopenssl_libraries		library/security/openssl
%define pnm_requires_SUNWopensslr			library/security/openssl

%define pnm_buildrequires_openssl			library/security/openssl
%define pnm_requires_openssl				library/security/openssl

%define pnm_buildrequires_library_security_openssl	library/security/openssl
%define pnm_requires_library_security_openssl		library/security/openssl


%define pnm_buildrequires_library_python_2_python_gnome_libs_26	library/python-2/python-gnome-libs-26
%define pnm_requires_library_python_2_python_gnome_libs_26	library/python-2/python-gnome-libs-26
%define pnm_buildrequires_SUNWgnome_python26_libs_devel	library/python-2/python-gnome-libs-26
%define pnm_requires_SUNWgnome_python26_libs_devel	library/python-2/python-gnome-libs-26
%define pnm_buildrequires_SUNWgnome_python26_libs	library/python-2/python-gnome-libs-26
%define pnm_requires_SUNWgnome_python26_libs		library/python-2/python-gnome-libs-26


#SUNWwgetu/SUNWwgetr/SUNWwget wget web/wget
%define pnm_buildrequires_web_wget			web/wget
%define pnm_requires_web_wget				web/wget
%define pnm_buildrequires_wget				web/wget
%define pnm_requires_wget				web/wget
%define pnm_buildrequires_SUNWwgetu			web/wget
%define pnm_requires_SUNWwgetu				web/wget
%define pnm_buildrequires_SUNWwgetr			web/wget
%define pnm_requires_SUNWwgetr				web/wget
%define pnm_buildrequires_SUNWwget			web/wget
%define pnm_requires_SUNWwget				web/wget

#SUNWGtku/SUNWGtkr/SUNWGtk Gtk library/desktop/gtk1
%define pnm_buildrequires_library_desktop_gtk1		library/desktop/gtk1
%define pnm_requires_library_desktop_gtk1		library/desktop/gtk1
%define pnm_buildrequires_SUNWGtk_devel			library/desktop/gtk1
%define pnm_buildrequires_SUNWGtk			library/desktop/gtk1
%define pnm_requires_SUNWGtk				library/desktop/gtk1
%define pnm_buildrequires_Gtk				library/desktop/gtk1
%define pnm_requires_Gtk				library/desktop/gtk1

%define pnm_requires_SUNWGtku				library/desktop/gtk1
%define pnm_requires_SUNWGtkr				library/desktop/gtk1

#samba service/network/samba
%define pnm_buildrequires_service_network_samba		service/network/samba
%define pnm_requires_service_network_samba		service/network/samba
%define pnm_buildrequires_SUNWsmba_devel		service/network/samba
%define pnm_buildrequires_SUNWsmba			service/network/samba
%define pnm_buildrequires_SUNWsmbar			service/network/samba
%define pnm_buildrequires_SUNWsmbau			service/network/samba
%define pnm_requires_SUNWsmba				service/network/samba
%define pnm_requires_SUNWsmbar				service/network/samba
%define pnm_requires_SUNWsmbau				service/network/samba
%define pnm_buildrequires_smba				service/network/samba
%define pnm_requires_smba				service/network/samba

# note: there is in real no SUNWlibC -devel package!
# note: that is renamed on OI to system/library/c++/sunpro !
%define pnm_buildrequires_SUNWlibC_devel		system/library/c++-runtime
%define pnm_buildrequires_SUNWlibC			system/library/c++-runtime
%define pnm_requires_SUNWlibC				system/library/c++-runtime

# note: there is in real no SUNWsqlite3 -devel package!
%define pnm_buildrequires_SUNWsqlite3_devel		database/sqlite-3
%define pnm_buildrequires_SUNWsqlite3			database/sqlite-3
%define pnm_requires_SUNWsqlite3			database/sqlite-3
%define pnm_buildrequires_sqlite3			database/sqlite-3
%define pnm_requires_sqlite3				database/sqlite-3


#kerberos
%define pnm_buildrequires_service_security_kerberos_5  system/security/kerberos-5
%define pnm_requires_service_security_kerberos_5       system/security/kerberos-5

%define pnm_buildrequires_SUNWkrb 		system/security/kerberos-5
%define pnm_buildrequires_SUNWkrbr		system/security/kerberos-5
%define pnm_buildrequires_SUNWkrbu		system/security/kerberos-5
%define pnm_requires_SUNWkrb                    system/security/kerberos-5
%define pnm_requires_SUNWkrbr 			system/security/kerberos-5
%define pnm_requires_SUNWkrbu 			system/security/kerberos-5

#plugin-php52 itself can't be checked for being installed (on IPS it is only
#a meta package!), use module instead.
#this overwrites content from packagenames.define-133.inc
#maybe could be moved to special cases packagenames.define-specialcases-133.inc ?
#web/server/apache-22/plugin/plugin-php52 -->> web/server/apache-22/module/apache-php5
%define pnm_buildrequires_web_server_apache_22_plugin_plugin_php52	web/server/apache-22/module/apache-php5
%define pnm_requires_web_server_apache_22_plugin_plugin_php52	web/server/apache-22/module/apache-php5
%define pnm_buildrequires_SUNWapch22m_php52_devel	web/server/apache-22/module/apache-php5
%define pnm_buildrequires_SUNWapch22m_php52	web/server/apache-22/module/apache-php5
%define pnm_requires_SUNWapch22m_php52		web/server/apache-22/module/apache-php5
%define pnm_buildrequires_apch22m_php52		web/server/apache-22/module/apache-php5
%define pnm_requires_apch22m_php52		web/server/apache-22/module/apache-php5

#>=133
%endif
#os2nnn
%endif
#END >=133 AND os2nnn    note: two closing endif

#separate packages for the various openssl pieces (libs, incclude, commands, ...)
#note: for running the build on SXCE we do *not* have the big bang package
#      rename project, so we have to define the target package names on SXCE
#below: our target system is an older build SolarisExpress (up to including 130)
%if %{SXCE}
#spec file orginates from a system/autor using the old package names with SUNW prefix
%define pnm_buildrequires_SUNWopenssl			SUNWopenssl-include
%define pnm_requires_SUNWopenssl			SUNWopenssl-libraries

%define pnm_buildrequires_openssl			SUNWopenssl-include
%define pnm_requires_openssl				SUNWopenssl-libraries

%define pnm_buildrequires_library_security_openssl	SUNWopenssl-include
%define pnm_requires_library_security_openssl		SUNWopenssl-libraries

#note: if you search for SUNWopenssl-include, use SUNWopenssl_include !!
%define pnm_buildrequires_SUNWopenssl_include		SUNWopenssl-include
%define pnm_requires_SUNWopenssl_include		SUNWopenssl-include
%define pnm_buildrequires_SUNWopenssl_libraries		SUNWopenssl-libraries
%define pnm_requires_SUNWopenssl_libraries		SUNWopenssl-libraries

##TODO##
#/var/sadm/pkg/SUNWruby18r
#/var/sadm/pkg/SUNWruby18u
%define pnm_buildrequires_SUNWruby18r			SUNWruby18r
%define pnm_buildrequires_SUNWruby18u			SUNWruby18u
%define pnm_buildrequires_SUNWruby18			SUNWruby18u

#SUNWwgetu/SUNWwgetr/SUNWwget wget web/wget
%define pnm_buildrequires_web_wget			SUNWwgetu
%define pnm_requires_web_wget				SUNWwgetu
%define pnm_buildrequires_wget				SUNWwgetu
%define pnm_requires_wget				SUNWwgetu
%define pnm_buildrequires_SUNWwget			SUNWwgetu
%define pnm_requires_SUNWwget				SUNWwgetu
%define pnm_buildrequires_SUNWwgetu			SUNWwgetu
%define pnm_requires_SUNWwgetu				SUNWwgetu
%define pnm_buildrequires_SUNWwgetr			SUNWwgetr
%define pnm_requires_SUNWwgetr				SUNWwgetr

#SUNWGtku/SUNWGtkr/SUNWGtk Gtk library/desktop/gtk1
%define pnm_buildrequires_library_desktop_gtk1		SUNWGtku
%define pnm_requires_library_desktop_gtk1		SUNWGtku
%define pnm_buildrequires_SUNWGtk_devel			SUNWGtku
%define pnm_buildrequires_SUNWGtk			SUNWGtku
%define pnm_requires_SUNWGtk				SUNWGtku
%define pnm_buildrequires_Gtk				SUNWGtku
%define pnm_requires_Gtk				SUNWGtku

%define pnm_requires_SUNWGtku				SUNWGtku
%define pnm_requires_SUNWGtkr				SUNWGtkr


#SUNWghostscriptu/SUNWghostscriptr/SUNWghostscript -> use always SUNWghostscriptu on SXCE
#ghostscript and print/filter/ghostscript
%define pnm_buildrequires_print_filter_ghostscript	SUNWghostscriptu
%define pnm_requires_print_filter_ghostscript		SUNWghostscriptu
%define pnm_buildrequires_ghostscript			SUNWghostscriptu
%define pnm_requires_ghostscript			SUNWghostscriptu
#never existed SUNWghostscript_devel
%define pnm_buildrequires_SUNWghostscript		SUNWghostscriptu
%define pnm_requires_SUNWghostscript			SUNWghostscriptu
%define pnm_buildrequires_SUNWghostscriptr		SUNWghostscriptr
%define pnm_requires_SUNWghostscriptr			SUNWghostscriptr
%define pnm_buildrequires_SUNWghostscriptu		SUNWghostscriptu
%define pnm_requires_SUNWghostscriptu			SUNWghostscriptu


%define pnm_buildrequires_text_texinfo			SUNWtexi
%define pnm_requires_text_texinfo			SUNWtexi
%define pnm_buildrequires_SUNWtexi			SUNWtexi
%define pnm_buildrequires_SUNWtexi			SUNWtexi
%define pnm_requires_SUNWtexi				SUNWtexi

%define pnm_buildrequires_text_doctools			SUNWdoc
%define pnm_requires_text_doctools			SUNWdoc
%define pnm_buildrequires_SUNWdoc_devel			SUNWdoc
%define pnm_buildrequires_SUNWdoc			SUNWdoc
%define pnm_requires_SUNWdoc				SUNWdoc


#Apache on a SXCE or S10  host

##ignored, too old SUNWapchd
##ignored, too old SUNWapchr
##ignored, too old SUNWapchu
#config files of modules are prerequisite to the modules, so only list modules here

%define pnm_buildrequires_SUNWapch22r 		SUNWapch22r
%define pnm_requires_SUNWapch22r		SUNWapch22r

%define pnm_buildrequires_SUNWapch22u		SUNWapch22u
%define pnm_requires_SUNWapch22u		SUNWapch22u

%define pnm_buildrequires_SUNWapch22		SUNWapch22u
%define pnm_requires_SUNWapch22			SUNWapch22u

%define pnm_buildrequires_apch22		SUNWapch22u
%define pnm_requires_apch22			SUNWapch22u

#doc
%define pnm_buildrequires_SUNWapch22d		SUNWapch22d
%define pnm_requires_SUNWapch22d		SUNWapch22d
%define pnm_buildrequires_apch22d		SUNWapch22d
%define pnm_requires_apch22d			SUNWapch22d

%define pnm_buildrequires_SUNWapch22m_dtrace	SUNWapch22m-dtrace
%define pnm_requires_SUNWapch22m_dtrace		SUNWapch22m-dtrace
%define pnm_buildrequires_apch22m_dtrace	SUNWapch22m-dtrace
%define pnm_requires_apch22m_dtrace		SUNWapch22m-dtrace

%define pnm_buildrequires_SUNWapch22m_fcgid	SUNWapch22m-fcgid
%define pnm_requires_SUNWapch22m_fcgid		SUNWapch22m-fcgid
%define pnm_buildrequires_apch22m_fcgid		SUNWapch22m-fcgid
%define pnm_requires_apch22m_fcgid		SUNWapch22m-fcgid

%define pnm_buildrequires_SUNWapch22m_proxy_html	SUNWapch22m-proxy-html
%define pnm_requires_SUNWapch22m_proxy_html	SUNWapch22m-proxy-html
%define pnm_buildrequires_apch22m_proxy_html	SUNWapch22m-proxy-html
%define pnm_requires_apch22m_proxy_html		SUNWapch22m-proxy-html

%define pnm_buildrequires_SUNWapch22m_php52	SUNWapch22m-php52
%define pnm_requires_SUNWapch22m_php52		SUNWapch22m-php52
%define pnm_buildrequires_apch22m_php52		SUNWapch22m-php52
%define pnm_requires_apch22m_php52		SUNWapch22m-php52

%define pnm_buildrequires_SUNWapch22m_security	SUNWapch22m-security
%define pnm_requires_SUNWapch22m_security	SUNWapch22m-security
%define pnm_buildrequires_apch22m_security	SUNWapch22m-security
%define pnm_requires_apch22m_security		SUNWapch22m-security

%define pnm_buildrequires_SUNWapch22m_sed	SUNWapch22m-sed
%define pnm_requires_SUNWapch22m_sed		SUNWapch22m-sed
%define pnm_buildrequires_apch22m_sed		SUNWapch22m-sed
%define pnm_requires_apch22m_sed		SUNWapch22m-sed

%define pnm_buildrequires_SUNWapch22m_jk	SUNWapch22m-jk
%define pnm_requires_SUNWapch22m_jk		SUNWapch22m-jk
%define pnm_buildrequires_apch22m_jk		SUNWapch22m-jk
%define pnm_requires_apch22m_jk			SUNWapch22m-jk

%define pnm_buildrequires_SUNWapch22m_xml2enc	SUNWapch22m-xml2enc
%define pnm_requires_SUNWapch22m_xml2enc	SUNWapch22m-xml2enc
%define pnm_buildrequires_apch22m_xml2enc	SUNWapch22m-xml2enc
%define pnm_requires_apch22m_xml2enc		SUNWapch22m-xml2enc

# php
#SUNWphp52d/          SUNWphp52r-mysql/    SUNWphp52r-xdebug/   SUNWphp52u-mysql/    SUNWphp52u-xdebug/
#SUNWphp52r/          SUNWphp52r-pear/     SUNWphp52u/          SUNWphp52u-pear/     
#SUNWphp52r-apc/      SUNWphp52r-pgsql/    SUNWphp52u-apc/      SUNWphp52u-pgsql/    
#SUNWphp52r-idn/      SUNWphp52r-suhosin/  SUNWphp52u-idn/      SUNWphp52u-suhosin/  
#SUNWphp52r-memcache/ SUNWphp52r-tcpwrap/  SUNWphp52u-memcache/ SUNWphp52u-tcpwrap/  


%define pnm_buildrequires_SUNWphp52u		SUNWphp52u
%define pnm_requires_SUNWphp52u			SUNWphp52u
%define pnm_buildrequires_SUNWphp52		SUNWphp52u
%define pnm_requires_SUNWphp52			SUNWphp52u

%define pnm_buildrequires_SUNWphp52r		SUNWphp52r
%define pnm_requires_SUNWphp52r			SUNWphp52r

%define pnm_buildrequires_SUNWphp52d		SUNWphp52d
%define pnm_requires_SUNWphp52d			SUNWphp52d


%define pnm_buildrequires_SUNWphp52r_mysql	SUNWphp52r-mysql
%define pnm_requires_SUNWphp52r_mysql		SUNWphp52r-mysql

%define pnm_buildrequires_SUNWphp52u_mysql	SUNWphp52u-mysql
%define pnm_requires_SUNWphp52u_mysql		SUNWphp52u-mysql

%define pnm_buildrequires_SUNWphp52_mysql	SUNWphp52u-mysql
%define pnm_requires_SUNWphp52_mysql		SUNWphp52u-mysql

%define pnm_buildrequires_php52_mysql		SUNWphp52u-mysql
%define pnm_requires_php52_mysql		SUNWphp52u-mysql

#-apc -idn -memcache skipped, can be added if needed
%define pnm_buildrequires_SUNWphp52_pear	SUNWphp52u-pear
%define pnm_requires_SUNWphp52_pear		SUNWphp52u-pear
%define pnm_buildrequires_php52_pear 		SUNWphp52u-pear
%define pnm_requires_php52_pear 		SUNWphp52u-pear

%define pnm_buildrequires_SUNWphp52_pgsql 	SUNWphp52u-psql
%define pnm_requires_SUNWphp52_pgsql 		SUNWphp52u-psql
%define pnm_buildrequires_SUNWphp52u_pgsql 	SUNWphp52u-psql
%define pnm_requires_SUNWphp52u_pgsql 		SUNWphp52u-psql
%define pnm_buildrequires_SUNWphp52r_pgsql 	SUNWphp52r-psql
%define pnm_requires_SUNWphp52r_pgsql 		SUNWphp52r-psql
%define pnm_buildrequires_php52_pgsql 		SUNWphp52u-psql
%define pnm_requires_php52_pgsql		SUNWphp52u-psql
#-suhosin -tcpwrap -xdebug skipped, can be added if needed

#various packages

%define pnm_buildrequires_SUNWbash              SUNWbash
%define pnm_requires_SUNWbash                   SUNWbash
%define pnm_buildrequires_SUNWpcre              SUNWpcre
%define pnm_requires_SUNWpcre                   SUNWpcre
%define pnm_buildrequires_SUNWggrp              SUNWggrp
%define pnm_requires_SUNWggrp                   SUNWggrp
%define pnm_buildrequires_SUNWlibsasl           SUNWlibsasl
%define pnm_requires_SUNWlibsasl                SUNWlibsasl

#kerberos
%define pnm_buildrequires_service_security_kerberos_5  SUNWkrbu
%define pnm_requires_service_security_kerberos_5       SUNWkrbu

%define pnm_buildrequires_SUNWkrb 		SUNWkrbu
%define pnm_buildrequires_SUNWkrbr		SUNWkrbr
%define pnm_buildrequires_SUNWkrbu		SUNWkrbu
%define pnm_requires_SUNWkrb                    SUNWkrbu
%define pnm_requires_SUNWkrbr 			SUNWkrbr
%define pnm_requires_SUNWkrbu 			SUNWkrbu

#samba
%define pnm_buildrequires_service_network_samba	SUNWsmbau
%define pnm_requires_service_network_samba	SUNWsmbau
%define pnm_buildrequires_SUNWsmba_devel 	SUNWsmbau
%define pnm_buildrequires_SUNWsmba		SUNWsmbau
%define pnm_buildrequires_SUNWsmbar		SUNWsmbar
%define pnm_buildrequires_SUNWsmbau		SUNWsmbau
%define pnm_requires_SUNWsmba			SUNWsmbau
%define pnm_requires_SUNWsmbar			SUNWsmbar
%define pnm_requires_SUNWsmbau			SUNWsmbau
%define pnm_buildrequires_smba			SUNWsmbau
%define pnm_requires_smba			SUNWsmbau

#SUNWlibtdl
%define pnm_buildrequires_SUNWltdl_devel	SUNWltdl
%define pnm_buildrequires_SUNWltdl		SUNWltdl
%define pnm_buildrequires_library_libtool_libltdl	SUNWltdl
%define pnm_requires_library_libtool_libltdl		SUNWltdl

#SUNWbtool
%define pnm_buildrequires_SUNWbtool_devel developer/object_file		SUNWbtool
%define pnm_buildrequires_SUNWbtool developer/object_file		SUNWbtool
%define pnm_buildrequires_developer_object_file		SUNWbtool
%define pnm_requires_developer_object_file		SUNWbtool

#various
%define pnm_buildrequires_SUNWflac_devel	SUNWflac-devel
%define pnm_requires_SUNWflac			SUNWflac
%define pnm_buildrequires_SUNWspeex_devel	SUNWspeex-devel
%define pnm_requires_SUNWspeex			SUNWspeex
%define pnm_buildrequires_SUNWpangomm_devel	SUNWpangomm-devel
%define pnm_requires_SUNWpangomm		SUNWpangomm
%define pnm_buildrequires_SUNWpango_devel	SUNWpango-devel
%define pnm_requires_SUNWpango			SUNWpango
%define pnm_buildrequires_SUNWglib2_devel	SUNWglib2-devel
%define pnm_requires_SUNWglib2			SUNWglib2
%define pnm_buildrequires_SUNWgtk2_devel	SUNWgtk2-devel
#exceptionally, because it is already in *133*inc
%define pnm_buildrequires_SUNWgtk2		SUNWgtk2
%define pnm_requires_SUNWgtk2			SUNWgtk2


# C++ Studio runtime is on IPS not detectable with "pkg info SUNWlibC"
# note: there is in real no SUNWlibC -devel package!
%define pnm_buildrequires_SUNWlibC_devel	SUNWlibC
%define pnm_buildrequires_SUNWlibC		SUNWlibC
%define pnm_requires_SUNWlibC			SUNWlibC
%define pnm_buildrequires_system_library_c___runtime	SUNWlibC
%define pnm_buildrequires_system_library_c___runtime	SUNWlibC
%define pnm_requires_system_library_c___runtime		SUNWlibC

# SUNWsqlite3 is on IPS not detectable with "pkg info SUNWsqlite3"
# note: there is in real no SUNWsqlite3 -devel package!
%define pnm_buildrequires_SUNWsqlite3_devel	SUNWsqlite3
%define pnm_buildrequires_SUNWsqlite3		SUNWsqlite3
%define pnm_requires_SUNWsqlite3		SUNWsqlite3
%define pnm_buildrequires_sqlite3		SUNWsqlite3
%define pnm_requires_sqlite3			SUNWsqlite3
%define pnm_buildrequires_database_sqlite3	SUNWsqlite3
%define pnm_requires_database_sqlite3		SUNWsqlite3


# SUNWlibsdl
%define pnm_buildrequires_SUNWlibsdl_devel	SUNWlibsdl-devel
%define pnm_buildrequires_SUNWlibsdl		SUNWlibsdl
%define pnm_requires_SUNWlibsdl 		SUNWlibsdl-devel
%define pnm_buildrequires_libsdl		SUNWlibsdl-devel
%define pnm_requires_libsdl			SUNWlibsdl
%define pnm_buildrequires_library_libsdl	SUNWlibsdl-devel
%define pnm_requires_library_libsdl		SUNWlibsdl

#SUNWxwplt SUNWxwplt
%define pnm_buildrequires_x11_clients		SUNWxwplt
%define pnm_requires_x11_clients		SUNWxwplt
%define pnm_buildrequires_SUNWxwplt_devel	SUNWxwplt
%define pnm_buildrequires_SUNWxwplt		SUNWxwplt
%define pnm_requires_SUNWxwplt			SUNWxwplt
%define pnm_buildrequires_xwplt			SUNWxwplt
%define pnm_requires_xwplt			SUNWxwplt
%define pnm_buildrequires_compatibility_packages_SUNWxwplt	SUNWxwplt
%define pnm_requires_compatibility_packages_SUNWxwplt		SUNWxwplt

#SUNWxwopt
%define pnm_buildrequires_SUNWxwopt_devel		SUNWxwopt
%define pnm_buildrequires_SUNWxwopt			SUNWxwopt
%define pnm_requires_SUNWxwopt				SUNWxwopt
%define pnm_buildrequires_x11_optional_clients		SUNWxwopt
%define pnm_requires_x11_optional_clients		SUNWxwopt

#SUNWntp SUNWntpu SUNWntpr ntp ...
%define pnm_buildrequires_service_network_ntp		SUNWntpu
%define pnm_requires_service_network_ntp		SUNWntpu
%define pnm_buildrequires_SUNWntp_devel			SUNWntpu
%define pnm_buildrequires_SUNWntp			SUNWntpu
%define pnm_requires_SUNWntp				SUNWntpu
%define pnm_buildrequires_ntp				SUNWntpu
%define pnm_requires_ntp				SUNWntpu

#sendmail SUNWsndm SUNWsndmu ...
%define pnm_buildrequires_SUNWsndm_devel		SUNWsndmu
%define pnm_buildrequires_SUNWsndm			SUNWsndmu
%define pnm_requires_SUNWsndm				SUNWsndmu
%define pnm_buildrequires_sndm				SUNWsndmu
%define pnm_requires_sndm				SUNWsndmu


#gnu SUNWgnu-gettex
#older OS (e.g. Solaris 10) would use un-archived archive/SUNWgnu-gettext.spec
%define pnm_buildrequires_SUNWgnu_gettext_devel		SUNWgnu-gettext
%define pnm_buildrequires_SUNWgnu_gettext		SUNWgnu-gettext
%define pnm_requires_SUNWgnu_gettext			SUNWgnu-gettext
%define pnm_buildrequires_developer_gnome_gettext	SUNWgnu-gettext
%define pnm_requires_developer_gnome_gettext		SUNWgnu-gettext
%define pnm_buildrequires_text_gnu_gettext		SUNWgnu-gettext
%define pnm_requires_text_gnu_gettext			SUNWgnu-gettext
%define pnm_buildrequires_gnu_gettext			SUNWgnu-gettext
%define pnm_requires_gnu_gettext			SUNWgnu-gettext

#libdiscid
#note for S10: add SFElibdiscid if necessary
%define pnm_buildrequires_library_musicbrainz_libdiscid SUNWlibdiscid-devel
%define pnm_requires_library_musicbrainz_libdiscid	SUNWlibdiscid
%define pnm_buildrequires_SUNWlibdiscid_devel		SUNWlibdiscid-devel
%define pnm_buildrequires_SUNWlibdiscid			SUNWlibdiscid-devel
%define pnm_requires_SUNWlibdiscid			SUNWlibdiscid
%define pnm_buildrequires_libdiscid			SUNWlibdiscid-devel
%define pnm_requires_libdiscid				SUNWlibdiscid

#libmusicbrainz
%define pnm_buildrequires_library_musicbrainz_libmusicbrainz	SUNWmusicbrainz-devel
%define pnm_requires_library_musicbrainz_libmusicbrainz		SUNWmusicbrainz
%define pnm_buildrequires_SUNWmusicbrainz_devel		SUNWmusicbrainz-devel
%define pnm_buildrequires_SUNWmusicbrainz		SUNWmusicbrainz-devel
%define pnm_requires_SUNWmusicbrainz			SUNWmusicbrainz
%define pnm_buildrequires_musicbrainz			SUNWmusicbrainz-devel
%define pnm_requires_musicbrainz			SUNWmusicbrainz

#zlib
%define pnm_buildrequires_SUNWzlib_devel		SUNWzlib
%define pnm_buildrequires_SUNWzlib			SUNWzlib
%define pnm_requires_SUNWzlib				SUNWzlib

#SUNWltdl
%define pnm_buildrequires_library_libtool_libltdl	SUNWltdl
%define pnm_requires_library_libtool_libltdl		SUNWltdl
%define pnm_buildrequires_SUNWltdl_devel		SUNWltdl
%define pnm_buildrequires_SUNWltdl			SUNWltdl
%define pnm_requires_SUNWltdl				SUNWltdl
%define pnm_buildrequires_ltdl				SUNWltdl
%define pnm_requires_ltdl				SUNWltdl

#SUNWautomake-111 SFEautomake-111
#starting with S11 175.1 we have developer/build/automake-111
%define pnm_buildrequires_developer_build_automake_111	SFEautomake-111
%define pnm_buildrequires_developer_build_automake_111	SFEautomake-111
%define pnm_buildrequires_SUNWautomake_111		SFEautomake-111
%define pnm_requires_SUNWautomake_111			SFEautomake-111
%define pnm_buildrequires_SFEautomake_111		SFEautomake-111
%define pnm_requires_SFEautomake_111			SFEautomake-111

#SUNWlibstdcxx4
%define pnm_buildrequires_SUNWlibstdcxx4_devel		SUNWlibstdcxx4
%define pnm_buildrequires_SUNWlibstdcxx4		SUNWlibstdcxx4
%define pnm_requires_SUNWlibstdcxx4			SUNWlibstdcxx4
%define pnm_buildrequires_libstdcxx4			SUNWlibstdcxx4
%define pnm_requires_libstdcxx4				SUNWlibstdcxx4

#SUNWncurses
%define pnm_buildrequires_library_ncurses 			SUNWncurses-devel
%define pnm_requires_library_ncurses			 	SUNWncurses
%define pnm_buildrequires_SUNWncurses_devel 			SUNWncurses-devel
%define pnm_buildrequires_SUNWncurses 				SUNWncurses-devel
%define pnm_requires_SUNWncurses 				SUNWncurses
%define pnm_buildrequires_ncurses 				SUNWncurses-devel
%define pnm_requires_ncurses 					SUNWncurses
#pre build 100 we're missing ncurses and use SFEncurses instead
#past build 100, use the settings below
%define pnm_buildrequires_SFEncurses_devel 			SUNWncurses-devel
%define pnm_buildrequires_SFEncurses 				SUNWncurses-devel
%define pnm_requires_SFEncurses 				SUNWncurses


#SFElibsndfile/SUNWlibsndfile
#for now, we always default to the SFE version 1.0.25 located in /usr/gnu
#for every platform
#SFElibsndfile/SFElibsndfile-devel or SUNWlibsndfile (no -devel)
#SFE in /usr/gnu
%define pnm_buildrequires_library_gnu_libsndfile		SFElibsndfile-devel
%define pnm_requires_library_gnu_libsndfile			SFElibsndfile
#Solaris/OI
%define pnm_buildrequires_library_libsndfile			SFElibsndfile-devel
%define pnm_requires_library_libsndfile				SFElibsndfile
#old OpenSolaris pre renaming
%define pnm_buildrequires_libsndfile				SFElibsndfile-devel
%define pnm_requires_libsndfile					SFElibsndfile
#S10 SXCE
#Devel-Package SUNWlibsndfile_devel doesn't really exist, but define it anyways:
%define pnm_buildrequires_SFElibsndfile_devel			SFElibsndfile-devel
%define pnm_buildrequires_SFElibsndfile				SFElibsndfile-devel
%define pnm_requires_SFElibsndfile				SFElibsndfile
%define pnm_buildrequires_SUNWlibsndfile_devel			SFElibsndfile-devel
%define pnm_buildrequires_SUNWlibsndfile			SFElibsndfile-devel
%define pnm_requires_SUNWlibsndfile				SFElibsndfile

%define pnm_buildrequires_SUNWaudh_devel 			SUNWaudh-devel
%define pnm_buildrequires_SUNWaudh 				SUNWaudh-devel
%define pnm_requires_SUNWaudh 					SUNWaudh
%define pnm_buildrequires_audh 					SUNWaudh-devel
%define pnm_requires_audh 					SUNWaudh
%define pnm_buildrequires_system_header_header_audio		SUNWaudh-devel
%define pnm_requires_system_header_header_audio 		SUNWaudh

#SUNWgnu-readline@5.2,5.11-0.132:20100130T084250Z
#library/readline@5.2,5.11-0.134:20100302T041122Z
%define pnm_buildrequires_library_readline			SFEreadline-devel
%define pnm_requires_library_readline				SFEreadline
%define pnm_buildrequires_SUNWgnu_readline_devel		SFEreadline-devel
%define pnm_buildrequires_SUNWgnu_readline			SFEreadline-devel
%define pnm_requires_SUNWgnu_readline				SFEreadline
%define pnm_buildrequires_gnu_readline				SFEreadline-devel
%define pnm_requires_gnu_readline				SFEreadline
#which SXCE build brought us SUNWgnu_readline ?
#just a guess, enter the correct osbuild
%if %( expr %{osbuild} '>=' 130 )
%define pnm_buildrequires_library_readline			SUNWgnu-readline
%define pnm_requires_library_readline				SUNWgnu-readline
%define pnm_buildrequires_SUNWgnu_readline_devel		SUNWgnu-readline
%define pnm_buildrequires_SUNWgnu_readline			SUNWgnu-readline
%define pnm_requires_SUNWgnu_readline				SUNWgnu-readline
%define pnm_buildrequires_gnu_readline				SUNWgnu-readline
%define pnm_requires_gnu_readline				SUNWgnu-readline
%endif

%define pnm_buildrequires_SUNWlibm_devel			SUNWlibm
%define pnm_buildrequires_SUNWlibm				SUNWlibm
%define pnm_requires_SUNWlibm					SUNWlibm

%define pnm_buildrequires_SUNWgnome_games_devel			SUNWgnome-games-devel
%define pnm_buildrequires_SUNWgnome_games			SUNWgnome-games-devel
%define pnm_requires_SUNWgnome_games				SUNWgnome-games

%define pnm_buildrequires_SUNWmlib_devel			SUNWmlib-devel,SUNWmlibe
%define pnm_buildrequires_SUNWmlib				SUNWmlib,SUNWmlibe
%define pnm_requires_SUNWmlib					SUNWmlib,SUNWmlibe

%define pnm_buildrequires_SUNWlua				SUNWlua
%define pnm_buildrequires_SUNWgsed				SUNWgsed

%define pnm_buildrequires_SUNWgnu_idn library/libidn		SUNWgnu-idn
%define pnm_requires_SUNWgnu_idn library/libidn			SUNWgnu-idn
%define pnm_buildrequires_SUNWgnu_idn				SUNWgnu-idn
%define pnm_requires_SUNWgnu_idn				SUNWgnu-idn

#Nvidia driver names
#for the moment, just make a file require, as this matches driver/graphics/nvidia and NVDAgraphics
#/usr/X11/include/NVIDIA/vdpau/vdpau.h
#users might have installed the SVR4 package directly from nvidia
#%define pnm_buildrequires_driver_graphics_nvidia		NVDAgraphics
#%define pnm_requires_driver_graphics_nvidia			NVDAgraphics
%define pnm_buildrequires_driver_graphics_nvidia		/usr/X11/include/NVIDIA/vdpau/vdpau.h
%define pnm_requires_driver_graphics_nvidia			/usr/X11/include/NVIDIA/vdpau/vdpau.h

##TODO## Add your packages here in case you specify an old
# package name now with the pnm_buildrequires_SUNWoldname makro

%endif
#END SXCE

#note: for simple cases don't open another separate include file
#packagenames.define-133.inc or packagenames.define-specialcases-133.inc
#just do it here instead.
#package names in sync with SXCE and os2nnn but got incorporated into other
#packages, examples. SUNWhea SUNWsfwhea

#pre/including nnn: SUNWhea    -> past nnn replacement is
#NOTE: superseeding the previous definitions SUNWsfwhea
#cases >=133
%if %( expr %{osbuild} '>=' 133 '|' %{solaris12} '>=' 1 )
%define pnm_buildrequires_SUNWhea	    system/header
%define pnm_requires_SUNWhea		    system/header
%define pnm_buildrequires_system_header	    system/header
%define pnm_requires_system_header	    system/header
%endif
#END >=133

#NOTE: this section might be superseeded by lower build numbers 
#cases <133
%if %( expr %{osbuild} '<' 133 '&' %{solaris12} '=' 0 )
%define pnm_buildrequires_SUNWhea		SUNWhea
%define pnm_requires_SUNWhea	 		SUNWhea
#this might be overwritten again by builds below 130
%define pnm_buildrequires_system_header		SUNWhea
%define pnm_requires_system_header		SUNWhea
%endif
#END <133

#pre/including 130: SUNWsfwhea -> past 130 replacement is system/header
##TODO## please verify build numbers and intended replacement packagename
%if %( expr %{osbuild} '>=' 130 '|' %{solaris12} '>=' 1 )
%define pnm_buildrequires_SUNWsfwhea	    SUNWhea
%define pnm_requires_SUNWsfwhea		    SUNWhea
%define pnm_buildrequires_system_header	    SUNWhea
%define pnm_requires_system_header	    SUNWhea
%endif
#END >=130

#NOTE: including SUNWhea too
#cases <130
%if %( expr %{osbuild} '<' 130 '&' %{solaris12} '=' 0 )
%define pnm_buildrequires_SUNWhea		SUNWsfwhea
%define pnm_requires_SUNWhea	 		SUNWsfwhea
%define pnm_buildrequires_SUNWsfwhea		SUNWsfwhea
%define pnm_requires_SUNWsfwhea	 		SUNWsfwhea
%define pnm_buildrequires_system_header		SUNWsfwhea
%define pnm_requires_system_header		SUNWsfwhea
%endif
#END <130

# SUNWgnome-xml-share, SUNWgnome-xml-root -> SUNWgnome-xml -> data/docbook


# SFEgnupg2 SUNWgnupg SUNWlibgpg-error SUNWlibgpg-error-devel SUNWlibgcrypt SUNWlibgcrypt-devel

#pre/including 130: SFEgnupg2 -> past 130 replacement is SUNWgnupg
#note: oihipster see sections below, needs to set IPS name (knows no legacy name any more)
%if %( expr %{osbuild} '>=' 130 '|' %{solaris12} '>=' 1 )
#pkg://solaris/crypto/gnupg@2.0.30-5.12.0.0.0.113.1:20161127T235134Z          ---
#sunw
%define pnm_buildrequires_SUNWgnupg_devel	crypto/gnupg
%define pnm_buildrequires_SUNWgnupg		crypto/gnupg
%define pnm_requires_SUNWgnupg			crypto/gnupg
%define pnm_buildrequires_crypto_gnupg	    	crypto/gnupg
%define pnm_requires_crypto_gnupg		crypto/gnupg
#sfe
%define pnm_buildrequires_SFEgnupg2_devel	crypto/gnupg
%define pnm_buildrequires_SFEgnupg2		crypto/gnupg
%define pnm_requires_SFEgnupg2			crypto/gnupg
%define pnm_buildrequires_sfe_crypto_gnupg	crypto/gnupg
%define pnm_requires_sfe_crypto_gnupg		crypto/gnupg

#pkg://solaris/system/library/security/libgcrypt@1.7.3-5.12.0.0.0.113.1:20161128T023501Z ---
#sunw
%define pnm_buildrequires_SUNWlibgcrypt_devel		system/library/security/libgcrypt
%define pnm_buildrequires_SUNWlibgcrypt			system/library/security/libgcrypt
%define pnm_requires_SUNWlibgcrypt			system/library/security/libgcrypt
%define pnm_buildrequires_system_library_security_libgcrypt		system/library/security/libgcrypt
%define pnm_requires_system_library_security_libgcrypt			system/library/security/libgcrypt

#sfe
#note: SUNWlibgcrypt(-devel) is in Solaris since a while (which osbuild number?)
#not set %define pnm_buildrequires_SUNWlibgcrypt_devel	SUNWlibgcrypt-devel
#not set %define pnm_buildrequires_SUNWlibgcrypt		SUNWlibgcrypt-devel
#not set %define pnm_requires_SUNWlibgcrypt		SUNWlibgcrypt
#not set %define pnm_buildrequires_system_library_security_libgcrypt	SUNWlibgcrypt-devel
#not set %define pnm_requires_system_library_security_libgcrypt		SUNWlibgcrypt

#pkg://solaris/library/security/libgpg-error@1.24-5.12.0.0.0.113.1:20161128T021722Z ---
#sunw
%define pnm_buildrequires_SUNWlibgpg_error_devel	library/security/libgpg-error
%define pnm_buildrequires_SUNWlibgpg_error		library/security/libgpg-error
%define pnm_requires_SUNWlibgpg_error			library/security/libgpg-error
%define pnm_buildrequires_library_security_libgpg_error	library/security/libgpg-error
%define pnm_requires_library_security_libgpg_error	library/security/libgpg-error
#sfe
%define pnm_buildrequires_SFElibgpg_error_devel			library/security/libgpg-error
%define pnm_buildrequires_SFElibgpg_error			library/security/libgpg-error
%define pnm_requires_SFElibgpg_error				library/security/libgpg-error
%define pnm_buildrequires_sfe_library_security_libgpg_error	library/security/libgpg-error
%define pnm_requires_sfe_library_security_libgpg_error		library/security/libgpg-error
%endif
#END >=130

#cases <130
%if %( expr %{osbuild} '<' 130 '&' %{solaris12} '=' 0 )
#sunw
%define pnm_buildrequires_SUNWgnupg_devel	SFEgnupg2
%define pnm_buildrequires_SUNWgnupg		SFEgnupg2
%define pnm_requires_SUNWgnupg			SFEgnupg2
%define pnm_buildrequires_crypto_gnupg	    	SFEgnupg2
%define pnm_requires_crypto_gnupg		SFEgnupg2
#sfe
%define pnm_buildrequires_SFEgnupg2_devel	SFEgnupg2
%define pnm_buildrequires_SFEgnupg2		SFEgnupg2
%define pnm_requires_SFEgnupg2			SFEgnupg2
%define pnm_buildrequires_sfe_crypto_gnupg	SFEgnupg2
%define pnm_requires_sfe_crypto_gnupg		SFEgnupg2
#sunw
#note: SUNWlibgcrypt(-devel) is in Solaris since a while (which osbuild number?)
#not set %define pnm_buildrequires_SUNWlibgcrypt_devel	SFElibgcrypt-devel
#not set %define pnm_buildrequires_SUNWlibgcrypt		SFElibgcrypt-devel
#not set %define pnm_requires_SUNWlibgcrypt		SFElibgcrypt
#not set %define pnm_buildrequires_system_library_security_libgcrypt	SFElibgcrypt-devel
#not set %define pnm_requires_system_library_security_libgcrypt		SFElibgcrypt
#sfe
#note: SUNWlibgcrypt(-devel) is in Solaris since a while (which osbuild number?)
#not set %define pnm_buildrequires_SUNWlibgcrypt_devel	SFElibgcrypt-devel
#not set %define pnm_buildrequires_SUNWlibgcrypt		SFElibgcrypt-devel
#not set %define pnm_requires_SUNWlibgcrypt		SFElibgcrypt
#not set %define pnm_buildrequires_system_library_security_libgcrypt	SFElibgcrypt-devel
#not set %define pnm_requires_system_library_security_libgcrypt		SFElibgcrypt
#sunw
%define pnm_buildrequires_SUNWlibgpg_error_devel	SFElibgpg-error-devel
%define pnm_buildrequires_SUNWlibgpg_error		SFElibgpg-error-devel
%define pnm_requires_SUNWlibgpg_error			SUNWlibgpg-error
%define pnm_buildrequires_library_security_libgpg_error	SFElibgpg-error-devel
%define pnm_requires_library_security_libgpg_error	SFElibgpg-error
#sfe
%define pnm_buildrequires_SFElibgpg_error_devel	SFElibgpg-error-devel
%define pnm_buildrequires_SFElibgpg_error		SFElibgpg-error-devel
%define pnm_requires_SFElibgpg_error			SFElibgpg-error
%define pnm_buildrequires_sfe_library_security_libgpg_error	SFElibgpg-error-devel
%define pnm_requires_sfe_library_security_libgpg_error	SFElibgpg-error
%endif
#END <130

%if %{oihipster}
#sunw
%define pnm_buildrequires_SUNWgnupg_devel	crypto/gnupg
%define pnm_buildrequires_SUNWgnupg		crypto/gnupg
%define pnm_requires_SUNWgnupg			crypto/gnupg
%define pnm_buildrequires_crypto_gnupg	    	crypto/gnupg
%define pnm_requires_crypto_gnupg		crypto/gnupg
#sfe
%define pnm_buildrequires_SFEgnupg2_devel	crypto/gnupg
%define pnm_buildrequires_SFEgnupg2		crypto/gnupg
%define pnm_requires_SFEgnupg2			crypto/gnupg
%define pnm_buildrequires_sfe_crypto_gnupg	crypto/gnupg
%define pnm_requires_sfe_crypto_gnupg		crypto/gnupg
#sunw
%define pnm_buildrequires_SUNWlibgcrypt_devel	system/library/security/libgcrypt
%define pnm_buildrequires_SUNWlibgcrypt		system/library/security/libgcrypt
%define pnm_requires_SUNWlibgcrypt		system/library/security/libgcrypt
%define pnm_buildrequires_system_library_security_libgcrypt	system/library/security/libgcrypt
%define pnm_requires_system_library_security_libgcrypt		system/library/security/libgcrypt
#sfe
#note: SUNWlibgcrypt(-devel) is in Solaris since a while (which osbuild number?)
#not set %define pnm_buildrequires_SUNWlibgcrypt_devel	SUNWlibgcrypt-devel
#not set %define pnm_buildrequires_SUNWlibgcrypt		SUNWlibgcrypt-devel
#not set %define pnm_requires_SUNWlibgcrypt		SUNWlibgcrypt
#not set %define pnm_buildrequires_system_library_security_libgcrypt	SUNWlibgcrypt-devel
#not set %define pnm_requires_system_library_security_libgcrypt		SUNWlibgcrypt
#sunw
%define pnm_buildrequires_SUNWlibgpg_error_devel	library/security/libgpg-error
%define pnm_buildrequires_SUNWlibgpg_error		library/security/libgpg-error
%define pnm_requires_SUNWlibgpg_error			library/security/libgpg-error
%define pnm_buildrequires_library_security_libgpg_error	library/security/libgpg-error
%define pnm_requires_library_security_libgpg_error	library/security/libgpg-error
#sfe
%define pnm_buildrequires_SFElibgpg_error_devel		library/security/libgpg-error
%define pnm_buildrequires_SFElibgpg_error		library/security/libgpg-error
%define pnm_requires_SFElibgpg_error			library/security/libgpg-error
%define pnm_buildrequires_sfe_library_security_libgpg_error	library/security/libgpg-error
%define pnm_requires_sfe_library_security_libgpg_error	library/security/libgpg-error

%define pnm_buildrequires_developer_documentation_tool_xmlto	text/xmlto
%define pnm_requires_developer_documentation_tool_xmlto		text/xmlto
%define pnm_buildrequires_SFExmlto				text/xmlto
%define pnm_requires_SFExmlto					text/xmlto

%endif
#END oihipster


#SUNWfftw3 was added with build 107
#http://wikis.sun.com/display/OSOLInstall/Build+107
#pkgs know about the renaming, so just handle a switch to SFEfftw3 in case
#the osbuild is too old

#defaults for all builds >= 107 - let pkg do the names translation if needed
#cases >=107
%define pnm_buildrequires_SFEfftw3		SUNWfftw3
%define pnm_requires_SFEfftw3			SUNWfftw3
%define pnm_buildrequires_SUNWfftw3		SUNWfftw3
%define pnm_requires_SUNWfftw3	 		SUNWfftw3
%define pnm_buildrequires_library_fftw_3	SUNWfftw3
%define pnm_requires_library_fftw_3	 	SUNWfftw3
#>=107

%if %( expr %{osbuild} '<' 107 '&' %{solaris12} '=' 0 )
#running an old build or Solaris 10
%define pnm_buildrequires_SFEfftw3		SFEfftw3
%define pnm_requires_SFEfftw3	 		SFEfftw3
%define pnm_buildrequires_SUNWfftw3		SFEfftw3
%define pnm_requires_SUNWfftw3	 		SFEfftw3
%define pnm_buildrequires_library_fftw_3	SFEfftw3
%define pnm_requires_library_fftw_3	 	SFEfftw3
%endif
#END <107

#paused# ##TODO##define exact osbuild number where SUNWfreetype disappeared
#paused# #rules: if osdistro does not know freetype2, then use SFEfreetype (2.x)
#paused# #defaults for all builds < 133 (just to have somehting to start with)

#paused# #the default settings from the other p*inc files are valid or overwritten here
#paused# %define pnm_buildrequires_SUNWfreetype2		SUNWfreetype2
#paused# %define pnm_requires_SUNWfreetype2		SUNWfreetype2
#paused# %define pnm_buildrequires_freetype2		SUNWfreetype2
#paused# %define pnm_requires_freetype2			SUNWfreetype2
#paused# #SFEfreetype replaced with SUNWfreetype2 
#paused# #NOTE: no "2" at the end!
#paused# %define pnm_buildrequires_SUNWfreetype_devel 	SUNWfreetype2
#paused# %define pnm_requires_SUNWfreetype		SUNWfreetype2

##TODO## below: probably obsolete or needs rethinking:
##TODO## which osbuild version is right?
%if %( expr %{osbuild} '<' 133 '&' %{solaris12} '=' 0 )
#replace requested SUNWfreetype2* with SFE version on older
#osbuild version
#NOTE: might adjust exact osbuild version later
%define pnm_buildrequires_SUNWfreetype2_devel	SFEfreetype-devel
%define pnm_buildrequires_SUNWfreetype2		SFEfreetype
%define pnm_requires_SUNWfreetype2		SFEfreetype
%define pnm_buildrequires_freetype2		SFEfreetype-devel
%define pnm_requires_freetype2			SFEfreetype
%define pnm_buildrequires_system_library_freetype_2	SFEfreetype-devel
%define pnm_requires_system_library_freetype_2	SFEfreetype
#SFE requested
%define pnm_buildrequires_SFEfreetype_devel	SFEfreetype-devel
%define pnm_requires_SFEfreetype		SFEfreetype
%endif
#END < 133

#defaults for all builds >= 99 - let pkg do the names translation if needed
%define pnm_buildrequires_SFElibmikmod_devel	SUNWlibmikmod-devel
%define pnm_buildrequires_SFElibmikmod		SUNWlibmikmod-devel
%define pnm_requires_SFElibmikmod		SUNWlibmikmod
%define pnm_buildrequires_SUNWlibmikmod_devel	SUNWlibmikmod-devel
%define pnm_buildrequires_SUNWlibmikmod		SUNWlibmikmod-devel
%define pnm_requires_SUNWlibmikmod		SUNWlibmikmod

%if %( expr %{osbuild} '<' 99 '&' %{solaris12} '=' 0 )
#running an old build or Solaris 10
%define pnm_buildrequires_SFElibmikmod_devel	SFElibmikmod-devel
%define pnm_buildrequires_SFElibmikmod		SFElibmikmod-devel
%define pnm_requires_SFElibmikmod	 	SFElibmikmod
%define pnm_buildrequires_SUNWlibmikmod_devel	SFElibmikmod-devel
%define pnm_buildrequires_SUNWlibmikmod		SFElibmikmod-devel
%define pnm_requires_SUNWlibmikmod	 	SFElibmikmod
%endif
#END <99

#defaults for all builds >= 116 - let pkg do the names translation if needed
%define pnm_buildrequires_library_database_gdbm	SUNWgnu-dbm
%define pnm_requires_library_database_gdbm	SUNWgnu-dbm
%define pnm_buildrequires_SFEgdbm		SUNWgnu-dbm
%define pnm_requires_SFEgdbm			SUNWgnu-dbm
%define pnm_buildrequires_SUNWgnu_dbm		SUNWgnu-dbm
%define pnm_requires_SUNWgnu_dbm		SUNWgnu-dbm

%if %( expr %{osbuild} '<' 116 '&' %{solaris12} '=' 0 '|' %{omnios} '|' %{oihipster} )
#running an old build or Solaris 10, old OpenSolaris or OmniOS - and not on Solaris 12 or Solaris 11
#library/database/gdbm@1.8.3,5.11-0.175.3.0.0.18.0 >= use from osdistro
#library/database/gdbm@1.8.3,5.12-5.12.0.0.0.70.0  >= use from osdistro
#omnios? oihipster? oi151a8?
%define pnm_buildrequires_library_database_gdbm	SFEgdbm
%define pnm_requires_library_database_gdbm	SFEgdbm
%define pnm_buildrequires_SFEgdbm		SFEgdbm
%define pnm_requires_SFEgdbm		 	SFEgdbm
%define pnm_buildrequires_SUNWgnu_dbm		SFEgdbm
%define pnm_requires_SUNWgnu_dbm	 	SFEgdbm
%endif
#END <116



#special case, pkgtool/pkgbuild can't see if packages are installed if
#meta-package data/docbook is requested (it shows never as being installed).
#up to 133 it was developer/documentation-tool/gtk-doc
#NOTE we overwrite what the include for 134 has defined
%if %( expr %{osbuild} '>=' 134 '|' %{solaris12} '>=' 1 )
%define pnm_buildrequires_developer_documentation_tool_gtk_doc    developer/documentation-tool/gtk-doc
%define pnm_requires_developer_documentation_tool_gtk_doc         developer/documentation-tool/gtk-doc
%define pnm_buildrequires_SUNWgtk_doc_devel     developer/documentation-tool/gtk-doc
%define pnm_buildrequires_SUNWgtk_doc           developer/documentation-tool/gtk-doc
%define pnm_requires_SUNWgtk_doc                developer/documentation-tool/gtk-doc
%define pnm_buildrequires_gtk_doc               developer/documentation-tool/gtk-doc
%define pnm_requires_gtk_doc                    developer/documentation-tool/gtk-doc
%define pnm_buildrequires_SUNWgtk_doc		developer/documentation-tool/gtk-doc
%define pnm_requires_SUNWgtk_doc		developer/documentation-tool/gtk-doc
%define pnm_buildrequires_SUNWgnome_xml         developer/documentation-tool/gtk-doc
%define pnm_requires_SUNWgnome_xml              developer/documentation-tool/gtk-doc
%define pnm_buildrequires_SUNWgtk_doc           developer/documentation-tool/gtk-doc
%define pnm_requires_SUNWgtk_doc                developer/documentation-tool/gtk-doc
%define pnm_buildrequires_data_docbook          developer/documentation-tool/gtk-doc
%define pnm_requires_data_docbook               developer/documentation-tool/gtk-doc
%endif
#END >= 134

#special case, pkgtool/pkgbuild can't see if packages are installed if
#meta-package x11/client is requested. up to 143 it was TBD
#NOTE we overwrite what the include for 133 / 134 has defined (target was x11/client)
%if %( expr %{osbuild} '>=' 144 '|' %{solaris12} '>=' 1 )
%define pnm_buildrequires_x11_clients		compatibility/packages/SUNWxwplt
%define pnm_requires_x11_clients		compatibility/packages/SUNWxwplt
%define pnm_buildrequires_SUNWxwplt_devel	compatibility/packages/SUNWxwplt
%define pnm_buildrequires_SUNWxwplt		compatibility/packages/SUNWxwplt
%define pnm_requires_SUNWxwplt			compatibility/packages/SUNWxwplt
%define pnm_buildrequires_xwplt			compatibility/packages/SUNWxwplt
%define pnm_requires_xwplt			compatibility/packages/SUNWxwplt
%define pnm_buildrequires_compatibility_packages_SUNWxwplt	compatibility/packages/SUNWxwplt
%define pnm_requires_compatibility_packages_SUNWxwplt		compatibility/packages/SUNWxwplt

#SUNWxwopt is now a compatibility package wich pulles in a number of smaller packages
#pkg://compatibility/packages/SUNWxwopt@0.5.11,5.11-0.144
%define pnm_buildrequires_SUNWxwopt_devel		compatibility/packages/SUNWxwopt
%define pnm_buildrequires_SUNWxwopt			compatibility/packages/SUNWxwopt
%define pnm_requires_SUNWxwopt				compatibility/packages/SUNWxwopt
%define pnm_buildrequires_x11_optional_clients		compatibility/packages/SUNWxwopt
%define pnm_requires_x11_optional_clients		compatibility/packages/SUNWxwopt

#SUNWxwinc is now a compatibility package which can be checked for being installed (against a consolidation which can't)
#   Name: x11/header Renamed to: pkg:/consolidation/X/X-incorporation pkg:/compatibility/packages/SUNWxwinc@0.5.11,5.11-0.144
%define pnm_buildrequires_SUNWxwinc_devel 	compatibility/packages/SUNWxwinc
%define pnm_buildrequires_SUNWxwinc 		compatibility/packages/SUNWxwinc
%define pnm_requires_SUNWxwinc 			compatibility/packages/SUNWxwinc
%endif
#END >= 144



%if %{oihipster}
#oihipster lost SUNWxwinc, try a replacement.
#  usr/include/X11/X.h pkg:/x11/header/xproto@7.0.28-2015.0.1.0
%define pnm_buildrequires_SUNWxwinc_devel	x11/header/xproto
%define pnm_buildrequires_SUNWxwinc		x11/header/xproto
%define pnm_requires_SUNWxwinc			x11/header/xproto
%endif
#END oihipster



#info: graphviz added around consolidation/userland/userland-incorporation@0.5.11,5.11-0.172:20110815T080358Z
#
#note: if you prefer the maybe more uptodate "version" ofr SFEgraphviz, then put that SFEpackagename into (Build)Requirements
#      if you need any version of graphviz, then use pnm_buildrequires_SUNWgraphviz or ..._SFEgraphviz
#20140707 Solaris 11.x has 
#20140707 OpenIndiana has none
#20140707 OpenIndiana-Hipster has image/graphviz@2.28.0,5.11-2014.0.1.3:20140528T102249Z
#set default
%define pnm_buildrequires_SUNWgraphviz		SFEgraphviz
%define pnm_requires_SUNWgraphviz		SFEgraphviz
%define pnm_buildrequires_SFEgraphviz		SFEgraphviz
%define pnm_requires_SFEgraphviz		SFEgraphviz
%define graphviz_default_prefix			/usr/gnu
%define graphviz_default_include		/usr/gnu/include
%define graphviz_default_libdir			/usr/gnu/lib

#set parameters for more fresh osbuild / osdistro
#Solaris 11 Solaris 12 
##TODO## add OI OpenIndiana Hipster image/graphviz@2.28.0,5.11-2014.0.1.3:20140528T102249Z
%if %( expr %{solaris11} '+' %{solaris12} '+' %{oihipster} '>=' 1 )
%define pnm_buildrequires_SUNWgraphviz		image/graphviz
%define pnm_requires_SUNWgraphviz		image/graphviz
%define pnm_buildrequires_SFEgraphviz		image/graphviz
%define pnm_requires_SFEgraphviz		image/graphviz
%define graphviz_default_prefix			/usr
%define graphviz_default_include		/usr/include
%define graphviz_default_libdir			/usr/lib
%endif
#END solaris11 solaris12 oihipster



#-----------------------------------------------------------------
#set defaults, in case the build is newer, overwrite them
#this is for all builds (below 151)
%define pnm_buildrequires_SFEvala_devel        	SFEvala-devel
%define pnm_buildrequires_SFEvala		SFEvala
%define pnm_requires_SFEvala			SFEvala
%define pnm_buildrequires_developer_vala        SFEvala-devel
%define pnm_requires_developer_vala		SFEvala

#cases >=151
%if %( expr %{osbuild} '>=' 151 '|' %{solaris12} '>=' 1 )
%define pnm_buildrequires_SFEvala_devel		developer/vala
%define pnm_buildrequires_SFEvala		developer/vala
%define pnm_requires_SFEvala			developer/vala
%define pnm_buildrequires_developer_vala	developer/vala
%define pnm_requires_developer_vala		developer/vala
%endif
#END >= 151

#-----------------------------------------------------------------
#set defaults for SFExz | compress/xz, in case the build is newer,
#overwrite them
#this is for S11 (all builds) and (OI < 151)
%define pnm_buildrequires_SFExz_gnu		SFExz-gnu
%define pnm_requires_SFExz_gnu			SFExz-gnu
%define pnm_buildrequires_compress_xz		SFExz-gnu
%define pnm_requires_compress_xz		SFExz-gnu

#cases >= 151 && ( OpenIndiana | OmniOS | OIHipster )
%if %( expr %{openindiana} '+' %{omnios} '+' %{oihipster} )
%if %( expr %{osbuild} '>=' 151 )
%define pnm_buildrequires_SFExz_gnu		compress/xz
%define pnm_requires_SFExz_gnu			compress/xz
%define pnm_buildrequires_compress_xz		compress/xz
%define pnm_requires_compress_xz		compress/xz
%endif
#END >= 151
%endif
#END openindiana

#-----------------------------------------------------------------
#set defaults for SFElibggz
#overwrite them in case the osdisto has its own libggz packaged in gnome-media or gnome-games
#this is for OI 151 all builds (and SXCE)
%define pnm_buildrequires_SFElibggz_devel	SUNWgnome-games-devel
%define pnm_buildrequires_SFElibggz		SUNWgnome-games-devel
%define pnm_requires_SFElibggz			SUNWgnome-games

#cases Solaris 11 or Solaris 12 has no longer libggz in the
#packages gnome/games
%if %( expr %{solaris11express} '>=' 1 '|' %{solaris12} '>=' 1 )
%define pnm_buildrequires_SFElibggz_devel	SFElibggz-devel
%define pnm_buildrequires_SFElibggz		SFElibggz-devel
%define pnm_requires_SFElibggz			SFElibggz
%endif
#END solaris11express or solaris 12


#-----------------------------------------------------------------
# this section overwrites settings form above originally applying to 
# osbuild >=133 AND os2nnn
# note: system/library/c++-runtime is renamed on OI to system/library/c++/sunpro
#cases >= 151 && OpenIndiana or OIHipster
%if %( expr %{openindiana}  '+' %{oihipster} )
%if %( expr %{osbuild} '>=' 151 )
%define pnm_buildrequires_SUNWlibC_devel		system/library/c++/sunpro
%define pnm_buildrequires_SUNWlibC			system/library/c++/sunpro
%define pnm_requires_SUNWlibC				system/library/c++/sunpro
%endif
#END >= 151
%endif
#END openindiana oihipster


#-----------------------------------------------------------------
# all distro
#cppunit
%define pnm_buildrequires_SFEcppunit		SFEcppunit-gpp
%define pnm_requires_SFEcppunit			SFEcppunit-gpp
%define pnm_buildrequires_developer_cppunit	SFEcppunit-gpp
%define pnm_requires_developer_cppunit		SFEcppunit-gpp

# but OIHipster brings its own packages, then use those (for those, osdistro delivered pkg is good enough)
%if %{oihipster}
#cppunit
#unfortunatly pkgtool can't see the complete name pkg://openindiana.org/.../... if this is intalled, only developer/cppunit
#but as we just don't have or local SFEccpunit in the repo/in an allowed version, this should work
#%define pnm_buildrequires_SFEcppunit		pkg://openindiana.org/developer/cppunit
#%define pnm_requires_SFEcppunit			pkg://openindiana.org/developer/cppunit
#%define pnm_buildrequires_developer_cppunit	pkg://openindiana.org/developer/cppunit
#%define pnm_requires_developer_cppunit		pkg://openindiana.org/developer/cppunit
%define pnm_buildrequires_SFEcppunit		developer/cppunit
%define pnm_requires_SFEcppunit			developer/cppunit
%define pnm_buildrequires_developer_cppunit	developer/cppunit
%define pnm_requires_developer_cppunit		developer/cppunit
%endif
#END oihipster

#-----------------------------------------------------------------
#special cases, set defaults first
%define pnm_buildrequires_SFEfreeglut		SFEfreeglut
%define pnm_requires_SFEfreeglut		SFEfreeglut
%define pnm_buildrequires_x11_library_freeglut	SFEfreeglut
%define pnm_requires_x11_library_freeglut	SFEfreeglut
#-----------------------------------------------------------------
#changes the defaults from above, in case the build is newer.
#this is for Solaris (Express) 11 builds (above excluding 151)
#which now includes freeglut
#%if %(expr %{solaris12} '>=' 1 '|' '(' %{solaris11express} '>=' 1 '&' %{osbuild} '>' 151 ')')
%if %( expr %{solaris12} '>=' 1 )
#%if 0
%define pnm_buildrequires_SFEfreeglut		x11/library/freeglut
%define pnm_requires_SFEfreeglut		x11/library/freeglut
%define pnm_buildrequires_x11_library_freeglut	x11/library/freeglut
%define pnm_requires_x11_library_freeglut	x11/library/freeglut

#starting with: developer/documentation-tool/asciidoc@8.6.8,5.12-5.12.0.0.0.34.0
%if %( expr %{osbuild} '>=' 34 )
%define pnm_buildrequires_SFEasciidoc   	developer/documentation-tool/asciidoc
%define pnm_requires_SFEasciidoc        	developer/documentation-tool/asciidoc
#END osbuild >= 34
%endif
#%define pnm_buildrequires_SFEasciidoc   	pkg://solaris/developer/documentation-tool/asciidoc
#%define pnm_requires_SFEasciidoc        	pkg://solaris/developer/documentation-tool/asciidoc
#END solaris12
%endif

%if %( expr %{solaris11express} '>=' 1 '&' %{osbuild} '>' 151 )
%define pnm_buildrequires_SFEfreeglut		x11/library/freeglut
%define pnm_requires_SFEfreeglut		x11/library/freeglut
%define pnm_buildrequires_x11_library_freeglut	x11/library/freeglut
%define pnm_requires_x11_library_freeglut	x11/library/freeglut
#END solaris11express > 151
%endif


#-----------------------------------------------------------------
#packages no longer available, we could bail out or just require a core package
#to continue for now, we just set a already existing package name, the spec file 
#might fail compiling or have reduced functionality then -> up to the individual
#spec file maintainer how to solve that

#cases >=156
%if %( expr %{solaris11express} '>=' 1 '|' %{solaris12} '>=' 1 )
%if %( expr %{osbuild} '>=' 156        '|' %{solaris12} '>=' 1 )
#https://defect.opensolaris.org/bz/attachment.cgi?id=4441
#(the attachment link from above is in: https://defect.opensolaris.org/bz/show_bug.cgi?id=17668)
%define pnm_buildrequires_library_python_2_python_pigment_26	SUNWcs
%define pnm_requires_library_python_2_python_pigment_26		SUNWcs
%define pnm_buildrequires_SUNWlibpigment			SUNWcs
%define pnm_buildrequires_SUNWlibpigment_devel			SUNWcs
%define pnm_buildrequires_SUNWlibpigment_python26		SUNWcs
%define pnm_buildrequires_SUNWlibpigment_python26_devel		SUNWcs
%define pnm_requires_SUNWlibpigment				SUNWcs
%define pnm_requires_SUNWlibpigment_devel			SUNWcs
%define pnm_requires_SUNWlibpigment_python26			SUNWcs
%define pnm_requires_SUNWlibpigment_python26_devel		SUNWcs
%endif
#END >=156
%endif
#END solaris11express (and newer, e.g. Solaris 11)

# cases >=160
# python
# library/python-2/python-gnome-libs-26 changed to a renamed-to package,
# so pkgtool can't see if its new dependents are installed.
# this is a workaround, we just require one of the dependents.
##TODO## improve: find the best matching replacement for library/python-2/python-gnome-libs-26
#for now we replace with library/python-2/pygtk2-26
%if %( expr %{solaris11express} '>=' 1 '|' %{solaris12} '>=' 1 '|' %{solaris12} '>=' 1 )
%if %( expr %{osbuild} '>=' 160        '|' %{solaris12} '>=' 1 '|' %{solaris12} '>=' 1 )
%define pnm_buildrequires_SUNWgnome_python26_libs_devel		library/python-2/pygtk2-26
%define pnm_requires_SUNWgnome_python26_libs_devel		library/python-2/pygtk2-26
%define pnm_buildrequires_SUNWgnome_python26_libs		library/python-2/pygtk2-26
%define pnm_requires_SUNWgnome_python26_libs			library/python-2/pygtk2-26
%endif
#END >=160
%endif
#END solaris11express (and newer, e.g. Solaris 11)

# audio headers got renamed several times, then 
# included in other package
%if %( expr %{solaris11express} '>=' 1 '|' %{solaris12} '>=' 1 )
%if %( expr %{osbuild} '>=' 163        '|' %{solaris12} '>=' 1 )
#with 163 system/header/header-audio moved into system/header
%define pnm_buildrequires_SUNWaudh_devel 			system/header
%define pnm_buildrequires_SUNWaudh 				system/header
%define pnm_requires_SUNWaudh 					system/header
%define pnm_buildrequires_audh 					system/header
%define pnm_requires_audh 					system/header
%define pnm_buildrequires_system_header_header_audio		system/header
%define pnm_requires_system_header_header_audio 		system/header

# SUNWfuse and SUNWlibfuse appeared -> replaces SFEfuse SFElibfuse on S11
# but names changed to library/libfuse and file-system/uvfs
%define pnm_buildrequires_SUNWfuse				file-system/uvfs
%define pnm_requires_SUNWfuse					file-system/uvfs
%define pnm_buildrequires_SUNWfusefs				file-system/uvfs
%define pnm_requires_SUNWfusefs					file-system/uvfs
%define pnm_buildrequires_SUNWlibfuse				library/libfuse
%define pnm_requires_SUNWlibfuse				library/libfuse

%endif
#END >=163
%endif
#END solaris11express

# header migrated into main package
#system/library/mozilla-nss@0.5.11-0.160 on s12_79
#nspr
#solaris 11 >= 160 or solaris12
#system/library/mozilla-nss renamed library/security/nss@4.12.10-0.172.0.0.0.0.0
#note: openindiana and oihipster 2015.0.1.0 still have system/library/mozilla-nss/header-nss
%if %( expr %{solaris12} '|' %{solaris11} '>=' 1 '&' %{osbuild} '>=' 160 )
%define pnm_buildrequires_system_library_mozilla_nss_header_nss	library/security/nss
%define pnm_requires_system_library_mozilla_nss_header_nss	library/security/nss
%define pnm_buildrequires_system_library_mozilla_nss		library/security/nss
%define pnm_requires_system_library_mozilla_nss			library/security/nss
%define pnm_buildrequires_SUNWtlsd_devel			library/security/nss
%define pnm_buildrequires_SUNWtlsd				library/security/nss
%define pnm_requires_SUNWtlsd					library/security/nss
%define pnm_buildrequires_tlsd					library/security/nss
%define pnm_requires_tlsd					library/security/nss
##TODO## nspr
%define pnm_buildrequires_library_nspr			library/nspr
%define pnm_requires_library_nspr			library/nspr
%define pnm_buildrequires_SUNWpr_devel			library/nspr
%define pnm_buildrequires_SUNWpr			library/nspr
%define pnm_requires_SUNWpr				library/nspr
%define pnm_buildrequires_pr				library/nspr
%define pnm_requires_pr					library/nspr
%define pnm_buildrequires_library_nspr_header_nspr	library/nspr
%define pnm_requires_library_nspr_header_nspr		library/nspr
%define pnm_buildrequires_SUNWprd_devel			library/nspr
%define pnm_buildrequires_SUNWprd			library/nspr
%define pnm_requires_SUNWprd				library/nspr
%define pnm_buildrequires_prd				library/nspr
%define pnm_requires_prd				library/nspr
%endif
#END solaris 12 | solaris 11 >= 160

#s12 sfe /localhomes/tom/spec-files-extra pkg info -r mozilla-nss                                                                                                                      
#          Name: system/library/mozilla-nss
#         State: Not installed (Renamed)
#    Renamed to: consolidation/sic_team/sic_team-incorporation
#                library/security/nss@4.12.10-0.172.0.0.0.0.0        XXXXXXXXXXXXXXXXXX
#     Publisher: solaris
#       Version: 0.5.11
#        Branch: 0.172.0.0.0.0.0
#Packaging Date: Tue Aug 16 07:11:53 2011
#          Size: 5.45 kB
#          FMRI: pkg://solaris/system/library/mozilla-nss@0.5.11-0.172.0.0.0.0.0:20110816T071153Z
#
#          Name: system/mozilla-nss
#         State: Not installed (Renamed)
#    Renamed to: security/nss-utilities@4.12.10-0.172.0.0.0.0.0        XXXXXXXXXXXXXXXXXX
#                consolidation/sic_team/sic_team-incorporation
#     Publisher: solaris
#       Version: 0.5.11
#        Branch: 0.172.0.0.0.0.0
#Packaging Date: Tue Aug 16 07:12:00 2011
#          Size: 5.45 kB
#          FMRI: pkg://solaris/system/mozilla-nss@0.5.11-0.172.0.0.0.0.0:20110816T071200Z
#
#
#          Name: system/library/mozilla-nss
#Zusammenfassung: 
#        Status: Nicht installiert (Umbenannt)
#  Umbenannt in: consolidation/sic_team/sic_team-incorporation
#                library/security/nss@4.12.10-0.172.0.0.0.0.0
#   Herausgeber: solaris
#       Version: 0.5.11
# Build-Version: 5.11
#         Zweig: 0.172.0.0.0.0.0
#Packaging-Datum: 16. August 2011 07:11:53 Uhr 
#         Größe: 5.45 KB
#          FMRI: pkg://solaris/system/library/mozilla-nss@0.5.11,5.11-0.172.0.0.0.0.0:20110816T071153Z
#
#          Name: system/library/mozilla-nss/header-nss
#Zusammenfassung: 
#        Status: Nicht installiert (Umbenannt)
#  Umbenannt in: system/library/mozilla-nss@0.5.11-0.160
#   Herausgeber: solaris
#       Version: 0.5.11
# Build-Version: 5.11
#         Zweig: 0.160
#Packaging-Datum: 28. Februar 2011 16:47:35 Uhr 
#         Größe: 0.00 B
#          FMRI: pkg://solaris/system/library/mozilla-nss/header-nss@0.5.11,5.11-0.160:20110228T164735Z


# math headers went from pkg://system/library/math/header-math
#                     to pkg://system/library/math@0.5.11-0.174.0.0.0.0.0
# OI stays unchanged for a while
# Hipster has header-math integrated into math
#with build 174 library/math/header-math moved into system/library/math, as well on S12 OIH
%if %( expr %{solaris12} '+' %{oihipster} '+' %{omnios} '>=' 1 '|' %{osbuild} '>=' 174 )
%define pnm_buildrequires_system_library_math_header_math	system/library/math
%define pnm_requires_system_library_math_header_math		system/library/math
%define pnm_buildrequires_SUNWlibm_devel			system/library/math
%define pnm_buildrequires_SUNWlibm				system/library/math
%define pnm_requires_SUNWlibm					system/library/math
%define pnm_buildrequires_libm					system/library/math
%define pnm_requires_libm					system/library/math
%endif
#END solaris12 oihipster osbuild >= 174 ....

##TODO## maybe re-locate the definitions below if that helps getting better overview
#SEE ALSO: new include file packagenames.define.initial.inc
#NOTE# Defaults here for os2nn, SXCE, and so on. This is overlayed if one 
#distro needs this different!
#pulseaudio, we currently have this in SFE - see below for more fresh distros
%define pnm_buildrequires_SFEpulseaudio				SFEpulseaudio-devel
%define pnm_requires_SFEpulseaudio				SFEpulseaudio
%define pnm_buildrequires_pulseaudio				SFEpulseaudio-devel
%define pnm_requires_pulseaudio				SFEpulseaudio

#automake version 1.11, we currently have this in SFE - see below for more fresh distros
%define pnm_buildrequires_developer_build_automake_111	SFEautomake-111
%define pnm_buildrequires_developer_build_automake_111	SFEautomake-111
%define pnm_buildrequires_SUNWautomake_111		SFEautomake-111
%define pnm_requires_SUNWautomake_111			SFEautomake-111
%define pnm_buildrequires_SFEautomake_111		SFEautomake-111
%define pnm_requires_SFEautomake_111			SFEautomake-111

#Added to S11.2, S12 but all others might not have it and go for sfe/shell/gnu-getopt
#set the SFE spec file as default for os20nn SXCE, overlay that for >=S11.2, S12
%define pnm_buildrequires_SFEgnugetopt			SFEgnugetopt
%define pnm_requires_SFEgnugetopt			SFEgnugetopt
%define pnm_buildrequires_shell_gnugetopt		SFEgnugetopt
%define pnm_requires_shell_gnugetopt			SFEgnugetopt

#doesn't autoinstall by resolveipspackages, to try this way
%define pnm_buildrequires_SFEgdbm		library/database/gdbm
%define pnm_requires_SFEgdbm		 	library/database/gdbm
%define pnm_buildrequires_SUNWgnu_dbm		library/database/gdbm
%define pnm_requires_SUNWgnu_dbm	 	library/database/gdbm



#NOTE# now overlay the above definitions if needed:

#START Solaris 11 without update, S11.0
%if %{solaris11}
%if %( expr  %{osdistrelnumber} '>=' 201100 )
#  service/hal was renamed to system/hal around S11.0    0.5.11-0.173.0.0.0.1.0     --r
#new
%define pnm_buildrequires_system_hal		system/hal
%define pnm_requires_system_hal			system/hal
#old
%define pnm_buildrequires_service_hal		system/hal
%define pnm_requires_service_hal		system/hal
%define pnm_buildrequires_SUNWhal_devel		system/hal
%define pnm_buildrequires_SUNWhal		system/hal
%define pnm_requires_SUNWhal			system/hal
%define pnm_buildrequires_hal			system/hal
%define pnm_requires_hal			system/hal

%endif
#END osdistrelnumber >= 201100 aka solaris11 11.0 and newer
%endif
#END solaris11


#START Solaris 11 Update 1
#
#pulseaudio, automake-111 w/o legacy name in Solaris 11.1 and newer
%if %{solaris11}
%if %( expr  %{osdistrelnumber} '>=' 201101 )
%define pnm_buildrequires_SFEpulseaudio				SUNWpulseaudio-devel
%define pnm_requires_SFEpulseaudio				SUNWpulseaudio
%define pnm_buildrequires_pulseaudio				SUNWpulseaudio-devel
%define pnm_requires_pulseaudio					SUNWpulseaudio

#SUNWautomake-111 SFEautomake-111
#starting with S11 175.1 we have developer/build/automake-111
#developer/build/automake-111@1.11.2,5.11-0.175.1.0.0.24.0:20120904T171150Z
%define pnm_buildrequires_developer_build_automake_111	developer/build/automake-111
%define pnm_buildrequires_developer_build_automake_111	developer/build/automake-111
%define pnm_buildrequires_SUNWautomake_111		developer/build/automake-111
%define pnm_requires_SUNWautomake_111			developer/build/automake-111
%define pnm_buildrequires_SFEautomake_111		developer/build/automake-111
%define pnm_requires_SFEautomake_111			developer/build/automake-111

#library/libedit@3.0,5.11-0.175.1.0.0.24.0:20120904T172539Z
%define pnm_buildrequires_library_libedit		library/libedit
%define pnm_requires_library_libedit			library/libedit
%define pnm_buildrequires_SFEeditline			library/libedit
%define pnm_requires_SFEeditline			library/libedit

%endif
#END osdistrelnumber >= 201101 aka solaris11 11.1 and newer
%endif
#END solaris11


#START Solaris 11 Update 2
#
#gnu-getopt added (S11.2, S12)
%if %{solaris11}
%if %( expr  %{osdistrelnumber} '>=' 201102 )

#Added to S11.2, S12 but all others might not have it and go for sfe/shell/gnu-getopt
%define pnm_buildrequires_SFEgnugetopt			pkg://solaris/shell/gnu-getopt
%define pnm_requires_SFEgnugetopt			pkg://solaris/shell/gnu-getopt
%define pnm_buildrequires_shell_gnugetopt		pkg://solaris/shell/gnu-getopt
%define pnm_requires_shell_gnugetopt			pkg://solaris/shell/gnu-getopt

%endif
#END osdistrelnumber >= 201102 aka solaris11 11.2 and newer
%endif
#END solaris11

#START Solaris 11 Update 3
#
%if %{solaris11}
%if %( expr  %{osdistrelnumber} '>=' 201103 )

#Added to S11.3 build 26 and S12 build 90
# developer/documentation-tool/xmlto@0.0.25,5.11-0.175.3.0.0.26.0
%define pnm_buildrequires_developer_documentation_tool_xmlto	developer/documentation-tool/xmlto
%define pnm_requires_developer_documentation_tool_xmlto		developer/documentation-tool/xmlto
%define pnm_buildrequires_SFExmlto				developer/documentation-tool/xmlto
%define pnm_requires_SFExmlto					developer/documentation-tool/xmlto

%endif
#END osdistrelnumber >= 201102 aka solaris11 11.2 and newer
%endif
#END solaris11


#START Solaris 12 - generic/(almost)all builds - more details below
#
#
#  Warning: as compiling and running builds older then a few weeks old doesn't make
#           much sense, we do not keep exact build numbers when things change.
#
#           example: Build 103 and following brought us Gnome3, but we anyways start
#                    setting rules here for *all* S12 builds, yes that may break
#                    compiling on older builds. Don't you want upgrading more often?
#
#           good style is to make a comment with which build the change happened,
#           so one gets a chance to make a workaround in case you can't upgrade the os today
#
%if %{solaris12}
%define pnm_buildrequires_SFEpulseaudio				SUNWpulseaudio-devel
%define pnm_requires_SFEpulseaudio				SUNWpulseaudio
%define pnm_buildrequires_pulseaudio				SUNWpulseaudio-devel
%define pnm_requires_pulseaudio					SUNWpulseaudio

#SUNWautomake-111 SFEautomake-111
#starting with S11 175.1 we have developer/build/automake-111
%define pnm_buildrequires_developer_build_automake_111	developer/build/automake-111
%define pnm_buildrequires_developer_build_automake_111	developer/build/automake-111
%define pnm_buildrequires_SUNWautomake_111		developer/build/automake-111
%define pnm_requires_SUNWautomake_111			developer/build/automake-111
%define pnm_buildrequires_SFEautomake_111		developer/build/automake-111
%define pnm_requires_SFEautomake_111			developer/build/automake-111

#SFEautomake-115 - may be replaced by an osdistro.
#if you get upgrade contraints, then uninstall the SFE automake-115 package
#starting with S12 (some build) we have developer/build/automake-115
%define pnm_buildrequires_developer_build_automake_115        developer/build/automake-115
%define pnm_buildrequires_developer_build_automake_115        developer/build/automake-115
%define pnm_buildrequires_SUNWautomake_115            developer/build/automake-115
%define pnm_requires_SUNWautomake_115                 developer/build/automake-115
%define pnm_buildrequires_SFEautomake_115             developer/build/automake-115
%define pnm_requires_SFEautomake_115                  developer/build/automake-115

#S12 lost the legacy name SUNWgnu-dbm
%define pnm_buildrequires_SFEgdbm		library/database/gdbm
%define pnm_requires_SFEgdbm		 	library/database/gdbm
%define pnm_buildrequires_SUNWgnu_dbm		library/database/gdbm
%define pnm_requires_SUNWgnu_dbm	 	library/database/gdbm

##TODO## check if this is the case as well for S11 (!)
#S12 lost the legacy name SUNWslang
%define pnm_buildrequires_SUNWslang_devel library/slang
%define pnm_buildrequires_SUNWslang library/slang
%define pnm_requires_SUNWslang library/slang

#Added to S11.2, S12 but all others might not have it and go for sfe/shell/gnu-getopt
%define pnm_buildrequires_SFEgnugetopt			pkg://solaris/shell/gnu-getopt
%define pnm_requires_SFEgnugetopt			pkg://solaris/shell/gnu-getopt
%define pnm_buildrequires_shell_gnugetopt		pkg://solaris/shell/gnu-getopt
%define pnm_requires_shell_gnugetopt			pkg://solaris/shell/gnu-getopt

#Added to S11.3 build 26 and S12 build 90
# developer/documentation-tool/xmlto
%define pnm_buildrequires_developer_documentation_tool_xmlto	developer/documentation-tool/xmlto
%define pnm_requires_developer_documentation_tool_xmlto		developer/documentation-tool/xmlto
%define pnm_buildrequires_SFExmlto				developer/documentation-tool/xmlto
%define pnm_requires_SFExmlto					developer/documentation-tool/xmlto

#with around build 103 gnome3 starts, gnome-audio obsoleted in build 112 (probably)
#we replace it with something very generic
%define pnm_buildrequires_gnome_gnome_audio	system/core-os
%define pnm_requires_gnome_gnome_audio		system/core-os
%define pnm_buildrequires_SUNWgnome_audio_devel	system/core-os
%define pnm_buildrequires_SUNWgnome_audio	system/core-os
%define pnm_requires_SUNWgnome_audio		system/core-os
%define pnm_buildrequires_gnome_audio		system/core-os
%define pnm_requires_gnome_audio		system/core-os

#historic:
# pkg contents -r -m SUNWgnome-common-devel@0.5.11,5.11-0.175
#set name=pkg.fmri value=pkg://solaris/SUNWgnome-common-devel@0.5.11,5.11-0.175.0.0.0.0.0:20110927T073138Z
#set name=pkg.renamed value=true
#depend fmri=developer/gnome/gettext@0.5.11-0.133 type=require
#depend fmri=consolidation/desktop/gnome-incorporation type=require

# IF you want gettext, then you may choose pnm_buildrequires_SUNWgnu_gettext

#mostly needed for "gettext" developer/gnome/gettext
#library/gnome/gnome-common pulls in developer/gnome/gettext
# and developer/gnome/gettext has been renamed to text/gnu-gettext
%define pnm_buildrequires_SUNWgnome_common_devel 	library/gnome/gnome-common
%define pnm_requires_SUNWgnome_common_devel 		library/gnome/gnome-common
%define pnm_buildrequires_gnome_common_devel 		library/gnome/gnome-common
%define pnm_requires_gnome_common_devel 		library/gnome/gnome-common

%define pnm_buildrequires_SUNWgnu_gettext_devel		text/gnu-gettext
%define pnm_buildrequires_SUNWgnu_gettext		text/gnu-gettext
%define pnm_requires_SUNWgnu_gettext			text/gnu-gettext
%define pnm_buildrequires_developer_gnome_gettext	text/gnu-gettext
%define pnm_requires_developer_gnome_gettext		text/gnu-gettext
%define pnm_buildrequires_text_gnu_gettext		text/gnu-gettext
%define pnm_requires_text_gnu_gettext			text/gnu-gettext
%define pnm_buildrequires_gnu_gettext			text/gnu-gettext
%define pnm_requires_gnu_gettext			text/gnu-gettext

#below may be redundant...check later
%define pnm_buildrequires_text_gnu_gettext text/gnu-gettext
%define pnm_requires_text_gnu_gettext text/gnu-gettext
%define pnm_buildrequires_SUNWgnu_gettext_devel text/gnu-gettext
%define pnm_buildrequires_SUNWgnu_gettext text/gnu-gettext
%define pnm_requires_SUNWgnu_gettext text/gnu-gettext
%define pnm_buildrequires_gnu_gettext text/gnu-gettext
%define pnm_requires_gnu_gettext text/gnu-gettext

#S12 adds gstreamer 1.x and obsoletes it on build 113
#library/audio/gstreamer                           0.10.32-5.12.0.0.0.87.0    i--
#library/audio/gstreamer/plugin/gnonlin            0.10.17-5.12.0.0.0.90.0    --o
#library/desktop/gstreamer-1                       1.4.5-5.12.0.0.0.112.1     i--
#library/desktop/gstreamer-1/gst-plugins-base      1.4.5-5.12.0.0.0.112.1     i--
#library/desktop/gstreamer-1/gst-plugins-good      1.4.5-5.12.0.0.0.112.1     i--
##TODO## open: what to do with the new package names. for a moment we can use pnm_macro
#        of old package name and still get the new package. would work across all supported osdistro
#
##TODO## open: how to handle library/desktop/gstreamer-1/gst-plugins-base and library/desktop/gstreamer-1/gst-plugins-good
##NOTE##   s/audio/desktop/
%define pnm_buildrequires_library_audio_gstreamer	library/desktop/gstreamer-1
%define pnm_requires_library_audio_gstreamer		library/desktop/gstreamer-1
#for now, just request library/desktop/gstreamer-1, details only handled once the need arises
%define pnm_buildrequires_SUNWgnome_media_devel		library/desktop/gstreamer-1
%define pnm_buildrequires_SUNWgnome_media		library/desktop/gstreamer-1
%define pnm_requires_SUNWgnome_media			library/desktop/gstreamer-1
%define pnm_buildrequires_gnome_media			library/desktop/gstreamer-1
%define pnm_requires_gnome_media			library/desktop/gstreamer-1
#for now, just request library/desktop/gstreamer-1, details only handled once the need arises
%define pnm_buildrequires_library_audio_gstreamer_plugin_gnonlin	library/desktop/gstreamer-1
%define pnm_requires_library_audio_gstreamer_plugin_gnonlin	library/desktop/gstreamer-1
%define pnm_buildrequires_SUNWgnonlin_devel		library/desktop/gstreame-1r
%define pnm_buildrequires_SUNWgnonlin			library/desktop/gstreamer-1
%define pnm_requires_SUNWgnonlin			library/desktop/gstreamer-1
%define pnm_buildrequires_gnonlin			library/desktop/gstreamer-1
%define pnm_requires_gnonlin				library/desktop/gstreamer-1


#codec/libvorbis                                   1.3.3-5.12.0.0.0.115.0     ---
#codec/ogg-vorbis                                  2.30.0-5.12.0.0.0.108.0    --r

#START solaris 12 - special build versions below >= 87
%endif
#END solaris12 - generic/(almost)all builds - more details below


%if %( expr %{solaris12} '&' %{osdistro_entire_padded_number4}.1 '>=' 0005001200000000000000870000.1 )
#many osdistro do not deliver the file "zlib.pc" for pkgconfig, SFE drops one in until the osdistro has one
#osdistro which have one, can replace this in pnm_macro include file (example: S12)
%define pnm_buildrequires_SFEzlib_pkgconfig     library/zlib
%define pnm_requires_SFEzlib_pkgconfig          library/zlib
%endif
#END solaris12 special build version 87 and newer


#START solaris 12 - special build versions below >= 108
%if %( expr %{solaris12} '&' %{osdistro_entire_padded_number4}.1 '>=' 0005001200000000000001080000.1 )
#Package codec/ogg-vorbis was renamed to pkg:/codec/libvorbis pkg:/codec/libogg  (NOTE: these are *two* packages!)
#pkg://solaris/codec/libogg@1.2.2-5.12.0.0.0.108.1:20160919T062323Z           ---
#pkg://solaris/codec/ogg-vorbis@2.30.0-5.12.0.0.0.108.0:20160919T062335Z

%define pnm_buildrequires_codec_ogg_vorbis	codec/libogg,codec/libvorbis
%define pnm_requires_codec_ogg_vorbis		codec/libogg,codec/libvorbis
%define pnm_buildrequires_SUNWogg_vorbis_devel	codec/libogg,codec/libvorbis
%define pnm_buildrequires_SUNWogg_vorbis	codec/libogg,codec/libvorbis
%define pnm_requires_SUNWogg_vorbis		codec/libogg,codec/libvorbis
%define pnm_buildrequires_ogg_vorbis		codec/libogg,codec/libvorbis
%define pnm_requires_ogg_vorbis			codec/libogg,codec/libvorbis
%endif
#END solaris12 special build version 108 and newer


#START setting perl5, defaults  - Part 1 of 3
#define perl defaults, primarily shared settings and default version, paths
#for older osbuilds/osdistros like OpenSolaris 134, SXCE/Nevada, Solaris 10
#STRONG NOTE: located *below* the osdistro and osbuild sections, there is *another*
#section evaluating the resulting paths on the disk, those are specific
#to the perl version in use. We hope, that we do not need to handle special
#cases there, e.g. this would be an odd distro deciding to relocate to 
#another path layout on disk....

#note: older Solaris releases did include "micro"-versionnumber in 
#modules path, e.g. vendor_perl/5.8.4
#more fresh versions do only set major.minor, this is e.g. vendor_perl/5.12
%define perl_version 5.8.4
%define perl_major_version 5
%define perl_major_minor_version 5.8
%define perl_major_minor_micro_version 5.8.4

###TODO## not clear if we should require SUNWperl584core or SUNWperl584usr
#both?
#note: the name is subject to change if we find a better one
#_default string is not meant to be a part of the package name...
%define pnm_buildrequires_perl_default	SUNWperl584core, SUNWperl584usr
%define pnm_requires_perl_default	SUNWperl584core, SUNWperl584usr

# NOTE the section sitting below the distro specfic settings
# where the resulting paths on the disk are evaluated!

#END setting perl5, defaults  - Part 1 of 3



#START setting perl5, changes with specific builds and distros  - Part 2 of 3

#the distro specific settings below.
#set specifics for more fresh osbuild/osdistro like Solaris 11 Express, OpenIndiana
#which integrate perl 5.10 or newer (please add more sections for overrides in 
#different distro releases. Order is: greatest osbuild must be listed last to
#override previous settings)

#set perl5 for Solaris 12
%if %{os2nnn}
%if %( expr  %{solaris12} '>=' 1 )
#set perl5 for Solaris 12
%define perl_version 5.12
%define perl_major_minor_version 5.12
%define perl_major_minor_micro_version 5.12.5
#runtime/perl-512 or library/perl-5/sun-solaris-512
%define pnm_buildrequires_perl_default runtime/perl-512
%define pnm_requires_perl_default	runtime/perl-512
%if %( expr %{osbuild} '>=' 95 )
%define perl_version 5.22
%define perl_major_minor_version 5.22
%define perl_major_minor_micro_version 5.22.1
#perl is 64-bit
%define pnm_buildrequires_perl_default runtime/perl-522
%define pnm_requires_perl_default	runtime/perl-522
%endif
#END build >= 95
%endif
#END solaris12
%endif
#END os2nnn

#set perl5 for Solaris 11, Solaris11Express
%if %{os2nnn}
%if %( expr %{solaris11express} '>=' 1 '&' %{osbuild} '>=' 166 )
#set perl5 for Solaris 11, Solaris 11 Express
%define perl_version 5.12
%define perl_major_minor_version 5.12
%define perl_major_minor_micro_version 5.12.3
#runtime/perl-512 or library/perl-5/sun-solaris-512
%define pnm_buildrequires_perl_default runtime/perl-512
%define pnm_requires_perl_default	runtime/perl-512
%endif
#END solaris11, solaris11express >= 166
%endif
#END os2nnn


#set perl5 for OpenIndiana
%if %{os2nnn}
%if %{openindiana}
##TODO## monitor closely when OpenIndiana starts shipping complete module sets with e.g. perl-512
%if %( expr %{osbuild} '>=' 151 )
#set perl5 for OpenIndiana 
#/usr/perl5/vendor_perl/5.10.0/i86pc-solaris-64int/ so we need perl_version to read 5.10.0
%define perl_version 5.10.0
%define perl_major_minor_version 5.10
##TODO## determine correct version %define perl_major_minor_micro_version 5.10.x
%define perl_major_minor_micro_version 5.10.0
#runtime/perl-510
%define pnm_buildrequires_perl_default runtime/perl-510
%define pnm_requires_perl_default	runtime/perl-510
%endif
#END >= 151
%endif
#END openindiana
%endif
#END os2nnn

#set perl5 for OIHipster
#runtime/perl-516@5.16.3,5.11-2014.0.1.1:20140528T081041Z
%if %( expr %{oihipster} '>=' 1 '&' %{osdistro_entire_padded_number4}.0 '>=' 2014000000010001000000000000.0 )
##TODO## monitor closely when OIHipster changes chipped perl-versions or adds perl-modules
#set perl5 for OIHipster
#looks like paths changed to: /usr/perl5/vendor_perl/5.16
%define perl_version 5.16
%define perl_major_minor_version 5.16
##TODO## determine correct version %define perl_major_minor_micro_version 5.16.x
%define perl_major_minor_micro_version 5.16.3
#runtime/perl-516
%define pnm_buildrequires_perl_default runtime/perl-516
%define pnm_requires_perl_default	runtime/perl-516
%endif
#END oihipster >= 2014.0.1.1


#set perl5 for OIHipster >= 2015.0.1.0    (was 2015.0.2.1)
#runtime/perl-522@5.22.0,5.11-2015.0.1.0:20150727T054604Z
#runtime/perl-522@5.22.0,5.11-2015.0.1.0:20150727T062342Z
#runtime/perl-522@5.22.0,5.11-2015.0.1.0:20151027T072513Z
#runtime/perl-522@5.22.0,5.11-2015.0.2.1:20151102T181230Z

##TODO## monitor closely when OIHipster changes chipped perl-versions or adds perl-modules
#ignore older perl-516@5.16.3,5.11-2014.1.2.3:20151027T072451Z
#use runtime/perl-522@5.22.0,5.11-2015.0.1.0:20150727T054604Z
#set perl5 for OIHipster
%if %( expr %{oihipster} '>=' 1 '&' %{osdistro_entire_padded_number4}.0 '>=' 2015000000010001000000000000.0 )
#paths changed to
%define perl_version 5.22
%define perl_major_minor_version 5.22
##TODO## determine correct version %define perl_major_minor_micro_version 5.16.x
%define perl_major_minor_micro_version 5.22.0
#runtime/perl-522
%define pnm_buildrequires_perl_default runtime/perl-522
%define pnm_requires_perl_default	runtime/perl-522
%endif
#END oihipster

#set perl5 for OmniOS
%if %{omnios}
##TODO## monitor closely when OmniOS changes chipped perl-versions or adds perl-modules
#set perl5 for OmniOS
%define perl_version 5.16
%define perl_major_minor_version 5.16
##TODO## determine correct version %define perl_major_minor_micro_version 5.16.x
%define perl_major_minor_micro_version 5.16.1
#runtime/perl-64
%define pnm_buildrequires_perl_default runtime/perl-64
%define pnm_requires_perl_default	runtime/perl-64
%endif
#END omnios


#add more distro here

#END setting perl5, changes with specific builds and distros  - Part 2 of 3


#START setting perl5, all builds, evaluated paths  - Part 3 of 3
# this is the section noted above which evaluates the resulting paths on the
# disk for the defaults for perl or the distro specific changed values e.g.
# more fresh perl version 5.8.4 -> 5.12 

#vendor_perl
# echo %{_prefix}/%{perl_path_vendor_perl}         -> prints /usr/perl5/vendor_perl
%define perl_path_vendor_perl perl%{perl_major_version}/vendor_perl

# echo %{_prefix}/%{perl_path_vendor_perl_version} -> prints /usr/perl5/vendor_perl/5.8.4 (or 5.10.0)
%define perl_path_vendor_perl_version perl%{perl_major_version}/vendor_perl/%{perl_version}


#site_perl
# echo %{_prefix}/%{perl_path_site_perl}           -> prints /usr/perl5/site_perl
%define perl_path_site_perl perl%{perl_major_version}/site_perl

# echo %{_prefix}/%{perl_path_site_perl_version}   -> prints /usr/perl5/site_perl/5.8.4 (or 5.10.0)
%define perl_path_site_perl_version perl%{perl_major_version}/site_perl/%{perl_version}

%if %{omnios}
#Exception! OmniOS uses different directory 5.16 -> 5.16.1
#overwrite the above settings now
#e.g. /usr/perl5/5.16.1/bin/perl         # that is also weird. others would use /usr/perl5/5.16/bin/perl
#example: /usr/perl5/vendor_perl/5.16.1
#example: /usr/perl5/5.16.1
%define perl_version %{perl_major_minor_micro_version}
%define perl_path_vendor_perl_version perl%{perl_major_version}/vendor_perl/%{perl_major_minor_micro_version}
%define perl_path_site_perl_version perl%{perl_major_version}/site_perl/%{perl_major_minor_micro_version}
%endif

%if %{?perl_dir:1}%{!?perl_dir:0}
#skip this, the perl_dir variable is already defined
%else

%ifarch sparc
%define perl_dir sun4-solaris-64int

%else
%define perl_dir i86pc-solaris-64int 

%if %{omnios}
%define perl_dir i86pc-solaris-thread-multi-64
%endif 
#END omnios

%if %( expr %{solaris12} '>=' 1 '&' %{osbuild} '>=' 95 )
%define perl_dir i86pc-solaris-thread-multi-64
%endif
#END solaris 12 osbuild >= 95

%endif
#END sparc else i86pc

%endif
#END ?perl_dir

#find include files if you compile against perl
#the EXTERN.h file would be found with CFLAGS="-I%{_prefix}/%{perl_default_includedir}"
#next line help to find /usr/perl5/5.8.4/lib/i86pc-solaris-64int/CORE/EXTERN.h
%define perl_default_includedir	perl%{perl_major_version}/%{perl_version}/lib/%{perl_dir}/CORE

#END setting perl5, all builds, evaluated paths  - Part 3 of 3

#various perl modules got bundles in perl versions later then 5.8.x
#so identify them here and let spec files use the pnm_macros to
#decide for a SFE package or use the osdistro bundled one
#START various perl modules now bundled
#define the defaults, then below overwrite if something has changed
%define pnm_buildrequires_SFEperl_extutils_cbuilder	SFEperl-extutils-cbuilder
%define pnm_requires_SFEperl_extutils_cbuilder		SFEperl-extutils-cbuilder

#most modules now bundled in the osdistro provided perl version:
%if %( expr %{perl_major_minor_version} '>=' 5.10 )
%define pnm_buildrequires_SFEperl_extutils_cbuilder	%{pnm_buildrequires_perl_default}
%define pnm_requires_SFEperl_extutils_cbuilder		%{pnm_requires_perl_default}
%endif perl_major_minor_version '>=' 5.10
#END various perl modules now bundled

#START setting Python, defaults  - Part 1 of 2
#define Python defaults, primarily shared settings and default versions and paths
#NOTE: we start initially only with setting Python 2.6 for *ALL* osbuild / osdistro
#this is to be extended in the future as required (for older osbuild/osdistro, *or* 
#for next Python 2.x or 3.x)

%define python_version 2.6
%define python_major_version 2
%define python_major_minor_version 2.6
%define python_major_minor_micro_version 2.6.4
#
#draft: NOTE: names/values subject to change - update all spec files 
#             accordingly if you change this!
#special strings here for packagenames: e.g. Python26
%define python_version_package_string 26

#note: the name is subject to change if we find a better one
#_default string is not meant to be a part of the package name...
%define pnm_buildrequires_python_default	SUNWPython26-devel,SUNWPython26
%define pnm_requires_python_default	SUNWPython26

# add sub-packagenames like "SUNWPython26-extra" and "-cherrypy" to the end, see examples:
#  BuildRequires:	%{pnm_buildrequires_python_default}-extra 
#  Requires:		%{pnm_requires_python_default}-extra 
#  BuildRequires:	%{pnm_buildrequires_python_default}-cherrypy
#  Requires:		%{pnm_requires_python_default}-cherrypy

#BIG NOTE read the "perl" examples in this file *IF* you want to 
#extend the logic to define a new osbuild/osdistro or switch to
#another Python version, e.g. 2.7 or 3.0 only for specific osbuild/osdistro
#combinations.
#Mind to write the same comments as for the perl section "Part n of m" to 
#highlight that a value may be re-defined later on for special cases
#END setting Python - Part 1 of 2

#START setting python, changes with specific builds and distros  - Part 2 of 2
# on S12 we don't have legacy package name SUNWPython26, so we need to
# use runtime/python-26 instead ##TODO## testing for OI151a8 as well
#before Solaris 12.0.0.0.86.0
%if %( expr %{osbuild} '>=' 133        '|' %{solaris12} '>=' 1 )
#note: the name is subject to change if we find a better one
#_default string is not meant to be a part of the package name...
%define pnm_buildrequires_python_default	runtime/python-26
%define pnm_requires_python_default		runtime/python-26
%endif
#END %{osbulild} => 133 or %{solaris12}


#Solaris >= 175.3.0.0.26.0
%if %( expr %{solaris11} '>=' 1 '&' %{osdistro_entire_padded_number4}.0 '>=' 0000017500030000000000260000.0 )
#note: the name is subject to change if we find a better one
#_default string is not meant to be a part of the package name...
%define python_version 2.7
%define python_major_version 2
%define python_major_minor_version 2.7
%define python_major_minor_micro_version 2.7.9
%define python_version_package_string 27
%define pnm_buildrequires_python_default	runtime/python-27
%define pnm_requires_python_default		runtime/python-27
%endif
#END %{solaris11} >= 11.3


#Solaris >= 175.3.0.0.30.0
%if %( expr %{solaris11} '>=' 1 '&' %{osdistro_entire_padded_number4}.0 '>=' 0000017500030000000000300000.0 )
#the IPS name changed from python-2/ to python/
##TODO##1 check if consuming specs can concentrate on only these pnm_macros below and not older/other variant
##TODO##2 prepare for new default python version on S11.3 build 26 and S12 b70
%define pnm_buildrequires_SUNWpython26_setuptools_devel	library/python/setuptools-26
%define pnm_buildrequires_SUNWpython26_setuptools	library/python/setuptools-26
%define pnm_requires_SUNWpython26_setuptools		library/python/setuptools-26
%define pnm_requires_library_python_setuptools_26	library/python/setuptools-26
%define pnm_buildrequires_library_python_setuptools_26	library/python/setuptools-26
%define pnm_requires_library_python_setuptools_26	library/python/setuptools-26
#there has been no SUNWpython27
%define pnm_requires_library_python_setuptools_27	library/python/setuptools-27
%define pnm_buildrequires_library_python_setuptools_27	library/python/setuptools-27
%define pnm_requires_library_python_setuptools_27	library/python/setuptools-27
%endif
#END %{solaris11} >= 11.3

#Solaris >= 12.0.0.0.70.0
%if %( expr %{solaris12} '>=' 1 '&' %{osdistro_entire_padded_number4}.0 '>=' 0005001200000000000000700000.0 )
#the IPS name changed from python-2/ to python/
##TODO##1 check if consuming specs can concentrate on only these pnm_macros below and not older/other variant
##TODO##2 prepare for new default python version on S11.3 build 26 and S12 b70
%define pnm_buildrequires_SUNWpython26_setuptools_devel	library/python/setuptools-26
%define pnm_buildrequires_SUNWpython26_setuptools	library/python/setuptools-26
%define pnm_requires_SUNWpython26_setuptools		library/python/setuptools-26
%define pnm_requires_library_python_setuptools_26	library/python/setuptools-26
%define pnm_buildrequires_library_python_setuptools_26	library/python/setuptools-26
%define pnm_requires_library_python_setuptools_26	library/python/setuptools-26
#there has been no SUNWpython27
%define pnm_requires_library_python_setuptools_27	library/python/setuptools-27
%define pnm_buildrequires_library_python_setuptools_27	library/python/setuptools-27
%define pnm_requires_library_python_setuptools_27	library/python/setuptools-27
%endif
#END %{solaris12} >= build 86


#Solaris >= 12.0.0.0.86.0
%if %( expr %{solaris12} '>=' 1 '&' %{osdistro_entire_padded_number4}.0 '>=' 0005001200000000000000860000.0 )
#note: the name is subject to change if we find a better one
#_default string is not meant to be a part of the package name...
%define python_version 2.7
%define python_major_version 2
%define python_major_minor_version 2.7
%define python_major_minor_micro_version 2.7.10
%define python_version_package_string 27
%define pnm_buildrequires_python_default	runtime/python-27
%define pnm_requires_python_default		runtime/python-27
%endif
#END %{solaris12} >= build 86

# additionaly, in OmniOS we have a different python micro version number:
%if %{omnios}
%define python_major_minor_micro_version 2.6.8
%endif
#END %{omnios}

# additionaly, in OIHpster we have a different python micro version number:
%if %{oihipster}
%define python_major_minor_micro_version 2.6.9
%endif
#END %{oihipster}

#pkg://openindiana.org/runtime/python-24@2.4.6-2015.0.2.0:20161003T120954Z    --o
#pkg://openindiana.org/runtime/python-25@2.5.4-2015.0.2.0:20161003T120954Z    --o
#pkg://openindiana.org/runtime/python-26@2.6.9-2016.0.1.0:20161003T120954Z    --o
#pkg://openindiana.org/runtime/python-26/tests@2.6.9-2016.0.1.0:20161003T120955Z --o
#pkg://openindiana.org/runtime/python-27@2.7.12-2016.0.1.2:20161003T102116Z   ---
#pkg://openindiana.org/runtime/python-27/tests@2.7.12-2016.0.1.2:20161003T102049Z ---
#pkg://openindiana.org/runtime/python-34@3.4.5-2016.0.1.1:20160916T143119Z    ---

# lets start (randomly) with python-27 as default in OIHpster >= 2015.0.1.1
%if %( expr %{oihipster} '>=' 1 '&' %{osdistro_entire_padded_number4}.0 '>=' 2015000000010001000000000000.0 )
#python-27@2.7.10-2015.0.1.0:20150603T172529Z
%define python_version 2.7
%define python_major_version 2
%define python_major_minor_version 2.7
%define python_major_minor_micro_version 2.7.10
%define python_version_package_string 27
%define pnm_buildrequires_python_default	runtime/python-27
%define pnm_requires_python_default		runtime/python-27
%endif
#END %{oihipster} >= 2015.0.1.1


#END setting python, changes with specific builds and distros  - Part 2 of 2

# note: some python package names may change with the default python version
#       therefore place those below the main python settings
#which build number removed SUNWpysqlite and used the python 2.6/2.7 internal pysqlite?
#if python is version 2.4, then we need SUNWpysqlite
##TODO## adjust the osbuild number which introduced Python2.6
%if %( expr %{osbuild} '>=' 133        '|' %{solaris12} '>=' 1 )
#all more recent builds should just require the current python default version of this platform
#instead of the SUNWpysqlite
%define pnm_buildrequires_SUNWpysqlite_devel 	%{pnm_buildrequires_python_default}
%define pnm_buildrequires_SUNWpysqlite 		%{pnm_buildrequires_python_default}
%define pnm_requires_SUNWpysqlite 		%{pnm_requires_python_default}
%define pnm_buildrequires_pysqlite 		%{pnm_buildrequires_python_default}
%define pnm_requires_pysqlite 			%{pnm_requires_python_default}
#
%else
#we are < 133
#note, we have in real world no -devel - macro only for convenience
%define pnm_buildrequires_SUNWpysqlite_devel 	SUNWpysqlite-devel
%define pnm_buildrequires_SUNWpysqlite 		SUNWpysqlite
%define pnm_requires_SUNWpysqlite 		SUNWpysqlite
%define pnm_buildrequires_pysqlite 		SUNWpysqlite-devel
%define pnm_requires_pysqlite 			SUNWpysqlite
%endif
#END < 133  (else)
#END if osbuild >= 133


#build numbers or other milestones are important to switch python versions at the right time
##TODO## should create "renamed-to" packages to uninstall our SFEpython26-importlib at the exact version when OSdistro's package appears
##      
#solaris12 has default python27 and knows library/python/importlib      - Yes for >= build 86 library/python/importlib
#          Note: python-26 removed/obsoleted, so we ignore old development build 86 in rules below

#solaris11 has default python26 and  *no* library/python*/importlib*    - Not present for 0.175.0.0.0.0.0 we need SFEpython26-importlib
#solaris11 has default python26 and knows library/python-2/importlib-26 - Yes for >= 0.175.2.0.0.42.1 there is OSdistro library/python-2/importlib-26
#solaris11 has default python26 and knows library/python/importlib      - Yes for >= 0.175.3.0.0.16.0 there is OSdistro library/python/importlib

##TODO## define s11 version first delivering importlib for/bundled with python27 ---- verify this

#OIHipster 2015xxxx has default python27 and knows library/python/importlib. verify this 
#OIHipster 20160421 has default python27 and knows library/python/importlib. Verified
#OI151a9 has default python26, which requires backported importlib, so requires SFEpython26-importlib
#r1510016 .. r1510018 and so on - check on public IPS publisher
#Omnios  has default python26, which requires backported importlib, so requires SFEpython26-importlib - TBC
#

# pkg list -avf "*/importlib*"

#s11 0.175.3.0.0.16.0 has a renamed package
#library/python-2/importlib-26                     1.0.2-0.175.3.0.0.16.0     --r
#s11 0.175.3.0.0.24.0 has python 2.7
#library/python/importlib                          1.0.2-0.175.3.0.0.24.0     ---

#pkg://solaris/library/python-2/importlib@1.0.2,5.11-0.175.2.0.0.42.1:20140623T014749Z ---
#pkg://solaris/library/python-2/importlib@1.0.2,5.11-0.175.2.6.0.3.0:20141222T165018Z ---
#pkg://solaris/library/python-2/importlib@1.0.2,5.11-0.175.3.0.0.16.0:20150215T210033Z --r
#pkg://solaris/library/python-2/importlib-26@1.0.2,5.11-0.175.2.0.0.42.1:20140623T014748Z ---
#pkg://solaris/library/python-2/importlib-26@1.0.2,5.11-0.175.2.6.0.3.0:20141222T165017Z ---
#pkg://solaris/library/python-2/importlib-26@1.0.2,5.11-0.175.3.0.0.16.0:20150215T210032Z --r
#pkg://solaris/library/python/importlib@1.0.2,5.11-0.175.3.0.0.30.0:20150821T170100Z i--
#pkg://solaris/library/python/importlib-26@1.0.2,5.11-0.175.3.0.0.30.0:20150821T170059Z i--

#pkg://localhostoih/library/python-2/importlib-27@1.0.3-0.0.151.1.8:20160215T002015Z i--
#pkg://localhostoih/library/python-2/importlib-27@1.0.3-0.0.151.1.8:20150810T214611Z ---
#pkg://localhostoih/library/python-2/importlib-27/src@1.0.3-0.0.151.1.8:20160215T001935Z ---
#pkg://localhostoih/library/python-2/importlib-27/src@1.0.3-0.0.151.1.8:20150810T214531Z ---


#remember: SFEpython26-importlib needs to get "renamed-to" section installing exactly at the OSdistro release where the
#OSdistro default python version changes (the case for S11 >= 0.175.3.0.0.16.0)

#for very modern OSdistro we set the default to be the python-27 and newer package, as it bundled importlib
#t and update later, in case an OSdistro is known to have its own package for importlib
#assuming here: python-27 and newer has importlib integrated
%define pnm_buildrequires_library_python_importlib	%{pnm_requires_python_default}
%define pnm_requires_library_python_importlib		%{pnm_requires_python_default}


#solaris12 we use this/and newer python as default
#runtime/python-27@2.7.10-5.12.0.0.0.88.0

#solaris11 added */importlib-26 on 0.175.2.0.0.42.1
#solaris11 renamed to */importlib on 0.175.3.0.0.16.0
#solaris11 changed to default python-27 (importlib included)

#Hipster is set in SFE to default_python being python-27 (or newer) (importlib included)

#OI151 has python-26 and needs SFEpython26-importlib

#now the special cases:
#Extend if necessary! Start with old OSdistro.
#Leave modern OSdistro releases with python-27 and up to the default which we define right before)

#below: very old Solaris 11 releases and have python26 and *no* importlib, we use SFEpython26-importlib
%if %( expr %{solaris11} '=' 1 '&' %{osdistro_entire_padded_number4}.0 '<' 0000017500020000000000420001.0 )
#   x < 0000017500020000000000420001.0
#now one exception, if solaris11 is very very old, then we have nothing and need to use SFEpython26-importlib
%define pnm_buildrequires_library_python_importlib	SFEpython26-importlib
%define pnm_requires_library_python_importlib		SFEpython26-importlib
%endif

#below: old S11 release has python26 and importlib-26 is available, but uses the old name importlib-26
%if %( expr %{solaris11} '=' 1 '&' %{osdistro_entire_padded_number4}.0 '<' 0000017500030000000000160000.0 )
#   x >= 0000017500020000000000420001.0 and x < 0000017500030000000000160000.0
#now one exception, if solaris11 is very old, then use the old name of the package with python-2 and "importlib-26":
%define pnm_buildrequires_library_python_importlib	library/python-2/importlib-26
%define pnm_requires_library_python_importlib		library/python-2/importlib-26
%endif

#OI151 has python 2.6 and needs SFEpython26-importlib       #%if %( expr %{openindiana} '=' 1 '&' %{oihipster} '=' 0 )
%if %( expr %{openindiana} '=' 1 '|' %{oihipster} '>=' 1 '&' %{osdistro_entire_padded_number4}.0 '<' 2015000000010001000000000000.0 )
%define pnm_buildrequires_library_python_importlib	SFEpython26-importlib
%define pnm_requires_library_python_importlib		SFEpython26-importlib
%endif

#OmniOS
#entire@11-0.151016 -> runtime/python-26@2.6.8-0.151016
##TODO## which will be the python default for 151018 for instance?
%if %( expr %{omnios} '=' 1 '&' %{osdistrelnumber} '<=' 151016 )
%define pnm_buildrequires_library_python_importlib	SFEpython26-importlib
%define pnm_requires_library_python_importlib		SFEpython26-importlib
%endif


#START setting mysql, defaults  - Part 1 of 3
#define mysql defaults, primarily shared settings and default version, paths
#for older osbuilds/osdistros like OpenSolaris 134, SXCE/Nevada, Solaris 10
#STRONG NOTE: located *below* the osdistro and osbuild sections, there is *another*
#section evaluating the resulting paths on the disk, those are specific
#to the mysql version in use. We hope, that we do not need to handle special
#cases there, e.g. this would be an odd distro deciding to relocate to 
#another path layout on disk....
##TODO## Solaris 10's mysql versions *not yet* covered here

#from SXCE on we have this:
%define mysql_version 5.1
%define mysql_major_version 5
%define mysql_major_minor_version 5.1
##not defined %define mysql_major_minor_micro_version 5.1.X

#we simplify the variants for mysql, we try to use only the newer one
#for *all* consuming spec files.
#include file /usr/mysql/5.1/include/mysql/mysql.h is in SUNWmysql51u
%define pnm_buildrequires_mysql_default	SUNWmysql51u
%define pnm_requires_mysql_default	SUNWmysql51u

#END setting mysql, defaults  - Part 1 of 3

#START setting mysql, changes with specific builds and distros  - Part 2 of 3
#set mysql for Solaris11Express or OpenIndiana or OpenSolaris
%if %{os2nnn}
#older IPS systems
%define pnm_buildrequires_mysql_default	SUNWmysql51
%define pnm_requires_mysql_default	SUNWmysql51
%if %( expr %{osbuild} '>=' 133        '|' %{solaris12} '>=' 1 )
#from build 133 and up we have
#database/mysql-51
#database/mysql-51                                 5.1.37-5.12.0.0.0.45.0     --o
#database/mysql-51/library                         5.1.37-5.12.0.0.0.45.0     --o
%define pnm_buildrequires_mysql_default	database/mysql-51,database/mysql-51/library
%define pnm_requires_mysql_default	database/mysql-51,database/mysql-51/library
%endif
#END >= 133
%if %( expr %{solaris12} '>=' 1 '&' %{osbuild} '>=' 63 )
%define mysql_version 5.5
%define mysql_major_version 5
%define mysql_major_minor_version 5.5
##not defined %define mysql_major_minor_micro_version 5.1.X
#database/mysql-55                                 5.5.31-5.12.0.0.0.63.0     ---
#database/mysql-55/client                          5.5.31-5.12.0.0.0.63.0     ---
#database/mysql-55/library                         5.5.31-5.12.0.0.0.63.0     i--
%define pnm_buildrequires_mysql_default	database/mysql-55,database/mysql-55/library
%define pnm_requires_mysql_default	database/mysql-55,database/mysql-55/library
%endif
#END S12 & >= 63
%endif
#END os2nnn

#add more distro here
##TODO## # OIHipster moved to Mariadb, mysql 5.1 still available

#END setting mysql, changes with specific builds and distros  - Part 2 of 3

##TODO## below. different versions of Sun/Oracle built mysql had an extra
#directory at the end:  include/mysql and lib/mysql  with newer versions > 5.1
#that is e.g. 5.5 the part /mysql is gone.
#introduce a switch or make the /mysql part of the defines depending on the
#version mysql is
# #
#  pkg contents -r -m database/mysql-51/library database/mysql-51 database/mysql-55/library database/mysql-55  | egrep "my_dir.h|libmysqlclient.so"; pkg contents -r -m database/mysql-55 | egrep "my_dir.h|libmysqlclient.so " | grep -v variant 
# 
# file 9370a8a70c0ced5fcbb2de964bd386d9c0065055 chash=7181a4411e66f4e19ea53ce939f1c26117647aa1 facet.devel=all group=bin mode=0444 owner=root path=usr/mysql/5.1/include/mysql/my_dir.h pkg.csize=1501 pkg.size=3460
# file 2cc545f744e3249d85ad5a7834f65539ba7420a7 chash=ffe9b08f69d43941d6bf26f4a3feb4a578255aee facet.devel=all group=bin mode=0444 owner=root path=usr/mysql/5.5/include/my_dir.h pkg.csize=1548 pkg.size=3573
# 
# link path=usr/mysql/5.1/lib/mysql/libmysqlclient.so target=libmysqlclient.so.16
# link path=usr/mysql/5.5/lib/libmysqlclient.so target=libmysqlclient.so.18
# 
# remember to adjust SFEqt-gpp.spec once the /mysql offset is re-engineered here



#START setting mysql, all builds, evaluated paths  - Part 3 of 3
# this is the section noted above which evaluates the resulting paths on the
# disk for the defaults for mysql or the distro specific changed values e.g.
# if a more fresh mysql version stores files somewehre else

#set handy partial paths to default locations where important mysql files
#are stored
#note: simplyfication: %{_prefix} must be prepended by the spec file itself

#default install directory of mysql
%define mysql_default_prefix	mysql/%{mysql_major_minor_version}

#example:
#the mysql.h file would be found with CFLAGS="-I%{_prefix}/%{mysql_default_includedir}/mysql"
#or
#the mysql.h file would be found with CFLAGS="-I%{_prefix}/%{mysql_default_includedir}"
%define mysql_default_includedir	mysql/%{mysql_major_minor_version}/include
#more information: #include "mysql/mysql.h" -->> /usr/mysql/5.1/include/mysql/mysql.h 
#if you only #include "mysql.h" then you need to use CFLAGS="-I%{_prefix}/%{mysql_default_includedir}/mysql"

#the mysql libs would be found with LDFLAGS and/or CFLAGS="-L%{_prefix}/%{mysql_default_libdir} -R%{_prefix}/%{mysql_default_libdir}"
%define mysql_default_libdir	mysql/%{mysql_major_minor_version}/lib
#you might need to keep an eye on 32-/64-bit locations of mysql libs
#you might need to use -L%{_prefix}/%{mysql_default_libdir}/mysql to get libraries found

#END setting mysql, all builds, evaluated paths  - Part 3 of 3



#START setting java, defaults  - Part 1 of 3
#define java defaults, primarily shared settings and default version, paths
#for older osbuilds/osdistros like OpenSolaris 134, SXCE/Nevada, Solaris 10
#STRONG NOTE: locate *below* the osdistro and osbuild sections, there is *another*
#section evaluating the resulting paths on the disk, those are specific
#to the java version in use. We hope, that we do not need to handle special
#cases there, e.g. this would be an odd distro deciding to relocate to 
#another path layout on disk....
##TODO## Solaris 10's java versions *not yet* complete here

#from SXCE on we have this:
%define java_version 1.6.0_17
%define java_major_version 1
%define java_major_minor_version 1.6
##not defined %define java_major_minor_micro_version 1.6.0_17
#JAVA
%define pnm_buildrequires_java_runtime_default		SUNWj6rt
%define pnm_requires_java_runtime_default		SUNWj6rt
#in case 32 bit is good enough
%define pnm_buildrequires_java_runtime_default_32	SUNWj6rt
%define pnm_requires_java_runtime_default_32		SUNWj6rt
#in case 64 bit is really needed or makes sense
%define pnm_buildrequires_java_runtime_default_64	SUNWj6rtx
%define pnm_requires_java_runtime_default_64		SUNWj6rtx

#END setting java, defaults  - Part 1 of 3

#START setting java, changes with specific builds and distros  - Part 2 of 3
#set java for Solaris11(Express) or OpenIndiana or OpenSolaris
%if %{os2nnn}
#older IPS systems
#use the default from before (e.g. SUNWj6rt and SUNWj6rtx
%if %( expr %{osbuild} '>=' 133        '|' %{solaris12} '>=' 1 )
#from build 133 and up we have
#runtime/java and runtime/java/runtime64
%define pnm_buildrequires_java_runtime_default		runtime/java
%define pnm_requires_java_runtime_default		runtime/java
#in case 32 bit is good enough
%define pnm_buildrequires_java_runtime_default_32	runtime/java
%define pnm_requires_java_runtime_default_32		runtime/java
#in case 64 bit is really needed or makes sense
%define pnm_buildrequires_java_runtime_default_64	runtime/java/runtime64
%define pnm_requires_java_runtime_default_64		runtime/java/runtime64

#experimental, subject to change, can be incomplete
#what about 32-bit and 64-bit? S12 jdk8 is 64-bit only
%define pnm_buildrequires_jdk_default			developer/java/jdk
%define pnm_requires_jdk_default			developer/java/jdk
%define pnm_buildrequires_jdk_7_default			developer/java/jdk-7
%define pnm_requires_jdk_7_default			developer/java/jdk-7
%define pnm_buildrequires_jdk_8_default			developer/java/jdk-8
%define pnm_requires_jdk_8_default			developer/java/jdk-8

%endif
#END >= 133
%endif
#END os2nnn

%if %{oihipster}
#experimental, subject to change, can be incomplete
#what about 32-bit and 64-bit? S12 jdk8 is 64-bit only
#oihipster: not mediated
%define pnm_buildrequires_jdk_default			developer/java/openjdk7
%define pnm_requires_jdk_default			developer/java/openjdk7
#%define pnm_buildrequires_jdk_7_default			developer/java/jdk-7
#%define pnm_requires_jdk_7_default			developer/java/jdk-7
#%define pnm_buildrequires_jdk_8_default			developer/java/jdk-8
#%define pnm_requires_jdk_8_default			developer/java/jdk-8
%endif
#END oihipster

#END setting java, changes with specific builds and distros  - Part 2 of 3
# oihipster going through huge changes with java ATM (circa mid 2015)
# Defaults will propably suffice

#START setting java, all builds, evaluated paths  - Part 3 of 3
# this is the section noted above which evaluates the resulting paths on the
# disk for the defaults for java or the distro specific changed values e.g.
# if a more fresh java version stores files somewehre else
# 
# intentionally left empty. maybe enhanced later with filesystempaths
##TODO## add content here to fill in JAVA_HOME
#
#
#END setting java, all builds, evaluated paths  - Part 3 of 3

#START setting ruby, defaults  - Part 1 of 3
#define ruby defaults, primarily shared settings and default version, paths
#for older osbuilds/osdistros like OpenSolaris 134, SXCE/Nevada, Solaris 10
#STRONG NOTE: located *below* the osdistro and osbuild sections, there is *another*
#section evaluating the resulting paths on the disk, those are specific
#to the ruby version in use. We hope, that we do not need to handle special
#cases there, e.g. this would be an odd distro deciding to relocate to 
#another path layout on disk....

%define ruby_version 1.8.7
%define ruby_major_version 1
%define ruby_major_minor_version 1.8
%define ruby_major_minor_micro_version 1.8.7

%define pnm_buildrequires_ruby_default	SUNWruby18u
%define pnm_requires_ruby_default	SUNWruby18u

##TODO## well, we *need* a better way to determine what
#sfe verison to use. Maybe putting ruby version number into
#include file and include that here for sfe_ruby_* and as well
#include that in SFEruby.spec - to keem them better in sync
#Exception! We have two ruby_defaul, we add a define for a ruby
#           version local to "SFE",
#currently all the same for all osdistro
#note1: different installation paths for SFE's ruby implementation,
#       the binaries go into /usr/gnu/<bin|*> .
#       See also: section Part 3 which defines variables with the
#       install path to ruby or sfe_ruby.
##TODO## think on how to replace the unpatched os ruby 1.8, see note2.
#note2: currently unused is SFEruby-18.spec which contains a
#       patched 1.8.7 to *replace* the OS provided SUNWruby/SUNWrubyu/SUNWrubyr

#here comes SFE's local ruby version stored in /usr/gnu:
#note the added _sfe_ in all variables including the variables-names
#pointing to the install-path
#       ....
%define sfe_ruby_version 1.9.3
%define sfe_ruby_major_version 1
%define sfe_ruby_major_minor_version 1.9
%define sfe_ruby_major_minor_micro_version 1.9.3

#                         ....
%define pnm_buildrequires_sfe_ruby_default	SFEruby
%define pnm_requires_sfe_ruby_default	SFEruby

# NOTE the section sitting below the distro specfic settings
# where the resulting paths on the disk are evaluated!

#END setting ruby, defaults  - Part 1 of 3



#START setting ruby, changes with specific builds and distros  - Part 2 of 3

#the distro specific settings below.
#set specifics for more fresh osbuild/osdistro like Solaris 11 Express, OpenIndiana
#which integrate ruby 5.10 or newer (please add more sections for overrides in 
#different distro releases. Order is: greatest osbuild must be listed last to
#override previous settings)

#set ruby for Solaris 12 - just a guess
#runtime/ruby-18@1.8.7
%if %{os2nnn}
%if %( expr  %{solaris12} '>=' 1 )
#set ruby for Solaris 12
%define ruby_version 1.8.7
%define ruby_major_minor_version 1.8
%define ruby_major_minor_micro_version 1.8.7
#runtime/ruby-18
%define pnm_buildrequires_ruby_default  runtime/ruby-18
%define pnm_requires_ruby_default	runtime/ruby-18
%endif
#END solaris12
%endif
#END os2nnn

#set ruby for Solaris 11
#pkg://runtime/ruby-18@1.8.7.334-0.175.0.0.0.2.537
%if %{os2nnn}
%if %( expr %{solaris11express} '>=' 1 )
#set ruby for Solaris 11, Solaris 11 Express
%define ruby_version 1.8.7
%define ruby_major_minor_version 1.8
%define ruby_major_minor_micro_version 1.8.7
#runtime/ruby-18 
%define pnm_buildrequires_ruby_default  runtime/ruby-18
%define pnm_requires_ruby_default       runtime/ruby-18
%endif
#END solaris11
%endif
#END os2nnn

#set ruby for OIHipster
%if %{oihipster}
##TODO## monitor closely when OIHipster starts shipping
#set ruby for OIHipster
%define ruby_version 1.9.3
%define ruby_major_minor_version 1.9
%define ruby_major_minor_micro_version 1.9.3
#runtime/ruby-18 
%define pnm_buildrequires_ruby_default  runtime/ruby-19
%define pnm_requires_ruby_default       runtime/ruby-19
%endif
#END oihipster

#set ruby for OpenIndiana
%if %{os2nnn}
%if %{openindiana}
##TODO## monitor closely when OpenIndiana starts shipping
%if %( expr %{osbuild} '>=' 151 )
#set ruby for OpenIndiana 
%define ruby_version 1.8.7
%define ruby_major_minor_version 1.8
%define ruby_major_minor_micro_version 1.8.7
#runtime/ruby-18 
%define pnm_buildrequires_ruby_default  runtime/ruby-18
%define pnm_requires_ruby_default       runtime/ruby-18
%endif
#END >= 151
%endif
#END openindiana
%endif
#END os2nnn

#add more distro here

#END setting ruby, changes with specific builds and distros  - Part 2 of 3


#START setting ruby, all builds, evaluated paths  - Part 3 of 3
# this is the section noted above which evaluates the resulting paths on the
# disk for the defaults for ruby or the distro specific changed values e.g.
# more fresh ruby version 

#currently none defined (examples see perl section)

#set handy partial paths to default locations where important ruby files
#are stored
#note: simplyfication: %{_prefix} must be prepended by the spec file itself
#note2: osdistro ruby is in /usr and sfe_ruby is in /usr/gnu

#default install directory of ruby.
##TODO## think if there is a smarter setting then the path hardcoded.
#        Not allowed to be influenced by a _prefix changed in the spec file
#        requiring this ruby implementation
%define     ruby_default_prefix	/usr
%define sfe_ruby_default_prefix	/usr/gnu

#example:
#note: in this implementation we include the version number
#note: in this implementation we as well set the _prefix part as
#      we always define explicitly that osdistro ruby lives in /usr
#                                              and sfe_ruby in /usr/gnu
#
#      e.g. /usr/ruby/1.8/lib/ruby/1.8/i386-solaris2.11/ruby.h  (osdistro)
#      e.g. /usr/gnu/include/ruby-1.9.3/ruby.h   (sfe)
#
#s11 (wrong) usr/lib/ruby/1.8/i386-solaris2.11/ruby.h           pkg://sfe/runtime/ruby-18@1.8.7.371-0.11.0
#s11 (wrong) usr/include/ruby-1.9.1/ruby.h                      pkg://runtime/ruby-19@1.9.3-0.11.0
#s11 (wrong) usr/include/ruby-1.9.1/ruby/ruby.h                 pkg://runtime/ruby-19@1.9.3-0.11.0
#s11 usr/ruby/1.8/lib/ruby/1.8/i386-solaris2.11/ruby.h  pkg://runtime/ruby-18@1.8.7.334-0.175.0.0.0.2.537
#s11 usr/ruby/1.8/lib/ruby/1.8/sparc-solaris2.11/ruby.h pkg://runtime/ruby-18@1.8.7.334-0.175.0.0.0.2.537

#the ruby.h file would be found with CFLAGS="-I{ruby_default_includedir}"
#the SFE's ruby.h file would be found with CFLAGS="-I{sfe_ruby_default_includedir}"
##TODO## need better detection for the ruby_arch (S10, S11, S12, OI, ...)
%ifarch sparc
%define __ruby_arch sparc-solaris2.11
%else
%define __ruby_arch i386-solaris2.11
%endif
%define     ruby_default_includedir	    %{ruby_default_prefix}/ruby/%{ruby_major_minor_version}/lib/ruby/%{ruby_major_minor_version}/%{__ruby_arch}
##
##TODO##
#after fixing sfe_ruby directory layout adjust the line below, should be similar to what ruby_default_includedir defines
%define sfe_ruby_default_includedir	%{sfe_ruby_default_prefix}/include/ruby-%{sfe_ruby_major_minor_micro_version}

#the ruby libs would be found with LDFLAGS and/or CFLAGS="-L%{ruby_default_libdir}     -R%{ruby_default_libdir}"
#                                  or                "-L%{sfe_ruby_default_libdir} -R%{sfe_ruby_default_libdir}"
#basename   link   usr/ruby/1.8/lib/libruby.so pkg://runtime/ruby-18@1.8.7.334-0.175.0.0.0.2.537
#basename   link   usr/gnu/lib/libruby.so          pkg://runtime/ruby-19@1.9.3-0.11.0
%define ruby_default_libdir	%{ruby_default_prefix}/ruby/%{ruby_major_minor_version}/lib
#after fixing sfe_ruby directory layout: %define sfe_ruby_default_libdir	%{sfe_ruby_default_prefix}/ruby/%{sfe_ruby_major_minor_version}/lib
#now with wrong sfe_ruby directory layout (SFEruby.spec version 1.9.3 svn rev =< 5117)
%define sfe_ruby_default_libdir	%{sfe_ruby_default_prefix}/ruby/%{sfe_ruby_major_minor_version}/lib

#you might need to keep an eye on 32-/64-bit locations of ruby libs if such appears

#END setting ruby, all builds, evaluated paths  - Part 3 of 3


#START setting apache2, defaults  - Part 1 of 3
#define apache2 defaults, primarily shared settings and default version, paths
#for older osbuilds/osdistros like OpenSolaris 134, SXCE/Nevada, Solaris 10
#STRONG NOTE: locate *below* the osdistro and osbuild sections, there is *another*
#section evaluating the resulting paths on the disk, those are specific
#to the apache2 version in use. We hope, that we do not need to handle special
#cases there, e.g. this would be an odd distro deciding to relocate to 
#another path layout on disk....
##TODO## Solaris 10's apache2 versions *not yet* complete here
#there was a mess with directories named /usr/apache2/ and later /usr/apache2/2.2/

#from SXCE on we have this:
#apache2 2.2
%define apache2_version 2.2
%define apache2_major_version 2
%define apache2_major_minor_version 2.2
##not defined %define apache2_major_minor_micro_version 2.2.X.X.X
%define apache2_version_package_string 22

%define pnm_buildrequires_apache2_default		%{pnm_buildrequires_SUNWapch22u}
%define pnm_requires_apache2_default			%{pnm_requires_SUNWapch22u}

#END setting apache2, defaults  - Part 1 of 3

#START setting apache2, changes with specific builds and distros  - Part 2 of 3
#set apache2 for Solaris11(Express) or OpenIndiana or OpenSolaris
%if %{os2nnn}
#older IPS systems
#use the default from before
%if %( expr %{osbuild} '>=' 133        '|' %{solaris12} '>=' 1 )
#from build 133 and up we have
#note: currently explicitly defined only for SXCE and for >=133
%define pnm_buildrequires_apache2_default		web/server/apache-%{apache2_version_package_string}
%define pnm_requires_apache2_default			web/server/apache-%{apache2_version_package_string}
#expect that to change soon, as apache2 2.4 is in preparation as additional
#version to apache2 2.2 (will dissapear with future OS versions)
%endif
#END >= 133
%endif
#END os2nnn
#END setting apache2, changes with specific builds and distros  - Part 2 of 3

#START setting apache2, all builds, evaluated paths  - Part 3 of 3
# this is the section noted above which evaluates the resulting paths on the
# disk for the defaults for apache2 or the distro specific changed values e.g.
# if a more fresh apache2 version stores files somewehre else

#set handy partial paths to default locations where important apache2 files
#are stored
#note: simplyfication: %{_prefix} must be prepended by the spec file itself

#include files for apache2
#CFLAGS="-I%{_prefix}/%{apache2_default_includedir}"
#more information: #include "libpq-fe.h" -->> /usr/apache2/2.2/include/libpq-fe.h 
#more information: #include "server/libpq.h" -->> /usr/apache2/2.2/include/server/libpq.h 
%define apache2_default_includedir	apache2/%{apache2_major_minor_version}/include


##TODO##
##NOTE## below: subject to change. want a more clever way to auto-set the variables
#        for distinguishing 32-bit or 64-bit builds. so the spec files can always use
#        the same variable to define the right library search path for current %_arch*...

#the apache2 libs would be found with 
#LDFLAGS and/or CFLAGS="-L%{_prefix}/%{apache2_default_libdir} -R%{_prefix}/%{apache2_default_libdir}"
#you might need to keep an eye on 32-/64-bit locations of apache2 libs
#NOTE: to get the 64-bit libs use  CFLAGS="-L%{_prefix}/%{apache2_default_libdir}/%{_arch64}"
#more information: /usr/apache2/2.2/lib /usr/apache2/2.2/lib/amd64 /usr/apache2/2.2/lib/sparcv9
#here go e.g. perl modules
%define apache2_default_libdir	apache2/%{apache2_major_minor_version}/lib
#here go the apache loadable modules!
%define apache2_default_libexecdir	apache2/%{apache2_major_minor_version}/libexec


#the magic apxs utility. NOTE: for 64-bit version use temporary, subject to change
#variable apache2_default_apxs_64

%define apache2_default_apxs	apache2/%{apache2_major_minor_version}/bin/apxs
##TODO## want more clever 32-bit / 64-bit handling!
##TODO## does it work at all? maybe _arch is getting evaluated too late!
#%define apache2_default_apxs_64	apache2/%{apache2_major_minor_version}/bin/%{_arch64}/apxs
#there is no nice workaround to get switched form 32- to 64-bits
%define apache2_default_apxs_64	apache2/%{apache2_major_minor_version}/bin/64/apxs

#END setting apache2, all builds, evaluated paths  - Part 3 of 3


# Apache apr utility
##TODO## upcoming osdistro may replace apr-13 wih apr-15
##TODO## if requested, add targets for older osdistro with e.g. SVR4 - for now we only resolve to new naming / IPS
#this is for all builds (below 151)
#cases >=151
%if %( expr %{osbuild} '>=' 151 '|' %{solaris12} '>=' 1 )
#library/apr-util-13@1.3.9,5.11-0.151.0.1:20101105T055007Z 	Install 	Manifest
#library/apr-util-13@1.3.9,5.11-0.151:20101027T143546Z 	Install 	Manifest
##TODO## re-visit the package names if the left hand side really existed in that naming
%define pnm_buildrequires_web_library_apache_apr_util_13			library/apr-util-13
%define pnm_requires_web_library_apache_apr_util_13				library/apr-util-13
%define pnm_buildrequires_library_apr_util_13					library/apr-util-13
%define pnm_requires_library_apr_util_13					library/apr-util-13
%define pnm_buildrequires_SUNWapu13_devel					library/apr-util-13
%define pnm_buildrequires_SUNWapu13						library/apr-util-13
%define pnm_requires_SUNWapu13							library/apr-util-13
%define pnm_buildrequires_apu13							library/apr-util-13
%define pnm_requires_apu13							library/apr-util-13
%define pnm_buildrequires_web_library_apache_apr_util_13_documentation		library/apr-util-13/documentation
%define pnm_buildrequires_library_apr_util_13_documentation			library/apr-util-13/documentation
#web/library/apache/apr-13                         1.3.9-0.134                --r
#web/library/apache/apr-13/documentation           1.3-0.134                  --r
#library/apr-13                                    1.3.9-0.175.0.0.0.0.0      i--
#library/apr-13/documentation                      1.3.9-0.175.0.0.0.0.0      ---
#library/apr-util-13/apr-ldap                      1.3.9-0.175.0.0.0.0.0      i--
#library/apr-util-13/dbd-mysql                     1.3.9-0.175.0.0.0.0.0      i--
#library/apr-util-13/dbd-pgsql                     1.3.9-0.146                --o
#library/apr-util-13/dbd-sqlite                    1.3.9-0.175.0.0.0.0.0      i--
#library/apr-util-13/documentation                 1.3.9-0.175.0.0.0.0.0      ---
%define pnm_buildrequires_web_library_apache_apr_13			library/apr-13
%define pnm_requires_web_library_apache_apr_13				library/apr-13
%define pnm_buildrequires_library_apr_13				library/apr-13
%define pnm_requires_library_apr_13					library/apr-13
%define pnm_buildrequires_SUNWapr13_devel				library/apr-13
%define pnm_buildrequires_SUNWapr13					library/apr-13
%define pnm_requires_SUNWapr13						library/apr-13
%define pnm_buildrequires_apr13						library/apr-13
%define pnm_requires_apr13						library/apr-13
%define pnm_buildrequires_web_library_apache_apr_13_documentation	library/apr-13/documentation
%define pnm_buildrequires_library_apr_13_documentation			library/apr-13/documentation
%endif
#END >= 151 | solaris12

#xxxxxxxxxxxxxxxx
#START setting apr, defaults  - Part 1 of 3
#define apr defaults, primarily shared settings and default version, paths

%define build_library_apr_renamed_to_osdistro_package      0
%define apr_version 1.3
%define apr_major_version 1
%define apr_major_minor_version 1.3
##not defined %define apr_major_minor_micro_version 1.3.X
%define apr_version_package_string 13

%define build_library_apr_util_renamed_to_osdistro_package 0
%define apr_util_version 1.3
%define apr_util_major_version 1
%define apr_util_major_minor_version 1.3
##not defined %define apr_util_major_minor_micro_version 1.3.X
%define apr_util_version_package_string 13

%define pnm_buildrequires_apr_default			%{pnm_buildrequires_library_apr_13}
%define pnm_requires_apr_default			%{pnm_buildrequires_library_apr_13}
%define pnm_buildrequires_apr_util_default		%{pnm_buildrequires_library_apr_util_13}
%define pnm_requires_apr_util_default			%{pnm_buildrequires_library_apr_util_13}

#END setting apr, defaults  - Part 1 of 3

#START setting apr, changes with specific builds and distros  - Part 2 of 3
#note: need to add ".0" to avoid integer too lage, use floating point instead
%if %( expr %{omnios} '|' %{openindiana} '|' %{oihipster} '|' %{solaris12} '=' 1 '&' %{osbuild} '>=' 63 '|' %{solaris11} '&' %{osdistro_entire_padded_number4}.0 '>=' 0000017500030000000000120001.0 )
#this is a special switch: Our SFE spec file will build a package using the same name as more recent distros do
%define build_library_apr_renamed_to_osdistro_package      1
%define apr_version 1.5
%define apr_major_version 1
%define apr_major_minor_version 1.5
##not defined %define apr_major_minor_micro_version 1.3.X

%define build_library_apr_util_renamed_to_osdistro_package 1
%define apr_version_package_string 15
%define apr_util_version 1.5
%define apr_util_major_version 1
%define apr_util_major_minor_version 1.5
##not defined %define apr_util_major_minor_micro_version 1.3.X
%define apr_util_version_package_string 15
%define pnm_buildrequires_apr_default		library/apr-15
%define pnm_requires_apr_default		library/apr-15
%define pnm_buildrequires_apr_util_default	library/apr-util-15
%define pnm_requires_apr_util_default		library/apr-util-15
#on S12 >= 63 and S11 >= entire .12. we need to make sure that apr apr-util comes from the osdistro repository
%if %( expr %{solaris12} '=' 1 '&' %{osbuild} '>=' 63 '|' %{solaris11} '&' %{osdistro_entire_padded_number4}.0 '>=' 0000017500030000000000120001.0 )
%define pnm_buildrequires_apr_default		pkg://solaris/library/apr-15
%define pnm_requires_apr_default		pkg://solaris/library/apr-15
%define pnm_buildrequires_apr_util_default	pkg://solaris/library/apr-util-15
%define pnm_requires_apr_util_default		pkg://solaris/library/apr-util-15
%endif
#END solaris12 >= 63 and solaris 11 >= entire .12.

#note below: openindiana, hipster and OmniOS: library/apr-15 comes from SFE, not the osdistro
%if %( expr %{omnios} '|' %{openindiana} '|' %{oihipster} )
#to make that clear and avoid confusion in IPS package names, just set the SVR4/spec-file-name here
%define pnm_buildrequires_apr_default		SFElibapr
%define pnm_requires_apr_default		SFElibapr
%define pnm_buildrequires_apr_util_default	SFEapr-util
%define pnm_requires_apr_util_default		SFEapr-util
%endif
#END omnios openindiana oihipster
%endif
#END setting apr, changes with specific builds and distros  - Part 2 of 3

#START setting apr, all builds, evaluated paths  - Part 3 of 3
# this is the section noted above which evaluates the resulting paths on the
# disk for the defaults for apr or the distro specific changed values e.g.
# if a more fresh apr version stores files somewehre else

#set handy partial paths to default locations where important apr files
#are stored
#note: simplyfication: %{_prefix} must be prepended by the spec file itself

#include files for apr
#CFLAGS="-I%{_prefix}/%{apr_default_includedir}"
#more information: #include "apr.h" -->> /usr/apr/1.5/include/apr.h
%define apr_default_includedir		apr/%{apr_major_minor_version}/include
%define apr_util_default_includedir	apr/%{apr_util_major_minor_version}/include
#experimental: (see the idea at %{gnu_inc} in base.inc
#-I/usr/apr/1.5/include
%define apr_default_inc			-I%{_prefix}/%{apr_default_includedir}
%define apr_util_default_inc		-I%{_prefix}/%{apr_util_default_includedir}


##TODO##
##NOTE## below: subject to change. want a more clever way to auto-set the variables
#        for distinguishing 32-bit or 64-bit builds. so the spec files can always use
#        the same variable to define the right library search path for current %_arch*...

#                   %{_basedir}/apr/1.5
#                          /usr/apr/1.5
%define apr_default_basedir		apr/%{apr_major_minor_version}
#                   %{_basedir}/apr-util/1.5
#                          /usr/apr-util/1.5
%define apr_util_default_basedir	apr-util/%{apr_util_major_minor_version}

#the apr libs would be found with 
#LDFLAGS and/or CFLAGS="-L%{_prefix}/%{apr_default_libdir} -R%{_prefix}/%{apr_default_libdir}"
#you might need to keep an eye on 32-/64-bit locations of apr libs
#NOTE: to get the 64-bit libs use  CFLAGS="-L%{_prefix}/%{apr_default_libdir}/%{_arch64}"
%define apr_default_libdir	apr/%{apr_major_minor_version}/lib
%define apr_util_default_libdir	apr-util/%{apr_util_major_minor_version}/lib
#experimental: (see the idea at %{gnu_lib_path} in base.inc
#this doesn't evaluate to the 64-bit lib directory unless apr_default_libdir gets prepared for 64-bit
%define apr_default_lib_path	-L%{_prefix}/%{apr_default_libdir} -R%{_prefix}/%{apr_default_libdir}
%define apr_util_default_lib_path	-L%{_prefix}/%{apr_util_default_libdir} -R%{_prefix}/%{apr_util_default_libdir}


%define apr_default_apr_1_config	apr/%{apr_major_minor_version}/bin/apr-1-config
##TODO## want more clever 32-bit / 64-bit handling!
##TODO## does it work at all? maybe _arch is getting evaluated too late!
#%define apr_default_apxs_64	apr/%{apr_major_minor_version}/bin/%{_arch64}/apxs
#there is no nice workaround to get switched form 32- to 64-bits
#experimental
%define apr_default_apr_1_config_64	apr/%{apr_major_minor_version}/bin/64/apr-1-config

#END setting apr, all builds, evaluated paths  - Part 3 of 3
#xxxxxxxxxxxxxxxx


#START setting postgres, defaults  - Part 1 of 3
#define postgres defaults, primarily shared settings and default version, paths
#for older osbuilds/osdistros like OpenSolaris 134, SXCE/Nevada, Solaris 10
#STRONG NOTE: located *below* the osdistro and osbuild sections, there is *another*
#section evaluating the resulting paths on the disk, those are specific
#to the postgres version in use. We hope, that we do not need to handle special
#cases there, e.g. this would be an odd distro deciding to relocate to 
#another path layout on disk....
##TODO## Solaris 10's postgres versions *not yet* covered here

##TODO## we might want to select the postgres versions maintained in SFE itself
##TODO## to cover the 9.x series. This would need a *LOCAL* overright on your
##TODO## system. Ideas on how to solve that are welcome! email me tom68@....

#from SXCE on we have this: (mind the execptions below!)
%define postgres_version 8.4
%define postgres_major_version 8
%define postgres_major_minor_version 8.4
##not defined %define postgres_major_minor_micro_version 8.4.X

#we simplify the variants for postgres, we try to use only the newer one
#for *all* consuming spec files. Please not that in the future  we might
#override on the local system with a much newer SFEpostgres version!
#include files:
#/usr/postgres/8.4/include/libpq-fe.h
#/usr/postgres/8.4/include/server/libpq/libpq.h
%define pnm_buildrequires_postgres_default	SUNWpostgr-84-devel
%define pnm_requires_postgres_default		SUNWpostgr-84-libs

#END setting postgres, defaults  - Part 1 of 3

#START setting postgres, changes with specific builds and distros  - Part 2 of 3
#set postgres for Solaris11Express or OpenIndiana or OpenSolaris
%if %{os2nnn}
#older IPS systems
%define pnm_buildrequires_postgres_default	SUNWpostgr-84-devel
%define pnm_requires_postgres_default		SUNWpostgr-84-libs
%if %( expr %{osbuild} '>=' 133        '|' %{solaris12} '>=' 1 )
#from build 133 and up we have
#database/postgres-51
%define pnm_buildrequires_postgres_default	database/postgres-84/developer
%define pnm_requires_postgres_default		database/postgres-84
%endif
#END >= 133
%endif
#END os2nnn


#for better readability repeat. This time special switch for Solaris build >= 147
%if %{os2nnn}
%if %( expr %{osbuild} '>=' 147        '|' %{solaris12} '>=' 1 )
#from build 147 and up we have postgres no longer in the Solaris repo
#database/postgres-91 - we default to the latest SFE postgres we know that is working fine

%define postgres_version 9.1
%define postgres_major_version 9
%define postgres_major_minor_version 9.1
##not defined %define postgres_major_minor_micro_version 9.1.X

%define pnm_buildrequires_postgres_default	database/postgres-91/developer
%define pnm_requires_postgres_default		database/postgres-91
%endif
#END >= 147
%endif

#Repeat for Hipster. This time special switch for hipster
# Needs more confirmation
%if %{oihipster}

%define postgres_version 9.6
%define postgres_major_version 9
%define postgres_major_minor_version 9.6
##not defined %define postgres_major_minor_micro_version 9.6.4

%define pnm_buildrequires_postgres_default	service/database/postgres-96
%define pnm_requires_postgres_default		service/database/postgres-96
%endif
#END oihipster


#add more distro here/below

#END setting postgres, changes with specific builds and distros  - Part 2 of 3

#START setting postgres, all builds, evaluated paths  - Part 3 of 3
# this is the section noted above which evaluates the resulting paths on the
# disk for the defaults for postgres or the distro specific changed values e.g.
# if a more fresh postgres version stores files somewehre else

#set handy partial paths to default locations where important postgres files
#are stored
#note: simplyfication: %{_prefix} must be prepended by the spec file itself

#default install directory of postgresql
%define postgres_default_prefix	postgres/%{postgres_major_minor_version}

#example:
#the libpq/libpg.h or libpq-fe.h file would be found with 
#CFLAGS="-I%{_prefix}/%{postgres_default_includedir}"
#more information: #include "libpq-fe.h" -->> /usr/postgres/8.4/include/libpq-fe.h 
#more information: #include "server/libpq.h" -->> /usr/postgres/8.4/include/server/libpq.h 
%define postgres_default_includedir	postgres/%{postgres_major_minor_version}/include

##TODO##
##NOTE## below: subject to change. want a more clever way to auto-set the variables
#        for distinguishing 32-bit or 64-bit builds. so the spec files can always use
#        the same variable to define the right library search path for current %_arch*...

#the postgres libs would be found with 
#LDFLAGS and/or CFLAGS="-L%{_prefix}/%{postgres_default_libdir} -R%{_prefix}/%{postgres_default_libdir}"
#you might need to keep an eye on 32-/64-bit locations of postgres libs
#NOTE: to get the 64-bit libs use  CFLAGS="-L%{_prefix}/%{postgres_default_libdir}/%{_arch64}"
#more information: /usr/postgres/8.4/lib /usr/postgres/8.4/lib/amd64 /usr/postgres/8.4/lib/sparcv9
%define postgres_default_libdir	postgres/%{postgres_major_minor_version}/lib

#pg_config to tell consuming programs how that postgresql version is configured
##TODO## want more clever 32-bit / 64-bit handling!
#there is no nice workaround to get switched form 32- to 64-bits
%define postgres_default_pg_config	postgres/%{postgres_major_minor_version}/bin/pg_config
%define postgres_default_pg_config_64	postgres/%{postgres_major_minor_version}/bin/64/pg_config

#END setting postgres, all builds, evaluated paths  - Part 3 of 3


##NOTE## we only resolve for boost and icu compiled with GCC/G++ for now, so there is
#        only a macro with _gpp_ in the name

##NOTE## SFEicu-gpp is kind of a piggyback here
#START setting boost and icu, defaults  - Part 1 of 3 START
#define boost and icu defaults, primarily shared settings and default version, paths
#STRONG NOTE: located *below* the osdistro and osbuild sections, there is *another*
#section evaluating the resulting paths on the disk, those are specific
#to the boost and icu version in use. We hope, that we do not need to handle special
#cases there, e.g. this would be an odd distro deciding to relocate to 
#another path layout on disk....

%define boost_gpp_version 1.58.0
%define boost_gpp_major_version 1
%define boost_gpp_major_minor_version 1.58
##not defined %define boost_gpp_major_minor_micro_version 1.58.0

%define icu_gpp_version 55.1
%define icu_gpp_major_version 55
%define icu_gpp_major_minor_version 55.1
##not defined %define icu_gpp_major_minor_micro_version 55.1

#on SVR4 SFEboost-gpp-devel ?
%define pnm_buildrequires_boost_gpp_default	SFEboost-gpp-devel
%define pnm_requires_boost_gpp_default		SFEboost-gpp

%define pnm_buildrequires_icu_gpp_default	SFEicu-gpp-devel
%define pnm_requires_icu_gpp_default		SFEicu-gpp

#END setting boost, and icu defaults  - Part 1 of 3 END

#START setting boost and icu, changes with specific builds and distros  - Part 2 of 3 START
#use our own SFEboost-gpp %if %{oihipster}
#use our own SFEboost-gpp #note, this section will be overwritten again in case ophipster is newer, see below
#for the moment, we use boost and icu supplied by OIHipster
#use our own SFEboost-gpp %define boost_gpp_version 1.55.0
#use our own SFEboost-gpp %define boost_gpp_major_version 1
#use our own SFEboost-gpp %define boost_gpp_major_minor_version 1.55
#use our own SFEboost-gpp ##not defined %define boost_gpp_major_minor_micro_version 1.55.0

#use our own SFEboost-gpp #this is osdistro provided, not from SFE!
#use our own SFEboost-gpp %define pnm_buildrequires_boost_gpp_default	system/library/g++/boost
#use our own SFEboost-gpp %define pnm_requires_boost_gpp_default		system/library/g++/boost
#use our own SFEboost-gpp %define pnm_buildrequires_boost_gpp_default	SFEboost-gpp
#use our own SFEboost-gpp %define pnm_requires_boost_gpp_default		SFEboost-gpp
#use our own SFEboost-gpp %endif
#use our own SFEboost-gpp #END oihipster

#http://pkg.openindiana.org/hipster-2015 as of 20150808
#system/library/boost@1.55.0,5.11-2014.1.3.1:20141212T044927Z 	Install 	Manifest
#system/library/boost@1.58.0,5.11-2015.0.1.3:20150623T013126Z 	Install 	Manifest
#system/library/boost@1.58.0,5.11-2015.0.1.3:20150715T072510Z 	Install 	Manifest
#system/library/boost@1.58.0,5.11-2015.0.1.3:20150715T074103Z 	Install 	Manifest
#system/library/g++/boost@1.55.0,5.11-2014.0.1.0:20150309T141137Z 	Install 	Manifest
#system/library/g++/boost@1.55.0,5.11-2014.0.1.0:20150529T113204Z 	Install 	Manifest
#system/library/g++/boost@1.55.0,5.11-2014.0.1.0:20150612T192514Z 	Install 	Manifest
#system/library/g++/boost@1.55.0,5.11-2014.0.1.0:20150727T195654Z 	Install 	Manifest
#system/library/g++/boost@1.55.0,5.11-2014.0.1.0:20150727T231744Z 	Install 	Manifest

##TODO## make the release detection more precise. e.g with osdistro_entire_padded_number4 >= 2015000000010003 aka 2015.0.1.3
%if %( expr %{oihipster} '&' %{oih20150330} )
#for the moment, we use boost and icu supplied by OIHipster
#this means, this is subject to change if it is e.g. more stable or better matching SFE versioning needs or compile options or ...
#please note, this osdistro boost and icu is not compiled with LINK_LIBGCC_SPEC from our SFEgcc compiler
#use our own SFEboost-gpp %define boost_gpp_version 1.58.0
#use our own SFEboost-gpp %define boost_gpp_major_version 1
#use our own SFEboost-gpp %define boost_gpp_major_minor_version 1.55
##not defined %define boost_gpp_major_minor_micro_version 1.58.0

#have no separate header package in OIH
#use our own SFEboost-gpp %define pnm_buildrequires_boost_gpp_default	system/library/boost
#use our own SFEboost-gpp %define pnm_requires_boost_gpp_default		system/library/boost
#use our own SFEboost-gpp %define pnm_buildrequires_boost_gpp_default	SFEboost-gpp
#use our own SFEboost-gpp %define pnm_requires_boost_gpp_default		SFEboost-gpp
%endif
#END oihipster >= 20150330
#END setting boost and icu, changes with specific builds and distros  - Part 2 of 3 END

#START setting boost and icu, all builds, evaluated paths  - Part 3 of 3
# this is the section noted above which evaluates the resulting paths on the
# disk for the defaults for boost and icu or the distro specific changed values e.g.
# if a more fresh boost and icu version stores files somewehre else

#set handy partial paths to default locations where important boost and icu files
#are stored
#note: simplyfication: %{_prefix} must be prepended by the spec file itself

#default install directory of boost and icu
%define boost_gpp_default_prefix	/usr/g++
%define icu_gpp_default_prefix	/usr/g++

#example:
#the libpq/libpg.h or libpq-fe.h file would be found with 
#CFLAGS="-I%{_prefix}/%{boost_gpp_default_includedir}"
#more information: #include "libpq-fe.h" -->> /usr/boost/8.4/include/libpq-fe.h 
#more information: #include "server/libpq.h" -->> /usr/boost/8.4/include/server/libpq.h 
%define boost_gpp_default_includedir	/usr/g++/include
%define icu_gpp_default_includedir	/usr/g++/include

##TODO##
##NOTE## below: subject to change. want a more clever way to auto-set the variables
#        for distinguishing 32-bit or 64-bit builds. so the spec files can always use
#        the same variable to define the right library search path for current %_arch*...

#the boost and icu libs would be found with 
#LDFLAGS and/or CFLAGS="-L%{_prefix}/%{boost_gpp_default_libdir} -R%{_prefix}/%{boost_gpp_default_libdir}"
#you might need to keep an eye on 32-/64-bit locations of boost libs
#NOTE: to get the 64-bit libs use  CFLAGS="-L%{_prefix}/%{boost_gpp_default_libdir}/%{_arch64}"
#more information: /usr/boost/8.4/lib /usr/boost/8.4/lib/amd64 /usr/boost/8.4/lib/sparcv9
%define boost_gpp_default_libdir	/usr/g++/lib
%define icu_gpp_default_libdir	/usr/g++/lib

#pg_config to tell consuming programs how that boost version is configured
##TODO## want more clever 32-bit / 64-bit handling!
#there is no nice workaround to get switched form 32- to 64-bits
##NOT_IMPLEMENTED## %define boost_gpp_default_pg_config	boost/%{boost_gpp_major_minor_version}/bin/pg_config
##NOT_IMPLEMENTED## %define boost_gpp_default_pg_config_64	boost/%{boost_gpp_major_minor_version}/bin/64/pg_config

#overwrite paths for special osdistro
%if %( expr %{oihipster} '&' %{oih20150330} )
#use our own SFEboost-gpp %define boost_gpp_default_prefix	/usr
#use our own SFEboost-gpp %define boost_gpp_default_includedir	/usr/include
#use our own SFEboost-gpp %define boost_gpp_default_libdir	/usr/lib
#use our own SFEicu-gpp %define icu_gpp_default_prefix	/usr
#use our own SFEicu-gpp %define icu_gpp_default_includedir	/usr/include
#use our own SFEicu-gpp %define icu_gpp_default_libdir	/usr/lib
%endif
#END oihipster >= 20150330

#END setting boost, all builds, evaluated paths  - Part 3 of 3

#add more distro here/below

##TODO## below: dumping place to collect examples to be integrated later

#  pkg contents -r -m system/header/header-audio
# set name=pkg.fmri value=pkg://solaris/system/header/header-audio@0.5.11,5.11-0.163:20110410T085804Z
# set name=variant.arch value=sparc value=i386
# set name=org.opensolaris.consolidation value=osnet
# set name=variant.opensolaris.zone value=global value=nonglobal
# set name=pkg.renamed value=true
# depend fmri=consolidation/osnet/osnet-incorporation type=require
# depend fmri=pkg:/system/header@0.5.11,5.11-0.163 type=require
 
#SUNWghostscript --- see SFEnasm.spec as example for osbuild dependent switches
#cut

#example #new os2nnn and starting with build 134
#example %if %{os2nnn}
#example %if %(expr %{osbuild} '>=' 134)
#example BuildRequires:		text/texinfo
#example BuildRequires:		print/filter/ghostscript
#example %endif
#example %endif
#example 
#example %if %{os2nnn}
#example %if %(expr %{osbuild} '>=' 100)
#example %if %(expr %{osbuild} '<' 134)
#example BuildRequires:       SUNWtexi
#example BuildRequires:       SUNWghostscript
#example %endif
#example %endif
#example %endif
#example 
#example %if %{os2nnn}
#example %if %(expr %{osbuild} '<' 100)
#example BuildRequires:       SUNWtexi
#example BuildRequires:       SUNWgscr
#example %endif
#example %endif
#example 
#example #SXCE
#example %if %SXCE
#example BuildRequires:       SUNWtexi
#example BuildRequires:       SUNWghostscriptr
#example BuildRequires:       SUNWghostscriptu
#example %endif
#example 


##TODO## SFEorc.spec - simpify ywith with pnm_macros
#example 
#example %if %{os2nnn}
#example %if %(expr %{osbuild} '>=' 134)
#example buildRequires: library/desktop/gtk2
#example BuildRequires: developer/documentation-tool/gtk-doc
#example BuildRequires: developer/gnome/gettext
#example BuildRequires: data/docbook
#example %endif
#example %endif
#example 
#example %if %{os2nnn}
#example %if %(expr %{osbuild} '>=' 116)
#example %if %(expr %{osbuild} '<' 134)
#example #library/desktop/gtk1
#example # >=75 <= 133
#example BuildRequires: SUNWGtk 
#example #developer/documentation-tool/gtk-doc
#example # >=116 <=133
#example BuildRequires: SUNWgtk-doc
#example #developer/gnome/gettext
#example BuildRequires: SUNWgnome-common-devel
#example #data/docbook
#example BuildRequires: SUNWgnome-xml
#example %endif
#example %endif
#example %endif
#example # note build versions in %{os2nnn} before 116 aren't covered
#example #SXCE
#example %if %SXCE
#example %if %(expr %{osbuild} '<=' 130)
#example BuildRequires: SUNWGtku
#example BuildRequires: SUNWGtkr
#example BuildRequires: SUNWgtk-doc
#example # BuildRequires: data/docbook
#example BuildRequires: SUNWgnome-xml-root
#example BuildRequires: SUNWgnome-xml-share
#example %endif
#example %endif
#example 
 
 
#place very special cases here, for instance in Solaris 10
##TODO## for a future version


#from: http://hg.opensolaris.cz/build-scripts/file/tip/build/finddeps.sh
#     26 depspacks=`echo ${depspacks} | sed 's/SFEsdl /SUNWlibsdl /'`
# 
#     27 depspacks=`echo ${depspacks} | sed 's/SFEsdl$/SUNWlibsdl/'`
# 
##done###     28 depspacks=`echo ${depspacks} | sed s/SFElibsndfile/SUNWlibsndfile/`
# 
#     29 depspacks=`echo ${depspacks} | sed s/SUNWgnome-common/SUNWgnome-common-devel/`
# 
#     30 depspacks=`echo ${depspacks} | sed 's/SUNWgtk /SUNWgtk-doc /'`
# 
#     31 depspacks=`echo ${depspacks} | sed 's/SUNWgtk$/SUNWgtk-doc/'`
# 
#     32 depspacks=`echo ${depspacks} | sed 's/SUNWGtku /SUNWGtk /'`
# 
#     33 depspacks=`echo ${depspacks} | sed 's/SUNWGtku$/SUNWGtk/'`
# 
#     34 depspacks=`echo ${depspacks} | sed 's/SUNWsndmu /SUNWsndm /'`
# 
#     35 depspacks=`echo ${depspacks} | sed 's/SUNWsndmu$/SUNWsndm/'`
# 
#     36 depspacks=`echo ${depspacks} | sed 's/SUNWapch22u /SUNWapch22 /'`
# 
#     37 depspacks=`echo ${depspacks} | sed 's/SUNWapch22u$/SUNWapch22/'`
# 

##TODO## if a consumer appears (e.g. S10)
#SUNWncurses
##%if %(expr %{osbuild} '>=' 100)
##BuildRequires: SUNWncurses-devel
##Requires: SUNWncurses
##%else
##BuildRequires: SFEncurses-devel
##Requires: SFEncurses
##%endif


##TODO## check if this is the case as well for S11 (!)
#S12 lost the legacy name SUNWslang


%changelog
* Sat Jul 29 2017 - Thomas Wagner
- bump %define postgres_major_minor_version 9.6 (9.6.4) as the new SFE default postgresql version
- fix pnm_macro pnm_buildrequires_codec_ogg_vorbis as it was renamed/split into two packages: codec/libogg,codec/libvorbis
* Sat Jan 14 2017 - Thomas Wagner
- handle gstreamer update to 1.x for S12 - map most of the packages for now to: library/audio/gstreamer-1
* Sun Dec 11 2016 - Thomas Wagner
- use OSDistro libgcrypt / libgpg / libgpg-error on (S12)
- add gnome audio pnm_macros for new name system/core-os on (S12)
- add gnome common devel pnm_macros for new name library/gnome/gnome-common on (S12)
- set SUNWgnu_gettext / developer_gnome_gettext  pnm_macros to text/gnu-gettext (S12)
- add SUNWogg_vorbis pnm_macros for new name codec/libogg (S12)
- minor change to boost_gpp_default and icu_gpp -> -devel (all)
* Thu Dec  8 2016 - Thomas Wagner
- for gnome3 replace package pnm_buildrequires_gnome_gnome_audio with generic system/core-os (S12)
* Mon Oct 31 2016 - Thomas Wagner
- request SFEboost-gpp-devel and SFEicu-gpp-devel package in pnm_buildrequires_boost_gpp_default pnm_buildrequires_icu_gpp_default
* Thu Oct 13 2016 - Thomas Wagner
- rework python imporlib section based on pjamas work. Note: re-orderd, keep package@version listings for a while
- rework older "%( expr .... )" to be more readable
* Sat Aug 20 2016 - Thomas Wagner
- set perl-522 as new default perl (LP64), add perl-522 and perl_dir i86pc-solaris-thread-multi-64 for (S12 >= 95)
* Mon May 23 2016 - Thomas Wagner
- move sane handling from packagenames.define.allbuilds.inc to packagenames.define.initial.inc
* Fri Apr 29 2016 - Thomas Wagner
- handle SFEautomake-115 / automake / pnm_requires_SFEautomake_115 (S12)
* Fri Apr 22 2016 - Thomas Wagner
- handle pnm_buildrequires_SFEzlib_pkgconfig SFEzlib-pkgconfig -> is regular library/zlib on (S12 build 87+)
* Tue Apr  5 2016 - Thomas Wagner
- IPS package name lost python"-2" library/python/setuptools-26 on S11.3 b30 and S12 b70
- python_default changed to 2.7 (27) on S11.3 b26 and S12 b86
* Thu Mar 24 2016 - Thomas Wagner
- handle pnm_requires_developer_documentation_tool_xmlto SFExmlto (older distro < S11.3b26 < S12b90 don't have it) (OIH has text/xmlto)
* Sun Mar 13 2016 - Thomas Wagner
- OmniOS perl is multi-threaded, needs perl_dir i86pc-solaris-thread-multi-64 or doesn't find its *.pm (OM)
* Sat Mar 12 2016 - Thomas Wagner
- Exception for perl_version on OmniOS: It uses different number 5.16 -> 5.16.1 (OM)
  solves perl module builds where /usr/perl5/%{perl_version}/bin/perl is /usr/perl5/5.16.1/bin/perl
* Tue Mar  8 2016 - Thomas Wagner
- Exception for perl_path_*** vendor_perl on OmniOS: It uses different directory 5.16 -> 5.16.1 (OM)
* Fri Dec 25 2015 - Thomas Wagner
- special setting  pnm_buildrequires_SUNWxwinc_devel  x11/header/xproto (OIH)
* Sun Dec 20 2015 - Thomas Wagner
- handle pnm_buildrequires_system_hal: service/hal renamed to system/hal (S11)
* Sat Dec  5 2015 - Thomas Wagner
- add nvidia as file requires to match IPS and SVR4 package name
* Mon Nov 30 2015 - Thomas Wagner
- handle pnm_buildrequires_SUNWxwinc_devel (S11 >=144, S12)
* Sat Nov 28 2015 - Thomas Wagner
- rename SFEcppunit to SFEcppunit-gpp
##TODO## needs refinement: perl version variables (OI, S12)
- add first set of updated perl version variables (OI, S12)
- update python default to python_version 2.7 (minimum) (S12 >=86)
- adjust pnm_buildrequires_library_python_importlib accordingly (all)
- fix typo SUNWlibggpg-error -> SUNWlibgpg-error
- "No legacy name" for SUNWgnupg crypto/gnupg and SUNWlibgpg_error library/security/libgpg-error on (OIH)
* Wed Oct 21 2015 - Thomas Wagner
- add variables to find icu_gpp and boost_gpp <prefix|lib|include> similarly (S11 S12 OIH OM)
- update boost_gpp_version to 1.58, icu_gpp_version 55.1, use SFEboost-gpp SFEicu-gpp for all osdistro for now (S11 S12 OIH OM)
- add more pnm_buildrequires_jdk_default / jdk_7 / jdk_8 (S11 OM)
- handle SFEeditline / library/libedit (S11)
- handle SUNWlibm math/header-math (add OM)
- handle more named for library/nspr SUNWprd
* Sat Okt 17 2015 - Thomas Wagner
- handle pnm_buildrequires_library_libedit SFEeditline
* Sun Sep 20 2015 - Thomas Wagner
- add missing %define to boost_gpp_default_libdir (pjama) (OIH >= oih20150330)
* Weg Aug 19 2015 - Thomas Wagner
- system/library/mozilla-nss/header-nss moved into main packages (S11 >= 160, S12)
- first try to handle pnm_buildrequires_library_python_importlib (S11, S12. TODO/verify: OI, hipster)
* Sat Aug 15 2015 - Thomas Wagner
- set directories for boost_gpp_default (/usr/g++ for S11 S12 OI, /usr for OIH) - OIH is subject to change if we decide for SFEboost-gpp as default one day
* Mon Aug 10 2015 - Thomas Wagner
- pause unconditional section for pnm_buildrequires_SUNWfreetype2 (needs to be clamped by osdistro != %{os2nnn} or more
* Wed Aug  5 2015 - Thomas Wagner
- add pnm_buildrequires_boost_gpp_default pnm_requires_boost_gpp_default (ALL: 0.55 from SFE, except OIH 0.55 or 0.58 from osdistro)
- add pnm_buildrequires_developer_cppunit (ALL: SFEcppunit, except OIH from osdistro)
- add %{oihipster} to handle pnm_buildrequires_SUNWgraphviz (OI, hipster)
* Mon Aug  3 2015 - Thomas Wagner
- library/math/header-math moved into system/library/math - add OIH
* Fri Jul  3 2015 - Thomas Wagner
- extend SFEgdbm selection for pnm_buildrequires_library_database_gdbm
* Thr Mar 19 2015 - Thomas Wagner
- fix to fetch from S12 repo: pnm_requires_apr_default pnm_buildrequires_apr_util_default pkg://solaris/library/apr-15 pkg://solaris/library/apr-util-15
* Sun Feb  1 2015 - Thomas Wagner
- fix package name for mysql_default version 5.5 (S12 >= 63)
* Sat Jan 24 2015 - Thomas Wagner
- prepare for renamed-to-package libapr apr-util
- fix syntax error around osdistro_entire_padded_number4
- work around for pkgtool not resolving library/apr-15 to spec file SFElibapr, library/apr-util-15 to SFEapr-util (OM)
* Thu Jan 22 2015 - Thomas Wagner
- set mysql_default version 5.5 (S12 >= 63)
* Sun Jan 17 2015 - Thomas Wagner
- add missing apr_util_default_libdir
* Sat Jan 17 2015 - Thomas Wagner
- add pnm_requires_apr_default (1.3 default, 1.5 for OM and maybe S12)
* Fri Jan 16 2015 - Thomas Wagner
- library/python-2/python-gnome-libs-26 is renamed=true - replace by library/python-2/pygtk2-26 (S11 >=160, S12)
- add %{omnios} to SFEgdbm (<116, !S12, true for OM=omnios)
- add  web/library/apache/apr-13      renamed to library/apr-13      (S11, S12, OI. For builds >=151)
       web/library/apache/apr-util-13 renamed to library/apr-util-13 (S11, S12, OI. For builds >=151)
* Fri Aug  8 2014 - Thomas Wagner
- add missing defaults for pnm_buildrequires_SUNWgraphviz
* Mon Jul  7 2014 - Thomas Wagner
- handle pnm_buildrequires_SUNWgraphviz (S11, S12. TODO: OI, hipster)
- set default to IPS name for pnm_buildrequires_SFEgdbm  library/database/gdbm (set defaults to IPSname, switch for S12)
* Fri May 16 2014 - Thomas Wagner
- enhanced pnm_buildrequires_SFExz_gnu (add OOS151008)
- set python_major_minor_micro_version 2.6.8 (OOS151008)
* Fri Apr 26 2014 - Thomas Wagner
- handle pnm_buildrequires_SFEasciidoc (S12 >= 34)
* Mon Apr 21 2014 - Thomas Wagner
- %define python_major_minor_micro_version 2.6.8 (OOS151008)
* Sat Apr 12 2014 - Thomas Wagner
- set pnm_buildrequires_SFExz_gnu compress/xz (OOS151008)
* Sat Apr 12 2014 - Thomas Wagner
- add perl_default 5.16.1 aka 6.4 for OmniOS (OOS151008)
* Sun Mar 23 2014 - Thomas Wagner
- use %{osdistrelnumber} '>=' 201101 instead of %{s110100} for pulseaudio, automake-111 in Solaris 11.1 (>= S11.1)
- handle SFEgnugetopt / sfe/shell/gnu-getopt / solaris/shell/gnu-getopt (>= S11.2, S12)
- need pkg://solaris/shell/gnu-getopt
* Mon Feb 17 2014 - Ian Johnson <ianj@tsundoku.ne.jp>
- switch pnm_buildrequires_apache2_default correctly for osbuild >= 133 (SUNWapch22u does not exist in S11+)
* Wed Feb 12 2014 - Thomas Wagner
- lost the legacy name SUNWslang on (S12) ##TODO## check if this is the case as well for (S11) (!)
- switch pnm_buildrequires_python_default correctly for osbuild >= 133 (S11, OI, S12)
* Mon Jan  6 2013 - Thomas Wagner
- S12 has no legacy name for library/database/gdbm (SFEgdbm SUNWgnu-dbm)
* Tue Dec 24 2013 - Thomas Wagner
- %define pnm_buildrequires_python_default runtime/python-26 on S12 (no legacy package name SUNWPython26)
* Mon Dec  9 2013 - Thomas Wagner
- handle library/libidn SUNWgnu-idn (SXCE)
* Sun Dec  1 2013 - Thomas Wagner
- handle %define pnm_buildrequires_SFElibggz_devel	SUNWgnome-games-devel (OI, SXCE), SFElibggz-devel (S11, S12)
- handle SUNWlua, SUNWgsed for SXCE
* Mon Oct  4 2013 - Thomas Wagner
- handle SUNWmlib for SXCE
- change for os2nnn target library/gnu/libsndfile to SFElibsndfile (pkgtool can't resolve otherwise)
* Sun Oct  3 2013 - Thomas Wagner
- handle SUNWlibm and SUNWgnome_games_devel for SXCE
* Thu Oct 17 2013 - Thomas Wagner
- typo, s/libdiscidlibdiscid/libdiscid/
* Wed Sep 18 2013 - Thomas Wagner
- special handling SUNWgnu-readline (SXCE >=130)
* Sat Sep 14 2013 - Thomas Wagner
- first implementation steps for pnm_requires_ruby_default (unfinished and needs fixed SFEruby.spec)
* Wed Aug 14 2013 - Thomas Wagner
- handle (partially) SUNWgnu-readline / library/readline / SFEreadline (SXCE)
* Sun Aug 11 2013 - Thomas Wagner
- handle SUNWaudh|audh|system/header/header-audio for SXCE
* Sat Jul 27 2013 - Thomas Wagner
- remove typos _devel$ -> -devel$
* Sun Jul 21 2013 - Thomas Wagner
- handle SUNWlibm / pnm_buildrequires_system_library_math_header_math -> system/library/math (S11* >= 174, S12)
  math headers went into system header package
- fix package name SFEpulseaudio-devel (SXCE)
- set perl version (S11.1, S12)
* Thu Jul  4 2013 - Thomas Wagner
- handle SFElibsndfile/SUNWlibsndfile to get default (1.0.25 for now, /usr/gnu)
  or solve missing legacy name SUNWlibsndfile
* Mon Jul  1 2013 - Thomas Wagner
- handle pnm_buildrequires_library_ncurses/SUNWncurses-devel (>=100,  S10: not yet implemented)
- handle SFEautomake-111 / automake / pnm_requires_SFEautomake_111 (>= 175.1 >= S11.1)
- handle SFEpulseaudio / pulseaudio / pnm_requires_SFEpulseaudioautomake_111 (>= 175.1 >= S11.1)
* Sun Jun 30 2013 - Thomas Wagner
- fix logic for pnm_buildrequires_x11_library_freeglut on Solaris 12
* Fri Jun 28 2013 - Thomas Wagner
- handle pnm_requires_SUNWtexi / text/texinfo
- handle pnm_requires_SUNWdoc / text/doctools
* Fri Jun 28 2013 - Thomas Wagner
- add solaris12 to osbuild related decisions
* Thu Jun 20 2013 - Thomas Wagner
- add feature flag etc_security_directorylayout (>=151)
* Sat Apr  6 2013 - Thomas Wagner
- add SVR4 package names for %define pnm_buildrequires_SUNWlibstdcxx4 (S10, SXCE)
* Sat Mar 23 2013 - Thomas Wagner
- fix expression %if %{?perl_dir:1}%{!?perl_dir:0}
  contributed by Martin C.  https://sourceforge.net/p/pkgbuild/spec-files-extra/44/
* Wed Jan 30 2013 - Thomas Wagner
- add SVR4 package names for pnm_buildrequires_SUNWltdl (S10, SXCE)
* Sat Jan 26 2013 - Thomas Wagner
- add mysql_default_prefix (e.g. %{prefix}%{mysql_default_prefix} = /usr/mysql/5.1 )
* Sun Jan 13 2013 - Thomas Wagner
- add SVR4 package names for pnm_buildrequires_SUNWzlib_devel SUNWzlib (S10, SXCE)
* Sat Jan 12 2013 - Thomas Wagner
- rename (add _gnu) pnm_buildrequires_SFExz_gnu SFExz-gnu compress/xz
  and change known consumer spec files
* Sat Jan  5 2013 - Thomas Wagner
- typo in variable name SUNWlibgpg_error / SFElibgpg_error
- rename service/database/postgres-91 to database/postgres-91.
* Fri Jan  4 2013 - Thomas Wagner
- handle special macro name pnm_buildrequires_postgres_default 
  pnm_requires_postgres_default (>=147 S11) and macros for postgres version.
  Default here to service/database/postgres-91. Updated version macros.
- correct pnm_buildrequires_postgres_default to ask for service/database/postgres-84/developer
  and service/database/postgres-91/developer
- handle SFEfreeglut x11/library/freeglut pnm_buildrequires_x11_library_freeglut (>151 S11)
- partial support for SUNWapch22u pnm_buildrequires_apache2_default (>=133)
* Sun Dec  9 2012 - Thomas Wagner
- handle SUNWlibdiscid /library/musicbrainz/libdiscid
- handle SUNWmusicbrainz /library/musicbrainz/libmusicbrainz
* Sun Nov  4 2012 - Thomas Wagner
- handle special macro name pnm_buildrequires_apache2_default pnm_requires_apache2_default
  and macros for apache2 version.
- handle special macro name pnm_buildrequires_postgres_default pnm_requires_postgres_default
  and macros for postgres version.
* Sun Nov  4 2012 - Thomas Wagner
- handle SUNWgnu-gettext developer_gnome_gettext text_gnu_gettext gnu_gettext
* Thu Oct 18 2012 - Thomas Wagner
- handle SUNW*plugin/php52* meta packages not detectable on IPS systems (use /module/php52 instead)
  web/server/apache-22/plugin/plugin-php52 -->> web/server/apache-22/module/apache-php5
* Mon Sep 17 2012 - Thomas Wagner
- handle SUNWkrb -> system/security/kerberos-5 (>=133)
* Thu Aug 16 2012 - Thomas Wagner
- fix %if {?$perl_dir} for case when already present, use {?$perl_dir:1}. perl_dir is a string
* Thu Aug  9 2012 - Thomas Wagner
- handle SUNWntp SUNWntpu SUNWntpr ntp ... for (S10, SXCE)
- handle SUNWsndm SUNWsndmu for (S10, SXCE)
- define %{perl_default_includedir} to help finding e.g. EXTERN.h from default perl
* Sat Aug  4 2012 - Thomas Wagner
- initial support for handling SFEpulseaudio / pulseaudio
* Mon Jul 30 2012 - Thomas Wagner
- make SFElibmikmod include -devel packages
* Mon Jul  9 2012 - Thomas Wagner
- add SVR4 SUNWxwopt SUNWlibdsl for pre-IPS systems
- append "/mysql" to the *examples* like this %{mysql_default_includedir}/mysql
  same for libaries
- add libraries to %{pnm_buildrequires_mysql_default} database/mysql-51,database/mysql-51/library
* Sat Jul  7 2012 - Thomas Wagner
- handle SUNWxwopt x11/optional-clients compatibility/packages/SUNWxwopt
- handle SUNWlibdsl (and select SFEsdl on older builds before it was added)
* Sun Jun 24 2012 - Thomas Wagner
- handle SUNWlibsdl(-devel) not detectable on IPS systems (pkg info SUNWlibsdl says not 
  installed but library/libsdl is) 
* Sat Jun 23 2012 - Thomas Wagner
- handle SUNWlibC: system/library/c++-runtime is renamed on OI to 
  system/library/c++/sunpro (OI>=151), S11 unchanged
* Sat Jun 23 2012 - Thomas Wagner
- handle compress/xz SFExz for S11 (all builds) and (OI < 151)
* Thu May 17 2012 - Thomas Wagner
- handle SFEgnupg2 SUNWgnupg SUNWlibgpg-error SUNWlibgpg-error-devel SUNWlibgcrypt
  SUNWlibgcrypt-devel (>=130), may need from 133/134 in new ips package names as target
* Sat May 12 2012 - Thomas Wagner
- handle SFEperl-extutils-cbuilder which is integrated in perl-510 (OI>=151 to be verified) and perl-512 (S11 >=175 to be verified)
* Fri May 11 2012 - Thomas Wagner
- adjust build-number where SUNWsfwhea was merged into SUNWhea
* Tue Apr 24 2012 - Thomas Wagner
- handle SFEvala developer/vala (>=151)
- handle SUNWlibC not detectable on IPS systems (pkg info SUNWlibC says not 
  installed but system/library/c++-runtime is), provide reverse alias as well
- handle SUNWsqlite3 not detectable on IPS systems (pkg info SUNWsqlite3 says
  not installed but database/sqlite-3 is), provide reverse alias as well
- handle SUNWpysqlite -> %{pnm_requires_python_default} (>=133)
- handle SUNWfuse file-system/uvfs (>=163)
- handle SUNWfusefs library/libfuse (>=163)
* Sun Apr 22 2012 - Thomas Wagner
- handle SUNWflac SUNWspeex SUNWpangomm SUNWpango SUNWglib2 SUNWgtk2 for SVR4 (S10, SXCE)
* Sat Mar 31 2012 - Thomas Wagner
- re-arranged notes and other information for future work
- add notes about spec files with logic which should be in pnm
- prepare draft version string for python package names: python_version_package_string 26
* Sat Mar 17 2012 - Thomas Wagner
- add pnm_buildrequires_java_runtime, pnm_buildrequires_java_runtime, and _32 _64 variants
  use this to get the platform default java package names
  ##TODO## add java filesystem location and version numbers if needed
* Tue Aug 23 2011 - Thomas Wagner
- handle SUNWltdl/library_libtool_libltdl
- handle SUNWbtool/pnm_requires_developer_object_file
* Mon Aug 14 2011 - Thomas Wagner
- fix SUNWsmba -> SUNWsmbau/SUNWsmbar because SUNWsmba not found on
  IPS systems build around 170 (not in legacy_pkg: SUNWsmba)
* Wed Jan  4 2012 - Thomas Wagner
- pkgtool/pkgbuild can't see if packages are installed: meta-package data/docbook
  is requested. up to 133 it was developer/documentation-tool/gtk-doc,
  now it's a never installed package because it got renamed to an incorporation
* Sat Dec 10 2011 - Thomas Wagner
- make SUNWsmba* be service/network/samba (>=133)
* Mon Nov  7 2011 - Thomas Wagner
- handle cases x11/client not being resolved properly pnm_buildrequires_SUNWxwplt compatibility/packages/SUNWxwplt (>=144)
* Sat Aug 13 2011 - Thomas Wagner
- fix typo SUNWsmbr -> SUNWsmbar SUNWsmbu SUNWsmbau, ...
- handle SUNWsmba_devel/SUNWsmbau/SUNWsmbar/SUNWsmba/smba/service_network_samba
- handle SUNWfreetype2/freetype2/SFEfreetype_devel/SFEfreetype/system_library_freetype_2
- fix selected metapackage to get installed-detection with autodeps satisfied for
  SUNWgtk_doc/developer_documentation_tool_gtk_doc/data_docbook (not fully tested)
* Mon Aug  2 2011 - Thomas Wagner
- handle special macro name pnm_buildrequires_mysql_default pnm_requires_mysql_default
  and macros for mysql version.
  add macro to point to the mysql_default_includedir and mysql_default_libdir.
  SUNWmysql51/SUNWmysql51u/database/mysql-51 is initially the only mysql-version
  for *all* osbuild / osdistro, to be extended as required later (for older 
  osbuild/osdistro, *or* for next mysql-versions 5.x or 6.x...)
* Mon Aug  1 2011 - Thomas Wagner
- handle SUNWkrb/SUNWkrbu/SUNWkrbr/service_security_kerberos_5
* Sun Jul 31 2011 - Thomas Wagner
- add SVR4 package names for SUNWbash SUNWpcre SUNWggrp SUNWlibsasl
- fix name *openssl-include  *openssl-includes
* Wed Jul 20 2011 - Thomas Wagner
- handle special macro name pnm_buildrequires_python_default pnm_requires_python_default
  and macros for python version.
  SUNWPython26 is initially the only Python-version for *all* osbuild / osdistro, to
  be extended as required later (for older osbuild/osdistro, *or* for next Python 2.x or 3.x)
* Sat Jul 16 2011 - Thomas Wagner
- handle SUNWapch22** (subset only. old SXCE/IPS_old/IPS_new_names)
- handle SUNWphp52**  (subset only. old SXCE/IPS_old/IPS_new_names)
* Thu Jun 23 2011 - Thomas Wagner
- enhance default (Build)Requires pnm_buildrequires_perl_default to include both
  SUNWperl584core, SUNWperl584usr. Only affects older distributions
* Sun Jun 19 2011 - Thomas Wagner
- handle SUNWaudh|audh|system/header/header-audio moved into system/header (>=163 s11ex)
* Fri Jun 17 2011 - Thomas Wagner
- handle different perl versions (5.8.4, 5.10, 5.12) and module paths 
- set perl to 5.12 on Solaris 11 to have modules in directory vendor_perl/5.12 (and not in 5.12.3)
- set perl to 5.10 on OpenIndiana to have modules in directory vendor_perl/5.10 (and not in 5.10.0)
- add note about omitting "micro"-versionnumber from the path to modules
- handle special macro name pnm_buildrequires_perl5_default pnm_requires_perl5_default (note: renamed!):
   SUNWperl584core/SUNWperl584usr runtime/perl-510 runtime/perl-512 (note the _default string)
- fine tune perl_vesion to be 5.10.0 and higher version numbers remain as 5.12 (w/o micro version)
- rename pnm_buildrequires_perl5_default to pnm_buildrequires_perl_default (+requires)
- remove >"< from %define perl_path_<vendor|site>*
* Sat Mar 27 2011 - Thomas Wagner
- handle SUNWGtku/SUNWGtkr/SUNWGtk Gtk library/desktop/gtk1
* Sat Mar 19 2011 - Thomas Wagner
- handle more cases SUNWwgetu/SUNWwgetr/SUNWwget wget web/wget (>=133)
- make endifs pretty commented
- reduce "else" code paths by negating %if clauses (new build numbers have less %if clauses)
* Fri Mar 18 2011 - Thomas Wagner
- make libpigment a dummy because obsoleted/removed (>=156)
* Thr Mar 17 2011 - Thomas Wagner
- handle SUNWwgetu/SUNWwgetr/SUNWwget wget web/wget
- handle SUNWghostscriptu/SUNWghostscriptr/SUNWghostscript ghostscript print/filter/ghostscript
- handle more cases of SUNWopenssl* (still incomplete)
- handle SFEgdbm or SUNWgnu-dbm (>=116)
* Wed Mar 16 2011 - Thomas Wagner
- improve/add support for pkg info SUNWopenssl reported as not installed (but renamed)
* Mon Feb 28 2011 - Thomas Wagner
- add alias ending on "s" helping with easy typos:
  pnm_buildrequires_SUNWopenssl_include / pnm_buildrequires_SUNWopenssl_includes (note the "s" at the end)
* Sun Feb  7 2011 - Thomas Wagner
- handle SFElibmodmod and SUNWlibmikmod (>=90)
* Wed Feb  2 2011 - Thomas Wagner
- handle SUNWsfehea and SUNWhea - system/header (>= 130, >= 133) (perl modules)
- handle SFEsane-backend | SUNWsane-backend (>= 90) make pnm*SUNWsane-backend 
  require SFEsane-backend below 90 (would need undelete of SFEsane-backend.spec)
- handle SFEfftw3 | SUNWfftw3 (>= 107)
* Sat Jun 12 2010 - Thomas Wagner
- initial include file
