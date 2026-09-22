/*
 * Deterministic animation compositor for the ImageGen-restored keyframe.
 * Art is generated once; this script animates exposure, eye bloom and a 6px rise.
 * Usage: npm ci && npm run build
 * Optional output: node build_goldrinn_animation.cjs /path/to/output
 * Requires the pinned sharp dependency in this directory's package-lock.json.
 */
const fs = require('node:fs/promises');
const path = require('node:path');
const assert = require('node:assert/strict');
const sharp = require('sharp');

const OUT = path.resolve(process.argv[2] || path.join(__dirname, 'generated'));
const W = 768, H = 1024, COUNT = 16;
const delays = [120, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 130, 1000];
const clamp = (x, low = 0, high = 1) => Math.min(high, Math.max(low, x));
const ease = (a, b, x) => { const t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
const gaussian = (x, y, cx, cy, sx, sy) => Math.exp(-0.5 * (((x - cx) / sx) ** 2 + ((y - cy) / sy) ** 2));
const eyes = [{ x: 572 / 1086 * W, y: 510 / 1448 * H }, { x: 681 / 1086 * W, y: 512 / 1448 * H }];

async function main() {
  await fs.mkdir(path.join(OUT, 'frames'), { recursive: true });
  const source = path.join(__dirname, 'goldrinn_artwork.png');
  const base = await sharp(source).resize(W, H, { fit: 'fill' }).removeAlpha().raw().toBuffer();
  await sharp(base, { raw: { width: W, height: H, channels: 3 } }).png().toFile(path.join(OUT, 'goldrinn_final.png'));
  const frames = [], timeline = [];
  const frameSize = W * H * 3;
  for (let i = 0; i < COUNT; i++) {
    const t = i / (COUNT - 1);
    const eyePower = ease(0, 0.36, t);
    const subjectPower = Math.pow(ease(0.22, 1, t), 1.22);
    const ambientPower = Math.pow(ease(0.32, 1, t), 1.15);
    const riseOffset = 6 * (1 - ease(0, 1, t));
    const frame = i === COUNT - 1 ? Buffer.from(base) : Buffer.alloc(frameSize);
    let luminanceSum = 0, deltaSum = 0;
    if (i !== COUNT - 1) {
      for (let y = 0; y < H; y++) {
        const sy = clamp(y - riseOffset, 0, H - 1);
        const y0 = Math.floor(sy), y1 = Math.min(H - 1, y0 + 1), mix = sy - y0;
        for (let x = 0; x < W; x++) {
          const p = (y * W + x) * 3;
          const p0 = (y0 * W + x) * 3, p1 = (y1 * W + x) * 3;
          const r = base[p0] * (1 - mix) + base[p1] * mix;
          const g = base[p0 + 1] * (1 - mix) + base[p1 + 1] * mix;
          const b = base[p0 + 2] * (1 - mix) + base[p1 + 2] * mix;
          const hero = gaussian(x, sy, W * 0.52, H * 0.48, W * 0.29, H * 0.34);
          const exposure = ambientPower + (subjectPower - ambientPower) * hero;
          let eyeMask = 0, eyeGlow = 0;
          for (const eye of eyes) {
            const dx = x - eye.x, dy = sy - eye.y;
            if (Math.abs(dx) > 50 || Math.abs(dy) > 40) continue;
            const iris = gaussian(x, sy, eye.x, eye.y, 6, 4.7);
            // Restrict the light source to existing warm iris pixels.
            const warmPixel = clamp((r - Math.max(g * 1.18, b * 1.3)) / 80);
            eyeMask = Math.max(eyeMask, iris * warmPixel);
            eyeGlow += gaussian(x, sy, eye.x, eye.y, 10, 7) * 0.35
              + gaussian(x, sy, eye.x, eye.y, 22, 16) * 0.12;
          }
          const irisLight = eyePower * eyeMask * (1 - exposure);
          const bloom = eyePower * Math.pow(1 - exposure, 2) * eyeGlow;
          frame[p] = Math.round(clamp(r * exposure + r * irisLight + 190 * bloom, 0, 255));
          frame[p + 1] = Math.round(clamp(g * exposure + g * 0.22 * irisLight + 9 * bloom, 0, 255));
          frame[p + 2] = Math.round(clamp(b * exposure + b * 0.15 * irisLight + 3 * bloom, 0, 255));
        }
      }
    }
    for (let p = 0; p < frameSize; p += 3) {
      luminanceSum += 0.2126 * frame[p] + 0.7152 * frame[p + 1] + 0.0722 * frame[p + 2];
      if (i > 0) for (let c = 0; c < 3; c++) deltaSum += Math.abs(frame[p + c] - frames[i - 1][p + c]);
    }
    const filename = `frame_${String(i + 1).padStart(2, '0')}.png`;
    await sharp(frame, { raw: { width: W, height: H, channels: 3 } }).png().toFile(path.join(OUT, 'frames', filename));
    frames.push(frame);
    timeline.push({ frame: i + 1, file: `frames/${filename}`, durationMs: delays[i], eyePower: +eyePower.toFixed(4), subjectPower: +subjectPower.toFixed(4), ambientPower: +ambientPower.toFixed(4), offsetY: +riseOffset.toFixed(3), meanLuminance: +(luminanceSum / (W * H)).toFixed(4), deltaFromPrevious: +(deltaSum / frameSize).toFixed(4) });
  }

  const animation = () => sharp(Buffer.concat(frames), { raw: { width: W, height: H * COUNT, channels: 3, pageHeight: H } });
  const gifOptions = { delay: delays, colours: 256, dither: 0.25, effort: 7, interFrameMaxError: 0, interPaletteMaxError: 0, keepDuplicateFrames: true };
  // One-shot entrance: retain the final pose instead of abruptly jumping back to black.
  await animation().gif({ ...gifOptions, loop: 1 }).toFile(path.join(OUT, 'goldrinn_entrance.gif'));
  await animation().gif({ ...gifOptions, loop: 0 }).toFile(path.join(OUT, 'goldrinn_entrance_loop.gif'));

  // Lossless full-colour companion avoids GIF's 256-colour palette limit.
  await animation().webp({ lossless: true, effort: 4, loop: 1, delay: delays }).toFile(path.join(OUT, 'goldrinn_entrance.webp'));

  const tileW = 192, tileH = 256, gap = 12, labelH = 30;
  const sheetW = gap + 4 * (tileW + gap), sheetH = gap + 4 * (tileH + labelH + gap);
  const layers = [];
  for (let i = 0; i < COUNT; i++) {
    const left = gap + (i % 4) * (tileW + gap), top = gap + Math.floor(i / 4) * (tileH + labelH + gap);
    layers.push({ input: await sharp(frames[i], { raw: { width: W, height: H, channels: 3 } }).resize(tileW, tileH).png().toBuffer(), left, top });
    const label = `<svg width="${tileW}" height="${labelH}"><text x="0" y="20" fill="#c5d7e4" font-family="Arial" font-size="13">${String(i + 1).padStart(2, '0')} / 16</text><text x="${tileW}" y="20" fill="#73899e" font-family="Arial" font-size="12" text-anchor="end">${delays[i]} ms</text></svg>`;
    layers.push({ input: Buffer.from(label), left, top: top + tileH });
  }
  await sharp({ create: { width: sheetW, height: sheetH, channels: 3, background: '#0b1119' } }).composite(layers).png().toFile(path.join(OUT, 'contact_sheet.png'));

  const validation = {};
  for (const name of ['goldrinn_entrance.gif', 'goldrinn_entrance_loop.gif', 'goldrinn_entrance.webp']) {
    const metadata = await sharp(path.join(OUT, name), { animated: true }).metadata();
    assert.equal(metadata.pages, COUNT, `${name}: expected exactly 16 frames`);
    assert.equal(metadata.width, W);
    assert.equal(metadata.pageHeight, H);
    assert.deepEqual(metadata.delay, delays);
    assert.equal(metadata.loop, name.includes('_loop') ? 0 : 1);
    validation[name] = { frames: metadata.pages, width: metadata.width, height: metadata.pageHeight, loop: metadata.loop, durationMs: metadata.delay.reduce((a, b) => a + b, 0), bytes: (await fs.stat(path.join(OUT, name))).size };
  }
  const final = await sharp(path.join(OUT, 'frames/frame_16.png')).removeAlpha().raw().toBuffer();
  assert.ok(final.equals(base), 'Final frame must exactly equal the resized artwork');
  assert.ok(frames[0].every(v => v === 0), 'First frame must start in darkness');
  assert.ok(timeline.every((f, i) => i === 0 || f.meanLuminance >= timeline[i - 1].meanLuminance), 'Scene must brighten monotonically');
  assert.equal(new Set(frames.map(f => require('node:crypto').createHash('sha256').update(f).digest('hex'))).size, COUNT);
  const decoded = await sharp(path.join(OUT, 'goldrinn_entrance.gif'), { animated: true }).ensureAlpha().raw().toBuffer();
  assert.equal(decoded.length, W * H * COUNT * 4, 'Every encoded GIF frame must decode');
  const report = { generatedArtworkTool: 'Built-in ImageGen', frameCompositor: 'Node.js + sharp', width: W, height: H, frameCount: COUNT, totalDurationMs: delays.reduce((a, b) => a + b, 0), finalFrameExactlyMatchesArtwork: true, uniqueFrames: COUNT, monotonicallyIncreasingSceneLuminance: true, eyes, timeline, validation };
  await fs.writeFile(path.join(OUT, 'animation_manifest.json'), JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ output: OUT, validation, luminance: timeline.map(f => f.meanLuminance), maxMeanFrameDelta: Math.max(...timeline.map(f => f.deltaFromPrevious)), finalFrameExactlyMatchesArtwork: true }, null, 2));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
