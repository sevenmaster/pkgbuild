#used by at least SFElibvanessa-* and SFEperdition.spec

#default version
%define perditionparentversion 2.2

#exceptions:
%if %( /usr/bin/grep -w OPENSSL_NO_EC /usr/include/openssl/opensslconf.h >/dev/null && echo 1 || echo 0 )
#the OpenSSL compile time config switched off EC
%define perditionparentversion 2.1
%endif


#%define perditionparentversion 1.19-rc4
# echo 1.19-rc4 | sed -e 's/-rc\([0-9]*\)/.\1/'
#1.19.4
# echo 1.19-rc4 | sed -e 's/-rc\([0-9]*\)/.0.\1/'
#1.19.0.4
#carefull!  1.19-rc4 -> 1.19.0.4 and 1.19 as relese does not auto-upgrade!
#because 1.19.0.4 is bigger then 1.19 .. will need a little trick unfortunatly
%define perditionparentversionips $( echo %perditionparentversion | sed -e 's/-rc\([0-9]*\)/.0.\1/' )

#              ##NOTE## to version bumpers!
# enter version numbers into the defines below (spec files pick up this include
# file)
#%define libvanessa_adt_version $( wget -q -N -O - http://www.vergenet.net/linux/perdition/download/%{perditionparentversion}/ | grep "vanessa.*tar.bz2" | sed -e 's/.*href="//' -e 's/".*//' | grep _adt- )
%define libvanessa_adt_version 0.0.9
%define libvanessa_logger_version 0.0.10
%define libvanessa_socket_version 0.0.12

# for checking yourself, run this command and read the version numbers
# wget -q -N -O - \
#   http://www.vergenet.net/linux/perdition/download/%{perditionparentversion}/ \
#   | grep "vanessa.*tar.bz2" | sed -e 's/.*href="//' -e 's/".*//'
# vanessa_adt-0.0.9.tar.bz2
# vanessa_logger-0.0.10.tar.bz2
# vanessa_socket-0.0.12.tar.bz2


##TODO## possibly define the lib versions as well (tied to the download-version directory)

%changelog
* Wed Aug 16 2017 - Thomas Wagner
- redefine version to 2.1 (perdition) if OpenSSL has switched off "EC" by OPENSSL_NO_EC in compile time config
* Thu Aug 15 2017 - Thomas Wagner
- bump to version 2.2 (perdition)
- bump to version 0.0.13 (libvanessa_logger_version)
* Thu May 21 2015 - Thomas Wagner
- bump to version 2.1
* Sun Feb 26 2012 - Thomas Wagner
- calculate perditionparentversionips for IPS use (numbers only, straight incremental)
* Mon Aug 02 2010 - Thomas Wagner
- add library version numbers (must be updated manually for now)
* Fri Jul  9 2010 - Thomas Wagner
- make the base download-directory maintained centrally

