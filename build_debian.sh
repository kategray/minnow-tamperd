#!/bin/bash
# Run from repository root directory with ./dist/build_debian.sh
# build-essential, dh-systemd, and git-buildpackage must be installed.
VERSION=`date +%Y%m%d`
PKG_VERSION=minnow-tamperd-${VERSION}

# Clean the build directories
rm -rf ${PWD}/TamperDaemon/__pycache__/ ${PWD}/tamperd.log ${PWD}/tamperd.log ${PWD}/tamperd.pid debian/minnow-tamperd/

# Add all files to the temporary archive
#TMP_ARCHIVE=`mktemp --suffix=.tar.bz2`
#SRC_ARCHIVE=${PWD}/build/${PKG_VERSION}.tar.bz2
#tar cvjf ${TMP_ARCHIVE} --exclude-vcs --exclude-vcs-ignores ./
#mv ${TMP_ARCHIVE} ${SRC_ARCHIVE}
#echo "Wrote ${SRC_ARCHIVE}"

# Write changelog
gbp dch -R -N ${VERSION}

# Build the package
dpkg-buildpackage -b -rfakeroot --no-sign
