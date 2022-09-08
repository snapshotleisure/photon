%define debug_package %{nil}
%define __os_install_post %{nil}
%define gopath_comp github.com/containerd/containerd
Summary:        Containerd
Name:           containerd
Version:        1.6.6
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://containerd.io/docs/
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/containerd/containerd/archive/containerd-%{version}.tar.gz
%define sha512  containerd=f16f23384dbaa67075f2d35b7fc752938dd15601bbe3a919bc8eaa53fa1b2dea2e2d7f613a0f2f492910213dc2f7e96f0a1d38dde35bfb6d15f18167313f9817
# Must be in sync with package version
%define CONTAINERD_GITCOMMIT 10c12954828e7c7c9b6e0ea9b0c02b01407d3ae1

Patch1:         containerd-service.patch
Patch2:         build-bin-gen-manpages-instead-of-using-go-run.patch
Source2:        containerd-config.toml
Source3:        disable-containerd-by-default.preset

BuildRequires:  btrfs-progs
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
# Upstream is unhappy with 1.14. 1.13 or 1.15+ is OK
BuildRequires:  go >= 1.16
BuildRequires:  go-md2man
BuildRequires:  systemd-devel

Requires:       libseccomp
Requires:       systemd
# containerd 1.4.5 and above allow to use runc 1.0.0-rc94 and above.
# refer to v1.4.5/RUNC.md
Requires:       runc >= 1.0.0.rc94

%description
Containerd is an open source project. It is available as a daemon for Linux,
which manages the complete container lifecycle of its host system.

%package        extras
Summary:        Extra binaries for containerd
Group:          Applications/File
Requires:       %{name} = %{version}-%{release}

%description    extras
Extra binaries for containerd

%package        doc
Summary:        containerd
Requires:       %{name} = %{version}-%{release}

%description    doc
Documentation for containerd.

%prep
# Using autosetup is not feasible
%setup -q -c
mkdir -p "$(dirname "src/%{gopath_comp}")"
%patch1 -p1 -d %{name}-%{version}
%patch2 -p1 -d %{name}-%{version}
mv %{name}-%{version} src/%{gopath_comp}

%build
export GOPATH="$(pwd)"
# We still have to use the GOPATH mode, as containerd only supports go.mod
# starting 1.5.0+ However, this mode might be soon removed --
# https://github.com/golang/go/wiki/GOPATH

# Also, attempting to create go.mod and re-vendor would be wrong in this case,
# as it could overwrite patches to vendor/, as well as fetching un-release
# upstream versions. Typically, embargoed CVEs can cause those versions to be hiddden.
export GO111MODULE=off
cd src/%{gopath_comp}
make %{?_smp_mflags} VERSION=%{version} REVISION=%{CONTAINERD_GITCOMMIT} BUILDTAGS='seccomp selinux apparmor' binaries man

%install
cd src/%{gopath_comp}
install -v -m644 -D -t %{buildroot}%{_datadir}/licenses/%{name} LICENSE
install -v -m644 -D -t %{buildroot}%{_unitdir} containerd.service
install -v -m644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/containerd/config.toml
install -v -m644 -D %{SOURCE3} %{buildroot}%{_presetdir}/50-containerd.preset
make %{?_smp_mflags} DESTDIR=%{buildroot} PREFIX=%{_prefix} install
make %{?_smp_mflags} DESTDIR=%{buildroot} PREFIX=%{_prefix} install-man

%post
%systemd_post containerd.service

%postun
%systemd_postun_with_restart containerd.service

%preun
%systemd_preun containerd.service

%check
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
make %{?_smp_mflags} test
make %{?_smp_mflags} root-test
make %{?_smp_mflags} integration

%files
%defattr(-,root,root)
%{_bindir}/ctr
%{_bindir}/containerd
%{_bindir}/containerd-shim
%{_datadir}/licenses/%{name}
%{_unitdir}/containerd.service
%{_presetdir}/50-containerd.preset
%config(noreplace) %{_sysconfdir}/containerd/config.toml

%files extras
%defattr(-,root,root)
%{_bindir}/containerd-shim-runc-v1
%{_bindir}/containerd-shim-runc-v2
%{_bindir}/containerd-stress

%files doc
%defattr(-,root,root)
%doc
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
* Wed Sep 14 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.6.6-1
- Update to version 1.6.6 to fix containerd panic with cgroup v2
* Fri Sep 9 2022 Shivani Agarwal <shivania2@vmware.com> 1.4.13-4
- Enable selinux
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.13-3
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.13-2
- Bump up version to compile with new go
* Fri Jun 03 2022 Bo Gan <ganb@vmware.com> 1.4.13-1
- Upgrade to 1.4.13
- Fix CVE-2022-31030 with ExecSync API
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.12-4
- Bump up version to compile with new go
* Fri Feb 25 2022 Bo Gan <ganb@vmware.com> 1.4.12-3
- Fix CVE-2022-23648, disable go.mod (unsupported by 1.4.x)
- Restore REVISION= Makefile variable
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.12-3
- Bump up version to compile with new go
* Fri Feb 11 2022 Piyush Gupta <gpiyush@vmware.com> 1.4.12-2
- Bump up version to compile with new go
* Mon Dec 13 2021 Nitesh Kumar <kunitesh@vmware.com> 1.4.12-1
- Upgrading to 1.4.12 to use latest runc.
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.4.4-8
- Bump up version to compile with new go
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.4.4-7
- Bump up version to compile with new go.
* Fri Oct 01 2021 Bo Gan <ganb@vmware.com> 1.4.4-6
- Fix CVE-2021-41103
* Fri Jul 16 2021 Bo Gan <ganb@vmware.com> 1.4.4-5
- Fix CVE-2021-32760
- Refactor containerd.service patching and installation
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.4.4-4
- Bump up version to compile with new go
* Thu May 27 2021 Bo Gan <ganb@vmware.com> 1.4.4-3
- Bump up release version to consume new runc dependency
* Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.4.4-2
- Bump up version to compile with new go
* Mon Mar 22 2021 Ankit Jain <ankitja@vmware.com> 1.4.4-1
- Update to 1.4.4
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.4.1-4
- Bump up version to compile with new go
* Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.4.1-3
- Bump up version to compile with new go
* Wed Oct 07 2020 Tapas Kundu <tkundu@vmware.com> 1.4.1-2
- Use latest runc
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.1-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
- Automatic Version Bump
* Tue Aug 27 2019 Shreyas B. <shreyasb@vmware.com> 1.2.8-1
- Initial version of containerd spec.
