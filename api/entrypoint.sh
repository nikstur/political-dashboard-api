#!/bin/bash

set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

uvicorn main:app --reload --host 0.0.0.0 --port 8000