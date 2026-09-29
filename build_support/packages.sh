#!/bin/bash

## =================================================================
## CS160 PACKAGE INSTALLATION
##
## This script will install all the packages that are needed to
## build and test your compiler: Python 3.11 or later, clang 15 or
## later, git, zip, and the ruff formatter and linter.
##
## Supported environments:
##  * Ubuntu 24.04 (x86-64 or ARM), including under WSL 2
##  * macOS 14 Sonoma or later (x86-64 or ARM)
## =================================================================

RUFF_VERSION=0.16.9
ROOT=$(cd "$(dirname "$0")/.." && pwd)

main() {
  set -o errexit

  if [ "$1" == "-y" ]
  then
    install
  else
    echo "PACKAGES WILL BE INSTALLED. THIS MAY BREAK YOUR EXISTING TOOLCHAIN."
    echo "YOU ACCEPT ALL RESPONSIBILITY BY PROCEEDING."
    read -p "Proceed? [y/N] : " yn

    case $yn in
      Y|y) install;;
      *) ;;
    esac
  fi

  echo "Script complete."
}

install() {
  set -x
  UNAME=$(uname | tr "[:lower:]" "[:upper:]" )

  case $UNAME in
    DARWIN) install_mac ;;

    LINUX)
      version=$(cat /etc/os-release | grep VERSION_ID | cut -d '"' -f 2)
      case $version in
        24.04) install_linux ;;
        *) give_up ;;
      esac
      ;;

    *) give_up ;;
  esac

  install_ruff
}

give_up() {
  set +x
  echo "Unsupported distribution '$UNAME'"
  echo "Please ask on the course Slack for help."
  echo "Be sure to include the contents of this message."
  echo "Platform: $(uname -a)"
  echo
  exit 1
}

install_mac() {
  # clang and git come with Apple's command-line tools.
  xcode-select -p > /dev/null 2>&1 || xcode-select --install
  # Install Homebrew.
  if test ! $(which brew); then
    echo "Installing Homebrew (https://brew.sh/)"
    bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
  fi
  # Update Homebrew.
  brew update
  # Install packages. The python3 that comes with the command-line tools is too old.
  brew ls --versions python@3.13 || brew install python@3.13
}

install_linux() {
  # Update apt-get.
  apt-get -y update
  # Install packages.
  apt-get -y install \
      clang \
      git \
      python3 \
      python3-venv \
      zip
}

install_ruff() {
  # ruff goes into build_support/.venv, owned by you even when this script runs with sudo.
  if [ -n "$SUDO_USER" ]; then
    sudo -u "$SUDO_USER" python3 -m venv "$ROOT/build_support/.venv"
    sudo -u "$SUDO_USER" "$ROOT/build_support/.venv/bin/pip" install --quiet "ruff==$RUFF_VERSION"
  else
    python3 -m venv "$ROOT/build_support/.venv"
    "$ROOT/build_support/.venv/bin/pip" install --quiet "ruff==$RUFF_VERSION"
  fi
}

main "$@"
