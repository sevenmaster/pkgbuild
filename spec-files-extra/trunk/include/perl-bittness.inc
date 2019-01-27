
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

PERL_CC=$( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:cc | sed -e 's?cc=.??' -e 's?.;$??' )
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
fi

%if %{perl_bitness_64}
echo "perl_bitness is %{perl_bitness}"
%define gnu_lib_path %( echo -L%{gnu_lib} -R%{gnu_lib} | sed -e 's?/lib?/lib/%{_arch64}?g' )
#omnios  -  perl -V:lddlflags
#64-bit, missing /amd64:  lddlflags='-G -64 -shared -m64 -L/usr/gnu/lib ';
#solaris 11.3
#32-bit                :  lddlflags='-G -L/usr/lib -L/usr/ccs/lib  -L/lib -L/usr/gnu/lib';
LDDLFLAGS=$( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:lddlflags | sed -e 's?lddlflags=.??' -e 's?.;$??' )
#omnios  -  perl -V:cccdlflags
# cccdlflags='-fPIC';
CCCDLFLAGS=$( %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:cccdlflags | sed -e 's?cccdlflags=.??' -e 's?.;$??' )

#(echo "-L/usr/gnu/lib"; echo "-L/lib/64"; echo "-L/usr/lib/amd64"; echo "-L/usr/lib/sparcv9"); echo ; (echo "-L/usr/gnu/lib"; echo "-L/lib/64"; echo "-L/usr/lib/amd64"; echo "-L/usr/lib/sparcv9") | gsed -e "/\/64\|\/%{_arch64}/! s?/lib?/lib/%{_arch64}?g"
#echo " -G -m64 -L/lib/64" ; echo "-G -64 -shared -m64 -L/usr/gnu/lib " )| gegrep -- "-L/.*(/64|/%{_arch64})"

if echo ${LDDLFLAGS} | egrep -- "-L/.*(/64|/%{_arch64})" >/dev/null; then
LDDLFLAGS=$(  echo "${LDDLFLAGS}"  | gsed -e "/\/64\|\/%{_arch64}/! s?/lib?/lib/%{_arch64}?g" )
CCCDLFLAGS=$( echo "${CCCDLFLAGS}" | gsed -e "/\/64\|\/%{_arch64}/! s?/lib?/lib/%{_arch64}?g" )
echo "Modified LDDLFLAGS and CCCDLFLAGS to print libdir for 64-bit)"
echo "LDDLFLAGS:  >>>${LDDLFLAGS}<<<"
echo "CCCDLFLAGS: >>>${CCCDLFLAGS}<<<"
fi
%endif

%changelog
* Mon Jan 28 2019 - Thomas Wagner
- cut out from SFEperl-dbfile.spec, to be included in SFEperl-module-module.spec if binary objects are involved, then perl-interpreter bittness (32 or 64-bit) is important
