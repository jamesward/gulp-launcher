import subprocess, pprint, sys, os

gulpcmd = os.path.normpath("../../python/dist/gulp.exe")

def run_test(dir, exp, stdin, setup, cleanup, args):
    args.insert(0, gulpcmd)
    cmd = " ".join(args)

    print "Running {0} in {1}".format(cmd, dir)
    print "STDIN: {0}".format(stdin)
    print "Expected: {0}".format(exp)
    print

    myenv = os.environ
    myenv["GULP_LAUNCHER_TRACE"] = "1"

    if setup:
        print "Setting up: {0}".format(setup)
        print
        subprocess.Popen(setup, shell=True, cwd=dir).communicate()

    try:
        p = subprocess.Popen(cmd, cwd=dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, env=myenv, shell=True)
        out, err = p.communicate(stdin + "\n")
    except (OSError, ValueError), e:
        print >>sys.stderr, "Execution failed:", e

    print "Output:"
    print(out)
    print

    if cleanup:
        print "Cleaning up: {0}".format(cleanup)
        print
        subprocess.Popen(cleanup, shell=True, cwd=dir).communicate()

    if err:
        print "Error:"
        print err
        print

    if exp in out:
        print "Test Passed!"
        print
    else:
        print "Test Failed!"
        sys.exit(1)

# Gulp dep isn't set and we tell the gulp launcher not to add it
run_test("no_gulp_dep", "No Gulp dependency was found", "no", "rm -rf node_modules", "", [])
# Gulp dep isn't set and we tell the gulp launcher to add it
run_test("no_gulp_dep", "Starting 'help'", "yes", "cp package.json package.json-", "mv package.json- package.json", [])

# Node engine isn't set and we tell the gulp launcher not to add it
run_test("no_node", "Exiting because the Node version could not be determined.", "no", "", "", [])
# Node engine isn't set and we tell the gulp launcher to add it
run_test("no_node","Starting 'help'", "yes", "cp package.json package.json-", "mv package.json- package.json", [])

# Node 0.10.x without a gulpfile and auto-add one
run_test("node_0.10.x_without_gulpfile", "Starting 'default'", "yes", "", "rm gulpfile.js", [])
# Node 0.10.x without a gulpfile but don't auto-add one
run_test("node_0.10.x_without_gulpfile", "No gulpfile.js found", "no", "", "", [])

# Node 0.10.x without a package.json and auto-add one
run_test("node_0.10.x_without_package_json", "Starting 'default'", "yes", "", "rm package.json", [])
# Node 0.10.x without a package.json but don't auto-add one
run_test("node_0.10.x_without_package_json","No package.json found", "no", "", "", [])

# Node 0.10.x with a gulpfile
run_test("node_0.10.x", "Starting 'help'", "", "", "", [])

# Node ~0.10.33
run_test("node_tilde0.10.33", "Starting 'help'", "", "", "", [])

# Node ^0.10.33
run_test("node_carret0.10.33", "Starting 'help'", "", "", "", [])

# Node 0.10.33
run_test("node_0.10.33", "Starting 'help'", "", "", "", [])

# Node 0.10.33 with a specified task
run_test("node_0.10.33", "Task 'asdf' is not in your gulpfile", "", "", "", ["asdf"])
