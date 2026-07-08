import autoprefixer from "autoprefixer";
import browserslist from "browserslist";
import * as esbuild from "esbuild";
import { esbuildPluginBrowserslist } from "esbuild-plugin-browserslist";
import { sassPlugin } from "esbuild-sass-plugin";
import postcss from "postcss";

const production = process.env.NODE_ENV === "production";

const options = {
    entryPoints: {
        "javascripts/application": "src/javascripts/application.js",
        "stylesheets/application": "src/stylesheets/application.scss",
    },
    bundle: true,
    outdir: "core/static",
    minify: production,
    sourcemap: !production,
    legalComments: "linked",
    logLevel: "info",
    // The compiled CSS references images by their runtime /static/ URL. Those files are owned
    // by Django's staticfiles pipeline, which serves and content-hashes them at collectstatic.
    // esbuild leaves the url()s untouched rather than trying to resolve them.
    external: ["/static/*"],
    plugins: [
        esbuildPluginBrowserslist(browserslist(), { printUnknownTargets: false }),
        sassPlugin({
            async transform(source) {
                const { css } = await postcss([autoprefixer]).process(source, { from: undefined });
                return css;
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
