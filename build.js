// Frontend build: bundles/minifies JavaScript and compiles SCSS (with Autoprefixer) into core/static/.
//   node build.js           one-off build (set NODE_ENV=production to minify)
//   node build.js --watch   rebuild on change
import autoprefixer from "autoprefixer";
import * as esbuild from "esbuild";
import { sassPlugin } from "esbuild-sass-plugin";
import postcss from "postcss";

const production = process.env.NODE_ENV === "production";

const options = {
    entryPoints: {
        "javascripts/application": "src/javascripts/application.js",
        "stylesheets/application": "src/stylesheets/application.scss",
    },
    outdir: "core/static",
    bundle: true,
    // Leave root-absolute url() references (served by Django at runtime) untouched
    // rather than trying to bundle them. Scoped to /static/ so it doesn't also
    // externalise JS imports (whose resolved paths are absolute).
    external: ["/static/*"],
    // Match the browserslist floor (iOS 10) that the old Babel config targeted.
    target: ["es2015"],
    minify: production,
    sourcemap: !production,
    // Extract dependencies' license/legal comments (e.g. govuk-frontend's MIT
    // notice) into a linked <output>.LEGAL.txt beside each bundle, rather than
    // dropping them on minify.
    legalComments: "linked",
    logLevel: "info",
    plugins: [
        sassPlugin({
            loadPaths: ["node_modules"], // resolve @import "govuk-frontend/..."
            async transform(css) {
                const result = await postcss([autoprefixer]).process(css, { from: undefined });
                return result.css;
            },
        }),
    ],
};

if (process.argv.includes("--watch")) {
    const context = await esbuild.context(options);
    await context.watch();
    console.log("Watching for changes …");
} else {
    await esbuild.build(options);
}
