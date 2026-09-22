const fs = require('node:fs/promises');
const path = require('node:path');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const sharp = require('sharp');

const root = __dirname;
const sha256 = data => crypto.createHash('sha256').update(data).digest('hex');

async function main() {
  const expected = JSON.parse(await fs.readFile(path.join(root, 'reference/animation_manifest.json'), 'utf8'));
  const actual = JSON.parse(await fs.readFile(path.join(root, 'generated/animation_manifest.json'), 'utf8'));
  for (const field of ['width', 'height', 'frameCount', 'totalDurationMs', 'finalFrameExactlyMatchesArtwork', 'uniqueFrames', 'monotonicallyIncreasingSceneLuminance', 'eyes', 'timeline']) {
    assert.deepEqual(actual[field], expected[field], `Manifest mismatch: ${field}`);
  }
  const frames = [];
  for (let i = 1; i <= expected.frameCount; i++) {
    const name = `frame_${String(i).padStart(2, '0')}.png`;
    const reference = await sharp(path.join(root, 'reference/frames', name)).removeAlpha().raw().toBuffer();
    const generated = await sharp(path.join(root, 'generated/frames', name)).removeAlpha().raw().toBuffer();
    assert.ok(reference.equals(generated), `Pixel mismatch: ${name}`);
    frames.push({ name, rgbPixelSha256: sha256(generated), matchesReference: true });
  }
  const gif = await sharp(path.join(root, 'generated/goldrinn_entrance.gif'), { animated: true }).removeAlpha().raw().toBuffer();
  const final = await sharp(path.join(root, 'generated/goldrinn_final.png')).removeAlpha().raw().toBuffer();
  assert.equal(gif.length, final.length * expected.frameCount);
  let errorSum = 0;
  for (let i = 0; i < final.length; i++) errorSum += Math.abs(final[i] - gif[final.length * 15 + i]);
  const result = {
    status: 'passed',
    scope: 'Offline reference material and deterministic compositor; no game or device integration tested.',
    command: 'npm ci && npm run build && npm run verify',
    runtime: { node: process.version, platform: process.platform, arch: process.arch, sharp: sharp.versions.sharp, vips: sharp.versions.vips },
    sourceArtworkSha256: sha256(await fs.readFile(path.join(root, 'goldrinn_artwork.png'))),
    promptSha256: sha256(await fs.readFile(path.join(root, 'generation_prompt.txt'))),
    matchedReferenceFrames: frames.length,
    manifestTimelineMatches: true,
    decodedGifFrames: gif.length / final.length,
    gifFinalFrameMeanAbsoluteEncodingError: errorSum / final.length,
    frames
  };
  await fs.writeFile(path.join(root, 'verification.json'), JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify({ status: result.status, matchedReferenceFrames: frames.length, decodedGifFrames: result.decodedGifFrames, gifFinalFrameMeanAbsoluteEncodingError: result.gifFinalFrameMeanAbsoluteEncodingError }, null, 2));
}
main().catch(error => { console.error(error); process.exitCode = 1; });
