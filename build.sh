#!/bin/sh
# Builds build/rpack-<version>+<mc>.jar for each Minecraft version in src/.
# A Fabric "datapack mod" is just a zip: fabric.mod.json + data/ + assets/.
# Fabric API loads the data/ folder as a built-in datapack in every world.
set -e
VERSION=2.0.1
cd "$(dirname "$0")"
rm -rf build
for MC in 26.2 26.3; do
  T=build/tmp-$MC
  mkdir -p "$T"
  cp -r src/common/. "$T"/
  cp -r "src/$MC/." "$T"/
  sed -e "s/@VERSION@/$VERSION/" -e "s/@MC@/$MC/g" src/fabric.mod.json.in > "$T/fabric.mod.json"
  cp LICENSE "$T"/
  (cd "$T" && zip -q -r -X "../rpack-$VERSION+$MC.jar" .)
  rm -rf "$T"
  echo "built build/rpack-$VERSION+$MC.jar"
done
