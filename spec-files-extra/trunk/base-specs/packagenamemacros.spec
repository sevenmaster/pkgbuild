#
#
#   STRONG note: this is an early stage, logic and variable names *might* change
#
#

# owner: Thomas Wagner (tom68) - please ask/discuss if you want non-trivial changes

# TODO: add more complete examples to help spec file engineers get the idea
# TODO: add copyright (CDDL?)


#
# EXAMPLE file for macro definitions for Solaris OS build and distro specific package names
# you just specify a macro name like "openssl" and get depending on the OS the currently
# active pacakge name (new IPS based library/security/openssl or SXCE SUNWopenssl-libraries 
# or S10 SUNWopenssly<u|r|whattheheckitisnamed>
# second EXAMPLE SUNWncurses/SUNWncurses-devel and "ncurses" and library/ncurses


#already included before?
%if %{?packagenamemacros:%{packagenamemacros}}%{?!packagenamemacros:0}
#we are already included
%else
%include packagenamemacros.inc
%endif

%include pkgbuild-features.inc

# help the demo: pkgtool --interactive prep base-specs/packagenamemacros.spec
Name: packagenamemacros

%description
Demo the packagenamemacros.inc use:

   pkgtool --interactive prep base-specs/packagenamemacros.spec


Demo packagenamemacros.inc in your own spec file:

Include this spec file by the "use" statement and do include include/packagenamemacros.inc into 
your own spec file.
  (remove the comment # signs)  
  (the include packagenamemacros.inc is always needed in your spec, the %use... and 
# %packagenamemacros.prep is only for demonstration)

Demo setup: Edit SFEyourspec.spec
#    #always do the include, this is the only line really required for normal operation
#    %include packagenamemacros.inc

#    #optional for demoing inside your spec file's prep section or elsewhere
#    %use packagenamemacros = packagenamemacros.spec

then call the demo osdistop.prep inside your regular prep section to see at pkgbuild runtime 
what the result of the includefile packagenamemacros.inc on your development machine running 
your spec file is.

#    #optional for demoing inside your spec file is the call to "%packagenamemacros.prep"
#    %prep    
#    %setup -q -n %name-%version    

#    %packagenamemacros.prep

then run "pkgtool --interactive prep SFEyourspec.spec" and watch the variabled your might use in %if statements or other spec files code. enjoy.

NOTE: replace in variable name all "-" with "_"   ("-" is not valid in a variable name)
NOTE: specify forward or reverse  SUNWopenssl -> SUNWopenssl or openssl or library/security/openssl
NOTE:                             openssl     -> SUNWopenssl or openssl or library/security/openssl
NOTE:                library/security/openssl -> SUNWopenssl or openssl or library/security/openssl

%prep
echo "
pnm: osbuild 		%{osbuild}
pnm: SXCE 		%{SXCE}
pnm: os2nnn 		%{os2nnn}
pnm: osdistro_entire    %{osdistro_entire}
pnm: osdistro_entire_padded_number4 %{osdistro_entire_padded_number4}
pnm: solaris12       	%{solaris12} Solaris 12
pnm: s110300         	%{s110300} Solaris 11.3 and up
pnm: s110200         	%{s110200} Solaris 11.2 and up
pnm: s110100         	%{s110100} Solaris 11.1 and up
pnm: s110000         	%{s110000} Solaris 11.0 and up
pnm: solaris11express	%{solaris11express} Solaris 11 Express yes/no
pnm: s11ex201100 		%{s11ex201100} Solaris 11 Express (some following release e.g. 166)
pnm: s11ex201011 		%{s11ex201011} Solaris 11 Express (first release end of 2010)
pnm: omnios		%{omnios} OmniOS
pnm: openindiana		%{openindiana} OpenIndiana yes/no
pnm: oi201100 		%{oi201100} OpenIndiana 151, experimental reworked
pnm: oi201009 		%{oi201009} OpenIndiana 147/148, experimental reworked
pnm: os201005 		%{os201005} not yet released, name might eventually change?
pnm: os201003 		%{os201003} deprecared, this release name was never used, will be removed
pnm: os200906 		%{os200906}
pnm: os200902 		%{os200902}
pnm: os200811 		%{os200811}
pnm: osdistrelnumber 	%{osdistrelnumber}
pnm: osdistrelname   	%{osdistrelname}
pnm: osdet299999 		%{osdet299999}

pnm: pkgbuild_ver_numeric	%{pkgbuild_ver_numeric}  (version encoded in a large number, usefull for comparisons)
pnm: pkgbuild_ips_legacy	%{pkgbuild_ips_legacy}   (is supporting IPS system)
pnm: pkgbuild_renamed_to	%{pkgbuild_renamed_to}   (is supporting the renamed_to package name tags)
pnm: pkgbuild_ver_1_3_109	%{pkgbuild_ver_1_3_109}  (doesn't necessarily mean that version exists at all)
pnm: pkgbuild_ver_1_3_108	%{pkgbuild_ver_1_3_108}
pnm: pkgbuild_ver_1_3_107	%{pkgbuild_ver_1_3_107}
pnm: pkgbuild_ver_1_3_106	%{pkgbuild_ver_1_3_106}
pnm: pkgbuild_ver_1_3_105	%{pkgbuild_ver_1_3_105}
pnm: pkgbuild_ver_1_3_104	%{pkgbuild_ver_1_3_104}
pnm: pkgbuild_ver_1_3_103	%{pkgbuild_ver_1_3_103}

pnm: pnm_buildrequires_perl_default: 		%{pnm_buildrequires_perl_default}
pnm: pnm_requires_perl_default: 			%{pnm_requires_perl_default}
pnm: perl_version number is:       		%{perl_version}
pnm: perl_major_version number is: 		%{perl_major_version}
pnm: perl_major_minor_version number is: 		%{perl_major_minor_version}
pnm: perl_major_minor_micro_version number is: 	%{perl_major_minor_micro_version}
pnm: _prefix/perl_path_vendor_perl	 	%{_prefix}/%{perl_path_vendor_perl}
pnm: _prefix/perl_path_vendor_perl_version 	%{_prefix}/%{perl_path_vendor_perl_version}
pnm: _prefix/perl_path_site_perl 			%{_prefix}/%{perl_path_site_perl}
pnm: _prefix/perl_path_site_perl_version 		%{_prefix}/%{perl_path_site_perl_version}

pnm: pnm_buildrequires_python_default: 		%{pnm_buildrequires_python_default}
pnm: pnm_requires_python_default: 		%{pnm_requires_python_default}
pnm: python_version number is:       		%{python_version}
pnm: python_major_version number is: 		%{python_major_version}
pnm: python_major_minor_version number is: 	%{python_major_minor_version}
pnm: python_major_minor_micro_version number is: 	%{python_major_minor_micro_version}
pnm: python_package_string: 			%{python_version_package_string}

pnm: pnm_buildrequires_mysql_default		%{pnm_buildrequires_mysql_default}
pnm: pnm_requires_mysql_default			%{pnm_requires_mysql_default}
pnm: _prefix/mysql_default_includedir		%{_prefix}/%{mysql_default_includedir}
pnm: _prefix/mysql_default_libdir			%{_prefix}/%{mysql_default_libdir}
pnm: mysql_version				%{mysql_version}
pnm: mysql_major_version				%{mysql_major_version}
pnm: mysql_major_minor_version			%{mysql_major_minor_version}

        OS:  (note: /usr, do not specify %%{_prefix})
pnm: pnm_buildrequires_ruby_default: 		%{pnm_buildrequires_ruby_default}
pnm: pnm_requires_ruby_default: 			%{pnm_requires_ruby_default}
pnm: ruby_version number is:       		%{ruby_version}
pnm: ruby_major_version number is:       		%{ruby_major_version}
pnm: ruby_major_minor_version number is: 		%{ruby_major_minor_version}
pnm: ruby_major_minor_micro_version number is: 		%{ruby_major_minor_micro_version}

        SFE: (note: /usr/gnu, do not specify %%{_prefix})
pnm: pnm_buildrequires_sfe_ruby_default: 		%{pnm_buildrequires_sfe_ruby_default}
pnm: pnm_requires_sfe_ruby_default: 			%{pnm_requires_sfe_ruby_default}
pnm: sfe_ruby_version number is:       		%{sfe_ruby_version}
pnm: sfe_ruby_major_version number is:       		%{sfe_ruby_major_version}
pnm: sfe_ruby_major_minor_version number is: 		%{sfe_ruby_major_minor_version}
pnm: sfe_ruby_major_minor_micro_version number is: 		%{sfe_ruby_major_minor_micro_version}

pnm: ruby_default_prefix		%{ruby_default_prefix}
pnm: ruby_default_includedir		%{ruby_default_includedir}
pnm: ruby_default_libdir		%{ruby_default_libdir}

pnm: sfe_ruby_default_prefix		%{sfe_ruby_default_prefix}
pnm: sfe_ruby_default_includedir		%{sfe_ruby_default_includedir}
pnm: sfe_ruby_default_libdir		%{sfe_ruby_default_libdir}

see include/packagenames.define.allbuilds.inc for detailed usage instructions!
pnm: pnm_buildrequires_postgres_default		%{pnm_buildrequires_postgres_default}
pnm: pnm_requires_postgres_default		%{pnm_requires_postgres_default}
pnm: _prefix/ . postgres/ . postgres_default_prefix	%{_prefix}/postgres/%{postgres_major_minor_version}
pnm: CFLAGS="-I%%{_prefix}/%%{postgres_default_includedir}" -I%{_prefix}/%{postgres_default_includedir}
pnm: LDFLAGS and CFLAGS="-L%%{_prefix}/%%{postgres_default_libdir} -R%%{_prefix}/%%{postgres_default_libdir}"	-L%{_prefix}/%{postgres_default_libdir} -R%{_prefix}/%{postgres_default_libdir}
pnm: _prefix/ . postgres/ . postgres_default_includedir . /include			%{_prefix}/postgres/%{postgres_major_minor_version}/include
pnm: _prefix/ . postgres/ . define postgres_default_libdir	. /lib			%{_prefix}/postgres/%{postgres_major_minor_version}/lib
pnm: _prefix/ . postgres/ . postgres_default_pg_config . /bin/pg_config		%{_prefix}/postgres/%{postgres_major_minor_version}/bin/pg_config
pnm: _prefix/ . postgres/ . postgres_default_pg_config_64 . /bin/64/pg_config	%{_prefix}/postgres/%{postgres_major_minor_version}/bin/64/pg_config
pnm: postgres_version				%{postgres_version}
pnm: postgres_major_version			%{postgres_major_version}
pnm: postgres_major_minor_version			%{postgres_major_minor_version}

pnm: pnm_requires_java_runtime_default	%{pnm_requires_java_runtime_default}
pnm: pnm_requires_java_runtime_default_32       %{pnm_requires_java_runtime_default_32}
pnm: pnm_requires_java_runtime_default_64       %{pnm_requires_java_runtime_default_64}
pnm: pnm_buildrequires_SUNWsmba                 %{pnm_buildrequires_SUNWsmba}
pnm: pnm_buildrequires_SUNWsmbau                 %{pnm_buildrequires_SUNWsmbau}
pnm: pnm_buildrequires_SUNWsmbar                 %{pnm_buildrequires_SUNWsmbar}
pnm: pnm_requires_SUNWsmba                 %{pnm_requires_SUNWsmba}
pnm: pnm_requires_SUNWsmbau                 %{pnm_requires_SUNWsmbau}
pnm: pnm_requires_SUNWsmbar                 %{pnm_requires_SUNWsmbar}
pnm: featureflags
pnm: etc_security_directorylayout		%{etc_security_directorylayout}
pnm: pnm_buildrequires_SUNWlibm			math headers are in package: %{pnm_buildrequires_SUNWlibm}

pnm: apache2_version 			%{apache2_version}
pnm: apache2_major_version			%{apache2_major_version}
pnm: apache2_major_minor_version			%{apache2_major_minor_version}
pnm: apache2_version_package_string			%{apache2_version_package_string}
pnm: pnm_buildrequires_apache2_default             %{pnm_buildrequires_apache2_default}
pnm: pnm_requires_apache2_default                  %{pnm_requires_apache2_default}
pnm: pnm_buildrequires_apache2_default		%{pnm_buildrequires_apache2_default}
pnm: pnm_requires_apache2_default		%{pnm_requires_apache2_default}
pnm: apache2_default_includedir    		%{apache2_default_includedir}
pnm: apache2_default_libdir        	%{apache2_default_libdir}
pnm: apache2_default_libexecdir    	%{apache2_default_libexecdir}
pnm: apache2_default_apxs  		%{apache2_default_apxs}
pnm: apache2_default_apxs_64		%{apache2_default_apxs_64}

pnm: pnm_buildrequires_apr_default	%{pnm_buildrequires_apr_default}
pnm: pnm_requires_apr_default	        %{pnm_requires_apr_default}
pnm: apr_version			%{apr_version}
pnm: apr_major_version			%{apr_major_version}
pnm: apr_major_minor_version		%{apr_major_minor_version}
pnm: apr_version_package_string		%{apr_version_package_string}
pnm: apr_default_includedir		%{apr_default_includedir}
pnm: apr_default_inc			%{apr_default_inc}
pnm: apr_default_libdir			%{apr_default_libdir}
pnm: apr_default_lib_path		%{apr_default_lib_path}
pnm: apr_default_apr_1_config		%{apr_default_apr_1_config}
#pnm: apr_default_apr_1_config_64	%{apr_default_apr_1_config_64}

pnm: pnm_buildrequires_apr_util_default	%{pnm_buildrequires_apr_util_default}
pnm: pnm_requires_apr_util_default	        %{pnm_requires_apr_util_default}
pnm: apr_util_version			%{apr_util_version}
pnm: apr_util_major_version			%{apr_util_major_version}
pnm: apr_util_major_minor_version		%{apr_util_major_minor_version}
pnm: apr_util_version_package_string		%{apr_util_version_package_string}
pnm: apr_util_default_includedir		%{apr_util_default_includedir}
pnm: apr_util_default_inc			%{apr_util_default_inc}
pnm: apr_util_default_libdir			%{apr_util_default_libdir}
pnm: apr_util_default_lib_path		%{apr_util_default_lib_path}

" >/dev/null


echo "
requesting package  SUNWopenssl resolves on %{osdistrelname} %{osdistrelnumber} build %{osbuild}:
  BuildRequires for SUNWopenssl is contained in  %{pnm_buildrequires_SUNWopenssl}
       Requires for SUNWopenssl is contained in  %{pnm_requires_SUNWopenssl}

requesting package  openssl w/o the SUNW prefix in the name resolves on %{osdistrelname} %{osdistrelnumber} build %{osbuild}:
  BuildRequires for openssl is contained in  %{pnm_buildrequires_openssl}
       Requires for openssl is contained in  %{pnm_requires_openssl}

requesting package  library/security/openssl resolves on %{osdistrelname} %{osdistrelnumber} build %{osbuild}:
  BuildRequires for library/security/openssl is contained in  %{pnm_buildrequires_library_security_openssl}
       Requires for library/security/openssl is contained in  %{pnm_requires_library_security_openssl}

requesting package  SUNWncurses / SUNWncurses-devel resolves on %{osdistrelname} %{osdistrelnumber} build %{osbuild}:
  BuildRequires for SUNWncurses-devel is contained in  %{pnm_buildrequires_SUNWncurses_devel}
       Requires for SUNWncurses is contained in  %{pnm_requires_SUNWncurses}

requesting package  ncurses w/o the SUNW prefix in the name resolves on %{osdistrelname} %{osdistrelnumber} build %{osbuild}:
  BuildRequires for ncurses is contained in  %{pnm_buildrequires_ncurses}
       Requires for ncurses is contained in  %{pnm_requires_ncurses}

requesting package  library/ncurses resolves on %{osdistrelname} %{osdistrelnumber} build %{osbuild}:
  BuildRequires for library/ncurses is contained in  %{pnm_buildrequires_library_ncurses}
       Requires for library/ncurses is contained in  %{pnm_requires_library_ncurses}

requesting package  x11/library/freeglut resolves on %{osdistrelname} %{osdistrelnumber} build %{osbuild}:
  BuildRequires for x11/library/freeglut is contained in  %{pnm_buildrequires_SFEfreeglut}
       Requires for x11/library/freeglut is contained in  %{pnm_requires_SFEfreeglut}

requesting package  library/database/gdbm resolves on %{osdistrelname} %{osdistrelnumber} build %{osbuild}:
  BuildRequires for library/database/gdbm is contained in  %{pnm_buildrequires_SUNWgnu_dbm}
       Requires for library/database/gdbm is contained in  %{pnm_requires_SUNWgnu_dbm}

requesting package  SUNWslang resolves on %{osdistrelname} %{osdistrelnumber} build %{osbuild}:
  BuildRequires for SUNWslang is contained in  %{pnm_buildrequires_SUNWslang}
       Requires for SUNWslang is contained in  %{pnm_requires_SUNWslang}

requesting package  SFEgnugetopt resolves on %{osdistrelname} %{osdistrelnumber} build %{osbuild}:
  BuildRequires for SFEgnugetopt is contained in  %{pnm_buildrequires_SFEgnugetopt}
       Requires for SFEgnugetopt is contained in  %{pnm_requires_SFEgnugetopt}

requesting package  SFExz resolves on %{osdistrelname} %{osdistrelnumber} build %{osbuild}:
  BuildRequires for SFExz is contained in  %{pnm_buildrequires_SFExz_gnu}
       Requires for SFExz is contained in  %{pnm_requires_SFExz_gnu}

" >/dev/null



%changelog
* Thu Jan 22 2015 - Thomas Wagner
- add %{osdistro_entire}
* Sat Jan 17 2015 - Thomas Wagner
- add %{pnm_buildrequires_apr_default}
* Fri Jan  2 2015 - Thomas Wagner
- modify infos on pkgbuild version, add more versions 1.3.105 .. 1.3.109
* Tue Jul  1 2014 - Thomas Wagner
- print informations about apache
* Mon Apr 21 2014 - Thomas Wagner
- add pnm_buildrequires_SUNWlibm
* Sat Apr 12 2014 - Thomas Wagner
- add omnios
- add example SFExz_gnu
* Sun Mar 23 2014 - Thomas Wagner
- add SFEgnugetopt, print %{osdistrelnumber}
* Wed Jan  8 2014 - Thomas Wagner
- add SUNWslang
* Mon Oct  7 2013 - Thomas Wagner
- add pkgbuild_ver / *, include pkgbuild-features.inc
* Mon Jul 1 2013 - Thomas Wagner
- add Solaris 11.0 11.1 12 (new variables)
- add featureflags: etc_security_directorylayout              %{etc_security_directorylayout}
- add example for freeglut package names 
* Sat Jan  5 2013 - Thomas Wagner
- add postgres examples
- add (incomplete) Solaris 11 11/11 examples
* Fri Nov  2 2012 - Thomas Wagner
- add pnm_buildrequires_SUNWsmba|SUNWsmbau|SUNWsmbar
* Sun Apr 29 2012 - Thomas Wagner
- add pnm_buildrequires_python_default / pnm_requires_python_default (note the special _default string)
* Sat Mar 31 2012 - Thomas Wagner
- add java examples
* Tue Aug  2 2011 - Thomas Wagner
- add mysql examples
- display more perl versions
* Sun Jul  3 2011 - Thomas Wagner
- rename variables perl5_default to perl_default
* Fri Jun 17 2011 - Thomas Wagner
- adjust changed names for osdistro variables (osdistro.inc)
- add perl version specific examples
- add pnm_buildrequires_perl5_default / pnm_requires_perl5_default (note the special _default string)
* Sat Oct 20 2010 - Thomas Wagner
- add oi to the mix
* Jun  1 2010 - Thomas Wagner
- inital to demo the name resolution depending on the operatingsystem type / distribution currently running
