# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global sname python-magnumclient
%global pname magnumclient

%global common_desc \
This is a client library for Magnum built on the Magnum API. \
It provides a Python API (the magnumclient module) and a \
command-line tool (magnum).

%global common_desc_tests Python-magnumclient test subpackage

Name:           python-%{pname}
Version:        XXX
Release:        XXX
Summary:        Client library for Magnum API

License:        ASL 2.0
URL:            https://launchpad.net/python-magnumclient
Source0:        https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
%{common_desc}

%package -n     python%{pyver}-%{pname}
Summary:        Client library for Magnum API
%{?python_provide:%python_provide python%{pyver}-%{pname}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
BuildRequires:  git
BuildRequires:  openstack-macros

# test dependencies
BuildRequires:  python%{pyver}-oslo-utils
BuildRequires:  python%{pyver}-openstackclient
BuildRequires:  python%{pyver}-oslo-serialization
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-osprofiler
BuildRequires:  python%{pyver}-stevedore
BuildRequires:  python%{pyver}-requests
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-keystoneauth1
BuildRequires:  python%{pyver}-prettytable

Requires:    python%{pyver}-babel
Requires:    python%{pyver}-cryptography
Requires:    python%{pyver}-keystoneauth1 >= 3.4.0
Requires:    python%{pyver}-oslo-i18n >= 3.15.3
Requires:    python%{pyver}-oslo-log >= 3.36.0
Requires:    python%{pyver}-oslo-serialization >= 2.18.0
Requires:    python%{pyver}-oslo-utils >= 3.33.0
Requires:    python%{pyver}-osc-lib >= 1.8.0
Requires:    python%{pyver}-os-client-config >= 1.28.0
Requires:    python%{pyver}-pbr
Requires:    python%{pyver}-prettytable
Requires:    python%{pyver}-six

# Handle python2 exception
%if %{pyver} == 2
Requires:    python-decorator
%else
Requires:    python%{pyver}-decorator
%endif

%description -n python%{pyver}-%{pname}
%{common_desc}

%package -n python-%{pname}-doc
Summary:        python-magnumclient documentation
BuildRequires:   python%{pyver}-sphinx
BuildRequires:   python%{pyver}-openstackdocstheme
BuildRequires:   python%{pyver}-os-client-config

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:   python-decorator
%else
BuildRequires:   python%{pyver}-decorator
%endif

%description -n python-%{pname}-doc
Documentation for python-magnumclient

%package -n python%{pyver}-%{pname}-tests
Summary: Python-magnumclient test subpackage
%{?python_provide:%python_provide python2-%{pname}-tests}

Requires:  python%{pyver}-%{pname} = %{version}-%{release}
Requires:  python%{pyver}-oslo-utils
Requires:  python%{pyver}-stevedore
Requires:  python%{pyver}-requests
Requires:  python%{pyver}-oslo-i18n
Requires:  python%{pyver}-fixtures
Requires:  python%{pyver}-mock
Requires:  python%{pyver}-testtools
Requires:  python%{pyver}-keystoneauth1
Requires:  python%{pyver}-prettytable

%description -n python%{pyver}-%{pname}-tests
%{common_desc_tests}

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# let RPM handle deps
%py_req_cleanup

%build
%{pyver_build}

# generate html docs
# (TODO) Re-add -W once https://review.openstack.org/#/c/554197 is in a
# tagged release
sphinx-build-%{pyver} -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%{pyver_install}

%check
# tests are failing due to unicode not defined
# we are skipping the test
%{pyver_bin} setup.py test ||

%files -n python%{pyver}-%{pname}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/%{pname}
%{_bindir}/magnum
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/%{pname}/tests

%files -n python-%{pname}-doc
%license LICENSE
%doc doc/build/html

%files -n python%{pyver}-%{pname}-tests
%{pyver_sitelib}/%{pname}/tests

%changelog
