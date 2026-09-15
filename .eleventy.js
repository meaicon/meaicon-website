const fs = require("node:fs");
const path = require("node:path");

const migratedPages = [
  "about.html",
  "case-studies.html",
  "consulting.html",
  "contact.html",
  "global-connectivity.html",
  "industries.html",
  "partners.html",
  "privacy-policy.html",
  "solutions.html",
  "terms-of-service.html"
];

module.exports = function (eleventyConfig) {
  eleventyConfig.ignores.add("index.html");
  migratedPages.forEach((page) => eleventyConfig.ignores.add(page));
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
    templateFormats: ["html", "njk"],
    htmlTemplateEngine: false,
    markdownTemplateEngine: false
  };
};
