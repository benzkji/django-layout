const path = require('path');
const _ = require('lodash');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');


module.exports = (env, argv) => {

    // simple webpack mode.
    // use dev folder for development
    // dist for production (under version control)

    const base_path = './apps/{{ project_name }}/';
    const entry_base_path = base_path + 'static_src/';
    const out_base_path = base_path + 'static/{{ project_name }}/';

    let config = {
        // context: __dirname,
        name: 'main',
        plugins: [new MiniCssExtractPlugin()],
        entry: {
            'bundle': entry_base_path + 'js/index.js',
            // 'print': entry_base_path + 'js/index_print.js',
        },
        output: {
            path: path.resolve(out_base_path + 'dist/'),
            filename: "[name].js",
            chunkFilename: "[id]-[chunkhash].js",  // ?!
            clean: true,
        },
        module: {
            rules: [
                {
                    // the sass job
                    test: /\.s[ac]ss$/i,
                    use: [
                        // Creates `style` nodes from JS strings
                        // "style-loader",
                        // creates files!
                        MiniCssExtractPlugin.loader,
                        // Translates CSS into CommonJS
                        "css-loader",
                        // Compiles Sass to CSS
                        "sass-loader",
                    ],
                },
                {
                    // otherwise throws errors when loading fonts in sass/css!
                    test: /\.(eot|woff|woff2|ttf|svg|png|jpg|gif)$/,
                    use: {
                        loader: 'url-loader', // requires url-loader packages
                        options: {
                            limit: 100000,
                            name: '[name].[ext]'
                        }
                    }
                },
                {
                    // enhancing back to IE11, maybe
                    test: /\.m?js$/,
                    exclude: /(node_modules|bower_components)/,
                    use: {
                        loader: 'babel-loader',
                        options: {
                            presets: ['@babel/preset-env'],
                            // plugins: ['@babel/plugin-proposal-object-rest-spread']
                        }
                    }
                }
            ],
        },
        devServer: {
            port: 8080,
            writeToDisk: true, // Write files to disk in dev mode, so Django can serve the assets
            // hot: true,  // hot module reloading...irk?
        },
    };
    // development? different directory!
    if (argv.mode === 'development') {
        // config.devtool = 'source-map';
        config.output.path = path.resolve(out_base_path + 'dev/');
    }
    // let print_config = {};
    // _.defaultsDeep(print_config, config);
    // print_config.name = 'print';
    // print_config.entry = entry_base_path + 'sass/print.sass';
    // print_config.output.filename = 'print.js';
    // print_config.devServer.port = 8081;
    // console.log(config.name);
    // console.log(print_config.name);
    return [config];

};
