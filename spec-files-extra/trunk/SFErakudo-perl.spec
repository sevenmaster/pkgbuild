#
# spec file for package SFErakudo
#

%include Solaris.inc
%define srcname rakudo-star
%define _pkg_docdir %_docdir/rakudo
%define srcvers 2015.09

Name:		SFErakudo
IPS_Package_Name:	runtime/rakudo
Summary:	A Perl 6 implementation using the Moar and Java virtual machines
URL:		http://www.rakudo.org/
Vendor:		Rakudo.org
Version:	2015.9
License:	Artistic License 2.0
Group:		Development/Perl
SUNW_Copyright:	rakudo.copyright
Source:		http://rakudo.org/downloads/star/%srcname-%srcvers.tar.gz
SUNW_BaseDir:	%_basedir
%include default-depend.inc
BuildRequires:	developer/java/jdk-8
Requires:	runtime/java/jre-8

%prep
%setup -q -n %srcname-%srcvers

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

# MoarVM does not presently build on Solaris because of
#	with #error "large files are not supported by libelf"
# See http://code.activestate.com/lists/perl6-compiler/8954/
# The patch given there did not lead to MoarVM getting built
#perl Configure.pl --backend=moar --gen-moar --prefix=%_prefix
perl Configure.pl --backend=jvm --gen-nqp
gmake -j$CPUS
gmake install DESTDIR=%buildroot

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %buildroot%_prefix
cp -r install/bin install/share %buildroot%_prefix

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%_bindir
%dir %attr (-, root, sys) %_datadir
%_datadir/nqp
%_datadir/perl6
%doc -d docs 2015-spw-perl6-course.pdf cheatsheet.txt CREDITS
%dir %attr (-, root, other) %_docdir


%changelog
* Fri Jan 29 2016 - Alex Viskovatoff <herzen@imap.cc>
- Update to 2015.09: rakudo no longer uses parrot VM, uses Moar and Java VMs now
- rename package from "rakudo-perl" to "rakudo"
* Tue Aug 30 2011 - Alex Viskovatoff
- Bump to 2011.07
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Sun May  1 2011 - Alex Viskovatoff
- Bump to 2011.04
* Fri Mar 11 2011 - Alex Viskovatoff
- Initial spec
