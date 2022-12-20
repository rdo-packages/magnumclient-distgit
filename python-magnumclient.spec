%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global sname python-magnumclient
%global pname magnumclient
%global with_doc 1

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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n     python3-%{pname}
Summary:        Client library for Magnum API
%{?python_provide:%python_provide python3-%{pname}}
Obsoletes: python2-%{pname} < %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  git-core
BuildRequires:  openstack-macros

# test dependencies
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-openstackclient
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslo-log
%if 0%{?rhel}
BuildRequires:  python3-osprofiler
%endif
BuildRequires:  python3-stevedore
BuildRequires:  python3-requests
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-fixtures
BuildRequires:  python3-mock
BuildRequires:  python3-testtools
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-prettytable
BuildRequires:  python3-stestr

Requires:    python3-cryptography
Requires:    python3-keystoneauth1 >= 3.4.0
Requires:    python3-oslo-i18n >= 3.15.3
Requires:    python3-oslo-log >= 3.36.0
Requires:    python3-oslo-serialization >= 2.18.0
Requires:    python3-oslo-utils >= 3.33.0
Requires:    python3-osc-lib >= 1.8.0
Requires:    python3-os-client-config >= 1.28.0
Requires:    python3-pbr
Requires:    python3-prettytable

Requires:    python3-decorator

%description -n python3-%{pname}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pname}-doc
Summary:        python-magnumclient documentation
BuildRequires:   python3-sphinx
BuildRequires:   python3-openstackdocstheme
BuildRequires:   python3-os-client-config

BuildRequires:   python3-decorator

%description -n python-%{pname}-doc
Documentation for python-magnumclient
%endif

%package -n python3-%{pname}-tests
Summary: Python-magnumclient test subpackage
%{?python_provide:%python_provide python2-%{pname}-tests}

Requires:  python3-%{pname} = %{version}-%{release}
Requires:  python3-oslo-utils
Requires:  python3-stevedore
Requires:  python3-requests
Requires:  python3-oslo-i18n
Requires:  python3-fixtures
Requires:  python3-mock
Requires:  python3-testtools
Requires:  python3-keystoneauth1
Requires:  python3-prettytable
Requires:  python3-stestr
%if 0%{?rhel}
Requires:  python3-osprofiler
%endif

%description -n python3-%{pname}-tests
%{common_desc_tests}

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git

# let RPM handle deps
%py_req_cleanup

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
# (TODO) Re-add -W once https://review.openstack.org/#/c/554197 is in a
# tagged release
sphinx-build-3 -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%check
%if 0%{?rhel}
PYTHON=%{__python3} stestr run --slowest
%else
PYTHON=%{__python3} stestr run --slowest || true
%endif

%files -n python3-%{pname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pname}
%{_bindir}/magnum
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/%{pname}/tests

%if 0%{?with_doc}
%files -n python-%{pname}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python3-%{pname}-tests
%{python3_sitelib}/%{pname}/tests

%changelog
