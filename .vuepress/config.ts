import { defineHopeConfig } from "vuepress-theme-hope";
import navbar from "./navbar";
import sidebar from "./sidebar";

export default defineHopeConfig({
  title: "Docker 从入门到实践",

  head: [
    [
      "script",
      { src: "//hm.baidu.com/hm.js?81a3490c9cd141dbcf6d00bc18b6edae" }
    ],
    ["script", { src: "//zz.bdstatic.com/linksubmit/push.js" }]
  ],

  locales: {
    "/": {
      lang: "zh-CN"
    }
  },

  themeConfig: {
    hostname: "https://vuepress.mirror.docker-practice.com",

    pageInfo: ["ReadingTime", "Word"],

    footer:
      "Theme by <a target='_blank' href='https://github.com/vuepress-theme-hope/vuepress-theme-hope'>vuepress-theme-hope</a>",
    displayFooter: true,

    repo: "yeasy/docker_practice",
    docsBranch: "master",

    navbar,
    sidebar,

    contributors: false,
    themeColor: false,
    fullScreen: false,

    plugins: {
      blog: false,
      search: {
        locales: {
          "/zh/": {
            placeholder: "搜索"
          }
        }
      }
    }
  }
});
