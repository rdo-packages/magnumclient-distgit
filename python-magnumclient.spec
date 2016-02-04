%global sname python-magnumclient
%global pname magnumclient

%if 0%{?fedora}
%global with_python3 1

%if 0%{?fedora} >= 24
%global default_python 3
%else
%global default_python 2
%endif

%endif


Name:           python-%{pname}
Version:        1.1.0
Release:        4%{?dist}
Summary:        Client library for Magnum API

License:        ASL 2.0
URL:            https://launchpad.net/python-magnumclient
Source0:        https://pypi.python.org/packages/source/p/%{sname}/%{sname}-%{version}.tar.gz
BuildArch:      noarch

%description
This is a client library for Magnum built on the Magnum API.
It provides a Python API (the magnumclient module) and a
command-line tool (magnum).

%package -n     python2-%{pname}
Summary:        Client library for Magnum API
%{?python_provide:%python_provide python2-%{pname}}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr

# test dependencies
BuildRequires:  python-oslo-utils
BuildRequires:  python-stevedore
BuildRequires:  python-requests
BuildRequires:  python-oslo-i18n
BuildRequires:  python-fixtures
BuildRequires:  python-mock
BuildRequires:  python-testtools
BuildRequires:  python-keystoneauth1
BuildRequires:  python-prettytable

Requires:    python-babel
Requires:    python-oslo-i18n
Requires:    python-oslo-serialization
Requires:    python-oslo-utils
Requires:    python-os-client-config
Requires:    python-prettytable

%description -n python2-%{pname}
This is a client library for Magnum built on the Magnum API.
It provides a Python API (the magnumclient module) and a
command-line tool (magnum).

%if 0%{?with_python3}
%package -n     python3-%{pname}
Summary:        Client library for Magnum API
%{?python_provide:%python_provide python3-%{pname}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr

# test dependencies
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-stevedore
BuildRequires:  python3-requests
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-fixtures
BuildRequires:  python3-mock
BuildRequires:  python3-testtools
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-prettytable

Requires:    python3-babel
Requires:    python3-oslo-i18n
Requires:    python3-oslo-serialization
Requires:    python3-oslo-utils
Requires:    python3-os-client-config
Requires:    python3-prettytable

%description -n python3-%{pname}
This is a client library for Magnum built on the Magnum API.
It provides a Python API (the magnumclient module) and a
command-line tool (magnum).
%endif

%package -n python-%{pname}-doc
Summary:        python-magnumclient documentation
BuildRequires:   python-sphinx
BuildRequires:   python-oslo-sphinx

%description -n python-%{pname}-doc
Documentation for python-magnumclient

%package -n python-%{pname}-tests
Summary: Python-magnumclient test subpackage

Requires:  python-%{pname} = %{version}-%{release}
Requires:  python-oslo-utils
Requires:  python-stevedore
Requires:  python-requests
Requires:  python-oslo-i18n
Requires:  python-fixtures
Requires:  python-mock
Requires:  python-testtools
Requires:  python-keystoneauth1
Requires:  python-prettytable

%description -n python-%{pname}-tests
Python-magnumclient test subpackage

%if 0%{?with_python3}
%package -n python3-%{pname}-tests
Summary: Python-magnumclient test subpackage

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

%description -n python3-%{pname}-tests
Python-magnumclient test subpackage
%endif

%prep
%autosetup -n %{sname}-%{version}

# let RPM handle deps
rm -rf {test-,}requirements.txt

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif
# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install

%if 0%{with_python3}
%py3_install
%if %{default_python} >= 3
mv %{buildroot}%{_bindir}/magnum ./magnum.py3
%endif
%endif

%py2_install

%if %{default_python} >= 3
mv magnum.py3 %{buildroot}%{_bindir}/magnum
%endif

%check
# tests are failing due to unicode not defined
# we are skipping the test
%{__python2} setup.py test ||:
%if 0%{?with_python3}
%{__python3} setup.py test ||:
%endif

%files -n python2-%{pname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pname}
%if %{default_python} <= 2
%{_bindir}/magnum
%endif
%{python2_sitelib}/*-%{version}-py?.?.egg-info
%exclude %{python2_sitelib}/%{pname}/tests

%if 0%{?with_python3}
%files -n python3-%{pname}
%doc README.rst
%license LICENSE
%if %{default_python} >= 3
%{_bindir}/magnum
%endif
%{python3_sitelib}/magnumclient
%{python3_sitelib}/*-%{version}-py?.?.egg-info
%exclude %{python3_sitelib}/%{pname}/tests
%endif

%files -n python-%{pname}-doc
%license LICENSE
%doc html

%files -n python-%{pname}-tests
%{python2_sitelib}/%{pname}/tests

%if 0%{?with_python3}
%files -n python3-%{pname}-tests
%{python3_sitelib}/%{pname}/tests
%endif

%changelog
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Chandan Kumar <chkumar246@gmail.com> - 1.1.0-3
* Minor python2 and python3 macro fixes

* Fri Dec 18 2015 Chandan Kumar <chkumar246@gmail.com> - 1.1.0-2
- Added test subpackage

* Mon Nov 30 2015 Chandan Kumar <chkumar246@gmail.com> - 1.1.0-1
- Initial package
