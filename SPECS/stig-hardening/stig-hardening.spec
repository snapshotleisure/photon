Summary:        VMware Photon OS 5.0 STIG Readiness Guide Ansible Playbook
Name:           stig-hardening
#Version x.y corresponds v<x>r<y> tag in the repo. Eg 1.1 = v1r1
Version:        1.1
Release:        1%{?dist}
License:        Apache-2.0
#Update this URL to github URL once the source code is available in github
URL:            https://packages.vmware.com/photon/photon_sources/1.0/%{name}-ph5-%{version}.tar.gz
Group:          Productivity/Security
Vendor:         VMware, Inc.
Distribution:   Photon

#Update this URL to github URL once the source code is available in github
Source0: https://packages.vmware.com/photon/photon_sources/1.0/%{name}-ph5-%{version}.tar.gz
%define sha512 %{name}-ph5-%{version}=414634c3e3023621fb19ca3a273d677e07745907b9f5c28f2eb01aaf060e9a79da17ee95c51cad24a33f00356e3d2ecfe153c6c73a0b5815c18ce9e297f905bf

Patch0: 0001-In-photon-5.0-.rpm.lock-file-path-has-changed.patch

BuildArch: noarch

Requires: ansible >= 2.14.2
Requires: ansible-community-general
Requires: ansible-posix
Requires: sshpass

%description
VMware Photon OS 5.0 STIG Readiness Guide Ansible Playbook

%prep
%autosetup -p1 -n %{name}-ph5-%{version}

%install
install -d %{buildroot}%{_datadir}/ansible/
cp -rp %{_builddir}/%{name}-ph5-%{version}/ %{buildroot}%{_datadir}/ansible/%{name}

%files
%defattr(-,root,root,-)
%{_datadir}/ansible/

%changelog
* Mon Jun 5 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1-1
- Initial version
