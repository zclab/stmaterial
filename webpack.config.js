const { resolve } = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const CopyPlugin = require("copy-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const dedent = require("dedent");
const { Compilation } = require("webpack");

// Compile our translation files
const { exec } = require("child_process");
exec("python src/stmaterial/_translations.py");

const scriptPath = resolve(__dirname, "src/stmaterial/assets/scripts");
const stylePath = resolve(__dirname, "src/stmaterial/assets/styles");
const staticPath = resolve(__dirname, "src/stmaterial/theme/stmaterial/static");
const vendorPath = resolve(staticPath, "vendor");

const maVersions = { maIcons: require("material-icons/package.json").version };
const maPath = { maIcons: resolve(vendorPath, "material-icons", maVersions.maIcons) };
/*******************************************************************************
 * functions to load the assets in the html head
 * the css, and js (preload/scripts) are digested for cache busting
 * the fonts are loaded from vendors
 */

function stylesheet(css) { return `<link href="{{ pathto('_static/${css}', 1) }}?digest=${this.hash}" rel="stylesheet" />`; }
function preload(js) { return `<link rel="preload" as="script" href="{{ pathto('_static/${js}', 1) }}?digest=${this.hash}" />`; }
function script(js) { return `<script src="{{ pathto('_static/${js}', 1) }}?digest=${this.hash}"></script>`; }
function font(woff2) { return `<link rel="preload" as="font" type="font/woff2" crossorigin href="{{ pathto('_static/${woff2}', 1) }}" />`; }


/*******************************************************************************
 * the assets to load in the macro
 */
const theme_stylesheets = [
    "styles/stmaterial.css", // all the css created for this specific theme
];
const theme_scripts = [
    "scripts/materialize.js",
    "scripts/stmaterial.js",
];
const ma_stylesheets = [
    `vendor/material-icons/${maVersions.maIcons}/iconfont/material-icons.css`,
];
const ma_fonts = [
    `vendor/material-icons/${maVersions.maIcons}/iconfont/material-icons.woff2`,
    `vendor/material-icons/${maVersions.maIcons}/iconfont/material-icons.woff`,
];

function macroTemplate({ compilation }) {

    return dedent(`\
        <!--
            AUTO-GENERATED from webpack.config.js, do **NOT** edit by hand.
            These are re-used in layout.html
        -->
        {# Load FontAwesome icons #}
        {% macro head_pre_icons() %}
            ${ma_stylesheets.map(stylesheet.bind(compilation)).join("\n")}
            ${ma_fonts.map(font).join("\n")}
        {% endmacro %}

        {% macro head_pre_assets() %}
        <!-- Loaded before other Sphinx assets -->
        ${theme_stylesheets.map(stylesheet.bind(compilation)).join("\n")}
        {% endmacro %}

        {% macro head_js_preload() %}
        <!-- Pre-loaded scripts that we'll load fully later -->
        ${theme_scripts.map(preload.bind(compilation)).join("\n")}
        {% endmacro %}

        {% macro body_post() %}
        <!-- Scripts loaded after <body> so the DOM is not blocked -->
        ${theme_scripts.map(script.bind(compilation)).join("\n")}
        {% endmacro %}
    `);
}

const htmlWebpackPlugin = new HtmlWebpackPlugin({
    filename: resolve(staticPath, "webpack-macros.html"),
    inject: false,
    minify: false,
    css: true,
    templateContent: macroTemplate,
});
/*******************************************************************************/

const copyPlugin = new CopyPlugin({
    patterns: [
        {
            context: "./node_modules/material-icons",
            from: "LICENSE",
            to: resolve(maPath.maIcons, "LICENSE.txt"),
        },
        {
            context: "./node_modules/material-icons/iconfont",
            from: "filled.css",
            to: resolve(maPath.maIcons, "iconfont", "material-icons.css"),
        },
        {
            context: "./node_modules/material-icons/iconfont",
            from: "material-icons.woff2",
            to: resolve(maPath.maIcons, "iconfont"),
        },
        {
            context: "./node_modules/material-icons/iconfont",
            from: "material-icons.woff",
            to: resolve(maPath.maIcons, "iconfont"),
        },
    ]
});


module.exports = {
    mode: "production",
    devtool: "source-map",
    entry: {
        "stmaterial": [
            resolve(scriptPath, "stmaterial.js"),
            resolve(stylePath, "stmaterial.sass"),
        ],
        "materialize": resolve(scriptPath, "materialize.js"),
    },
    output: { filename: "scripts/[name].js", path: staticPath },
    plugins: [new MiniCssExtractPlugin({ filename: "styles/[name].css" }), htmlWebpackPlugin, copyPlugin],
    optimization: { minimizer: [`...`, new CssMinimizerPlugin()] },
    module: {
        rules: [{
            test: /\.s[ac]ss$/i,
            use: [
                MiniCssExtractPlugin.loader,
                { loader: "css-loader", options: { url: false, } },
                { loader: "postcss-loader", options: { sourceMap: true } },
                {
                    loader: "sass-loader", options: {
                        sourceMap: true,
                        implementation: require("sass"),
                        sassOptions: { outputStyle: "expanded" }
                    }
                },
            ],
        }],
    },
};