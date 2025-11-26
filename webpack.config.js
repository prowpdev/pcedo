const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    entry: './assets/js/index.js',

    output: {
        path: path.resolve(__dirname, 'static/dist'),
        filename: 'bundle.js',
    },

    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: { loader: 'babel-loader' },
            },

            // CSS Loader
            {
                test: /\.css$/i,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader'
                ],
            },

            // SCSS Loader
            {
                test: /\.scss$/i,
                use: [
                    MiniCssExtractPlugin.loader, // extract CSS to file
                    'css-loader',                // turn css into JS modules
                    'sass-loader'                // compile SCSS → CSS
                ],
            },
        ],
    },

    plugins: [
        new MiniCssExtractPlugin({
            filename: 'styles.css', // output css file
        }),
    ],

    mode: 'development',
};
