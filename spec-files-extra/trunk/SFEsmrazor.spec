#
# spec file for package SFEsmrazor
#
# includes module(s): smrazor
#
%include Solaris.inc

%define	src_name smrazor
%define _pkg_docdir %_docdir/%src_name

Name:                SFEsmrazor
IPS_Package_Name:	mail/smrazor
Summary:             SMRazor - Milter that checks mail messages using razor-check
License:             Unknown
Version:             0.2.1
URL:                 http://www.sapros.com/smrazor/
Source:              http://www.sapros.com/smrazor/smrazor-%{version}.tar.gz
Source2:             smrazor.xml
Patch1:        	     smrazor-01-bin-path.diff
Group:               Applications/System Utilities
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWsndmu
Requires:	SUNWsndmu

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%description
This is a Milter for Sendmail 8.12 that checks mail messages using
razor-check and rejects ones that are found in the razor database.

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
cp %{SOURCE2} smrazor.xml

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
            --sbindir=%{_sbindir}		\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --sysconfdir=%{_sysconfdir}		\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/sbin
cp smrazor $RPM_BUILD_ROOT/usr/sbin
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp smrazor.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/
mkdir -p ${RPM_BUILD_ROOT}/var/smrazor

%clean
rm -rf $RPM_BUILD_ROOT

%pre root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/groupadd smrazor';
  echo '/usr/sbin/useradd -d /var/lib/smrazor -s /bin/true -g smrazor smrazor';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%postun root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo '/usr/sbin/userdel smrazor';
  echo '/usr/sbin/groupdel smrazor';
) | $BASEDIR/var/lib/postrun/postrun -i -a

%actions
group groupname="smrazor"
user ftpuser=false gcos-field="SMRazor Reserved UID" username="smrazor" password=NP group="smrazor" home-dir="/var/smrazor"

%files
%defattr (-, root, bin)
%{_sbindir}

%files root
%defattr (-, root, sys)
%dir %attr (0755, smrazor, smrazor) %{_localstatedir}/smrazor
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/smrazor.xml

%changelog
* Thu Jan 31 2012 - Logan Bruns <logan@gedanken.org>
- initial version
