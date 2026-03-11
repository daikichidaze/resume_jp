import { rename, rm, stat, mkdir } from "node:fs/promises";
import { basename, dirname, join, resolve } from "node:path";
import { spawn } from "node:child_process";

const { chromium } = await import(
  "/home/daikichi/.nvm/versions/node/v22.18.0/lib/node_modules/playwright/index.mjs"
);

const DEFAULT_URL = "http://localhost:4000";
const DEFAULT_OUTPUT = "dist/resume-a4.pdf";
const SIZE_TARGET_BYTES = 1_000_000;

function runCommand(command, args) {
  return new Promise((resolvePromise, rejectPromise) => {
    const child = spawn(command, args, { stdio: ["ignore", "pipe", "pipe"] });
    let stderr = "";

    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });

    child.on("error", (error) => {
      rejectPromise(error);
    });

    child.on("close", (code) => {
      if (code === 0) {
        resolvePromise();
        return;
      }

      rejectPromise(
        new Error(`${command} exited with code ${code}${stderr ? `: ${stderr.trim()}` : ""}`),
      );
    });
  });
}

async function optimizePdfWithGhostscript(inputPath, outputPath) {
  const tempPath = join(dirname(outputPath), `${basename(outputPath, ".pdf")}.raw.pdf`);

  await rename(outputPath, tempPath);

  try {
    await runCommand("gs", [
      "-sDEVICE=pdfwrite",
      "-dCompatibilityLevel=1.4",
      "-dPDFSETTINGS=/ebook",
      "-dNOPAUSE",
      "-dQUIET",
      "-dBATCH",
      `-sOutputFile=${outputPath}`,
      tempPath,
    ]);
  } catch (error) {
    await rename(tempPath, outputPath);
    throw error;
  }

  await rm(tempPath, { force: true });
}

async function main() {
  const targetUrl = process.argv[2] || DEFAULT_URL;
  const outputPath = resolve(process.argv[3] || DEFAULT_OUTPUT);

  await mkdir(dirname(outputPath), { recursive: true });

  const browser = await chromium.launch({
    headless: true,
  });

  try {
    const context = await browser.newContext({
      viewport: {
        width: 1280,
        height: 1800,
      },
    });
    const page = await context.newPage();

    await page.emulateMedia({ media: "print" });
    await page.goto(targetUrl, { waitUntil: "networkidle" });
    await page.evaluate(async () => {
      if (document.fonts?.ready) await document.fonts.ready;
      await new Promise((resolvePromise) =>
        requestAnimationFrame(() => requestAnimationFrame(resolvePromise)),
      );
    });

    await page.pdf({
      path: outputPath,
      format: "A4",
      landscape: false,
      printBackground: true,
      preferCSSPageSize: true,
      margin: {
        top: "0",
        right: "0",
        bottom: "0",
        left: "0",
      },
    });

    try {
      await optimizePdfWithGhostscript(outputPath, outputPath);
      console.log("Optimized PDF with Ghostscript (/ebook).");
    } catch (error) {
      console.warn(`Skipped Ghostscript optimization: ${error.message}`);
    }

    const outputStat = await stat(outputPath);

    console.log(`Saved PDF: ${outputPath}`);
    console.log("Paper size: A4 portrait");
    console.log(`File size: ${outputStat.size} bytes`);
    if (outputStat.size > SIZE_TARGET_BYTES) {
      console.warn(`Warning: PDF size exceeds ${SIZE_TARGET_BYTES} bytes.`);
    }
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
