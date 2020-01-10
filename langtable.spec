%if 0%{?fedora}
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

Name:           langtable
Version:        0.0.31
Release:        4%{?dist}
Summary:        Guessing reasonable defaults for locale, keyboard layout, territory, and language.
Group:          Development/Tools
# the translations in languages.xml and territories.xml are (mostly)
# imported from CLDR and are thus under the Unicode license, the
# short name for this license is "MIT", see:
# https://fedoraproject.org/wiki/Licensing:MIT?rd=Licensing/MIT#Modern_Style_without_sublicense_.28Unicode.29
License:        GPLv3+
URL:            https://github.com/mike-fabian/langtable
Source0:        http://mfabian.fedorapeople.org/langtable/%{name}-%{version}.tar.gz
Patch0:         Revert-Make-eurlatgr-the-default-console-font-for-la.patch
Patch1:         Add-language-endonym-for-tl.patch
Patch2:         Some-translation-fixes-from-CLDR.patch
Patch3:         Translation-fix-from-Wikipedia.patch
Patch4:         Translation-fix-for-Tagalog-Filipino.patch
Patch5:         Translation-fix-from-CLDR.patch
Patch6:         Add-sphinx-markup-to-public-functions.patch
Patch7:         Add-a-function-list_scripts-to-list-scripts-used-for.patch
Patch8:         Make-tw-the-default-keyboard-layout-for-zh_TW.patch
BuildArch:      noarch
BuildRequires:  python2-devel
%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # if with_python3

%description
langtable is used to guess reasonable defaults for locale, keyboard layout,
territory, and language, if part of that information is already known. For
example, guess the territory and the keyboard layout if the language
is known or guess the language and keyboard layout if the territory is
already known.

%package python
Summary:        Python module to query the langtable-data
Group:          Development/Tools
License:        GPLv3+
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-data = %{version}-%{release}

%description python
This package contains a Python module to query the data
from langtable-data.

%if 0%{?with_python3}
%package python3
Summary:        Python module to query the langtable-data
Group:          Development/Tools
License:        GPLv3+
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-data = %{version}-%{release}

%description python3
This package contains a Python module to query the data
from langtable-data.

%endif # with_python3

%package data
Summary:        Data files for langtable
Group:          Development/Tools
License:        GPLv3+ and MIT
Requires:       %{name} = %{version}-%{release}

%description data
This package contains the data files for langtable.

%prep
%setup -q
%patch0 -p1 -b .Revert-Make-eurlatgr-the-default-console-font-for-la
%patch1 -p1 -b .Add-language-endonym-for-tl
%patch2 -p1 -b .Some-translation-fixes-from-CLDR
%patch3 -p1 -b .Translation-fix-from-Wikipedia
%patch4 -p1 -b .Translation-fix-for-Tagalog-Filipino
%patch5 -p1 -b .Translation-fix-from-CLDR
%patch6 -p1 -b .Add-sphinx-markup-to-public-functions
%patch7 -p1 -b .Add-a-function-list_scripts-to-list-scripts-used-for
%patch8 -p1 -b .Make-tw-the-default-keyboard-layout-for-zh_TW

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
perl -pi -e "s,_datadir = '(.*)',_datadir = '%{_datadir}/langtable'," langtable.py
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
perl -pi -e "s,_datadir = '(.*)',_datadir = '%{_datadir}/langtable'," langtable.py
%{__python3} setup.py build
popd
%endif # with_python3

%install
%{__python} setup.py install --skip-build --prefix=%{_prefix} --install-data=%{_datadir}/langtable --root $RPM_BUILD_ROOT
gzip --force --best $RPM_BUILD_ROOT/%{_datadir}/langtable/*.xml

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --prefix=%{_prefix} --install-data=%{_datadir}/langtable --root $RPM_BUILD_ROOT
popd
# the .xml files copied by the “python3 setup.py install” are identical
# to those copied in the “python2 setup.py install”,
# it does not hurt to gzip them again:
gzip --force --best $RPM_BUILD_ROOT/%{_datadir}/langtable/*.xml
%endif # with_python3

%check
(cd $RPM_BUILD_DIR/%{name}-%{version}/data; PYTHONPATH=.. %{__python} ../test_cases.py; %{__python} ../langtable.py)
%if 0%{?with_python3}
(cd $RPM_BUILD_DIR/%{name}-%{version}/data; LC_CTYPE=en_US.UTF-8 PYTHONPATH=.. %{__python3} ../test_cases.py; %{__python3} ../langtable.py)
%endif # with_python3
xmllint --noout --relaxng $RPM_BUILD_ROOT/%{_datadir}/langtable/schemas/keyboards.rng $RPM_BUILD_ROOT/%{_datadir}/langtable/keyboards.xml.gz
xmllint --noout --relaxng $RPM_BUILD_ROOT/%{_datadir}/langtable/schemas/languages.rng $RPM_BUILD_ROOT/%{_datadir}/langtable/languages.xml.gz
xmllint --noout --relaxng $RPM_BUILD_ROOT/%{_datadir}/langtable/schemas/territories.rng $RPM_BUILD_ROOT/%{_datadir}/langtable/territories.xml.gz
xmllint --noout --relaxng $RPM_BUILD_ROOT/%{_datadir}/langtable/schemas/timezoneidparts.rng $RPM_BUILD_ROOT/%{_datadir}/langtable/timezoneidparts.xml.gz
xmllint --noout --relaxng $RPM_BUILD_ROOT/%{_datadir}/langtable/schemas/timezones.rng $RPM_BUILD_ROOT/%{_datadir}/langtable/timezones.xml.gz

%files
%doc README COPYING ChangeLog unicode-license.txt test_cases.py
%dir %{_datadir}/langtable/
%{_datadir}/langtable/schemas

%files python
%{python_sitelib}/*

%if 0%{?with_python3}
%files python3
%{python3_sitelib}/*
%endif # with_python3

%files data
%dir %{_datadir}/langtable/
%{_datadir}/langtable/*.xml.gz

%changelog
* Fri May 10 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.31-4
- Make tw the default keyboard layout for zh_TW
- Resolves: rhbz#1708092

* Mon Jul 13 2015 Mike FABIAN <mfabian@redhat.com> - 0.0.31-3
- Add patches to support listing scripts for languages and/or regions
- Resolves: rhbz#1242571

* Tue Apr 28 2015 Mike FABIAN <mfabian@redhat.com> - 0.0.31-2
- Do not package the files in /usr/share/langtable/ twice
- Resolves: rhbz#1202875

* Wed Apr 01 2015 Mike FABIAN <mfabian@redhat.com> - 0.0.31-1
- Update langtable to 0.0.31
- Resolves: rhbz#1202875
- Revert change included in 0.0.31 which uses "eurlatgr" as the default
  consolefont for many languages because that font is not available in RHEL
- Remove patches which are already included in 0.0.31

* Mon Mar 16 2015 Mike FABIAN <mfabian@redhat.com> - 0.0.13-5
- Fix keyboard for sr_ME
- Resolves: rhbz#1190072

* Thu Jan 09 2014 Mike FABIAN <mfabian@redhat.com> - 0.0.13-4
- Add Add-support-for-timezone-translations.patch (Related: rhbz#1015209)
- Add Fix-Chinese-translation-problem.patch (Related: rhbz#1015209)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.0.13-3
- Mass rebuild 2013-12-27

* Thu Dec 12 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.13-2
- Change English translation for or from “Oriya” to “Odia” (Resolves: rhbz#1040778)

* Thu Sep 05 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.13-1
- Update to 0.0.13
- Serbian keyboards are 'rs' not 'sr' (by Vratislav Podzimek)

* Wed Aug 28 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.12-1
- Update to 0.0.12
- Match case insensitively in languageId() (Resolves: rhbz#1002000 (case insensitive languageId function needed))

* Mon Aug 19 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.11-1
- Update to 0.0.11
- Add translations for DE and NL territories in nds (reported by Vratislav Podzimek)

* Tue Aug 13 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.10-1
- Update to 0.0.10
- Add translations for Belarusian and Belarus in Latin script (reported by Vratislav Podzimek)

* Sat Aug 03 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.9-1
- Update to 0.0.9
- Add endonyms for pa_Arab (and pa_PK) and translation of country name for Pakistan for pa_Arab
- make languageId() return something even if a language name like "language (territory)" is given (Resolves: rhbz#986659 - some language name to its locale code failed)

* Tue Jul 30 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.8-1
- Update to 0.0.8
- Add endonym for Maithili
- Return True by default from supports_ascii (by Vratislav Podzimek)
- Add grc, eo, ak, GH, cop, dsb, fj, FJ, haw, hil, la, VA, ln, kg, CD, CG, AO, mos, BF, ny, MW, smj, tet, TL, tpi, PG (Resolves: rhbz#985332 - some language codes are missing)
- Import more translations from CLDR
- Give pa_IN.UTF-8 higher weight than pa_PK.UTF-8 (Resolves: rhbz#986658, rhbz#986155)

* Thu Jul 04 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.7-1
- Update to 0.0.7
- Add examples for list_consolefonts()
- Add a list_timezones() function
- Add functions languageId() and territoryId()
- Fix some translations of language names to get unique results returned by languageId()

* Wed Jun 12 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.6-1
- Update to 0.0.6
- Add RelaxNG schemas for the XML files (Vratislav Podzimek <vpodzime@redhat.com>)
- Use SAX instead of the ElementTree (Vratislav Podzimek <vpodzime@redhat.com>)
- Use 'trName' instead of 'name' for translated names (Vratislav Podzimek <vpodzime@redhat.com>)

* Fri Jun 07 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.5-1
- Update to 0.0.5
- Accept script names as used by glibc locales as well
- Support reading gzipped xml files
- Set ASCII support to “True” for cz and sk keyboard layouts

* Mon May 27 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.4-1
- Update to 0.0.4
- Remove backwards compatibility init() function
- Add ia (Interlingua), see https://bugzilla.redhat.com/show_bug.cgi?id=872423

* Thu May 16 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.3-1
- Update to 0.0.3
- Move the examples from the README to the source code
- Some tweaks for the translation of Serbian
- Prefix all global functions and global variables which are internal with “_”
- Rename country → territory, countries → territories in keyboards.xml
- Add keyboard “in(eng)” and make it the default for all Indian languages
- Add a comment stating which functions should be considered public API
- Add a supports_ascii() function
- Run Python’s doctest also on langtable.py, not only the extra test_cases.txt

* Fri May 10 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.2-1
- update to 0.0.2
- Prefer values for language, script, and territory found in languageId over those found in the other parameters

* Tue May 07 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.1-1
- initial package



