
%define _totalmemory 1024
%define _totalmemory %( /usr/sbin/prtconf | grep Memo | awk '{print $3}' )

%define _cpus        %( /usr/sbin/psrinfo | gawk '$2=="on-line"{cpus++}END{print cpus==0?1:cpus}' )

#if number of CPUS is greater then totalmemory/1024, then use memory/1024 as limiting factor to number of CPUS
#e.g. _cpus=16, _totalmemory=4096, then calculate _cpus_memory=4 instead of 16
%define _cpus_memory_768  %( test %{_cpus} -gt `expr %{_totalmemory} / 768` ] && expr %{_totalmemory} '/' 768  || echo %{_cpus} )
%define _cpus_memory_1024  %( test %{_cpus} -gt `expr %{_totalmemory} / 1024` ] && expr %{_totalmemory} '/' 1024  || echo %{_cpus} )
%define _cpus_memory_1536  %( test %{_cpus} -gt `expr %{_totalmemory} / 1536` ] && expr %{_totalmemory} '/' 1536  || echo %{_cpus} )
%define _cpus_memory_2048  %( test %{_cpus} -gt `expr %{_totalmemory} / 2048` ] && expr %{_totalmemory} '/' 2048  || echo %{_cpus} )

%define _cpus_memory %{_cpus_memory_1024}

#sollte man "1" abziehen fuer das OS? Oder am Memory einen Sockelbetrag abziehen?

%changelog
* Fri Jan  5 2018 - Thomas Wagner
- add _cpus_memory_2048 (got out-of-memory with pstgresql-96 9.6.6
* Fri Dec 15 2017 - Thomas Wagner
- remove ( ) from gawk command (interpreted by old pkgbuild)
* Mon Feb 13 2017 - Thomas Wagner
- create _cpus_memory_768 / _cpus_memory_1024 / _cpus_memory_1536 to allow 1 CPU per 768MB or 1024MB or 1536MB, set default to 1 CPU per 1024MB
* Sun Jan  3 2016 - Thomas Wagner
- calculate _cpus_memory with less memory (one CPU count per 768 / 1024 / 1536 MB memory)
