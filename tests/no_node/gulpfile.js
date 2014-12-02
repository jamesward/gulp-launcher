var gulp = require("gulp");

gulp.task("help", function(next) {
  console.log("help");
  next();
});

gulp.task("default", ["help"]);
