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
    const expectedVersion = JSON.parse(fs.readFileSync(path.join(__dirname, 'version.json'), 'utf8')).version;
    assert.equal(await page.locator('meta[name="visualizer-version"]').getAttribute('content'), expectedVersion);
    const frame = page.frameLocator('iframe');
    const root = frame.locator('#coordinate-lift-v1');
    await root.waitFor();
    assert.equal(await frame.locator('html').getAttribute('lang'), 'ja');
    for (let i = 0; i < 3; i++) await frame.locator('#lift-apply').click();
    await frame.locator('#lift-universe').selectOption('grid');
    const svg = frame.locator('.lift-scene'), bounds = await svg.boundingBox();
    await page.mouse.move(bounds.x + 120, bounds.y + 120); await page.mouse.down();
    await page.mouse.move(bounds.x + 210, bounds.y + 150, { steps: 5 }); await page.mouse.up();
    await page.mouse.wheel(0, -120);
    await root.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    const camera = await root.evaluate(root => ({ yaw: Number(root.dataset.viewYaw), pitch: Number(root.dataset.viewPitch), zoom: Number(root.dataset.viewZoom) }));
    assert.notEqual(camera.yaw, .63);
    assert(camera.zoom > 1);
    const geometry = await frame.locator('#lift-geometry').innerHTML();
    const stored = await page.waitForFunction(() => Object.keys(localStorage).some(key => {
      try { const s = JSON.parse(localStorage.getItem(key)); return s?.modelContent?.coordinateCount === 3 && s?.modelContent?.mode === 'grid'; }
      catch { return false; }
    }));
    assert(await stored.jsonValue());
    await page.waitForFunction(camera => Object.keys(localStorage).some(key => {
      try {
        const s = JSON.parse(localStorage.getItem(key));
        return s?.privateContent?.version === 2 && ['yaw', 'pitch', 'zoom'].every(k => s.privateContent.camera[k] === camera[k]);
      } catch { return false; }
    }), camera);
    await page.reload();
    await root.waitFor();
    assert.equal(await root.getAttribute('data-coordinate-count'), '3');
    assert.equal(await root.getAttribute('data-mode'), 'grid');
    assert.equal(await root.getAttribute('data-sample-count'), '27');
    assert.deepEqual(await root.evaluate(root => ({ yaw: Number(root.dataset.viewYaw), pitch: Number(root.dataset.viewPitch), zoom: Number(root.dataset.viewZoom) })), camera);
    assert.equal(await frame.locator('#lift-geometry').innerHTML(), geometry, 'Reload preserves rotated and zoomed lattice');
    fs.mkdirSync('tmp/visualizer-v020/qa', { recursive: true });
    await page.screenshot({ path: 'tmp/visualizer-v020/qa/final-desktop.png', fullPage: true });
    await page.setViewportSize({ width: 352, height: 820 });
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.reload(); await root.waitFor();
    await svg.evaluate(node => new Promise(resolve => {
      const ready = () => Number(node.getAttribute('viewBox').split(' ')[2]) === node.clientWidth
        ? requestAnimationFrame(() => requestAnimationFrame(resolve)) : requestAnimationFrame(ready);
      ready();
    }));
    await page.screenshot({ path: 'tmp/visualizer-v020/qa/final-mobile-dark.png', fullPage: true });
    const widths = await root.evaluate(root => [root.clientWidth, root.scrollWidth]);
    assert(widths[1] <= widths[0] + 1);
    await page.evaluate(() => {
      for (const key of Object.keys(localStorage)) {
        try {
          const state = JSON.parse(localStorage.getItem(key));
          if (state?.modelContent?.coordinateCount === 3) {
            state.privateContent = { version: 1 }; localStorage.setItem(key, JSON.stringify(state));
          }
        } catch {}
      }
    });
    await page.reload(); await root.waitFor();
    assert.equal(await root.getAttribute('data-coordinate-count'), '3');
    assert.equal(await root.getAttribute('data-mode'), 'grid');
    assert.equal(await root.getAttribute('data-view-yaw'), '0.63');
    assert.equal(await root.getAttribute('data-view-zoom'), '1');
    assert.deepEqual(errors, []);
    console.log('PASS: standalone HTTP page, version metadata, camera/model persistence and reload, legacy state migration, mobile layout; no runtime errors.');
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
