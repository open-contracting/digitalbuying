import gulp from "gulp";
import del from "del";
import gulpif from "gulp-if";
import sourcemaps from "gulp-sourcemaps";
import autoprefixer from "gulp-autoprefixer";
import csso from "gulp-csso";
import browserSync from "browser-sync";
import browserify from "browserify";
import babelify from "babelify";
import source from "vinyl-source-stream";
import buffer from "vinyl-buffer";
import uglify from "gulp-uglify";
import connect from "gulp-connect-php";
import plumber from "gulp-plumber";
import notifier from "node-notifier";
import standard from "gulp-standard";

const sass = require("gulp-sass")(require("sass"));
const prod = process.env.NODE_ENV === "production";
const sassOpts = { errLogToConsole: true, includePaths: "node_modules" };
const paths = {
    javascripts: {
        src: ["frontend/javascripts/**/*.js"],
        manifest: "frontend/javascripts/application.js",
        dist: "ictcg/assets/javascripts",
    },
    stylesheets: {
        src: ["frontend/stylesheets/**/*.scss", "!frontend/stylesheets/__tests__/*.scss"],
        dist: "ictcg/assets/stylesheets",
    },
    images: {
        src: ["frontend/images/**/*"],
        dist: "ictcg/assets/images",
    },
    dist: "dist",
};

gulp.task("clean", () =>
    del([`${paths.javascripts.dist}/*.*`, `${paths.stylesheets.dist}/*.*`]).then((dirs) =>
        console.log(`Deleted files and folders:\n ${dirs.join("\n")}`),
    ),
);

gulp.task("stylesheets", () => {
    return gulp
        .src(paths.stylesheets.src)
        .pipe(
            plumber({
                errorHandler: function (error) {
                    console.log(error.message);
                    gulpif(
                        !prod,
                        notifier.notify({
                            title: "SCSS Error",
                            message: error.message,
                        }),
                    );
                    this.emit("end");
                },
            }),
        )
        .pipe(sass(sassOpts))
        .pipe(gulpif(!prod, sourcemaps.init()))
        .pipe(autoprefixer("last 2 versions"))
        .pipe(
            csso({
                restructure: true,
                sourceMap: true,
                debug: true,
            }),
        )
        .pipe(sourcemaps.write("."))
        .pipe(gulp.dest(paths.stylesheets.dist))
        .pipe(
            gulpif(
                !prod,
                browserSync.reload({
                    stream: true,
                }),
            ),
        );
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
            .pipe(plumber())
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

gulp.task("lint-javascripts", () => {
    return gulp
        .src(paths.javascripts.src)
        .pipe(standard())
        .pipe(
            standard.reporter("default", {
                breakOnError: true,
                quiet: true,
            }),
        );
});

gulp.task(
    "browser-sync",
    gulp.series(gulp.parallel("javascripts", "stylesheets"), () => {
        connect.server({}, () => {
            browserSync({
                open: false,
                proxy: "127.0.0.1:8000",
            });
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

gulp.task("lint", gulp.parallel("lint-javascripts"));
