const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const WebpackBar = require("webpackbar");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const { ProvidePlugin } = require("webpack");
const Dotenv = require("dotenv-webpack");

const isDev = process.env.NODE_ENV !== "production";

module.exports = {
  target: "web",

  context: path.join(__dirname, "../"),

  entry: {
    project: path.resolve(__dirname, "../static_src/js/project"),
    vendors: path.resolve(__dirname, "../static_src/js/vendors"),
  },

  output: {
    path: path.resolve(__dirname, "../assets/webpack_bundles"),
    publicPath: "/static/webpack_bundles/",
    filename: "js/[name]-[fullhash].js",
    chunkFilename: "js/[name]-[contenthash].js",
    clean: true,
  },

  plugins: [
    new BundleTracker({
      path: path.resolve(__dirname, "../assets"),
      filename: "webpack-stats.json",
    }),

    new WebpackBar({
      name: "compiler",
    }),

    new MiniCssExtractPlugin({
      filename: "css/[name].[contenthash].css",
    }),

    new CopyWebpackPlugin({
      patterns: [
        {
          from: path.resolve(__dirname, "../static/images"),
          to: "images",
          noErrorOnMissing: true,
        },
      ],
    }),

    new Dotenv({
      path: path.resolve(__dirname, "../.env"),
    }),

    new ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      axios: "axios",
    }),
  ],

  module: {
    rules: [
      // JavaScript
      {
        test: /\.[jt]sx?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },

      // Images
      {
        test: /\.(png|jpe?g|gif|svg|webp)$/i,
        type: "asset/resource",
        generator: {
          filename: "images/[name]-[contenthash][ext]",
        },
      },

      // Fonts
      {
        test: /\.(woff2?|eot|ttf|otf)$/i,
        type: "asset/resource",
        generator: {
          filename: "fonts/[name]-[contenthash][ext]",
        },
      },

      // CSS / SCSS / Tailwind
      {
        test: /\.(css|scss|sass)$/i,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: "css-loader",
            options: {
              importLoaders: 2,
              sourceMap: isDev,
            },
          },
          {
            loader: "postcss-loader",
            options: {
              sourceMap: isDev,
            },
          },
          {
            loader: "sass-loader",
            options: {
              sourceMap: isDev,
            },
          },
        ],
      },
    ],
  },

  resolve: {
    modules: ["node_modules"],

    extensions: [
      ".js",
      ".jsx",
      ".ts",
      ".tsx",
      ".json",
    ],

    alias: {
      "@images": path.resolve(__dirname, "../static_src/images"),
      "@fonts": path.resolve(__dirname, "../static_src/fonts"),
      "@js": path.resolve(__dirname, "../static_src/js"),
      "@scss": path.resolve(__dirname, "../static_src/scss"),
    },
  },

  devtool: isDev ? "source-map" : false,

  devServer: {
    hot: true,

    proxy: {
      "/api": {
        target: process.env.BACKEND_URL,
        changeOrigin: true,
      },
    },
  },

  stats: {
    children: false,
    modules: false,
  },
};