##TODO## pre-set for Solaris where ffmpeg, vlc, flvstreamer, 
##TODO## add dependencies (optional)

#
# spec file for package SFEmediathek
#

%include Solaris.inc

%define src_name  mediathek
%define subdir    mediathek
%define docversion 2.6.0

%define _use_internal_dependency_generator 0

Name:                    SFEmediathek
IPS_package_name:        media/mediathek
Group:                   Applications/Sound and Video
Summary:                 mediathek - download TV broadcasters online offers, download podcasts
URL:                     http://zdfmediathk.sourceforge.net/
Version:                 11
Source:                  %{sf_download}/project/zdfmediathk/Mediathek/Mediathek\ %{version}/MediathekView_%{version}.zip
Source2:                 %{sf_download}/project/zdfmediathk/Mediathek/Mediathek\ %{docversion}/Kurzanleitung_%{docversion}.pdf


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc

%description
Das Programm durchsucht die Mediathek verschiedener Sender (ARD, ZDF, Arte, 3Sat, MDR, NDR, ORF, SF), laedt Beitraege mit einem Programm eigener Wahl und kann Themen als Abos anlegen und neue Beitraege automatisch downloaden. Es gibt auch eine Moeglichkeit, Podcast zu verwalten und zu Downloaden.


%prep
%setup -c -q -n %{src_name}-%version
cp -p %{SOURCE2} .

%build
#nothing to do

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p             $RPM_BUILD_ROOT%{_basedir}/lib/%{subdir}/
cp -p  MediathekView.jar $RPM_BUILD_ROOT%{_basedir}/lib/%{subdir}/
cp -pr lib/          $RPM_BUILD_ROOT%{_basedir}/lib/%{subdir}/
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
echo "java -jar "%{_basedir}/lib/%{subdir}/"MediathekView.jar" > $RPM_BUILD_ROOT%{_bindir}/%{src_name}
chmod a+rx $RPM_BUILD_ROOT%{_bindir}/%{src_name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc Kurzanleitung_%{docversion}.pdf 
#%doc Anleitung.pdf 
%dir %attr (0755, root, bin) %{_basedir}/lib/%{subdir}/
%{_basedir}/lib/%{subdir}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}


%changelog
* Thu Mar 27 2016 - Thomas Wagner
- bump to version 11
* Thu Mar 26 2015 - Thomas Wagner
- bump to version 9
* Mon Dec 15 2014 - Thomas Wagner
- bump to version 8
* Sun Jul 20 2014 - Thomas Wagner
- bump to version 7
* Sun May 11 2014 - Thomas Wagner
- bump to 6 - Bug fixes (delete temprary files)
* Mon Apr  7 2014 - Thomas Wagner
- bump to 5
* Sun Mar 23 2014 - Thomas Wagner
- bump to 4.0.0.1 respin to avoid invalid UTF-8 in %description
- use IPS_component_version instead version bump
* Thu Mar 20 2014 - Thomas Wagner
- bump to 4
* Thu Sep 19 2013 - Thomas Wagner
- bump to 3.3.0
* Sat Mar 23 2013 - Thomas Wagner
- bump to 3.2.1
* Sun Jan 27 2013 - Thomas Wagner
- add IPS_package_name, Group
* Wed Jan 23 2013 - Thomas Wagner
- bump to 3.1.0
* Mon May 14 2012 - Thomas Wagner
- bump to 3.0.0
*                 - Thomas Wagner
- bump to 2.5.0
*                 - Thomas Wagner
- bump to 2.1.2
* Sun Apr 25 2010 - Thomas Wagner
- bump to 2.1.2
* Sun Apr 25 2010 - Thomas Wagner
- Initial spec
