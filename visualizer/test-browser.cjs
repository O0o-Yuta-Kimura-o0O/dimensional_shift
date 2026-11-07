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
    const qa = 'tmp/visualizer-v020/qa';
    mkdirSync(qa, { recursive: true });
    const count = async n => assert.equal(await root.getAttribute('data-coordinate-count'), String(n));
    const shot = async name => await root.screenshot({ path: qa + '/' + name + '.png' });
    const svg = frame.locator('.lift-scene');
    const view = async () => root.evaluate(root => Object.fromEntries(['yaw', 'pitch', 'zoom', 'scale'].map(key =>
      [key, Number(root.dataset['view' + key[0].toUpperCase() + key.slice(1)])])));
    const rendered = async () => root.evaluate(() => document.querySelector('#lift-geometry').innerHTML);
    const settleView = async () => root.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
    const close = (a, b, message) => assert.ok(Math.abs(a - b) < 1e-6 * Math.max(1, Math.abs(a), Math.abs(b)), `${message}: ${a} vs ${b}`);
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
    // Drag changes the common projection, including the newest fourth coordinate,
    // without changing the independent-coordinate model or causing auto-fit zoom.
    await root.evaluate(() => {
      window.cameraSaveCount = 0;
      const save = window.openai.setWidgetState.bind(window.openai);
      window.openai.setWidgetState = value => { window.cameraSaveCount++; return save(value); };
    });
    const initialView = await view(), initialGeometry = await rendered();
    const initialAxes = await frame.locator('#lift-axes').innerHTML();
    const bounds = await svg.boundingBox();
    await page.mouse.move(bounds.x + bounds.width / 2, bounds.y + bounds.height / 2);
    await page.mouse.down();
    await page.mouse.move(bounds.x + bounds.width / 2 + 95, bounds.y + bounds.height / 2 - 35, { steps: 8 });
    await settleView();
    assert.equal(await root.evaluate(() => window.cameraSaveCount), 0, 'Dragging does not save each pointer frame');
    assert.notEqual(await rendered(), initialGeometry);
    assert.notEqual(await frame.locator('#lift-axes').innerHTML(), initialAxes);
    close((await view()).scale, initialView.scale, 'Rotation keeps fixed scale');
    await count(4);
    await page.mouse.up(); await settleView();
    assert.equal(await root.evaluate(() => window.cameraSaveCount), 1, 'A completed drag saves once');
    assert.equal(await svg.getAttribute('class'), 'lift-scene');
    await shot('camera-rotated-real-4');
    await mode.selectOption('grid');
    assert.equal(await root.getAttribute('data-sample-count'), '81');
    const gridBefore = await rendered();
    // Pointer capture keeps working outside the viewport and release clears it.
    await page.mouse.move(bounds.x + 80, bounds.y + 80); await page.mouse.down();
    await page.mouse.move(bounds.x + 35, bounds.y - 12, { steps: 4 }); await page.mouse.up();
    await settleView();
    assert.notEqual(await rendered(), gridBefore);
    assert.equal(await root.getAttribute('data-sample-count'), '81');
    assert.equal(await svg.getAttribute('class'), 'lift-scene');
    await count(4); await shot('camera-rotated-grid-4');
    // Chromium may omit the release outside a sandbox iframe. Re-entry with no
    // pressed mouse buttons must clear the stale gesture without another turn.
    await page.mouse.move(bounds.x + 50, bounds.y + 50); await page.mouse.down();
    await page.mouse.move(bounds.x - 8, bounds.y + 40); await page.mouse.up();
    await page.mouse.move(bounds.x + 50, bounds.y + 50); await settleView();
    assert.equal(await svg.getAttribute('class'), 'lift-scene');
    // Cancelling and losing capture both end the gesture; the next drag is usable.
    for (const eventName of ['pointercancel', 'lostpointercapture']) {
      await svg.evaluate(node => node.addEventListener('pointerdown', event => { node.dataset.pointerId = event.pointerId; }, { once: true }));
      await page.mouse.move(bounds.x + 100, bounds.y + 100); await page.mouse.down();
      await svg.evaluate((node, name) => {
        const pointerId = Number(node.dataset.pointerId);
        if (name === 'lostpointercapture') node.releasePointerCapture(pointerId);
        else node.dispatchEvent(new PointerEvent(name, { pointerId }));
      }, eventName);
      await page.mouse.move(bounds.x + 110, bounds.y + 110); await page.mouse.up(); await settleView();
      assert.equal(await svg.getAttribute('class'), 'lift-scene');
    }
    await frame.locator('#lift-view-reset').click(); await settleView();
    assert.deepEqual(await view(), initialView, 'Reset restores only the camera');
    await count(4); assert.equal(await root.getAttribute('data-mode'), 'grid');
    await mode.selectOption('real');
    const extent = async () => frame.locator('#lift-geometry polygon').evaluate(node => node.getBBox().width);
    const widthBefore = await extent();
    await page.mouse.move(bounds.x + bounds.width / 2, bounds.y + bounds.height / 2);
    await page.mouse.wheel(0, -120); await settleView();
    close(await extent() / widthBefore, Math.exp(.18), 'Wheel expands geometry exponentially');
    await page.mouse.wheel(0, 120); await settleView();
    close(await extent(), widthBefore, 'Reverse wheel restores geometry size');
    const dispatchWheel = async (deltaY, deltaMode = 0) => svg.evaluate((node, values) => {
      const event = new WheelEvent('wheel', { deltaY: values[0], deltaMode: values[1], bubbles: true, cancelable: true });
      node.dispatchEvent(event); return event.defaultPrevented;
    }, [deltaY, deltaMode]);
    assert(await dispatchWheel(-1, 1)); await settleView();
    close((await view()).zoom, Math.exp(.024), 'Line wheel delta uses pixel normalization');
    await frame.locator('#lift-view-reset').click(); await settleView();
    assert(await dispatchWheel(-1, 2)); await settleView();
    close((await view()).zoom, Math.exp(bounds.height * .0015), 'Page wheel delta uses viewport height');
    for (let i = 0; i < 4; i++) await dispatchWheel(-10000);
    await settleView(); assert.equal((await view()).zoom, 5); await fits();
    assert(await frame.locator('#lift-zoom-in').isDisabled());
    for (let i = 0; i < 4; i++) await dispatchWheel(10000);
    await settleView(); assert.equal((await view()).zoom, .25);
    assert(await frame.locator('#lift-zoom-out').isDisabled());
    assert.equal(await apply.evaluate(node => {
      const event = new WheelEvent('wheel', { deltaY: 120, bubbles: true, cancelable: true });
      node.dispatchEvent(event); return event.defaultPrevented;
    }), false, 'Wheel outside the viewport remains available to page scrolling');
    await frame.locator('#lift-view-reset').click();
    await frame.locator('#lift-view-reset').focus(); await page.keyboard.press('ArrowRight'); await settleView();
    close((await view()).yaw, initialView.yaw + .12, 'Keyboard rotation');
    await page.keyboard.press('Enter'); await settleView(); assert.deepEqual(await view(), initialView);
    await frame.locator('#lift-zoom-in').click(); await settleView(); close((await view()).zoom, 1.2, 'Zoom button');
    await frame.locator('#lift-zoom-out').click(); await settleView(); close((await view()).zoom, 1, 'Zoom out button');
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
    close((await view()).zoom, 1, 'Legacy state restores default camera');
    close((await view()).yaw, .63, 'Legacy state restores default orientation');
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
    // Touch uses the same captured gesture; compact controls remain reachable.
    const mobile = await browser.newPage({ viewport: { width: 352, height: 820 }, hasTouch: true, reducedMotion: 'reduce' });
    mobile.on('pageerror', error => errors.push(error.message));
    await mobile.goto(page.url());
    const mobileFrame = mobile.frameLocator('iframe'), mobileRoot = mobileFrame.locator('#coordinate-lift-v1');
    await mobileRoot.waitFor();
    for (let i = 0; i < 3; i++) await mobileFrame.locator('#lift-apply').click();
    const mobileSvg = mobileFrame.locator('.lift-scene'), touchBounds = await mobileSvg.boundingBox();
    const touchBefore = await mobileRoot.getAttribute('data-view-yaw');
    const cdp = await mobile.context().newCDPSession(mobile);
    const touch = (type, x, y) => cdp.send('Input.dispatchTouchEvent', { type,
      touchPoints: type === 'touchEnd' ? [] : [{ x, y }] });
    await touch('touchStart', touchBounds.x + 100, touchBounds.y + 120);
    await touch('touchMove', touchBounds.x + 165, touchBounds.y + 95);
    await touch('touchEnd');
    await mobileRoot.evaluate(() => new Promise(resolve => requestAnimationFrame(resolve)));
    assert.notEqual(await mobileRoot.getAttribute('data-view-yaw'), touchBefore, 'Touch drag rotates');
    assert.equal(await mobileRoot.getAttribute('data-coordinate-count'), '3');
    assert.equal(await mobileSvg.getAttribute('class'), 'lift-scene');
    await mobileFrame.locator('#lift-zoom-in').tap();
    await mobileRoot.evaluate(() => new Promise(resolve => requestAnimationFrame(resolve)));
    assert.equal(await mobileRoot.getAttribute('data-view-zoom'), '1.2');
    await mobileRoot.screenshot({ path: qa + '/mobile-touch-rotated.png' });
    await mobile.close();
    assert.deepEqual(errors, []);
    console.log('PASS: L/undo, real/grid geometry, camera drag/capture/cancel, fixed rotation scale, normalized/clamped wheel zoom, page scroll, view reset, keyboard, touch, legacy restore, 320px dark layout, 100 coordinates, reduced motion and extrusion animation; no runtime errors.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
