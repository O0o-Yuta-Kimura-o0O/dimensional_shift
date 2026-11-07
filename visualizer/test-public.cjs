// Verify the exported page with an ordinary HTTP origin and no Codex host.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
  const file = path.resolve(process.argv[2] || 'tmp/publish/visualizer-site/index.html');
  const document = fs.readFileSync(file);
  const server = http.createServer((req, res) => {
    if (req.url !== '/') { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' }); res.end(document);
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  let browser;
  try {
    browser = await chromium.launch({ headless: true,
      ...(process.env.LIFT_BROWSER_PATH ? { executablePath: process.env.LIFT_BROWSER_PATH } : {}) });
    const page = await browser.newPage({ viewport: { width: 960, height: 760 }, reducedMotion: 'reduce' });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    const url = `http://127.0.0.1:${server.address().port}/`;
    const response = await page.goto(url);
    assert.equal(response.status(), 200);
    assert.equal(await page.locator('html').getAttribute('lang'), 'ja');
    assert.equal(await page.locator('meta[name="visualizer-version"]').getAttribute('content'), 'visualizer-v0.1.1');
    const frame = page.frameLocator('iframe');
    const root = frame.locator('#coordinate-lift-v1');
    await root.waitFor();
    assert.equal(await frame.locator('html').getAttribute('lang'), 'ja');
    for (let i = 0; i < 3; i++) await frame.locator('#lift-apply').click();
    await frame.locator('#lift-universe').selectOption('grid');
    const stored = await page.waitForFunction(() => Object.keys(localStorage).some(key => {
      try { const s = JSON.parse(localStorage.getItem(key)); return s?.modelContent?.coordinateCount === 3 && s?.modelContent?.mode === 'grid'; }
      catch { return false; }
    }));
    assert(await stored.jsonValue());
    await page.reload();
    await root.waitFor();
    assert.equal(await root.getAttribute('data-coordinate-count'), '3');
    assert.equal(await root.getAttribute('data-mode'), 'grid');
    assert.equal(await root.getAttribute('data-sample-count'), '27');
    fs.mkdirSync('tmp/publish/qa', { recursive: true });
    await page.screenshot({ path: 'tmp/publish/qa/public-desktop.png', fullPage: true });
    await page.setViewportSize({ width: 352, height: 820 });
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.screenshot({ path: 'tmp/publish/qa/public-mobile-dark.png', fullPage: true });
    const widths = await root.evaluate(root => [root.clientWidth, root.scrollWidth]);
    assert(widths[1] <= widths[0] + 1);
    assert.deepEqual(errors, []);
    console.log('PASS: standalone HTTP page, localStorage fallback, reload state recovery, version metadata, mobile layout; no runtime errors.');
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
