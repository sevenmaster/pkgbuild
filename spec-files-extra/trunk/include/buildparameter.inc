
%define _totalmemory 1024
%define _totalmemory %( /usr/sbin/prtconf | grep Memo | awk '{print $3}' )

%define _cpus        %( /usr/sbin/psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}' )

#if number of CPUS is greater then totalmemory/1024, then use memory/1024 as limiting factor to number of CPUS
#e.g. _cpus=16, _totalmemory=4096, then calculate _cpus_memory=4 instead of 16
%define _cpus_memory  %( test %{_cpus} -gt `expr %{_totalmemory} / 1024` ] && expr %{_totalmemory} '/' 1024  || echo %{_cpus} )




