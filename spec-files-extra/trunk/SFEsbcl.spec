#
# spec file for package: SFEsbcl
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# Do not bother building both x86 and amd64 binaries
# A possibility would be to give a choice of which one to build
# For now, settle for building x86, since that requires fewer
# modifications to the spec

%define build_64 0
%define src_version 1.3.1
%define bindist sbcl-1.2.7-x86-solaris

%include Solaris.inc

%if %build_64
%include arch64.inc
%define sbclarch x86-64
%use sbcl_64 = sbcl.spec
%endif
%include base.inc
%ifarch i386
%define sbclarch x86
%endif
%ifarch sparc sparcv9
%define src_version 1.0.23
%define bindist sbcl-1.0.23-sparc-solaris
%define sbclarch sparc
%endif
%use sbcl = sbcl.spec

Name:		SFEsbcl
IPS_Package_Name:	 runtime/sbcl 
Version:	%src_version
Summary:	Steel Bank Common Lisp
Group:		Development/Other Languages
License:	Public Domain/BSD
Url:		http://www.sbcl.org/
SUNW_BaseDir:	%{_basedir}
SUNW_Copyright:	%{name}.copyright
Source1:	%sf_download/sourceforge/sbcl/%bindist-binary.tar.bz2

%include default-depend.inc
BuildRequires: text/texinfo

Meta(info.upstream):		SBCL <sbcl-devel@lists.sourceforge.net>
Meta(info.upstream_url):	http://www.sbcl.org/
Meta(info.classification):	org.opensolaris.category.2008:Development/Other Languages

%description
Steel Bank Common Lisp (SBCL) is an open source (free software) compiler and
runtime system for ANSI Common Lisp. It provides an interactive environment
including an integrated native compiler, a debugger, and many extensions.

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
%if %build_64
mkdir %{name}-%{version}/%{_arch64}
%sbcl_64.prep -d %{name}-%{version}/%{_arch64}
%endif
mkdir %{name}-%{version}/%{base_arch}
%sbcl.prep -d %{name}-%{version}/%{base_arch}
cd %name-%version
bzip2 -dc %SOURCE1 | tar -xf -

%build
# Place /usr/bin in front of /usr/gnu/bin, because gnu nm produces an error
export PATH=/opt/dtbld/bin:/usr/bin:/usr/gnu/bin:/usr/sbin
%if %build_64
%sbcl_64.build -d %{name}-%{version}/%{_arch64}
%endif
%sbcl.build -d %{name}-%{version}/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%if %build_64
%sbcl_64.install -d %{name}-%{version}/%{_arch64}
mkdir $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
mv $RPM_BUILD_ROOT%{_bindir}/sbcl $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
mkdir $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
mv $RPM_BUILD_ROOT%{_libdir}/sbcl $RPM_BUILD_ROOT%{_libdir}/%{_arch64}
%endif

%sbcl.install -d %{name}-%{version}/%{base_arch}

%if %build_64
%ifarch i386
%if %can_isaexec
mkdir $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
mv $RPM_BUILD_ROOT%{_bindir}/sbcl $RPM_BUILD_ROOT%{_bindir}/%{base_isa}
cd $RPM_BUILD_ROOT%{_bindir}
ln -s ../lib/isaexec sbcl
%endif
%endif
%endif

rm %buildroot%_infodir/dir
rmdir %buildroot%_docdir/sbcl/html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%if %build_64
%ifarch amd64
%{_bindir}/%{_arch64}/sbcl
%{_libdir}/%{_arch64}/sbcl
%endif
%ifarch i386
%if %can_isaexec
# i386 and can isaexec
%{_bindir}/%{base_isa}/sbcl
%hard %{_bindir}/sbcl
%else
# i386 and can't isaexec
%{_bindir}/sbcl
%endif
%endif
%else
%_bindir/sbcl
%endif
%ifarch sparc sparcv9
# sparc
%{_bindir}/sbcl
%endif
%{_libdir}/sbcl
%attr(755,root,sys) %dir %{_datadir}
%attr(755,root,other) %dir %{_datadir}/doc
%{_datadir}/doc/sbcl
%{_mandir}/man1/sbcl.1
%_infodir

%changelog
* Sat Jan 23 2016 - Alex Viskovatoff <herzen@imap.cc>
- Update to 1.3.1; build documentation
- Eliminate multi-arch, which serves no useful purpose in this case
* Fri Jul 01 2011 - James Lee <jlee@thestaticvoid.com>
- Bump to version 1.0.49.
- Prepare for SFE inclusion.
* Wed Nov 25 2009 - James Lee <jlee@thestaticvoid.com>
- Bump to version 1.0.32
* Sun May 31 2009 - James Lee <jlee@thestaticvoid.com>
- Add header and correct copyright
* Sat May 30 2009 - jlee@thestaticvoid.com
- Initial version


Tests run for version 1.3.1 on i386:

Finished running tests.
Status:
 Skipped (broken):   debug.impure.lisp / (TRACE ENCAPSULATE NIL)
 Expected failure:   debug.impure.lisp / (TRACE-RECURSIVE ENCAPSULATE NIL)
 Skipped (broken):   exhaust.impure.lisp / (EXHAUST BASIC)
 Skipped (broken):   exhaust.impure.lisp / (EXHAUST NON-LOCAL-CONTROL)
 Skipped (broken):   exhaust.impure.lisp / (EXHAUST RESTARTS)
 Invalid exit status: gc.impure.lisp
 Expected failure:   packages.impure.lisp / USE-PACKAGE-CONFLICT-SET
 Expected failure:   packages.impure.lisp / IMPORT-SINGLE-CONFLICT
 Failure:            swap-lispobjs.impure.lisp / SWAP-LISPOBJS/PREPARE
 Failure:            swap-lispobjs.impure.lisp / SWAP-LISPOBJS
 (53 tests skipped for this combination of platform and features)
test failed, expected 104 return code, got 1
