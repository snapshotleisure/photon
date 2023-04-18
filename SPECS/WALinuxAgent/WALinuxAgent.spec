Name:           WALinuxAgent
Summary:        The Windows Azure Linux Agent
Version:        2.4.0.2
Release:        3%{?dist}
License:        Apache License Version 2.0
Group:          System/Daemons
Url:            https://github.com/Azure/WALinuxAgent
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/Azure/WALinuxAgent/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=ddabe0cd65a66a289dfa1db179c442f4e0e71dd3df429804844d3ebc8501484a1f3db4a7ada4177f88b3bd931299ce019aeca15a5c5f630c32c903bd6c6ef10c

Patch0:         Add-PhotonOS-support.patch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  systemd
BuildRequires:  python3-distro

Requires:       python3
Requires:       python3-libs
Requires:       python3-xml
Requires:       python3-pyasn1
Requires:       openssh
Requires:       openssl
Requires:       util-linux
Requires:       /bin/sed
Requires:       /bin/grep
Requires:       sudo
Requires:       iptables
Requires:       systemd
Requires:       python3-distro

BuildArch:      noarch

%description
The Windows Azure Linux Agent supports the provisioning and running of Linux
VMs in the Windows Azure cloud. This package should be installed on Linux disk
images that are built to run in the Windows Azure environment.

%prep
%autosetup -p1

%build
%py3_build

%install
%{python3} setup.py install --skip-build install -O1 --lnx-distro='photonos' --root=%{buildroot}

mkdir -p %{buildroot}%{_var}/log \
         %{buildroot}%{_var}/opt/waagent/log \
         %{buildroot}%{_var}/log

mkdir -p -m 0700 %{buildroot}%{_sharedstatedir}/waagent
touch %{buildroot}%{_var}/opt/waagent/log/waagent.log
ln -sfv /opt/waagent/log/waagent.log %{buildroot}%{_var}/log/waagent.log

%check
python3 setup.py check && python3 setup.py test

%post
%systemd_post waagent.service

%preun
%systemd_preun waagent.service

%postun
%systemd_postun_with_restart waagent.service

%files
%defattr(-,root,root)
%{_unitdir}/*
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/waagent
%attr(0755,root,root) %{_bindir}/waagent2.0
%config %{_sysconfdir}/waagent.conf
%dir %{_var}/opt/waagent/log
%{_var}/log/waagent.log
%ghost %{_var}/opt/waagent/log/waagent.log
%dir %attr(0700, root, root) %{_sharedstatedir}/waagent
%{python3_sitelib}/*

%changelog
* Tue Apr 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.4.0.2-3
- Add python3-distro to requires
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.4.0.2-2
- Bump up to compile with python 3.10
* Sat Nov 13 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.4.0.2-1
- Upgrade to version 2.4.0.2
* Mon Jan 11 2021 Tapas Kundu <tkundu@vmware.com> 2.2.51-1
- Version Bump
* Tue Oct 13 2020 Tapas Kundu <tkundu@vmware.com> 2.2.49.2-3
- Build with python 3.9
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.2.49.2-2
- openssl 1.1.1
* Fri Aug 28 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.49.2-1
- Automatic Version Bump
* Sun Jul 26 2020 Tapas Kundu <tkundu@vmware.com> 2.2.49-2
- Use python3.8
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.49-1
- Automatic Version Bump
* Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 2.2.35-3
- Use python3
* Wed Apr 29 2020 Anisha Kumari <kanisha@vmware.com> 2.2.35-2
- Added patch to fix CVE-2019-0804
* Tue Feb 12 2019 Tapas Kundu <tkundu@vmware.com> 2.2.35-1
- Update to 2.2.35
* Tue Oct 23 2018 Anish Swaminathan <anishs@vmware.com> 2.2.22-1
- Update to 2.2.22
* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  2.2.14-3
- Fixed the log file directory structure
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.14-2
- Requires /bin/grep, /bin/sed and util-linux or toybox
* Thu Jul 13 2017 Anish Swaminathan <anishs@vmware.com> 2.2.14-1
- Update to 2.2.14
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.0.18-4
- Use python2 explicitly to build
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.18-3
- GA - Bump release of all rpms
* Tue May 10 2016 Anish Swaminathan <anishs@vmware.com> 2.0.18-2
- Edit post scripts
* Thu Apr 28 2016 Anish Swaminathan <anishs@vmware.com> 2.0.18-1
- Update to 2.0.18
* Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> 2.0.14-3
- Removed redundant requires
* Thu Aug 6 2015 Anish Swaminathan <anishs@vmware.com>
- Added sha1sum
* Fri Mar 13 2015 - mbassiouny@vmware.com
- Initial packaging
