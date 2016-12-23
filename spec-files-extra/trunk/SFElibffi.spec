#
# spec file for package SFElibffi
#
# includes module(s): libffi
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define cc_is_gcc 1
%include usr-gnu.inc
%include base.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libffi_64 = libffi.spec
%endif

%include base.inc
%use libffi = libffi.spec

Name:		SFElibffi
IPS_Package_Name:	library/gnu/libffi
Summary:	 (/usr/gnu)
Group:		System/Multimedia Libraries
Version:	%{libffi.version}
URL:		https://sourceware.org/libffi/
License:        MIT
SUNW_Copyright:	%{name}.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SFEgcc
Requires:      SFEgccruntime

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libffi_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libffi.prep -d %name-%version/%{base_arch}

%build
export CC=gcc

%ifarch amd64 sparcv9
%libffi_64.build -d %name-%version/%_arch64
%endif

%libffi.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libffi_64.install -d %name-%version/%_arch64
%endif

%libffi.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%_libdir/libffi.so*
%ifarch amd64 sparcv9
%_libdir/%_arch64/libffi.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/info/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/libffi.pc
%_libdir/libffi-*
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %_libdir/%_arch64/pkgconfig
%_libdir/%_arch64/pkgconfig/libffi.pc
%_libdir/%_arch64/libffi-*
%endif

%changelog
* Thu Dec 23 2016 - Thomas Wagner
- initial spec version 3.2.1



COMPONENT_TEST_DIR =    $(@D)/testsuite

# The 32 test suite is trying various ABI (fastcall, thiscall, stdcall).
# We don't support those on Solaris.
COMPONENT_TEST_TRANSFORMS += \
        '-e "s|^Test Run By.*$$|XXX_REMOVE_XXX|g" ' \
        '-e "s|^Native configuration is.*$$|XXX_REMOVE_XXX|g" ' \
        '-e "s|^make.*: Leaving directory.*$$|XXX_REMOVE_XXX|g" ' \
        '-e "s|^make.*: Entering directory.*$$|XXX_REMOVE_XXX|g" ' \
        '-e "/^XXX_REMOVE_XXX$$/d" '

CFLAGS += -DFFI_MMAP_EXEC_WRIT=1

CONFIGURE_OPTIONS += --disable-raw-api

REQUIRED_PACKAGES += system/library/gcc/gcc-c-runtime


# Copyright (c) 2015, 2016, Oracle and/or its affiliates. All rights reserved.
#

<transform file path=usr.*/man/.+ -> default mangler.man.stability uncommitted>
set name=pkg.fmri \
    value=pkg:/library/libffi@$(IPS_COMPONENT_VERSION),$(BUILD_VERSION)
set name=pkg.summary value="Foreign Function Interface Library"
set name=pkg.description \
    value="The libffi library provides a portable, high level programming interface to various calling conventions."
set name=com.oracle.info.description value="Foreign Function Interface Library"
set name=com.oracle.info.tpno value=$(TPNO)
set name=info.classification \
    value=org.opensolaris.category.2008:System/Libraries
set name=info.source-url value=$(COMPONENT_ARCHIVE_URL)
set name=info.upstream-url value=$(COMPONENT_PROJECT_URL)
set name=org.opensolaris.arc-caseid value=PSARC/2008/542
set name=org.opensolaris.consolidation value=$(CONSOLIDATION)
file path=usr/lib/$(MACH64)/libffi-$(COMPONENT_VERSION)/include/ffi.h
file path=usr/lib/$(MACH64)/libffi-$(COMPONENT_VERSION)/include/ffitarget.h
link path=usr/lib/$(MACH64)/libffi.so target=libffi.so.6.0.4
link path=usr/lib/$(MACH64)/libffi.so.5 target=libffi.so.6
link path=usr/lib/$(MACH64)/libffi.so.5.0.10 target=libffi.so.6.0.4
link path=usr/lib/$(MACH64)/libffi.so.6 target=libffi.so.6.0.4
file path=usr/lib/$(MACH64)/libffi.so.6.0.4
file path=usr/lib/$(MACH64)/pkgconfig/libffi.pc
file path=usr/lib/libffi-$(COMPONENT_VERSION)/include/ffi.h
file path=usr/lib/libffi-$(COMPONENT_VERSION)/include/ffitarget.h
link path=usr/lib/libffi.so target=libffi.so.6.0.4
link path=usr/lib/libffi.so.5 target=libffi.so.6
link path=usr/lib/libffi.so.5.0.10 target=libffi.so.6.0.4
link path=usr/lib/libffi.so.6 target=libffi.so.6.0.4
file path=usr/lib/libffi.so.6.0.4
file path=usr/lib/pkgconfig/libffi.pc
file path=usr/share/man/man3/ffi.3
file path=usr/share/man/man3/ffi_call.3
file path=usr/share/man/man3/ffi_prep_cif.3
file path=usr/share/man/man3/ffi_prep_cif_var.3
license LICENSE license=MIT
~                                                                        
