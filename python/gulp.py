# gulp-laucher for windows: run build.bat to turn into a standalone .exe file
import urllib2, os, sys, shutil, platform, json, tarfile, pprint, subprocess

class Configuration(dict):
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, val):
        self[attr] = val

cf = Configuration(
    CLEANUP = os.getenv("GULP_LAUNCHER_CLEANUP"),
    TRACE = os.getenv("GULP_LAUNCHER_TRACE"),
    NODE_VERSION = None,
    NODE_BIN = None,
    NPM_BIN = None,
    NODE_DOWNLOAD_PATH = None,
    NODE_HOST="nodejs.org",
    DEFAULT_NODE_VERSION = "0.10.33",
    DEFAULT_NPM_VERSION = "1.4.12",
    DEFAULT_GULP_VERSION = "3.8.10",
    OS = platform.system(),
    ARCHITECTURE = platform.architecture()[0], # 64bit or 32bit
    BASE_LOCAL_DIR = "{APPDATA}\\gulp-launcher".format(APPDATA=os.getenv("APPDATA")),
    GULP_RAW_VERSION = None,
    GULP_BIN = os.path.normpath("node_modules/gulp/bin/gulp.js"),
)

if cf.TRACE:
    pprint.pprint(cf)

package_json = """\
{{
  "name": "YOUR_PROJECT_NAME",
  "version": "0.0.0",
  "description": "YOUR PROJECT DESCRIPTION",
  "devDependencies": {{
    "gulp": "{DEFAULT_GULP_VERSION}"
  }},
  "engines": {{
    "node": "{DEFAULT_NODE_VERSION}",
    "npm": "{DEFAULT_NPM_VERSION}"
  }}
}}
""".format(**cf)

gulpfile_js = """\
var gulp = require('gulp');

gulp.task('default', function() {
  // place code for your default task here
});
"""

def answer_is_yes(prompt):
    response = raw_input(prompt + " [yes] ")
    return response == "" or response.startswith('y') or response.startswith('Y')

def ensure_file_exists(filename, newfile):
    if not os.path.exists(filename):
        print("You need to run gulp in a directory containing a " + filename + " file.")
        if answer_is_yes("Should one be created for you?"):
            file(filename, 'w').write(newfile)
        else:
            print("No " + filename + " found. Aborting.")
            sys.exit(1)

# Clean up all effects of running this program:
if cf.CLEANUP:
    print "Cleaning up artifacts ...",
    def removeFile(fname):
        if os.path.exists(fname):
            print("removing %s" % fname)
            os.remove(fname)
    def removeDir(dirname):
        if os.path.exists(dirname):
            print("removing %s" % dirname)
            shutil.rmtree(dirname, ignore_errors = True)
    removeDir(cf.BASE_LOCAL_DIR)
    removeDir("node_modules") # Off current working directory
    print "Done"

ensure_file_exists("package.json", package_json)
ensure_file_exists("gulpfile.js", gulpfile_js)

def get_raw_node_version():
    package = json.load(file("package.json"))
    if cf.TRACE:
        pprint.pprint(package)
    if package.has_key('engines') and package['engines'].has_key('node'):
        return package['engines']['node']
    return None

def get_node_version():
    if cf.NODE_VERSION:
        return cf.NODE_VERSION
    if not get_raw_node_version():
        print("The Node version was not specified.")
        if answer_is_yes("Should the latest be used?"):
            cf.NODE_VERSION = urllib2.urlopen("https://semver.io/node/stable").read()
        else:
            print("Exiting because the Node version could not be determined.")
            print("Set a specific node version in the package.json file.")
            sys.exit()
    else:
        nrv = get_raw_node_version()
        if any([c in nrv for c in "^x~<>"]):
            cf.NODE_VERSION = urllib2.urlopen("https://semver.io/node/resolve/" + nrv).read()
        else:
            cf.NODE_VERSION = get_raw_node_version()

    if not cf.NODE_VERSION:
        cf.NODE_VERSION = urllib2.urlopen("https://semver.io/node/stable").read()

    return cf.NODE_VERSION


def download_node_binary():
    cf.NODE_VERSION = get_node_version()
    cf.NODE_DIR = cf.BASE_LOCAL_DIR + "\\tools\\node-" + cf.NODE_VERSION

    if platform.system() == "Windows":
        cf.NODE_BIN = cf.NODE_DIR + "\\node.exe"
        cf.NPM_BIN="{NODE_DIR}\\node_modules\\npm\\cli.js".format(**cf)
        if cf.ARCHITECTURE == "32bit":
            # I assume this is the right one for 32bit. There's also node-v0.10.33-x86.msi
            cf.NODE_DOWNLOAD_PATH = "/dist/v{NODE_VERSION}/node.exe".format(**cf)
        if cf.ARCHITECTURE == "64bit":
            # There's also https://nodejs.org/dist/v0.10.33/x64/node-v0.10.33-x64.msi
            cf.NODE_DOWNLOAD_PATH = "/dist/v{NODE_VERSION}/x64/node.exe".format(**cf)

    if not os.path.exists(cf.NODE_BIN):
        if not os.path.exists(cf.NODE_DIR):
            os.makedirs(cf.NODE_DIR)

        if platform.system() == "Windows":
            print("Downloading Node {NODE_VERSION} for {ARCHITECTURE} {OS}".format(**cf))
            url = "https://{NODE_HOST}{NODE_DOWNLOAD_PATH}".format(**cf)
            if cf.TRACE:
                print url
            file(cf.NODE_BIN, 'wb').write(urllib2.urlopen(url).read())

    if not os.path.exists(cf.NPM_BIN):
        if not os.path.exists(cf.NODE_DIR):
            os.makedirs(cf.NODE_DIR)

        if platform.system() == "Windows":
            print("Downloading npm {DEFAULT_NPM_VERSION} for {ARCHITECTURE} {OS}".format(**cf))
            url = "http://{NODE_HOST}/dist/npm/npm-{DEFAULT_NPM_VERSION}.tgz".format(**cf)
            if cf.TRACE:
                print url
            file(cf.NODE_DIR + "\\npm.tgz", 'wb').write(urllib2.urlopen(url).read())
            tarfile.open(cf.NODE_DIR + "\\npm.tgz", "r:gz").extractall(os.path.join(cf.NODE_DIR, "node_modules"))

def cmdline(arglist):
    assert(isinstance(arglist, list))
    if cf.TRACE:
        print "arglist: "
        pprint.pprint(arglist)
    p = subprocess.call(arglist, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = p.communicate()
    print(out)
    print(err)

def install_gulp():
    download_node_binary()
    if not os.path.exists(cf.GULP_BIN):
        print("Installing gulp")
        package = json.load(file("package.json"))
        if package.has_key('devDependencies') and package['devDependencies'].has_key('gulp'):
            cf.GULP_RAW_VERSION = package['devDependencies']['gulp']
        if not cf.GULP_RAW_VERSION:
            print("No Gulp dependency was found in your package.json file")
            if answer_is_yes("Should the latest be used?"):
                cmdline(["{NODE_BIN}".format(**cf), "{NPM_BIN}".format(**cf), "install --save-dev gulp"])
        else:
            cmdline(["{NODE_BIN}".format(**cf), "{NPM_BIN}".format(**cf), "install"])

        if not os.path.exists(cf.GULP_BIN):
            print("Gulp could not be downloaded. Aborting.")
            sys.exit(1)

def run_gulp():
    install_gulp()
    cf.gulpargs = " ".join(sys.argv[1:]).strip()
    if cf.TRACE:
        print "gulpargs: '" + cf.gulpargs + "'"
    cmdline(["{NODE_BIN}".format(**cf), "{GULP_BIN}".format(**cf), "{gulpargs}".format(**cf)])

run_gulp()
