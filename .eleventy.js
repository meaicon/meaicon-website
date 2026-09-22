const fs = require("node:fs");
const path = require("node:path");

module.exports = function (eleventyConfig) {
  // Ignore old standalone HTML files (replaced by pages/*.njk templates)
  eleventyConfig.ignores.add("*.html");
  eleventyConfig.ignores.add("content/page-template.njk");
  eleventyConfig.ignores.add("migrated/");
  eleventyConfig.ignores.add("products.html");

  // Keep legacy filters for backward compatibility (site-head.njk references them)
  eleventyConfig.addFilter("legacyBody", (source) => {
    const html = fs.readFileSync(path.join(process.cwd(), source), "utf8");
    const body = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i)?.[1];
    const main = body?.match(/<main[^>]*>[\s\S]*?<\/main>/i)?.[0];
    if (!main) throw new Error(`Could not extract <main> from ${source}`);
    return main;
  });

  eleventyConfig.addFilter("legacyJsonLd", (source) => {
    const html = fs.readFileSync(path.join(process.cwd(), source), "utf8");
    return [...html.matchAll(/<script type="application\/ld\+json">[\s\S]*?<\/script>/gi)]
      .map((match) => match[0])
      .join("\n");
  });

  eleventyConfig.addPassthroughCopy({ assets: "assets" });
  eleventyConfig.addPassthroughCopy({ "favicon.ico": "favicon.ico" });
  eleventyConfig.addPassthroughCopy({ "favicon.svg": "favicon.svg" });
  eleventyConfig.addPassthroughCopy({ "apple-touch-icon.png": "apple-touch-icon.png" });
  eleventyConfig.addPassthroughCopy({ "robots.txt": "robots.txt" });
  eleventyConfig.addPassthroughCopy({ sitemap: "sitemap" });
  eleventyConfig.addPassthroughCopy({ _headers: "_headers" });
  eleventyConfig.addWatchTarget("assets/");

  // GitHub Pages serves under /meaicon-website/, production serves from root
  eleventyConfig.addGlobalData("baseUrl", process.env.GITHUB_ACTIONS ? "/meaicon-website/" : "/");

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
