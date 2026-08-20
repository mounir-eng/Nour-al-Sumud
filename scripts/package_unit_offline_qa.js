const assert = require('assert');
const path = require('path');
const { chromium } = require('/vercel/sandbox/node_modules/playwright');

(async () => {
  const root = process.env.UNIT_QA_ROOT;
  assert(root, 'UNIT_QA_ROOT is required');
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/usr/local/bin/chromium',
    args: ['--no-sandbox', '--allow-file-access-from-files'],
  });
  for (const [folder, foundation] of [
    ['physics', 'physics-foundation.html'],
    ['chemistry', 'chemistry-foundation.html'],
  ]) {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('file://' + path.join(root, folder, 'index.html'));
    assert.strictEqual(await page.locator('.hub-course-card').count(), 4);
    assert((await page.locator('body').innerText()).includes('مدخل تأسيسي'));
    const overflow = await page.evaluate(() => ({
      doc: document.documentElement.scrollWidth,
      inner: innerWidth,
    }));
    assert(overflow.doc <= overflow.inner + 1, JSON.stringify({ folder, overflow }));
    await page.goto('file://' + path.join(root, folder, foundation));
    await page.waitForSelector('.rv-hero');
    assert(await page.locator('.rv-route').isVisible());
    assert.strictEqual(errors.length, 0, errors.join('\n'));
    await page.close();
  }
  await browser.close();
  console.log('UNIT_PACKS_FILE_OFFLINE_QA_OK');
})().catch(error => {
  console.error(error.stack || error);
  process.exit(1);
});
