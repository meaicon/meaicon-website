module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy({ assets: "assets" });
  eleventyConfig.addPassthroughCopy({ "favicon.ico": "favicon.ico" });
  eleventyConfig.addPassthroughCopy({ "favicon.svg": "favicon.svg" });
  eleventyConfig.addPassthroughCopy({ "apple-touch-icon.png": "apple-touch-icon.png" });
  eleventyConfig.addPassthroughCopy({ "robots.txt": "robots.txt" });
  eleventyConfig.addPassthroughCopy({ "sitemap.xml": "sitemap.xml" });
  eleventyConfig.addPassthroughCopy({ _headers: "_headers" });
  eleventyConfig.addWatchTarget("assets/");
  eleventyConfig.addGlobalData("eleventyComputed", {
    permalink: (data) => `/${data.page.fileSlug || "index"}.html`
  });

  return {
    dir: {
      input: ".",
      output: "_site"
    },
    templateFormats: ["html"],
    htmlTemplateEngine: false,
    markdownTemplateEngine: false
  };
};
