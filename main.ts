// Entry point for the news-image-20261124 submission.
//
// The whole entry is the poster in entry.png next to this file. This
// program's only job is to deliver those exact bytes to the grader:
// it checks the poster is present and within the size gate, then
// copies it into the output directory unchanged.
//
// The grader mounts the output directory at /output; anywhere else,
// set MAKEFUN_OUTPUT_DIR to stand in for it, e.g.
//   MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ONE_MIB = 1024 * 1024;

const here = dirname(fileURLToPath(import.meta.url));
const posterPath = join(here, 'entry.png');
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const targetPath = join(outputDir, 'entry.png');

function fail(message) {
  console.error(`main.ts: error: ${message}`);
  process.exit(1);
}

if (!existsSync(posterPath)) {
  fail(`entry.png not found beside main.ts (looked in ${here})`);
}

const poster = statSync(posterPath);
if (!poster.isFile()) {
  fail(`entry.png exists but is not a regular file: ${posterPath}`);
}
if (poster.size === 0) {
  fail('entry.png is empty; refusing to hand in a blank poster');
}
if (poster.size > ONE_MIB) {
  fail(`entry.png is ${poster.size} bytes, over the 1 MiB gate (${ONE_MIB} bytes)`);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(posterPath, targetPath);

const delivered = statSync(targetPath);
console.log(`main.ts: copied entry.png (${delivered.size} bytes) to ${targetPath}`);
