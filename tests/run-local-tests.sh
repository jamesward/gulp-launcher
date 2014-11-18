#!/bin/sh

readonly GULP=../../gulp

runTest() {
  local DIR=$1
  local EXPECTED=$2
  local IN=$3
  local CLEANUP=$4

  echo "Running the gulp launcher in $DIR"

  # start fresh
  local OUTPUT=$(rm -rf ~/.gulp-launcher)
  local OUTPUT=$(rm -rf $DIR/node_modules)

  cd $DIR

  if [ "$IN" == "" ]; then
    readonly OUTPUT=$(../../gulp)
  else
    readonly OUTPUT=$(echo $IN | ../../gulp)
  fi

  cd ..

  if [ "$CLEANUP" != "" ]; then
    $CLEANUP
  fi

  if [ "${OUTPUT#*$EXPECTED}" != "$OUTPUT" ]; then
    echo "Test passed!"
  else
    echo "Test failed!"
    echo "Output:\n$OUTPUT"
    echo "Expected:\n$EXPECTED"
    exit
  fi
}

# Gulp dep isn't set and we tell the gulp launcher not to add it
runTest "no_gulp_dep" "No Gulp dependency was found" "no"
# Gulp dep isn't set and we tell the gulp launcher to add it
runTest "no_gulp_dep" "Starting 'help'" "yes" "git checkout no_gulp_dep/package.json"

# no_gulp_dep               node_0.10.x               node_tilde0.10.33
# no_node                   node_0.10.x_with_gulpfile run-local-tests.sh
# node_0.10.33              node_carret0.10.33

