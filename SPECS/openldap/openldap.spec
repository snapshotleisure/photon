%global _default_patch_fuzz 2
%global debug_package       %{nil}

Summary:        OpenLdap-2.6.4
Name:           openldap
Version:        2.6.4
Release:        1%{?dist}
License:        OpenLDAP
URL:            https://www.openldap.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.openldap.org/software/download/OpenLDAP/openldap-release/%{name}-%{version}.tgz
%define sha512 %{name}=4be49c4866e47e96677d0e1f7caa380791917c9df8d6bb343d032aba45031c87db3bd4f6b953e914a1f40044fa68f4886ae96929a410b7188c0ed9bb75073a30

# Patch0 is downloaded from:
# https://www.linuxfromscratch.org/patches/blfs/svn
Patch0: %{name}-%{version}-consolidated-1.patch
Patch2: openldap-add-export-symbols-LDAP_CONNECTIONLESS.patch

Requires: openssl
Requires: cyrus-sasl
Requires: systemd

BuildRequires: cyrus-sasl-devel
BuildRequires: openssl-devel
BuildRequires: groff
BuildRequires: e2fsprogs-devel
BuildRequires: libtool
BuildRequires: systemd-devel

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.

%package devel
Summary: LDAP development libraries and header files
Requires: %{name} = %{version}-%{release}
Requires: cyrus-sasl-devel

%description devel
The openldap-devel package includes the development libraries and
header files needed for compiling applications that use LDAP
(Lightweight Directory Access Protocol) internals. LDAP is a set of
protocols for enabling directory services over the Internet. Install
this package only if you plan to develop or will need to compile
customized LDAP clients.

%prep
%autosetup -p1

%build
export CFLAGS="${CFLAGS} ${LDFLAGS} -Wl,--as-needed -DLDAP_CONNECTIONLESS"
%configure \
         $(test %{_host} != %{_build} && echo "CC=%{_host}-gcc --with-yielding-select=yes --with-sysroot=/target-%{_arch}") \
        --disable-static \
        --disable-slapd \
        --disable-ndb \
        --with-tls=openssl \
        --enable-debug \
        --enable-dynamic \
        --enable-syslog \
        --enable-ipv6 \
        --enable-local \
        --enable-crypt \
        --enable-spasswd \
        --enable-modules \
        --enable-backends \
        --enable-overlays=mod \
        --with-cyrus-sasl \
        --with-threads \
        --with-pic \
        --with-gnu-ld

if [ %{_host} != %{_build} ]; then
 sed -i '/#define NEED_MEMCMP_REPLACEMENT 1/d' include/portable.h
fi
%make_build

%install
%make_install %{?_smp_mflags}
%{_fixperms} %{buildroot}/*

%if 0%{?with_check}
%check
make %{?_smp_mflags} test
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

# TODO: need to create deve sub package
%files
%defattr(-,root,root)
%{_bindir}/*
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/ldap.conf.default
%config(noreplace) %{_sysconfdir}/%{name}/ldap.conf
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
* Tue Sep 19 2023 Nitesh Kumar <kunitesh@vmware.com> 2.6.4-1
- Version upgrade to v2.6.4 to fix CVE-2023-2953
* Fri Feb 10 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.6.3-1
- Upgrade to v2.6.3
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.4.58-2
- Bump up release for openssl
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.4.58-1
- Automatic Version Bump
* Mon Dec 14 2020 Dweep Advani <dadvani@vmware.com> 2.4.53-3
- Patched for CVE-2020-25692
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.4.53-2
- openssl 1.1.1
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.4.53-1
- Automatic Version Bump
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.4.52-1
- Automatic Version Bump
* Wed Aug 26 2020 Piyush Gupta <gpiyush@vmware.com> 2.4.51-2
- Release bump up
* Fri Aug 14 2020 Susant Sahani <ssahani@vmware.com> 2.4.51-1
- Version Bump and fix build
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.4.50-1
- Automatic Version Bump
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 2.4.46-3
- Cross compilation support
* Mon Nov 5 2018 Sriram Nambakam <snambakam@vmware.com> 2.4.46-2
- export CPPFLAGS before invoking configure
* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.4.46-1
- Upgrade to 2.4.46
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 2.4.44-3
- Use standard configure macros
* Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 2.4.44-2
- Applied patch for CVE-2017-9287
* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.44-1
- Update to 2.4.44
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.4.43-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.43-2
- GA - Bump release of all rpms
* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.43-1
- Updated to version 2.4.43
* Fri Aug 14 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.40-2
- Patches for CVE-2015-1545 and CVE-2015-1546.
* Wed Oct 08 2014 Divya Thaluru <dthaluru@vmware.com> 2.4.40-1
- Initial build. First version
