import { createRequire } from 'module';
import { mkdirSync, readdirSync } from 'fs';
import { join } from 'path';

const require = createRequire(import.meta.url);
const { chromium } = require('/Users/sm/Library/Caches/ms-playwright-go/1.50.1/package/index.js');

const url = process.argv[2] || 'http://localhost:3000';
const label = process.argv[3] || '';

const dir = './temporary screenshots';
mkdirSync(dir, { recursive: true });

let n = 1;
try {
  const files = readdirSync(dir);
  const nums = files.map(f => parseInt(f.match(/screenshot-(\d+)/)?.[1])).filter(Boolean);
  if (nums.length) n = Math.max(...nums) + 1;
} catch {}

const filename = label ? `screenshot-${n}-${label}.png` : `screenshot-${n}.png`;
const outPath = join(dir, filename);

const browser = await chromium.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});
const page = await browser.newPage();
await page.setViewportSize({ width: 1440, height: 900 });
await page.goto(url, { waitUntil: 'networkidle', timeout: 15000 });
await page.waitForTimeout(1500);
await page.screenshot({ path: outPath, fullPage: false });
await browser.close();

console.log(`Screenshot saved: ${outPath}`);
