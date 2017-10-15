const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
var CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
    entry: {
        index: './src/index.js',
        learn: './src/learn.js'
    },
    output: {
        path: path.resolve(__dirname, './dist/'),
        filename: 'assets/js/[name].[hash].min.js'
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
                    name: 'assets/img/[name].[ext]?[hash]'
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
            { from: 'src/assets/favicon', to: 'assets/img/favicon' },
            { from: 'src/assets/css', to: 'assets/css' },
            { from: 'src/assets/js', to: 'assets/js' }
        ]),
        new HtmlWebpackPlugin({
            filename: 'templates/index.html',
            template: 'templates/index.html',
            chunks: ['index'],
            inject: false,
            chunksSortMode: 'dependency'
        }),
        new HtmlWebpackPlugin({
            filename: 'templates/learn.html',
            template: 'templates/learn.html',
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
