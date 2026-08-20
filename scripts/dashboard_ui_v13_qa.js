const assert = require('assert');
const { chromium } = require('/vercel/sandbox/node_modules/playwright');

const BASE = process.env.QA_BASE || 'http://127.0.0.1:8765';
const DESKTOP = '/data/student_samed_dashboard_v13_desktop.png';
const MOBILE = '/data/student_samed_dashboard_v13_mobile.png';
const HUB = '/data/student_samed_physics_hub_v13.png';

const profile = { name: 'منير', grade: 12, subjects: ['physics', 'chemistry'], pin: '', createdAt: Date.now() };
const progress = {
  'physics12-foundation-momentum': { percent: 100 },
  'physics12-review-momentum': { percent: 40 },
  'physics12-textbook-momentum': { percent: 12 },
  'physics12-momentum': { percent: 0 },
  'chemistry12-foundation-atom': { percent: 0 },
  'chemistry12-review-unit1': { percent: 0 },
  'chemistry12-textbook-unit1': { percent: 0 },
  'chemistry12-atomic-structure': { percent: 0 },
};

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: '/usr/local/bin/chromium', args: ['--no-sandbox'] });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  const fatal = [];
  page.on('pageerror', error => fatal.push('pageerror: ' + error.message));
  page.on('console', msg => { if (msg.type() === 'error' && !msg.text().includes('favicon')) fatal.push('console: ' + msg.text()); });
  await page.addInitScript(({profile, progress}) => {
    localStorage.setItem('samed-profile-v1', JSON.stringify(profile));
    localStorage.setItem('samed-offline-progress-v1', JSON.stringify(progress));
  }, { profile, progress });

  await page.goto(BASE + '/index.html', { waitUntil: 'networkidle' });
  await page.waitForSelector('#dashboard:not([hidden])');
  assert.strictEqual(await page.locator('html').getAttribute('dir'), 'rtl');
  assert.strictEqual((await page.locator('#heroPct').textContent()).trim(), '30%');
  assert((await page.locator('#doneMetric').textContent()).includes('12'));
  assert((await page.locator('#stageMetric').textContent()).includes('4'));
  assert((await page.locator('#xpMetric').textContent()).includes('1250'));
  assert((await page.locator('#welcome').textContent()).includes('منير'));
  assert.strictEqual(await page.locator('#timeline .stage-card').count(), 4);
  const active = page.locator('#timeline .stage-card.is-active');
  assert.strictEqual(await active.count(), 1);
  assert((await active.locator('h3').textContent()).includes('مراجعة الوحدة'));
  assert((await active.locator('.stage-meta b').textContent()).includes('40%'));
  assert.strictEqual(await page.locator('#moduleList .module-card').count(), 3);
  for (const title of ['الزخم الخطي والدفع', 'الكهرباء الساكنة', 'البناء الإلكتروني للذرة']) {
    assert((await page.locator('#moduleList').innerText()).includes(title));
  }
  const bg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  assert(['rgb(248, 250, 252)', 'rgba(0, 0, 0, 0)'].includes(bg), bg);
  const heroBg = await page.locator('.student-hero').evaluate(el => getComputedStyle(el).backgroundImage);
  assert(heroBg.includes('linear-gradient'), heroBg);
  const widths = await page.locator('#timeline .stage-card').evaluateAll(items => items.map(x => x.getBoundingClientRect().width));
  assert(widths[1] > widths[0] + 30, JSON.stringify(widths));
  assert(await page.locator('.stage-cta', { hasText: 'تابع التعلّم' }).isVisible());
  await page.screenshot({ path: DESKTOP, fullPage: true });

  await page.setViewportSize({ width: 390, height: 844 });
  await page.reload({ waitUntil: 'networkidle' });
  await page.waitForSelector('#dashboard:not([hidden])');
  const overflow = await page.evaluate(() => ({ doc: document.documentElement.scrollWidth, inner: innerWidth, body: document.body.scrollWidth, timeline: document.querySelector('#timeline').scrollWidth, timelineClient: document.querySelector('#timeline').clientWidth }));
  assert(overflow.doc <= overflow.inner + 1, JSON.stringify(overflow));
  assert(overflow.body <= overflow.inner + 1, JSON.stringify(overflow));
  assert(overflow.timeline > overflow.timelineClient, JSON.stringify(overflow));
  await page.screenshot({ path: MOBILE, fullPage: true });

  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto(BASE + '/physics-hub.html', { waitUntil: 'networkidle' });
  assert.strictEqual(await page.locator('.hub-course-card').count(), 4);
  assert.strictEqual(await page.locator('.hub-course-card.is-current').count(), 1);
  assert((await page.locator('.hub-course-card.is-current h2').textContent()).includes('مراجعة الوحدة'));
  await page.screenshot({ path: HUB, fullPage: true });

  await page.goto(BASE + '/physics-foundation.html', { waitUntil: 'networkidle' });
  await page.waitForSelector('.rv-hero');
  assert(await page.locator('.rv-route').isVisible());
  assert((await page.locator('body').innerText()).includes('مدخل تأسيسي'));

  await page.goto(BASE + '/index.html', { waitUntil: 'networkidle' });
  await page.waitForSelector('#dashboard:not([hidden])');
  await page.evaluate(() => navigator.serviceWorker && navigator.serviceWorker.ready);
  await page.reload({ waitUntil: 'networkidle' });
  await context.setOffline(true);
  await page.reload({ waitUntil: 'domcontentloaded', timeout: 20000 });
  await page.waitForSelector('#dashboard:not([hidden])');
  assert.strictEqual((await page.locator('#heroPct').textContent()).trim(), '30%');
  await context.setOffline(false);

  assert.strictEqual(fatal.length, 0, fatal.join('\n'));
  await browser.close();
  console.log('DASHBOARD_UI_V13_BROWSER_QA_OK');
  console.log(JSON.stringify({ desktop: DESKTOP, mobile: MOBILE, hub: HUB }));
})().catch(async error => {
  console.error(error.stack || error);
  process.exit(1);
});
