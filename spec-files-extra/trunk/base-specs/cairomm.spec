#
# spec file for package cairomm 
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:                    cairomm
License:		 LGPL
Group:			 System/Libraries
#see calling spec file Version:                 1.10.0
Version:	%{cairomm_osspecific_version}
Release:		 1
URL:                     http://cairographics.org/cairomm/
Source:                  http://cairographics.org/releases/cairomm-%{version}.tar.gz

%package devel
Summary:                 %{summary} - development files

%prep
%setup -q -n cairomm-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --sysconfdir=%{_sysconfdir} 	\
	    --disable-documentation
make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Copied the example programs and binaries for testing
#mkdir -p $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/pdf-surface
#cp examples/pdf-surface/main.cc $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/pdf-surface
#cp examples/pdf-surface/.libs/example_pdf_file $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/pdf-surface

#mkdir -p $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/png-file
#cp examples/png_file/main.cc $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/png-file
#cp examples/png_file/.libs/example_png_file $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/png-file

# mkdir -p $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/ps-surface
# cp examples/ps-surface/main.cc $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/ps-surface
# cp examples/ps-surface/.libs/example_ps_file $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/ps-surface

# mkdir -p $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/svg-surface
# cp examples/svg-surface/main.cc $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/svg-surface
# cp examples/svg-surface/.libs/example_svg_file $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/svg-surface

# mkdir -p $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/text-rotate
# cp examples/text-rotate/text-rotate.cc $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/text-rotate
# cp examples/text-rotate/.libs/text_rotate $RPM_BUILD_ROOT/%{_datadir}/doc/cairomm/examples/text-rotate

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat  1 Nov 2013 - Thomas Wagner
- move "Version:" to calling spec file and calculate version based on what osdistro provides for library/desktop/cairo
* Wed Oct 30 2013 - Alex Viskovatoff
- update to 1.10.0
* Fri Aug  5 2011 - Alex Viskovatoff
- update to 1.8.6
* Tue Feb 19 2008 - ghee.teo@sun.com
- Modified according to review comments.
* Fri Feb 08 2008 - ghee.teo@sun.com
- Modified SFEcairomm.spec to make SUNWcairomm.spec and cairomm.spec
