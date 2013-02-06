#
# spec file for package SFElibtextcat
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define src_name   libtextcat

Name:                SFElibtextcat
IPS_Package_Name:    text/library/libtextcat
Summary:             libTextCat - N-Gram-Based Text Categorization library
Version:             2.2
URL:                 http://software.wise-guys.nl/libtextcat/
Source:              http://software.wise-guys.nl/download/libtextcat-%{version}.tar.gz
License:      	     BSD
SUNW_Copyright:      SFElibtextcat.copyright
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:      SFEgcc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%description
Libtextcat is a library with functions that implement the
classification technique described in Cavnar & Trenkle, "N-Gram-Based
Text Categorization" [1]. It was primarily developed for language
guessing, a task on which it is known to perform with near-perfect
accuracy.

The central idea of the Cavnar & Trenkle technique is to calculate a
"fingerprint" of a document with an unknown category, and compare this
with the fingerprints of a number of documents of which the categories
are known. The categories of the closest matches are output as the
classification. A fingerprint is a list of the most frequent n-grams
occurring in a document, ordered by frequency. Fingerprints are
compared with a simple out-of-place metric. See the article for more
details.

Considerable effort went into making this implementation fast and
efficient. The language guesser processes over 100 documents/second on
a simple PC, which makes it practical for many uses. It was developed
for use in our webcrawler and search engine software, in which it it
handles millions of documents a day.

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_includedir}

cp src/textcat.h $RPM_BUILD_ROOT%{_includedir}

rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue Feb 5 2013 - Logan Bruns <logan@gedanken.org>
- initial version
