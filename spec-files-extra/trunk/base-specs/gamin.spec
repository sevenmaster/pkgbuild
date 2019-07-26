##TODO## use pnm_macros for OSDISTRO default python version


#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:	gamin
Version:	0.1.10
Source: http://people.gnome.org/~veillard/gamin/sources/gamin-%{version}.tar.gz

#imported from solaris userland
Source1: libgamin-1.3
Source2: gam_server.1

Patch1: gamin-01-all.patch
Patch2: gamin-02-gamin.patch
Patch3: gamin-03-const.patch

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1

#OmniOS 151030 says FIONREAD not defined. Look not be included by ioctl.h...
gsed -i.bak -e '/#include <sys\/inotify.h>/ a\
#include <sys/filio.h>' \
server/inotify-kernel.c


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

%if %cc_is_gcc
export CC=gcc
export CXX=g++
%endif

export CFLAGS="%optflags"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%_ldflags"


export DAEMON_LIBS="-lglib-2.0 -lgobject-2.0 -lgio-2.0"
export PYTHON_SITE_PACKAGES=%{_libdir}/python2.7/vendor-packages
#--with-python=$(PYTHON)
autoreconf -if
./configure --prefix=%{_prefix}	\
	--libdir=%{_libdir}	\
        --libexecdir=%{_libdir} \
	--mandir=%{_mandir}	\
	--enable-shared=yes	\
	--disable-static        \

gmake -j$CPUS


%install
make install DESTDIR=$RPM_BUILD_ROOT
# pythondir=%{_libdir}/python2.7/vendor-packages
#pythondir=$(PYTHON_VENDOR_PACKAGES)
#/usr/lib/python2.6/vendor-packages
#$(BUILD_DIR_64)/.built: COMPONENT_POST_BUILD_ACTION = ( \
#	cd $(@D)/python/.libs ; \
#	mkdir -p 64 ; \
#	cp _gamin.so 64 \
#)
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la

#Source1: libgamin-1.3
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3/
cp -p %{SOURCE1} ${RPM_BUILD_ROOT}%{_mandir}/man3/

#Source2: gam_server.1
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1/
cp -p %{SOURCE2} ${RPM_BUILD_ROOT}%{_mandir}/man1/


%clean

#solaris userland says:
chmod 777 $RPM_BUILD_ROOT/*/python/tests/temp_dir &> /dev/null || true

#solaris userland says: # The tests can leave a socket behind, which makes the tests fail next time
rm -f /tmp/fam-$$LOGNAME/fam-test

#don't! rm -rf $RPM_BUILD_ROOT


%changelog
* Fri Jul 26 2019 - Thomas Wagner
- fix FIONREAD not found (root cause not identified) (OM 151030)
* Fri Nov 17 2017 - Thomas Wagner
- initial spec
/var/tmp/pkgbuild-sfe/SFEgamin-0.1.10-build/usr/lib/amd64/python2.7/site-packages/_gamin.so
