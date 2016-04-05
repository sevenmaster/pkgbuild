
# put special cases here

##TODO## since library/python/setuptools-26                      0.9.6-0.175.3.0.0.30.0     i--
##       the name is without python"-2"  -> library/python/setuptools-26
%define pnm_buildrequires_library_python_setuptools_26 library/python-2/setuptools-26
%define pnm_requires_library_python_setuptools_26 library/python-2/setuptools-26

# SXCE with SUNW prefix   -->> name on 133/134 and up
# without SUNW prefix     -->> name on 133/134 and up
# new after rename big bang -> name on 133/134 and up

%changelog
* Tue Apr  5 2016 - Thomas Wagner
- prepare for IPS name change to library/python/setuptools-26 in S11.3 0.175.3.0.0.30.0
* Sat Jun 12 2010 - Thomas Wagner
- initial include file
