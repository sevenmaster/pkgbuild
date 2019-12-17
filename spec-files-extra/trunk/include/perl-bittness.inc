
# include file for perl modules that involve linking against a binary object.
# example: perl-db_file linkgs against binary libraries of Berkely DB
# bittness of perl interpreter (32-bit or 64-bit) requires to link against matching bittness of external library files

#perl -V | grep gcc
#    config_args='-de -Dmksymlinks -Ulocincpth= -Uloclibpth= -Dbin=/usr/perl5/5.24/bin -Dcc=/usr/gcc/4.9/bin/gcc -m64 -Dcf_email=oi-dev@openindiana.org -Dcf_by=perl-bugs -Dlibperl=libperl.so -Dmyhostname=localhost -Dprefix=/usr/perl5/5.24 -Dprivlib=/usr/perl5/5.24/lib -Dsitelib=/usr/perl5/site_perl/5.24 -Dsiteprefix=/usr/perl5/5.24 -Dvendorlib=/usr/perl5/vendor_perl/5.24 -Dvendorprefix=/usr/perl5/5.24 -Duse64bitall -Duseshrplib -Dusedtrace -Dusethreads -Dlibpth=/lib/64 /usr/lib/64'
#    cc='/usr/gcc/4.9/bin/gcc -m64', ccflags ='-D_REENTRANT -m64 -fwrapv -fno-strict-aliasing -pipe -fstack-protector-strong -D_LARGEFILE64_SOURCE -D_FORTIFY_SOURCE=2 -DPERL_USE_SAFE_PUTENV',
#    ccversion='', gccversion='4.9.4', gccosandvers=''
#    ld='/usr/gcc/4.9/bin/gcc -m64', ldflags =' -m64 -fstack-protector-strong '
#    libpth=/lib/64 /usr/lib/64 /usr/gcc/4.9/lib /usr/lib /usr/ccs/lib
#fix hipster used /usr/gcc/4.9/bin/gcc and we in SFE have different path
#solution 1) remove path compoment from cc and ld

export PERL_CC=$( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:cc | sed -e 's?cc=.??' -e 's?.;$??' )
if [ ! -x "${PERL_CC}" ]; then
  echo "ALARM es ist nicht vorhanden/ausfuehrbar  >>>${PERL_CC}<<<"
   #hipster '/usr/gcc/4.9/bin/gcc -m64'
   PERL_CC=$( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:cc | sed -e 's?cc=.??' -e 's?.;$??' )
   #hipster  '/usr/gcc/4.9/bin/gcc -m64'
   PERL_LD=$( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:ld | sed -e 's?ld=.??' -e 's?.;$??' )
   #PERL_CC=$( /usr/bin/basename $PERL_CC )
   #PERL_LD=$( /usr/bin/basename $PERL_LD )
   #test: (echo "/usr/gnu/bin/gcc -m64" ; echo "gcc -m64" ; echo "gcc") | sed -e 's?.*/??'
   PERL_CC=$( echo "${PERL_CC}" | sed -e 's?.*/??' )
   PERL_LD=$( echo "${PERL_LD}" | sed -e 's?.*/??' )
   echo "PERL CC:  >>>${PERL_CC}<<<"
   echo "PERL LD:  >>>${PERL_LD}<<<"
#   echo "PERL EXTRA FLAGS: >>--config cc=${PERL_CC}<<"

fi

%if %( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:cc | grep -w "cc='.*/*gcc *" >/dev/null && echo 1 || echo 0 )
echo "Setting cc_is_gcc to 1 and re-include base.inc >%{perl_cc}<"
%define cc_is_gcc 1
%include base.inc
%endif
 

#fetch default values, then modify them if needed in the %if %{perl_bitness_64} section
export OPTFLAGS_LOCAL="%{optflags}"

#fetch default values, then modify them if needed in the %if %{perl_bitness_64} section
# omnios  -  perl -V:lddlflags
# 64-bit, missing /amd64:  lddlflags='-G -64 -shared -m64 -L/usr/gnu/lib ';
# solaris 11.3
# 32-bit                :  lddlflags='-G -L/usr/lib -L/usr/ccs/lib  -L/lib -L/usr/gnu/lib';
export LDDLFLAGS=$( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:lddlflags | sed -e 's?lddlflags=.??' -e 's?.;$??' )

#fetch default values, then modify them if needed in the %if %{perl_bitness_64} section
# omnios  -  perl -V:cccdlflags
# cccdlflags='-fPIC';
export CCCDLFLAGS=$( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:cccdlflags | sed -e 's?cccdlflags=.??' -e 's?.;$??' )


%if %{perl_bitness_64}
echo "perl_bitness is %{perl_bitness}"
%include arch64.inc

#obsolete %define gnu_lib_path %( echo -L%{gnu_lib} -R%{gnu_lib} | sed -e 's?/lib?/lib/%{_arch64}?g' )


#if sfe sets 32-bit in FLAGS, then we need to change it to 64-bit
#obsolete export OPTFLAGS_LOCAL=$( echo '%{optflags}' | sed -e 's?-m32?-m64?g' -e 's?-32?-64?g' -e 's?-mincoming-stack-boundary=2??' )
export OPTFLAGS_LOCAL="%{optflags64}"

#we need to use the 64-bit subdirectory paths for libraries
if echo ${LDDLFLAGS} | egrep -- "-L/.*(/64|/%{_arch64})" >/dev/null; then
export LDDLFLAGS=$(  echo "${LDDLFLAGS}"  | gsed -e "/\/64\|\/%{_arch64}/! s?/lib?/lib/%{_arch64}?g" )
export CCCDLFLAGS=$( echo "${CCCDLFLAGS}" | gsed -e "/\/64\|\/%{_arch64}/! s?/lib?/lib/%{_arch64}?g" )
echo "Modified LDDLFLAGS and CCCDLFLAGS to print libdir for 64-bit)"
fi
%endif

echo "LDDLFLAGS:  >>>${LDDLFLAGS}<<<"
echo "CCCDLFLAGS: >>>${CCCDLFLAGS}<<<"
echo "OPTFLAGS_LOCAL: >>>${OPTFLAGS_LOCAL}<<<"

%changelog
* Tue Dec 17 2019 - Thomas Wagner
- set cc_is_gcc if PERL_CC is gcc and then re-include base.inc to get correct optflags (OM)
* Thu Feb 28 2019 - Thomas Wagner
- add OPTFLAGS_LOCAL to make, to get back some extra flags from before bittness include files have been introduced, improve 64-bit flags
- new ordering and setting default values for OPTFLAGS_LOCAL, LDDLFLAGS, CCCDLFLAGS
* Mon Jan 28 2019 - Thomas Wagner
- cut out from SFEperl-dbfile.spec, to be included in SFEperl-module-module.spec if binary objects are involved, then perl-interpreter bittness (32 or 64-bit) is important
