
# set correct compiler options for the perl version on this system
%if %omnios
#perl built with gcc / g++
%define cc_is_gcc 1
%include base.inc
%endif


%changelog
* Thu Feb 28 2019 - Thomas Wagner
- initial - get correct initialization for compiler used to build perl - switch logic may need improvements

