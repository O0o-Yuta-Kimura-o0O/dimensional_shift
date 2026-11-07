// Optional browser smoke test. Run with Playwright available on NODE_PATH.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const { resolve } = require('node:path');
const { pathToFileURL } = require('node:url');
const { mkdirSync } = require('node:fs');

(async () => {
  const browser = await chromium.launch({ headless: true,
    ...(process.env.LIFT_BROWSER_PATH ? { executablePath: process.env.LIFT_BROWSER_PATH } : {}) });
  try {
    const page = await browser.newPage({ viewport: { width: 768, height: 860 }, reducedMotion: 'reduce' });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(pathToFileURL(resolve(process.argv[2] || 'tmp/visualizer/preview.html')).href);
    const frame = page.frameLocator('iframe');
    const root = frame.locator('#coordinate-lift-v1');
    const apply = frame.locator('#lift-apply');
    const mode = frame.locator('#lift-universe');
    await root.waitFor();
    mkdirSync('tmp/visualizer', { recursive: true });
    const count = async n => assert.equal(await root.getAttribute('data-coordinate-count'), String(n));
    const shot = async name => await root.screenshot({ path: 'tmp/visualizer/' + name + '.png' });
    const fits = async () => {
      const problems = await root.evaluate(root => {
        const bounds = root.getBoundingClientRect();
        const problems = [];
        for (const node of root.querySelectorAll('button, select, svg text')) {
          const r = node.getBoundingClientRect();
          if (r.left < bounds.left - 1 || r.right > bounds.right + 1) problems.push(node.textContent);
        }
        if (root.scrollWidth > root.clientWidth + 1) problems.push('horizontal overflow');
        return problems;
      });
      assert.deepEqual(problems, []);
    };
    await count(0);
    assert(await frame.locator('#lift-undo').isDisabled());
    await shot('real-0');
    for (let n = 1; n <= 4; n++) {
      await apply.click(); await count(n); await fits();
      await shot('real-' + n);
      await mode.selectOption('grid'); await count(n);
      assert.equal(await root.getAttribute('data-sample-count'), String(3 ** n));
      if (n <= 3) assert.equal(await frame.locator('#lift-geometry circle').count(), 3 ** n);
      assert.equal(await frame.locator('#lift-geometry line, #lift-geometry polygon').count(), 0);
      await shot('grid-' + n);
      await mode.selectOption('real'); await count(n);
    }
    for (let n = 5; n <= 7; n++) { await apply.click(); await count(n); }
    await mode.selectOption('grid');
    assert.equal(await root.getAttribute('data-sample-count'), '729');
    assert.match(await frame.locator('#lift-window').innerText(), /標本/);
    assert.match(await frame.locator('#lift-size').innerText(), /2,187/);
    await shot('grid-7');
    await frame.locator('#lift-undo').click(); await count(6);
    assert(!/標本/.test(await frame.locator('#lift-window').innerText()));
    for (let n = 6; n > 0; n--) await frame.locator('#lift-undo').click();
    await count(0);
    assert.equal(await frame.locator('#lift-geometry circle').count(), 1);
    assert(await frame.locator('#lift-undo').isDisabled());
    // Keyboard activation follows the same transition, including the initial point.
    await apply.focus(); await page.keyboard.press('Enter'); await count(1);
    await root.evaluate(async () => {
      await window.openai.setWidgetState({ modelContent: { mode: 'real', coordinateCount: 4 }, privateContent: { version: 1 } }).catch(() => {});
    });
    await count(4);
    await page.setViewportSize({ width: 352, height: 900 });
    await page.emulateMedia({ colorScheme: 'dark' });
    await fits(); await shot('narrow-dark-real-4');
    await mode.selectOption('grid'); await fits(); await shot('narrow-dark-grid-4');
    // Sustained additions update dynamic state rather than revealing a preallocated maximum.
    await apply.evaluate(button => { for (let i = 0; i < 96; i++) button.click(); });
    await count(100);
    assert.equal(await root.getAttribute('data-sample-count'), '729');
    assert.match(await frame.locator('#lift-coordinates').innerText(), /x₁₀₀/);
    await mode.selectOption('real'); await count(100);
    await fits();
    await root.evaluate(async () => {
      await window.openai.setWidgetState({ modelContent: { mode: 'real', coordinateCount: 2 }, privateContent: { version: 1 } }).catch(() => {});
    });
    await page.emulateMedia({ reducedMotion: 'no-preference' });
    const stages = await apply.evaluate(button => new Promise(resolve => {
      button.click();
      const polygon = () => document.querySelector('#lift-geometry polygon').getAttribute('points');
      const initial = polygon();
      requestAnimationFrame(() => requestAnimationFrame(() => {
        const moving = polygon();
        setTimeout(() => resolve([initial, moving, polygon()]), 500);
      }));
    }));
    assert.notEqual(stages[0], stages[1], 'Extrusion changes positions between animation frames');
    assert.notEqual(stages[1], stages[2], 'State-save echo must not finish animation early');
    await count(3);
    assert.deepEqual(errors, []);
    console.log('PASS: L/undo, mode preservation, exact grids, bounded samples, restore, keyboard, 320px dark layout, 100 coordinates, extrusion animation; no runtime errors.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
