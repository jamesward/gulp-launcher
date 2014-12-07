import subprocess, pprint, sys, os

gulpcmd = os.path.normpath("../python/dist/gulp.exe")

def run_test(dir, exp, stdin, cleanup, args):
    args.insert(0, gulpcmd)

    print "Running {0} in {1}".format(" ".join(args), dir)
    print "STDIN: {0}".format(stdin)
    print "Expected: {0}".format(exp)
    print

    p = subprocess.Popen(args, cwd=dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, env={"GULP_LAUNCHER_TRACE": "1"})
    out, err = p.communicate(stdin)

    print "Output:"
    print(out)
    print

    if cleanup:
        print "Cleaning up: {0}".format(cleanup)
        print
        subprocess.Popen(cleanup, shell=True, cwd=dir).communicate()

    if exp in out:
        print "Test Passed!"
        print
    else:
        print "Test Failed!"
        sys.exit(1)

# Gulp dep isn't set and we tell the gulp launcher not to add it
run_test("no_gulp_dep", "No Gulp dependency was found", "no", "", [])
# Gulp dep isn't set and we tell the gulp launcher to add it
run_test("no_gulp_dep", "Starting 'help'", "yes", "git checkout package.json", [])

# Node engine isn't set and we tell the gulp launcher not to add it
run_test("no_node", "Exiting because the Node version could not be determined.", "no", "", [])
# Node engine isn't set and we tell the gulp launcher to add it
run_test("no_node","Starting 'help'", "yes", "git checkout package.json", [])

# Node 0.10.x without a gulpfile and auto-add one
run_test("node_0.10.x_without_gulpfile", "Starting 'default'", "yes", "rm gulpfile.js", [])
# Node 0.10.x without a gulpfile but don't auto-add one
run_test("node_0.10.x_without_gulpfile", "No gulpfile.js found", "no", "", [])

# Node 0.10.x without a package.json and auto-add one
run_test("node_0.10.x_without_package_json", "Starting 'default'", "yes", "rm package.json", [])
# Node 0.10.x without a package.json but don't auto-add one
run_test("node_0.10.x_without_package_json","No package.json found", "no", "", [])

# Node 0.10.x with a gulpfile
run_test("node_0.10.x", "Starting 'help'", "", "", [])

# Node ~0.10.33
run_test("node_tilde0.10.33", "Starting 'help'", "", "", [])

# Node ^0.10.33
run_test("node_carret0.10.33", "Starting 'help'", "", "", [])

# Node 0.10.33
run_test("node_0.10.33", "Starting 'help'", "", "", [])

# Node 0.10.33 with a specified task
run_test("node_0.10.33", "Task 'asdf' is not in your gulpfile", "", "", ["asdf"])
