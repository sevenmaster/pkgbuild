#17:43 <@tomww> pfexec pkg install -nv libreoffice52-desktop-int
#17:44 <@tomww> yes
#17:44 < jimklimov> I'll see how my internet goes now... maybe can try :)
#17:45 <@tomww> if dryrun gets happy, then I think it'l just work in real. Interesting part will be if the libsmb downgrade with the version facet is still necessary.
#17:45 <@tomww> thank you!
#17:45 < jimklimov> i'm in the middle of relocation, so got a modem just today
#17:45 <@tomww> if libsmb version facet is still necessary, then the focus shifts to samba and libiconv
#17:45 <@tomww> no hurry please! :)
#17:45 < jimklimov> or so they called it... a several-hundred-megabit modem :\
#17:46 < jimklimov> well, gotta test what works here and what needs a chisel ;)
#17:46 <@tomww> yeah, you are in luck if your location has offerst of that kind. even in germany you sometimes you get only 1 or 3 Mbits downstream
#17:47 < jimklimov> I lived for 3 years in 40kbyte/s on good weather
#17:47 < jimklimov> and nothing when the hatches got wet
#17:48 < jimklimov> dryrun is upset about oi and sfe both providing libglew
#17:48 <@tomww> oh, so you got enough time for programming because loading a webpage gave you enough time between clicks, right
#17:48 < jimklimov> otherwise no complaints :)
#17:48 <@tomww> ah, very goot catch.
#17:48 < jimklimov> half a dozen of pairs like
#17:48 < jimklimov> The following packages all deliver file actions to usr/lib/libGLEWmx.so.1.13.0:
#17:48 < jimklimov>   pkg://localhostoih/sfe/library/libglew@1.13.0,5.11-0.0.151.1.8:20160108T184333Z
#17:48 < jimklimov>   pkg://openindiana.org/x11/library/libglew@1.13.0,5.11-2017.0.0.0:20170306T133728Z
#17:49 <@tomww> maybe the complaints appear in a later phase. I'll check for glew ... most likely just a rename of the package on the SFE_OI side.
#17:49 < jimklimov> or "pkg depend either of ... " :)
#17:49 <@tomww> it'l take some few days until I can make that
#17:50 < jimklimov> ok, good luck
#17:50 <@tomww> I think I'll find out soon. Last question, what is your system's version of those packages right now:
#17:51 <@tomww>  pkg info name osnet-incorporation entire | grep FMRI
#17:51 <@tomww> so I can replay here on the build-VM for SFE-OI package
#17:51  * jimklimov called back to the cupboards ;)
#17:51 < jimklimov> root@jimoi:/root# pkg info name osnet-incorporation entire | grep FMRI
#17:51 < jimklimov> pkg: info: no packages matching the following patterns you specified are
#17:51 < jimklimov> installed on the system.  Try querying remotely instead:
#17:51 < jimklimov>         entire
#17:51 < jimklimov>           FMRI: pkg://openindiana.org/consolidation/osnet/osnet-incorporation@0.5.11-2017.0.0.16923:20171223T005150Z
#17:51 < jimklimov>           FMRI: pkg://openindiana.org/release/name@0.5.11-2017.0.0.5:20171030T214925Z
#17:52 <@tomww> entire is uninstalled?
#17:52 < jimklimov> I guess I nuked entire back when that was fashionable :)
#17:52 <@tomww> entire is not not important to me.
#17:52 <@tomww> thank you, I'm now perfectly prepared.
#17:52 < jimklimov> not unimportant?
#17:52 < jimklimov> :)
#17:52 < jimklimov> good luck nailing this :)
#17:53 <@tomww> haha, thanks. It this is only glew, than it is manageable :)
#17:53 <@tomww> *If

#
# spec file for package SFElibglew
#
# includes module: glew
#
## TODO ##
#
##


%include Solaris.inc
%define cc_is_gcc 1
%include usr-gnu.inc
%include base.inc
%include packagenamemacros.inc

#%define major_version 1.12
#%define major_version 1.10
%define major_version 1.13
%define minor_version 0

%define src_name glew
%define src_url  http://downloads.sourceforge.net/%src_name/%major_version.%minor_version

Name:		SFElibglew
IPS_Package_Name:	sfe/library/libglew
Summary:	OpenGL Extension Wrangler Library (/usr/gnu/)
Group:		System/Libraries
URL:		http://glew.sourceforge.net/
Version:	%major_version.%minor_version
License:	LGPLv2.1+
Source:		%{src_url}/%src_name-%{version}.tgz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

# Requirements
#     GNU make
#     perl
#     wget
#     GNU sed
#     gcc compiler
#     git

BuildRequires:  SFEgcc
Requires:       SFEgccruntime

# Requires glu
# which Hipster has /x11/library/glu
# and OI has in x11/library/mesa

# # Warning, on hipster, glew.pc, requires glu.pc which requires something, which requires xcb.pc, which requires
# x11/library/libpthread-stubs which isn't installed by default. But LibreOffice configure tells you glew failed.
%if %{oihipster}
BuildRequires:	x11/library/libpthread-stubs
Requires:	x11/library/libpthread-stubs
%endif

%description
The OpenGL Extension Wrangler Library (GLEW) is a cross-platform
open-source C/C++ extension loading library. GLEW provides efficient
run-time mechanisms for determining which OpenGL extensions are
supported on the target platform. OpenGL core and extension
functionality is exposed in a single header file.

%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name



%prep
%setup -q -n glew-%version


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

export SYSTEM="solaris-gcc"
export GLEW_PREFIX="%{_prefix}"
export GLEW_DEST="%{_prefix}"

export LD=`which ld-wrapper`
[ -z "$LD" ] && LD=/usr/bin/ld

make LD="$LD" all


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT GLEW_PREFIX=%{_prefix} GLEW_DEST=%{_prefix} SYSTEM="solaris-gcc" install.all
rm $RPM_BUILD_ROOT%{_libdir}/*.*a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/visualinfo
%{_bindir}/glewinfo

%dir %attr (0755, root, bin) %_libdir
%_libdir/libGLEW.so*
%_libdir/libGLEWmx.so*

%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/glew.pc
%_libdir/pkgconfig/glewmx.pc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%_includedir/GL


%changelog
* Fri Jan 19 2018 - Thomas Wagner
- fix relocation in %install phase
* Sun Nov  6 2016 - Thomas Wagner
- relocate to /usr/gnu/ because (OIH) has its own libglew starting with 2016
  export GLEW_DEST="%{_prefix}"
* Fri Oct 23 2015 - Thomas Wagner
- merge in pjama's changes. Help finding LD on various build environments
* Sun Jun 14 2015 - pjama
- initial spec
#historic log, this looks like a major rewrite
* Sun Feb 12 2012 - Milan Jurik
- bump to 1.7.0
* Sat Mar 05 2011 - Milan Jurik
- bump to 1.5.8
* Sun Dec 19 2010 - Milan Jurik
- bump to 1.5.7
* Sat May 15 2010 - Milan Jurik
- Initial package
