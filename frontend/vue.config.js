const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  assetsDir: 'static',
  pages: {
    index: {
      entry: "src/main.js",
      title: "Calendar csv maker"
    }
  }
})
