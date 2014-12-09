#!/bin/bash

BASEDIR=$(dirname $0)
cd $BASEDIR

if [ "$1" == "" ]; then
    printf "You must specify the gulp launcher to use. e.g. ../../bash/gulp\n"
    exit 1
else
    readonly GULP=$1
fi

# Runs a test
#
# Usage:
#
#  run_test base_dir expected_output [stdin] [setup] [cleanup] [args]
#
run_test() {
  local DIR=$1
  local EXPECTED=$2
  local IN=$3
  local SETUP=$4
  local CLEANUP=$5
  local ARGS=$6

  printf "Running $GULP in $DIR\n"
  printf "STDIN: $IN\n"
  printf "SETUP: $SETUP\n"
  printf "CLEANUP: $CLEANUP\n"
  printf "ARGS: $ARGS\n\n"

  cd $DIR

  if [ "$SETUP" != "" ]; then
    $SETUP
  fi

  if [ "$IN" == "" ]; then
    local OUTPUT=$($GULP --no-color $ARGS 2>&1)
  else
    local OUTPUT=$(echo $IN | $GULP --no-color $ARGS 2>&1)
  fi

  if [ "$CLEANUP" != "" ]; then
    $CLEANUP
  fi

  cd ..

  printf "Output:\n$OUTPUT\n\n"
  printf "Expected:\n$EXPECTED\n\n"

  if [ "${OUTPUT#*$EXPECTED}" != "$OUTPUT" ]; then
    printf "Test passed!\n\n"
  else
    printf "Test failed!\n\n"
    exit 1
  fi
}

# Gulp dep isn't set and we tell the gulp launcher not to add it
run_test "no_gulp_dep" "No Gulp dependency was found" "no" "rm -r node_modules"
# Gulp dep isn't set and we tell the gulp launcher to add it
run_test "no_gulp_dep" "Starting 'help'" "yes" "cp package.json package.json-" "mv package.json- package.json"

# Node engine isn't set and we tell the gulp launcher not to add it
run_test "no_node" "Exiting because the Node version could not be determined." "no"
# Node engine isn't set and we tell the gulp launcher to add it
run_test "no_node" "Starting 'help'" "yes" "cp package.json package.json-" "mv package.json- package.json"

# Node 0.10.x without a gulpfile and auto-add one
run_test "node_0.10.x_without_gulpfile" "Starting 'default'" "yes" "" "rm gulpfile.js"
# Node 0.10.x without a gulpfile but don't auto-add one
run_test "node_0.10.x_without_gulpfile" "No gulpfile.js found" "no"

# Node 0.10.x without a package.json and auto-add one
run_test "node_0.10.x_without_package_json" "Starting 'default'" "yes" "" "rm package.json"
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

# Node 0.10.33 with a specified task
run_test "node_0.10.33" "Task 'asdf' is not in your gulpfile" "" "" "" "asdf"
