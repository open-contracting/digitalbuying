import babelify from "babelify";
import browserSync from "browser-sync";
import browserify from "browserify";
import del from "del";
import gulp from "gulp";
import csso from "gulp-csso";
import gulpif from "gulp-if";
import sourcemaps from "gulp-sourcemaps";
import uglify from "gulp-uglify";
import buffer from "vinyl-buffer";
import source from "vinyl-source-stream";

const sass = require("gulp-sass")(require("sass"));
const prod = process.env.NODE_ENV === "production";
const paths = {
    javascripts: {
        src: ["frontend/javascripts/**/*.js"],
        dist: "ictcg/static/javascripts",
        manifest: "frontend/javascripts/application.js",
    },
    stylesheets: {
        src: ["frontend/stylesheets/**/*.scss"],
        dist: "ictcg/static/stylesheets",
    },
    images: {
        src: ["frontend/images/**/*"],
        dist: "ictcg/static/images",
    },
};

gulp.task("clean", () =>
    del([`${paths.javascripts.dist}/*.*`, `${paths.stylesheets.dist}/*.*`]).then((dirs) =>
        console.log(`Deleted files and folders:\n ${dirs.join("\n")}`),
    ),
);

gulp.task("stylesheets", () => {
    return gulp
        .src(paths.stylesheets.src)
        .pipe(sass({ errLogToConsole: true, includePaths: "node_modules", quietDeps: true }))
        .pipe(gulpif(!prod, sourcemaps.init()))
        .pipe(csso({ restructure: true, sourceMap: true, debug: true }))
        .pipe(sourcemaps.write("."))
        .pipe(gulp.dest(paths.stylesheets.dist))
        .pipe(gulpif(!prod, browserSync.reload({ stream: true })));
});

gulp.task("images", () => {
    return gulp.src(paths.images.src).pipe(gulp.dest(paths.images.dist));
});

gulp.task("javascripts", () => {
    const bundler = browserify({
        entries: [paths.javascripts.manifest],
        debug: true,
        cache: {},
        packageCache: {},
        fullPaths: false,
    }).transform(babelify, {});

    function bundle() {
        console.log("bundling <<<<<<");
        return bundler
            .bundle()
            .pipe(source(paths.javascripts.manifest.split("/").slice(-1)[0]))
            .pipe(buffer())
            .pipe(uglify())
            .pipe(sourcemaps.init({ loadMaps: true }))
            .pipe(sourcemaps.write("./"))
            .pipe(gulp.dest(paths.javascripts.dist))
            .pipe(gulpif(!prod, browserSync.reload({ stream: true })));
    }

    bundler.on("error", function (error) {
        console.log(error);
        browserSync.notify(error.message, 3000);
        this.emit("end");
    });

    return bundle();
});

gulp.task(
    "browser-sync",
    gulp.series(gulp.parallel("javascripts", "stylesheets"), () => {
        browserSync.init({
            open: false,
            proxy: "127.0.0.1:8000",
        });
    }),
);

gulp.task("watch", (done) => {
    gulp.watch(paths.stylesheets.src, gulp.series("build"));
    gulp.watch(paths.javascripts.src, gulp.series("build"));
    gulp.watch(["**/*.{html,php,svg}", "!node_modules/**"], browserSync.reload);
    done();
});

gulp.task("serve", gulp.series("clean", gulp.parallel("browser-sync", "watch")));

gulp.task("build", gulp.series("clean", "javascripts", "stylesheets", "images"));
