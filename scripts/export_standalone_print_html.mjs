import fs from "node:fs/promises";
import path from "node:path";

const rootDir = process.cwd();
const siteDir = path.join(rootDir, "_site");
const inputHtml = path.join(siteDir, "index.html");
const outputHtml = path.join(rootDir, "dist", "takuma-yoshioka-print.html");
const baseUrl = "";

const mimeTypes = new Map([
  [".css", "text/css"],
  [".gif", "image/gif"],
  [".ico", "image/x-icon"],
  [".jpg", "image/jpeg"],
  [".jpeg", "image/jpeg"],
  [".png", "image/png"],
  [".svg", "image/svg+xml"],
  [".ttf", "font/ttf"],
  [".woff", "font/woff"],
  [".woff2", "font/woff2"],
  [".eot", "application/vnd.ms-fontobject"],
]);

function mimeType(filePath) {
  return mimeTypes.get(path.extname(filePath).toLowerCase()) || "application/octet-stream";
}

function isExternalUrl(url) {
  return /^(?:https?:)?\/\//i.test(url) || /^(?:mailto|tel):/i.test(url);
}

function stripUrlFragment(url) {
  return url.split("#")[0].split("?")[0];
}

function resolveSitePath(url, fromDir = siteDir) {
  if (!url || url.startsWith("data:") || isExternalUrl(url) || url.startsWith("#")) {
    return null;
  }

  let normalized = stripUrlFragment(url);
  if (baseUrl && normalized.startsWith(`${baseUrl}/`)) {
    normalized = normalized.slice(baseUrl.length + 1);
  } else if (normalized.startsWith("/")) {
    normalized = normalized.slice(1);
  } else {
    return path.resolve(fromDir, normalized);
  }

  return path.join(siteDir, normalized);
}

async function fileToDataUri(filePath) {
  const data = await fs.readFile(filePath);
  return `data:${mimeType(filePath)};base64,${data.toString("base64")}`;
}

async function inlineCssUrls(css, cssFilePath) {
  const cssDir = path.dirname(cssFilePath);
  const urlPattern = /url\((['"]?)([^'")]+)\1\)/g;
  const replacements = [];

  for (const match of css.matchAll(urlPattern)) {
    const [, , rawUrl] = match;
    const assetPath = resolveSitePath(rawUrl, cssDir);
    if (!assetPath) continue;

    try {
      const dataUri = await fileToDataUri(assetPath);
      replacements.push([match[0], `url("${dataUri}")`]);
    } catch {
      // Keep the original URL if an optional asset is missing.
    }
  }

  return replacements.reduce((result, [from, to]) => result.replaceAll(from, to), css);
}

async function inlineStylesheets(html) {
  const linkPattern = /<link\b[^>]*rel=["'][^"']*stylesheet[^"']*["'][^>]*>/gi;
  const replacements = [];

  for (const tag of html.match(linkPattern) || []) {
    const href = tag.match(/\bhref=["']([^"']+)["']/i)?.[1];
    const cssPath = resolveSitePath(href);
    if (!cssPath) {
      replacements.push([tag, ""]);
      continue;
    }

    try {
      let css = await fs.readFile(cssPath, "utf8");
      css = await inlineCssUrls(css, cssPath);
      replacements.push([tag, `<style>\n${css}\n</style>`]);
    } catch {
      replacements.push([tag, ""]);
    }
  }

  return replacements.reduce((result, [from, to]) => result.replace(from, to), html);
}

async function inlineImages(html) {
  const imgPattern = /<img\b[^>]*\bsrc=["']([^"']+)["'][^>]*>/gi;
  const replacements = [];

  for (const match of html.matchAll(imgPattern)) {
    const [tag, src] = match;
    const imagePath = resolveSitePath(src);
    if (!imagePath) continue;

    try {
      const dataUri = await fileToDataUri(imagePath);
      replacements.push([tag, tag.replace(src, dataUri)]);
    } catch {
      // Leave missing images unchanged.
    }
  }

  return replacements.reduce((result, [from, to]) => result.replace(from, to), html);
}

async function inlineIcons(html) {
  const iconPattern = /<link\b[^>]*rel=["'][^"']*(?:icon|shortcut icon)[^"']*["'][^>]*>/gi;
  const replacements = [];

  for (const tag of html.match(iconPattern) || []) {
    const href = tag.match(/\bhref=["']([^"']+)["']/i)?.[1];
    const iconPath = resolveSitePath(href);
    if (!iconPath) {
      replacements.push([tag, ""]);
      continue;
    }

    try {
      const dataUri = await fileToDataUri(iconPath);
      replacements.push([tag, tag.replace(href, dataUri)]);
    } catch {
      replacements.push([tag, ""]);
    }
  }

  return replacements.reduce((result, [from, to]) => result.replace(from, to), html);
}

function removeRuntimeDependencies(html) {
  return html
    .replace(/<script\b[\s\S]*?<\/script>/gi, "")
    .replace(/<link\b[^>]*rel=["'](?:preconnect|preload|alternate|canonical)["'][^>]*>/gi, "")
    .replace(/<noscript\b[\s\S]*?<\/noscript>/gi, "");
}

async function main() {
  let html = await fs.readFile(inputHtml, "utf8");
  html = removeRuntimeDependencies(html);
  html = await inlineStylesheets(html);
  html = await inlineIcons(html);
  html = await inlineImages(html);

  await fs.mkdir(path.dirname(outputHtml), { recursive: true });
  await fs.writeFile(outputHtml, html);

  const size = (await fs.stat(outputHtml)).size;
  console.log(`Saved standalone print HTML: ${path.relative(rootDir, outputHtml)} (${size.toLocaleString()} bytes)`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
