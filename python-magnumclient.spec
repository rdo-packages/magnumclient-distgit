%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
%global sname python-magnumclient
%global pname magnumclient
%global with_doc 1
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%if ! 0%{?rhel}
%global excluded_brs %{excluded_brs} osprofiler
%endif

%global common_desc \
This is a client library for Magnum built on the Magnum API. \
It provides a Python API (the magnumclient module) and a \
command-line tool (magnum).

%global common_desc_tests Python-magnumclient test subpackage

Name:           python-%{pname}
Version:        XXX
Release:        XXX
Summary:        Client library for Magnum API

License:        Apache-2.0
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

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core
BuildRequires:  openstack-macros

%description -n python3-%{pname}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pname}-doc
Summary:        python-magnumclient documentation

%description -n python-%{pname}-doc
Documentation for python-magnumclient
%endif

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


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%check
%if 0%{?rhel}
%tox -e %{default_toxenv}
%else
%tox -e %{default_toxenv} || true
%endif


%files -n python3-%{pname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pname}
%{_bindir}/magnum
%{python3_sitelib}/*.dist-info
%exclude %{python3_sitelib}/%{pname}/tests

%if 0%{?with_doc}
%files -n python-%{pname}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python3-%{pname}-tests
%{python3_sitelib}/%{pname}/tests

%changelog
