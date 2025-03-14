Name:           pycurl3
Version:        7.45.1
Release:        2%{?dist}
Summary:        A Python interface to libcurl
Group:          Development/Languages
License:        LGPLv2+ and an MIT/X
URL:            http://pycurl.sourceforge.net
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://pycurl.sourceforge.net/download/pycurl-%{version}.tar.gz
%define sha512 pycurl=05639d484aac6d6688677589e391975158c5ef778456a47df575ad13fb8bd0db67ff8f5a39bdd99d82a67926aca421c01e687eec9d4fd87f32822b492b429635

%if 0%{?with_check}
Patch0: Fix_makecheck.patch
%endif

BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-devel

%if 0%{?with_check}
BuildRequires: python3-setuptools
BuildRequires: vsftpd
BuildRequires: curl-libs
BuildRequires: python3-xml
%endif

Requires:       curl
Requires:       python3

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%package doc
Summary:    Documentation and examples for pycurl
Requires:   %{name} = %{version}-%{release}

%description doc
Documentation and examples for pycurl

%prep
# Using autosetup is not feasible
%autosetup -p1 -cn pycurl-%{version}
mv pycurl-*/* .
rm -r pycurl-*
rm -f doc/*.xml_validity
# removing prebuilt-binaries
rm -f tests/fake-curl/libcurl/*.so

%build
export CFLAGS="$RPM_OPT_FLAGS -DHAVE_CURL_OPENSSL"
%py3_build

%install
%py3_install
rm -rf %{buildroot}%{_datadir}/doc/pycurl
chmod 755 %{buildroot}%{python3_sitelib}/pycurl*.so

%if 0%{?with_check}
%check
export PYCURL_VSFTPD_PATH=vsftpd
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 nose nose-show-skipped bottle==0.12.16 flaky pyflakes
rm -f tests/multi_option_constants_test.py tests/ftp_test.py tests/option_constants_test.py tests/seek_cb_test.py
LANG=en_US.UTF-8  make test PYTHON=python%{python3_version} NOSETESTS="nosetests-3.4 -v"
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%files doc
%defattr(-,root,root)
%doc COPYING-LGPL COPYING-MIT RELEASE-NOTES.rst ChangeLog README.rst examples doc tests

%changelog
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 7.45.1-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 7.45.1-1
- Automatic Version Bump
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 7.43.0.6-4
- Bump up release for openssl
* Tue Nov 24 2020 Tapas Kundu <tkundu@vmware.com> 7.43.0.6-3
- Fix make check
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 7.43.0.6-2
- openssl 1.1.1
* Thu Sep 10 2020 Gerrit Photon <photon-checkins@vmware.com> 7.43.0.6-1
- Automatic Version Bump
* Mon Jul 27 2020 Tapas Kundu <tkundu@vmware.com> 7.43.0.5-1
- Update to 7.43.0.5
* Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 7.43.0-5
- Mass removal python2
* Mon Nov 12 2018 Tapas Kundu <tkundu@vmware.com> 7.43.0-4
- Fixed the make check.
* Mon Aug 14 2017 Chang Lee <changlee@vmware.com> 7.43.0-3
- Added check requires and fixed check
* Wed May 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 7.43.0-2
- Using python2 explicitly while building
* Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 7.43.0-1
- Upgrade to 7.43.0  and add pycurl3
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 7.21.5-5
- BuildRequires curl-devel.
* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 7.21.5-4
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.21.5-3
- GA - Bump release of all rpms
* Fri Apr 29 2016 Divya Thaluru <dthaluru@vmware.com> 7.21.5-2
- Removing prebuilt binaries
* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 7.21.5-1
- Upgrade version
* Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 7.19.5.1-2
- Added Doc subpackage. Removed chmod a-x for examples.
* Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 7.19.5.1
- Initial build.  First version
