# !/bin/sh

# Go to frontend dir and switch to build package
cd frontend
mv package.json package-dev.json
mv package-build.json package.json

# Install build dependencies and build
yarn install
yarn build

# Switch back to dev
mv package.json package-build.json
mv package-dev.json package.json
yarn install