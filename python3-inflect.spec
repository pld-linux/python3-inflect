# TODO: finish doc and tests (BRs)
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation
%bcond_with	tests	# unit tests

Summary:	Correctly generate plurals, singular nouns, ordinals, indefinite articles
Summary(pl.UTF-8):	Poprawne generowanie liczby mnogiej i pojedynczej, liczebników, przedimków nieokreślonych
Name:		python3-inflect
Version:	5.4.0
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/inflect/
Source0:	https://files.pythonhosted.org/packages/source/i/inflect/inflect-%{version}.tar.gz
# Source0-md5:	98e2983eba8db51c77adace0bc16b711
URL:		https://pypi.org/project/inflect/
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools >= 1:31.0.1
BuildRequires:	python3-setuptools_scm >= 3.4.1
BuildRequires:	python3-toml
%if %{with tests}
BuildRequires:	python3-pygments
BuildRequires:	python3-pytest >= 6
BuildRequires:	python3-pytest-black >= 0.3.7
#BuildRequires:	python3-pytest-checkdocs >= 2.4
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-enabler >= 1.0.1
BuildRequires:	python3-pytest-flake8
BuildRequires:	python3-pytest-mypy
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-jaraco.packaging >= 8.2
BuildRequires:	python3-jaraco.tidelift >= 1.4
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Correctly generate plurals, singular nouns, ordinals, indefinite
articles; convert numbers to words.

%description -l pl.UTF-8
Poprawne generowanie liczby mnogiej i pojedynczej, liczebników,
przedimków nieokreślonych; przekształcanie liczb na słowa.

%package apidocs
Summary:	API documentation for Python inflect module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona inflect
Group:		Documentation

%description apidocs
API documentation for Python inflect module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona inflect.

%prep
%setup -q -n inflect-%{version}

%build
%py3_build

%if %{with tests}
ln -snf ../tests build-3/tests
cd build-3
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_black_multipy,pytest_flake8,pytest_cov.plugin \
PYTHONPATH=$(echo $(pwd)/build-3/lib) \
%{__python3} -m pytest tests
cd ..
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py3_sitescriptdir}/inflect
%{py3_sitescriptdir}/inflect-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
