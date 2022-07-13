%global major_version 5.3

Summary:    Programming language
Name:       lua
Version:    5.3.4
Release:    3%{?dist}
License:    MIT
URL:        http://www.lua.org
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution: Photon

Source0:    http://www.lua.org/ftp/%{name}-%{version}.tar.gz
%define sha1 %{name}=79790cfd40e09ba796b01a571d4d63b52b1cd950

Patch0:     %{name}-%{version}-shared_library-1.patch
Patch1:     CVE-2022-28805.patch
Patch2:     CVE-2022-33099.patch

BuildRequires:  readline-devel

Requires:   readline

%description
Lua is a powerful, light-weight programming language designed for extending
applications. Lua is also frequently used as a general-purpose, stand-alone
language. Lua is free software

%package devel
Summary:    Libraries and header files for lua
Requires:   %{name} = %{version}
%description devel
Static libraries and header files for the support library for lua

%prep
# Using autosetup is not feasible
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

sed -i '/#define LUA_ROOT/s:/usr/local/:/usr/:' src/luaconf.h
sed -i 's/CFLAGS= -fPIC -O2 /CFLAGS= -fPIC -O2 -DLUA_COMPAT_MODULE /' src/Makefile

%build
make VERBOSE=1 %{?_smp_mflags} linux

%install
make %{?_smp_mflags} \
    INSTALL_TOP=%{buildroot}%{_usr} TO_LIB="liblua.so \
    liblua.so.%{major_version} liblua.so.%{version}" \
    INSTALL_DATA="cp -d" \
    INSTALL_MAN=%{buildroot}%{_mandir}/man1 \
    install

install -vdm 755 %{buildroot}%{_libdir}/pkgconfig

cat > %{buildroot}%{_libdir}/pkgconfig/%{name}.pc <<- "EOF"
    V=%{major_version}
    R=%{version}

    prefix=%{_usr}
    INSTALL_BIN=${prefix}/bin
    INSTALL_INC=${prefix}/include
    INSTALL_LIB=${prefix}/lib
    INSTALL_MAN=${prefix}/man/man1
    exec_prefix=${prefix}
    libdir=${exec_prefix}/lib
    includedir=${prefix}/include

    Name: Lua
    Description: An Extensible Extension Language
    Version: ${R}
    Requires:
    Libs: -L${libdir} -llua -lm
    Cflags: -I${includedir}
EOF

rmdir %{buildroot}%{_libdir}/%{name}/%{major_version} \
      %{buildroot}%{_libdir}/%{name}

%check
%if 0%{?with_check}
make test %{?_smp_mflags}
%endif

%clean
rm -rf %{buildroot}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/liblua.so.*
%{_mandir}/*/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/liblua.so

%changelog
* Thu Jul 14 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.3.4-3
- Fix CVE-2022-33099
* Mon Apr 18 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.3.4-2
- Fix CVE-2022-28805
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 5.3.4-1
- Update package version
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.3.2-2
- GA - Bump release of all rpms
* Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> 5.3.2-1
- Update to version 5.3.2.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.2.3-1
- Initial build.  First version
