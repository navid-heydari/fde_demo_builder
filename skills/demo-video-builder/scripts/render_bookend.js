#!/usr/bin/env node
/**
 * render_bookend.js — record an HTML/Canvas scene to an MP4 (opener or outro).
 *
 * Loads a local HTML file in headless Chrome, calls window.__start() to kick off its
 * animation *after* recording begins (so the animation clock lines up with the video),
 * records for the requested duration, then muxes in a narration MP3 if provided.
 *
 *   npm i puppeteer puppeteer-screen-recorder
 *   node render_bookend.js scenes/opener.html out/opener.mp4 12 vo/opener.mp3
 *                          ^scene              ^out          ^sec ^optional narration
 *
 * The scene HTML should:
 *   - render at 1920x1080,
 *   - define `window.__start()` to begin its animation (called once recording is rolling),
 *   - finish its animation within the requested duration.
 */
const { PuppeteerScreenRecorder } = require("puppeteer-screen-recorder");
const puppeteer = require("puppeteer");
const path = require("path");
const { spawnSync } = require("child_process");
const fs = require("fs");

async function main() {
  const [scene, out, secStr, vo] = process.argv.slice(2);
  if (!scene || !out) {
    console.error("usage: node render_bookend.js <scene.html> <out.mp4> [seconds] [vo.mp3]");
    process.exit(1);
  }
  const seconds = parseFloat(secStr || "12");
  const raw = out.replace(/\.mp4$/, "") + ".raw.mp4";

  const browser = await puppeteer.launch({
    headless: "new",
    args: ["--no-sandbox", "--force-device-scale-factor=1", "--window-size=1920,1080"],
    defaultViewport: { width: 1920, height: 1080 },
  });
  const page = await browser.newPage();
  await page.goto("file://" + path.resolve(scene), { waitUntil: "networkidle0" });

  const rec = new PuppeteerScreenRecorder(page, { fps: 30, videoFrame: { width: 1920, height: 1080 } });
  await rec.start(raw);
  await page.evaluate(() => window.__start && window.__start());
  await new Promise((r) => setTimeout(r, (seconds + 0.3) * 1000));
  await rec.stop();
  await browser.close();

  // mux narration if provided, else keep silent raw as the output
  if (vo && fs.existsSync(vo)) {
    spawnSync("ffmpeg", ["-y", "-i", raw, "-i", vo,
      "-filter_complex", "[1:a]adelay=150:all=1,apad[a]",
      "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
      "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
      "-shortest", out], { stdio: "inherit" });
    fs.unlinkSync(raw);
  } else {
    fs.renameSync(raw, out);
  }
  console.log("wrote", out);
}
main().catch((e) => { console.error(e); process.exit(1); });
