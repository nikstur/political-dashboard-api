#!/bin/bash

set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update

apt-get -y upgrade

# Install a new package, without unnecessary recommended packages:
apt-get -y install --no-install-recommends apt-utils

apt-get -y upgrade

# Delete cached files
apt-get clean
rm -rf /var/lib/apt/lists/*
