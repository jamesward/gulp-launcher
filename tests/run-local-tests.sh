#!/bin/sh

BASEDIR=$(dirname $0)
cd $BASEDIR

readonly GULP=../../gulp

run_test() {
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
    exit 1
  fi
}

# Gulp dep isn't set and we tell the gulp launcher not to add it
run_test "no_gulp_dep" "No Gulp dependency was found" "no"
# Gulp dep isn't set and we tell the gulp launcher to add it
run_test "no_gulp_dep" "Starting 'help'" "yes" "git checkout no_gulp_dep/package.json"

# Node engine isn't set and we tell the gulp launcher not to add it
run_test "no_node" "Exiting because the Node version could not be determined." "no"
# Node engine isn't set and we tell the gulp launcher to add it
run_test "no_node" "No gulpfile found" "yes" "git checkout no_node/package.json"

# Node 0.10.x without a gulpfile
run_test "node_0.10.x" "No gulpfile found"

# Node 0.10.x with a gulpfile
run_test "node_0.10.x_with_gulpfile" "Starting 'help'"

# Node ~0.10.33 without a gulpfile
run_test "node_tilde0.10.33" "No gulpfile found"

# Node ^0.10.33 without a gulpfile
run_test "node_carret0.10.33" "No gulpfile found"

# Node 0.10.33 without a gulpfile
run_test "node_0.10.33" "No gulpfile found"
