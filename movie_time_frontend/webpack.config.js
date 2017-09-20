let path = require("path");

let DIST_DIR = path.resolve(__dirname, "dist");
let SRC_DIR = path.resolve(__dirname, "src");

let config = {
    entry: SRC_DIR + "/app/index.js",
    output: {
        path: DIST_DIR + "/app",
        filename: "bundle.js",
        publicPath: "/app/"
    },
    module: {
        loaders: [
            {
                test: /\.js?/,
                include: SRC_DIR,
                loader: "babel-loader",
                query: {presets: ["react", "es2015", "stage-1"]}
            },
            {
                test: /\.css$/,
                loader: "style-loader"
            },
            {
                test: /\.css$/,
                loader: "css-loader"
            },
            {
                test: /\.(gif|ttf|eot|svg|woff2?)$/,
                loader: 'url-loader?name=[name].[ext]'
            }
        ],
    },
    devServer: {
        historyApiFallback: true
    }
};

module.exports = config;
