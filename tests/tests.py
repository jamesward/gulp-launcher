import subprocess, sys, os, platform

if len(sys.argv) >= 2:
    gulpcmd = os.path.normpath(sys.argv[1])
else:
    if platform.system() == "Windows":
        gulpcmd = os.path.normpath("../../python/dist/gulp.exe")
    else:
        gulpcmd = os.path.normpath("../../bash/gulp")

def run_test(dir, exp, stdin, setup, cleanup, args):
    args.insert(0, gulpcmd)

    if not os.path.exists(os.path.join(dir, gulpcmd)):
        print "{} not found".format(gulpcmd)
        sys.exit(1)


    print "Running {} in {}".format(" ".join(args), dir)

    if stdin:
        print "STDIN: {}".format(stdin)

    print "Expected: {}".format(exp)
    print

    myenv = os.environ
    myenv["GULP_LAUNCHER_TRACE"] = "1"

    if setup:
        print "Setting up: {}".format(setup)
        print
        subprocess.Popen(setup, shell=True, cwd=dir).communicate()

    try:
        p = subprocess.Popen(args, cwd=dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, env=myenv)
        if stdin:
            out, err = p.communicate(stdin)
        else:
            out, err = p.communicate()
    except (OSError, ValueError), e:
        out = ""
        err = e

    if cleanup:
        print "Cleaning up: {0}".format(cleanup)
        print
        subprocess.Popen(cleanup, shell=True, cwd=dir).communicate()

    if out:
        print "Output:"
        print(out)
        print

    if err:
        print "Error:"
        print(err)
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
