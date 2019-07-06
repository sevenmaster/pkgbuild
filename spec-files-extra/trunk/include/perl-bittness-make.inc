
# include file for perl modules that involve linking against a binary object.
# example: perl-db_file linkgs against binary libraries of Berkely DB
# bittness of perl interpreter (32-bit or 64-bit) requires to link against matching bittness of external library files


#note: %{gnu_lib_path} is modified above to match the %{_arch} corresponding to perl's bitness
%if %( perl -V:cc | grep -w "cc='.*/*gcc *" >/dev/null && echo 1 || echo 0 )
  make CCCDLFLAGS="${CCCDLFLAGS} -I%{gnu_inc} %{gnu_lib_path}" OPTIMIZE="${OPTFLAGS_LOCAL}" LDDLFLAGS="${LDDLFLAGS} %{gnu_lib_path}" CC="${PERL_CC}" LD="${PERL_LD}" 

%else
  # make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC
  make  CC=$CC CCCDLFLAGS="${CCCDLFLAGS} -I%{gnu_inc}" OPTIMIZE="${OPTFLAGS_LOCAL}" LDDLFLAGS="${LDDLFLAGS} %{gnu_lib_path}" LD=$CC
%endif

else
  # style "Build.PL"
  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl Build.PL \
    --installdirs vendor --makefile_env_macros 1 \
    --install_path lib=%{_prefix}/%{perl_path_vendor_perl_version} \
    --install_path arch=%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    --install_path bin=%{_bindir} \
    --install_path bindoc=%{_mandir}/man1 \
    --install_path libdoc=%{_mandir}/man3 \
    --destdir $RPM_BUILD_ROOT \



  %{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl --config cc=${CC} Build build
fi

%changelog
* Sun Thu Feb 28 2019 - Thomas Wagner
- add OPTFLAGS_LOCAL to make, to get back some extra flags from before bittness include files have been introduced
* Mon Jan 28 2019 - Thomas Wagner
- cut out from SFEperl-dbfile.spec, to be included in SFEperl-module-module.spec if binary objects are involved, then perl-interpreter bittness (32 or 64-bit) is important
* Apr 21 2019 - Thomas Wagner
- initial - get correct initialization for compiler
