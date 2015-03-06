#
# spec file for package SFEqt-gpp
#

################################################################################
# NOTE: Applications that use JavaScript and have it enabled currently crash.  #
################################################################################

##TODO## verify new pnm_macro mysql dependencies on different osbuild/osdistro
##TODO## re-visit disabled (Build)Requires with check-deps script

%define _basedir /usr/g++
%define standard_prefix /usr
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define srcname qt-everywhere-opensource-src
%define run_autotests 0

%include packagenamemacros.inc

Name:                SFEqt-gpp
IPS_Package_Name:	library/desktop/g++/qt
Summary:             Cross-platform development framework/toolkit (g++)
Group:               Desktop (GNOME)/Libraries
URL:                 http://qt-project.org
License:             LGPLv2
Version:             4.8.5
Source:              http://download.qt-project.org/official_releases/qt/4.8/%version/%srcname-%version.tar.gz
Source1:	     qt-webkit-StackBounds.cpp

# These were obtained from http://solaris.bionicmutton.org/hg/kde4-specs-470/file/db0a8c7904f6/specs/gcc/patches/qt
# patches only got new names on Aug  2 2011 and moved out of subdirectory patches/qt-gpp/
Patch1:		qt-gpp-01-gc-sections.diff
#Patch2:		qt-gpp-02-MathExtras.diff
# For Patch3, we use our own, which sets the SFE /usr/g++ paths
# see pkgbuild.wiki.osurceforce.net for the directory layout (g++)
Patch3:		qt-gpp-03-qmake.SFE.diff
%if %{run_autotests}
Patch4:		qt-gpp-04-tests-auto-qwidget_window.diff
#from upstream
Patch5:		qt-gpp-05-auto-tests-qhttpnetworkconnection.diff
%endif
# patch2 and patch6: bundled webkit  std::isinf std::isnan ...
# This is required to build with gcc 4.6.0/4.6.1 and up.
# note the fixes found on the web aren't complete 
# (gcc 4.5.3 *or* 4.6.1 works, never both)
# our fix enables both. 
Patch6:		qt-gpp-06-isnan.diff
#Patch7:		qt-gpp-07-471-shm.diff
#Patch8:		qt-gpp-08-QPixmap-warning.diff
Patch9:		qt-gpp-09-qdbus.patch
Patch10:		qt-gpp-10-yield.diff
Patch11:		qt-gpp-11-pthread_getattr.diff
Patch12:		qt-gpp-12-plt.diff
Patch13:		qt-gpp-13-fix-namespace-tr1.diff
Patch14:		qt-gpp-14-webcore-sql.patch

SUNW_Copyright:	     qt.copyright
SUNW_BaseDir:        %_basedir
%include default-depend.inc

%if %( expr %{solaris12} '|' %{omnios} )
#assume that use gcc 4.8.x
BuildRequires:		SFEgcc
Requires:		SFEgccruntime
%else
BuildRequires:		SFEgcc-46
Requires:		SFEgccruntime-46
%endif

# Guarantee X/freetype environment concisely (hopefully):
BuildRequires: SUNWgtk2
Requires:      SUNWgtk2
BuildRequires: %{pnm_buildrequires_SUNWxwplt}
Requires: %{pnm_requires_SUNWxwplt}
# The above bring in many things, including SUNWxwice and SUNWzlib
Requires: SUNWxwxft
# The above also pulls in SUNWfreetype2
# This package only provides libraries
BuildRequires: %{pnm_buildrequires_mysql_default}
Requires: %{pnm_requires_mysql_default}
BuildRequires: SUNWdbus
Requires: SUNWdbus

# Follow example of developer/icu for IPS package name
%package devel
IPS_package_name:	developer/desktop/g++/qt
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package doc
IPS_package_name:	library/desktop/g++/qt/documentation
Summary:        %{summary} - documentation files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{srcname}-%{version}

%if %{run_autotests}
# Unroll the extra source for the autotests
tar xzf %{SOURCE1}
%endif

# Don't pass --fuzz=0 to patch
%define _patch_options --unified
%patch1 -p1
%patch3
%patch6 -p1
%patch9
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%if %{run_autotests}
%patch4
%patch5
%endif
# Use StackBounds.cpp from WebKit trunk revision 151817, which is supposed
# to fix this bug: https://bugs.webkit.org/show_bug.cgi?id=114978
cp -p %SOURCE1 src/3rdparty/webkit/Source/JavaScriptCore/wtf/StackBounds.cpp


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

%define extra_includes -I/usr/include/dbus-1.0 -I/usr/lib/dbus-1.0/include -I/usr/include/libpng14 -I%{standard_prefix}/%{mysql_default_includedir}/mysql
%define extra_libs  -L%{standard_prefix}/%{mysql_default_libdir}/mysql -R%{standard_prefix}/%{mysql_default_libdir}/mysql

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -fPIC"
#export CXXFLAGS="%cxx_optflags -pthreads -fpermissive"
export CXXFLAGS="%cxx_optflags -pthreads"

#/usr/gcc/bin/gcc -v 2>&1| egrep "gcc version 4\."
$CC -v -v 2>&1| egrep "gcc version 4\.[7-]" && export CFLAGS="$CFLAGS -std=gnu++11" && export CXXFLAGS="$CXXFLAGS -std=gnu++11"

export LDFLAGS="%{_ldflags} -L/usr/g++/lib -R/usr/g++/lib %{gnu_lib_path} -pthreads -fPIC"

# Assume i386 CPU is not higher than Pentium 4
# This can be changed locally if your CPU is newer
./configure -prefix %{_prefix} \
           -confirm-license \
           -opensource \
           -platform solaris-g++ \
           -docdir %{_docdir}/qt \
	   -bindir %{_bindir} \
	   -libdir %{_libdir} \
           -headerdir %{_includedir}/qt \
           -plugindir %{_libdir}/qt/plugins \
           -datadir %{_datadir}/qt \
           -translationdir %{_datadir}/qt/translations \
           -examplesdir %{_datadir}/qt/examples \
           -demosdir %{_datadir}/qt/demos \
           -nomake examples \
           -nomake demos \
           -sysconfdir %{_sysconfdir} \
	   -webkit \
           -L /usr/gnu/lib \
           -R /usr/gnu/lib \
	   -optimized-qmake \
           -reduce-relocations \
           -opengl desktop \
           -shared \
           -plugin-sql-mysql \
           -no-3dnow \
           -no-ssse3 -no-sse4.1 -no-sse4.2 -no-avx \
           %extra_includes \
           %extra_libs


make -j$CPUS

%if %{run_autotests}
#running autotests. This requires a vncserver preconfigured.
#According to docs, we should have a KDE session running, so far it does not seem necessary for most of the tests.
export QTDIR=${PWD}
export QTSRCDIR=${PWD}
export PATH=${PWD}/bin:${PATH}

cd tests/auto

make
vncserver -kill :1 || true
vncserver :1
export DISPLAY=:1
./test.pl . U
vncserver -kill :1
#hopefully this will break the build
#false
%endif


%install
rm -rf %buildroot

make install INSTALL_ROOT=%buildroot

rm %buildroot%_libdir/*.la
rm -rf %buildroot%_prefix/examples
rm -rf %buildroot%_prefix/demos
rm -rf %buildroot%_prefix/tests

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
#devel %dir %attr (0755, root, bin) %{_bindir}
#devel %{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/lib*.prl
%dir %attr (0755, root, bin) %{_libdir}/qt
%{_libdir}/qt/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/qt/phrasebooks
%{_datadir}/qt/translations

%files devel
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, other) %{_includedir}/qt
%{_includedir}/qt/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig 
%{_libdir}/pkgconfig/*
%{_libdir}/libQtUiTools.a
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/qt/mkspecs
%dir %attr (0755, root, other) %{_prefix}/imports
%{_prefix}/imports/*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/qt/q3porting.xml
%{_datadir}/qt/demos/*
%{_datadir}/qt/examples/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*


%changelog
* Fri Mar  6 2015 - Thomas Wagner
- change (Build)Requires to SFEgcc / SFEgcc-runtime (4.8.x) (S12, OM)
* Sun Nov  3 2013 - Alex Viskovatoff <herzen@imapmail.org>
- use WebKit source for one JavaScript source file, as a partial fix for crashes
* Sun Oct 27 2013 - Alex Viskovatoff
- bump to 4.8.5
- do not compile with use of AVX instructions
- unconditionally do not compile 3DNow! instructions: AMD has dropped support
- do not hardcode path of gcc
* Sun Jun 30 2013 - Thomas Wagner
- add patch13 qt-gpp-13-fix-namespace-tr1.diff - or get TypeTraits.h:173:69: error: 'std::tr1' has not been declared with gcc 4.7.x __GXX_EXPERIMENTAL_CXX0X__
- for the time now, BuildRequires SFEgcc-46 and SFEgcc-46-runtime to get around errors when compiling with c++11 enabled gcc 4.7.x
* Mon Jan 21 2013 - Thomas Wagner
- align SFEqt-gpp.spec and SFEqt.spec
* Wed Dec  5 2012 - Logan Bruns <logan@gedanken.org>
- updated to 4.8.4.
* Mon Jul  9 2012 - Thomas Wagner
- fix finding a spec providing e.g. SFEqt-gpp-devel (remove %name- from %package)
- force mysql inclusion as plugin -plugin-sql-mysql and add trailing "/mysql" to
  -I and -L -R paths
* Sat Jun 23 2012 - Thomas Wagner
- add back regular sub-packages with IPS-tags for -devel and -doc
  to get back automatic dependencys with pkgtool on build farms
* Fri Jun 22 2012 - Logan Bruns <logan@gedanken.org>
- Use psrinfo -pv instead of prtdiag -v to detect CPU since only the
  former works in a zone.
* Wed Feb  2 2011 - James Choi
- add no3dnow for Intel cpus, build fpic
* Wed Jan  4 2011 - Alex Viskovatoff
- do not delete libQtUiTools.a (there is no libQtUiTools.so)
* Mon Nov  7 2011 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWxwplt}
* Wed Nov  2 2011 - Alex Viskovatoff
- update to 4.7.4, reworking two patches and adding another
* Tue Aug 16 2011 - Thomas Wagner
- need -R /usr/g++/lib and -R /usr/gnu/lib earlier in RUNPATH, via LDFLAGS,
  needs updated SFEgcc patch gcc-03-gnulib.diff to work
* Tue Aug  8 2011 - Thomas Wagner
- fix typo in mysql include and lib paths - "{}" in wrong position, correct variable name
- define standard_prefix /usr , used for mysql paths
* Tue Aug  6 2011 - Thomas Wagner
- move patches out of subdir qt-gpp/ and rework patches,
  works with unpatched pkgbuild 1.3.103
- patch2 and patch6 tested with gcc 4.3.3/4.5.1/4.6.1
- add  -fpermissive to CXXFLAGS
- pnm_macro to specify mysql dependencies
- removed dependencies, need check-deps and re-added those needed
* Tue Aug  2 2011 - Thomas Wagner
- relocate and rename patches to regular SFE naming convention name-<nn>-subject.diff
  (no changes in content)
- add mysql_default macros
- rework (Build)Requires according to check-deps
- rework patch6 qt-gpp-06-isnan.diff to only be effective for __GNUC__ >=4 __GNUC_MINOR__ >= 6
* Sun Jul 31 2011 - Alex Viskovatoff <hezen@imap.cc>
- Add two patches fixing WebKit; stop deleting imports/
- Enable exceptions, so that libQtXmlPatterns gets built
- Rename to SFEqt-gpp.spec
* Tue Jul 26 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Mon Jul 18 2011 - Alex Viskovatoff <hezen@imap.cc>
- Add patch qt-isnan.diff to enable building with gcc 4.6
* Sat Jul  2 2011 - Alex Viskovatoff <hezen@imap.cc>
- Add missing dependency on SFEgcc
* Sat Jun 25 2011 - Alex Viskovatoff <hezen@imap.cc>
- Use patches from kde-solaris instead of those inherited from SFEqt47.spec
- Bump to 4.7.3
* Wed Mar 30 2011 - Alex Viskovatoff
- update to 4.7.2; create separate doc package
* Tue Mar 29 2011 - Thomas Wagner
- re-add %package and %files -n %name-devel, easier to have a complete package
- change BuildRequires to %{pnm_buildrequires_library_desktop_gtk1}
* Mar 23 2011 - Alex Viskovatoff
- Use /usr/g++ as basedir, not sharing headers with stdcxx anymore
* Feb  8 2011 - Alex Viskovatoff
- Use /usr/stdcxx as basedir; use -pthreads
* Jan 30 2011 - Alex Viskovatoff
- Do not bother with a separate devel SVr4 package, as it is only 50 K
* Nov 30 2010 - Alex Viskovatoff
- Fork SFEqt47-gpp.spec off SFEqt47.spec, not packaging files in
  _datadir, _include_dir, and _bindir.  Those are in SFEqt47.
* Nov 17 2010 - Alex Viskovatoff
- Add patch by russiane39 to correctly use libpng14 headers under snv_151
  and adding some configure options
* Nov 11 2010 - Alex Viskovatoff
- Fork SFEqt47.spec off SFEqt4.spec, disregarding stlport and snv < 147
- To make the build work, disable examples and phonon.  Disable demos
  because that is what kde-solaris does.
* Nov  4 2010 - Alex Viskovatoff
- Spec needs "%include osdistro.inc" (pointed out by Thomas Wagner)
* Nov  3 2010 - Alex Viskovatoff
- Add patch by Milan Jurik to use new libpng names only for osbuild >= 147
- Use cxx_optflags
* Oct 16 2010 - Alex Viskovatoff
- Fix broken use of stlport: if -library=stlport4 is passed to the compiler,
  it must also be passed to the linker
- Update to version 4.5.3, obviating the need for the existing patches
- Add a patch to use changed field names in libpng-1.4
- Use stdcxx instead of stlport, while allowing use of the deprecated
  stlport as an option. (BionicMutton uses stdcxx.)
- Remove dependency on SUNWgccruntime
* Mar 07 2009 - Thomas Wagner
- rework shared patch qt-01-use_bash.diff (to be more independent of qt version SFEqt SFEqt4 in verison 4.x / 4.5)
* Wed Mar 04 2009 - Thomas Wagner
- fix path to SunStudio compiler. Tested with SunStudioExpress November 2008 in /opt/SUNWspro/bin
- enable configure's hint -no-exceptions (smaller code, less memory)
* Sat Nov 29 2008 - dauphin@enst.fr
- Try to compile with studio12
* Mon Nov 24 2008 - alexander@skwar.name
- Add qt-01-use_bash.diff, which replaces all calls to sh with bash,
  because Qt won't build when sh isn't bash.
  Cf. http://markmail.org/message/hzb3fypsc5sopf2b ff. and there
  http://markmail.org/message/l7yleonbjqnl7nfv
- Remove tarball_version - version is good enough
* Sun Nov 11 2008 - dick@nagual.nl
- Bump to 4.4.3
* Sun Sep 21 2008 - dick@nagual.nl
- Bump to 4.4.2
* Tue May 13 2008 - nonsea@users.sourceforge.net
- Bump to 4.4.0
* Fri Mar 21 2008 - nonsea@users.sourceforge.net
- Bump to 4.4.0-rc1
- Remove upstreamed patch time.diff
* Fri Mar 21 2008 - nonsea@users.sourceforge.net
- Bump to 4.4.0-beta1, and update %files
- Add patch time.diff
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
- Bump to 4.2.3
* Thu Dec 07 2006 - Eric Boutilier
- Initial spec
