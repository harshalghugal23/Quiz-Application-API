#!/bin/bash
# ----------------------------------------
# Script: pull_lfs_silent.sh
# Purpose: Install Git LFS and pull large files silently
# ----------------------------------------

set -e

# Update packages silently
sudo apt update -qq

# Install Git LFS if not installed
if ! command -v git-lfs &> /dev/null
then
    sudo apt install -y git-lfs -qq
fi

# Initialize Git LFS silently
git lfs install -q

# Pull LFS files silently
git lfs pull -q
