# !/bin/sh
cd frontend
mv package.json package-dev.json
mv package-build.json package.json
yarn install
yarn build
mv package.json package-build.json
mv package-dev.json package.json