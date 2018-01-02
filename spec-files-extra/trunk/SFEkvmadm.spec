#
# spec file for package SFEkvmadm.spec
#
# includes module(s): kvmadm
#
%include Solaris.inc
%include packagenamemacros.inc

%if %( expr %{omnios} '+' %{oihipster} '=' 0 )
# every other osdistro: "Error: only supported on OmniOS or OpenIndiana"
exit 254
%endif

#consider switching off dependency_generator to speed up packaging step
#if there are no binary objects in the package which link to external binaries
%define _use_internal_dependency_generator 0

%define src_name	kvmadm

Name:                   SFEkvmadm
IPS_Package_Name:	system/management/kvmadm
Summary:                Manage KVM instances under SMF control
Version:                0.12.2
URL:			http://kvmadm.org
Source:                 http://github.com/hadfl/kvmadm/releases/download/v%{version}/kvmadm-%{version}.tar.gz
License:		GPLv3
SUNW_Copyright:		%{license}.copyright
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#dependencies
#SFEperl-test-pod	#added
#SFEperl-module-build	#updated by chance
#SFEperl-data-processor	#added
#SFEperl-dist-milla	#added
#SFEperl-dist-zilla	#added
#SFEperl-illumos-smf	#added
#SFEperl-illumos-zones.spec	#added

#SFEperl-illumos-smf	#added
#it is the last in the depencency chain and pulls in the above
BuildRequires: SFEperl-illumos-smf
Requires:      SFEperl-illumos-smf
#only if perl from os is <= 5.24.x
BuildRequires: SFEperl-json
Requires:      SFEperl-json
BuildRequires: SFEperl-json-xs
Requires:      SFEperl-json-xs
#new perl has own JSON::PP, file conflict /usr/bin/json_pp
%if %( expr %{perl_version_padded}.0 '<' 0005002400000000.0 )
BuildRequires: SFEperl-json-pp
Requires:      SFEperl-json-pp
%endif

%description
http://kvmadm.org
kvmadm takes care of setting up kvm instances on illumos derived operating systems with SMF support. The kvm hosts run under smf control. Each host will show up as a separate SMF service instance. kvmadm supports KVM instances set-up as SMF service instance within individual zones.

This tool should run on OmniOS and OpenIndiana.

Please use your internet search engine for instructions on how to use the tool and provision KVM instances.

%prep
%setup -q -n %{src_name}-%{version}

%build

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

gmake V=2


#perl path
#lib path to own extensions
#dependencies come from IPS, not from this package
#uses Modules installed in /usr/perl5/vendor_perl/5.24.1/ so we tie the perl binary to that version too
perl -pi -e 's:^#! */usr/bin/env *perl.*:#!%{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl:' \
  bin/kvmadm \
  bin/system-kvm \
  probes/dns_probe \
  probes/ping_probe \

%{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -i -p -e 's{.*# PERL5LIB}{use lib qw(); # PERL5LIB}' bin/kvmadm bin/system-kvm
%{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -i -p -e 's{.*# LIBDIR}{use lib qw(/usr/lib); # LIBDIR}' bin/kvmadm bin/system-kvm
%{_prefix}/perl%{perl_major_version}/%{perl_version}/bin/perl -i -p -e 's{^my .*# RUNPATH}{my \$RUN_PATH = "/var/run"; # RUNPATH};' KVMadm/Config.pm

%install
rm -rf $RPM_BUILD_ROOT
#don't use gmake install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install -c bin/kvmadm bin/system-kvm probes/dns_probe probes/ping_probe $RPM_BUILD_ROOT/%{_bindir}

mkdir -p $RPM_BUILD_ROOT/%{_libdir}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/KVMadm
install -c -m 644  lib/KVMadm/Config.pm lib/KVMadm/Progress.pm lib/KVMadm/Utils.pm lib/KVMadm/Monitor.pm $RPM_BUILD_ROOT/%{_libdir}/KVMadm

#no, wo use system provided modules# cp -fr thirdparty/lib/perl5/* $RPM_BUILD_ROOT/%{_libdir}

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/man/man1
install -c -m 644 man/kvmadm.1 $RPM_BUILD_ROOT/%{_datadir}/man/man1

mkdir -p %{buildroot}%/lib/svc/manifest/system/
install -m 0644 smf/system-kvm.xml %{buildroot}%/lib/svc/manifest/system/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%dir %attr (0755,root,sys) %{_datadir}
%{_mandir}

%class(manifest) %attr(0444, root, sys) /lib/svc/manifest/system/system-kvm.xml



%changelog
* Tue Jan  2 2018 - Thomas Wagner
- put manifest into /lib/svc
* Fri Dec 15 2017 - Thomas Wagner
- bump to 0.12.2
- install SMF manifest system-kvm.xml
* Sun Dec  3 2017 - Thomas Wagner
- Initial version 0.12.1
