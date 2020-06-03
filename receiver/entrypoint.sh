#!/bin/bash

set -eu

export DEBIAN_FRONTEND=noninteractive

python -m receiver.main
