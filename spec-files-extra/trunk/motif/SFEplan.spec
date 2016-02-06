#
# spec file for package SFEplan
#

%include Solaris.inc
%define srcname plan

Name:		SFEplan
IPS_Package_Name:	motif/project-management/plan 
Summary:	A calendar and day planner
Group:		Applications/Office
Version:	1.10
URL:		http://www.bitrot.de/plan.html
Source:		ftp://ftp.fu-berlin.de/unix/X11/apps/plan/%srcname-%version.1.tar.gz
Source1:	plan-Makefile

BuildRequires:	library/motif

%prep
%setup -q -n %srcname-%version.1
# ./configure can only be run interactively, hence we saved an appropriate Makefile
cp %SOURCE1 src/Makefile

%build

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
cd src
make

%install
rm -rf %buildroot
cd src
make install DESTDIR=%buildroot

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_bindir
%_libdir/plan
