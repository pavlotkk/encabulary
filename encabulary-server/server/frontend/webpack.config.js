const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
    entry: {
        index: './mobile/src/index.js',
        learn: './mobile/src/learn.js'
    },
    output: {
        path: path.resolve(__dirname, './dist/'),
        filename: 'assets/mobile/js/[name].[hash].min.js'
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
                options: {
                    loaders: {}
                    // other vue-loader options go here
                }
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                loader: 'file-loader',
                options: {
                    name: 'assets/mobile/img/[name].[ext]?[hash]'
                }
            }
        ]
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    },
    devServer: {
        historyApiFallback: true,
        noInfo: true
    },
    performance: {
        hints: false
    },
    devtool: '#eval-source-map',
    plugins: [
        new CopyWebpackPlugin([
            { from: 'mobile/src/assets/favicon', to: 'assets/img/favicon' },
            { from: 'mobile/src/assets/css', to: 'assets/mobile/css' },
            { from: 'mobile/src/assets/js', to: 'assets/mobile/js' },
            // desktop
            { from: 'desktop/templates', to: 'templates/desktop'},
            { from: 'desktop/assets', to: 'assets/desktop'}
        ]),
        new HtmlWebpackPlugin({
            filename: 'templates/mobile/index.html',
            template: 'mobile/templates/index.html',
            chunks: ['index'],
            inject: false,
            chunksSortMode: 'dependency'
        }),
        new HtmlWebpackPlugin({
            filename: 'templates/mobile/learn.html',
            template: 'mobile/templates/learn.html',
            chunks: ['learn'],
            inject: false,
            chunksSortMode: 'dependency'
        })
    ]
};

if (process.env.NODE_ENV === 'production') {
    module.exports.devtool = '#source-map';
    module.exports.plugins = (module.exports.plugins || []).concat([
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: '"production"'
            }
        }),
        new webpack.optimize.UglifyJsPlugin({
            sourceMap: true,
            compress: {
                warnings: false
            }
        }),
        new webpack.LoaderOptionsPlugin({
            minimize: true
        })
    ])
}
