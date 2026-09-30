const Image = require("@11ty/eleventy-img");

module.exports = function (eleventyConfig) {
  // Ignore old standalone HTML files (replaced by pages/*.njk templates)
  eleventyConfig.ignores.add("*.html");
  eleventyConfig.ignores.add("content/page-template.njk");
  eleventyConfig.ignores.add("migrated/");
  eleventyConfig.ignores.add("products.html");
  eleventyConfig.ignores.add("research-data/");

  eleventyConfig.addAsyncShortcode("image", async function (src, alt, classes) {
    if (!alt) throw new Error(`Missing \`alt\` on responsive image from: ${src}`);
    let metadata = await Image(src, {
      widths: [400, 800, 1200],
      formats: ["avif", "webp", "jpeg"],
      outputDir: "./_site/assets/img/",
      urlPath: "/assets/img/"
    });
    let imageAttributes = { alt, sizes: "100vw", class: classes, loading: "lazy", decoding: "async" };
    return Image.generateHTML(metadata, imageAttributes);
  });

  eleventyConfig.addPassthroughCopy({ assets: "assets" });
  eleventyConfig.addPassthroughCopy({ "favicon.ico": "favicon.ico" });
  eleventyConfig.addPassthroughCopy({ "favicon.svg": "favicon.svg" });
  eleventyConfig.addPassthroughCopy({ "apple-touch-icon.png": "apple-touch-icon.png" });
  eleventyConfig.addPassthroughCopy({ "robots.txt": "robots.txt" });
  eleventyConfig.addPassthroughCopy({ "sitemap.xml": "sitemap.xml" });
  eleventyConfig.addPassthroughCopy({ _headers: "_headers" });
  eleventyConfig.addWatchTarget("assets/");

  // GitHub Pages serves under /meaicon-website/, production serves from root
  const baseUrl = process.env.GITHUB_ACTIONS ? "/meaicon-website/" : "/";

  // Rewrite root-relative URLs to include the base path on GitHub Pages
  if (process.env.GITHUB_ACTIONS) {
    eleventyConfig.addTransform("gh-pages-basepath", function (content) {
      if (this.page.outputPath && this.page.outputPath.endsWith(".html")) {
        // Rewrite href="/..." and src="/..." to /meaicon-website/...
        content = content.replace(/(href|src)="(\/[^"]*)"/g, (match, attr, path) => {
          if (path === "/") return `${attr}="${baseUrl}"`;
          return `${attr}="${baseUrl}${path.slice(1)}"`;
        });
      }
      return content;
    });
  }

  return {
    dir: {
      input: ".",
      output: "_site",
      includes: "_includes"
    },
    templateFormats: ["html", "njk"],
    htmlTemplateEngine: false,
    markdownTemplateEngine: false
  };
};
