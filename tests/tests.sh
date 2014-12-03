#!/bin/bash

BASEDIR=$(dirname $0)
cd $BASEDIR

readonly GULP=../../gulp

# Runs a test
#
# Usage:
#
#  run_test base_dir expected_output [stdin] [cleanup]
#
run_test() {
  local DIR=$1
  local EXPECTED=$2
  local IN=$3
  local CLEANUP=$4

  printf "Running the gulp launcher in $DIR\n\n"

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
    printf "Test passed!\n\n"
    printf "Output:\n$OUTPUT\n\n"
    printf "Expected:\n$EXPECTED\n\n"
  else
    printf "Test failed!\n\n"
    printf "Output:\n$OUTPUT\n\n"
    printf "Expected:\n$EXPECTED\n\n"
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
run_test "no_node" "Starting 'help'" "yes" "git checkout no_node/package.json"

# Node 0.10.x without a gulpfile and auto-add one
run_test "node_0.10.x_without_gulpfile" "Starting 'default'" "yes" "rm node_0.10.x_without_gulpfile/gulpfile.js"
# Node 0.10.x without a gulpfile but don't auto-add one
run_test "node_0.10.x_without_gulpfile" "No gulpfile.js found" "no"

# Node 0.10.x without a package.json and auto-add one
run_test "node_0.10.x_without_package_json" "Starting 'default'" "yes" "rm node_0.10.x_without_package_json/package.json"
# Node 0.10.x without a package.json but don't auto-add one
run_test "node_0.10.x_without_package_json" "No package.json found" "no"

# Node 0.10.x with a gulpfile
run_test "node_0.10.x" "Starting 'help'"

# Node ~0.10.33
run_test "node_tilde0.10.33" "Starting 'help'"

# Node ^0.10.33
run_test "node_carret0.10.33" "Starting 'help'"

# Node 0.10.33
run_test "node_0.10.33" "Starting 'help'"
