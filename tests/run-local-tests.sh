#!/bin/sh


runTest() {
  local DIR=$1
  local EXPECTED=$2

  echo "Running the gulp launcher in $DIR"

  # start fresh
  local OUTPUT=$(rm -rf ~/.gulp-launcher)
  local OUTPUT=$(rm -rf $DIR/node_modules)

  cd $DIR

  readonly OUTPUT=$(../../gulp)

  echo $OUTPUT
}

runTest "no_gulp_dep" "asdf"

# no_gulp_dep               node_0.10.x               node_tilde0.10.33
# no_node                   node_0.10.x_with_gulpfile run-local-tests.sh
# node_0.10.33              node_carret0.10.33

