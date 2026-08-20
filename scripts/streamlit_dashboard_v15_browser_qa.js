const assert = require('assert');
const { chromium } = require('/vercel/sandbox/node_modules/playwright');
const BASE = process.env.QA_BASE || 'http://127.0.0.1:8876';
const DESKTOP = '/data/student_samed_streamlit_dashboard_v15_desktop.png';
const MOBILE = '/data/student_samed_streamlit_dashboard_v15_mobile.png';

async function waitForDashboard(page) {
  await page.goto(BASE + '/scripts/dashboard_component_harness_v15.html', { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.__componentReady === true);
  const frame = page.frames().find(item => item.url().includes('/dashboard_component/index.html'));
  assert(frame, 'component iframe missing');
  await frame.waitForFunction(() => document.querySelector('#heroPct')?.textContent === '30%');
  await page.waitForTimeout(700);
  return frame;
}

async function assertStableHeight(page, frame, maxHeight) {
  const first = await page.locator('#component').evaluate(el => Math.round(el.getBoundingClientRect().height));
  const countBefore = await page.evaluate(() => window.__heightEvents.length);
  await page.waitForTimeout(1200);
  const second = await page.locator('#component').evaluate(el => Math.round(el.getBoundingClientRect().height));
  const countAfter = await page.evaluate(() => window.__heightEvents.length);
  assert.strictEqual(second, first, `iframe kept growing: ${first} -> ${second}`);
  assert(second > 900 && second < maxHeight, `unexpected iframe height ${second}`);
  assert(countAfter - countBefore <= 1, `height kept emitting: ${countBefore} -> ${countAfter}`);
  const geometry = await frame.evaluate(() => ({
    innerHeight,
    mainBottom: Math.ceil(document.querySelector('.student-main').getBoundingClientRect().bottom),
    scrollHeight: document.documentElement.scrollHeight,
  }));
  assert(geometry.mainBottom <= geometry.innerHeight, JSON.stringify(geometry));
  assert(geometry.innerHeight - geometry.mainBottom <= 12, JSON.stringify(geometry));
  return { height: second, events: countAfter, geometry };
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: '/usr/local/bin/chromium', args: ['--no-sandbox'] });
  const errors = [];
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  const frame = await waitForDashboard(page);
  assert((await frame.locator('#welcome').textContent()).includes('منير'));
  assert.strictEqual(await frame.locator('.quick-access').count(), 1);
  assert.strictEqual(await frame.locator('#timeline .stage-card').count(), 4);
  assert.strictEqual(await frame.locator('#timeline .stage-card.is-active').count(), 1);
  assert.strictEqual(await frame.locator('#moduleList .module-card').count(), 3);
  assert.strictEqual(await frame.locator('#platformFooter').count(), 1);
  assert.strictEqual(await frame.locator('.trust-item').count(), 3);
  assert((await frame.locator('#platformFooter').innerText()).includes('خصوصية محلية'));
  assert((await frame.locator('#platformFooter').innerText()).includes('مصممة للاتصال الضعيف'));
  const stableDesktop = await assertStableHeight(page, frame, 2700);
  await frame.locator('#continueQuick').click();
  await page.waitForFunction(() => window.__componentValues.some(value => value && value.action === 'phys_1'));
  await page.screenshot({ path: DESKTOP, fullPage: true });

  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 } });
  mobile.on('pageerror', error => errors.push(error.message));
  mobile.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  const mobileFrame = await waitForDashboard(mobile);
  const stableMobile = await assertStableHeight(mobile, mobileFrame, 3900);
  const overflow = await mobile.evaluate(() => ({ width: innerWidth, doc: document.documentElement.scrollWidth, body: document.body.scrollWidth }));
  assert(overflow.doc <= overflow.width + 1, JSON.stringify(overflow));
  assert(overflow.body <= overflow.width + 1, JSON.stringify(overflow));
  const timeline = await mobileFrame.locator('#timeline').evaluate(el => ({ scroll: el.scrollWidth, client: el.clientWidth }));
  assert(timeline.scroll > timeline.client, JSON.stringify(timeline));
  const footerColumns = await mobileFrame.locator('.footer-main').evaluate(el => getComputedStyle(el).gridTemplateColumns.split(' ').length);
  assert.strictEqual(footerColumns, 1);
  await mobile.screenshot({ path: MOBILE, fullPage: true });

  assert.strictEqual(errors.length, 0, errors.join('\n'));
  await browser.close();
  console.log('STREAMLIT_DASHBOARD_V15_STABLE_UX_BROWSER_QA_OK');
  console.log(JSON.stringify({ desktop: DESKTOP, mobile: MOBILE, stableDesktop, stableMobile }));
})().catch(error => { console.error(error.stack || error); process.exit(1); });
