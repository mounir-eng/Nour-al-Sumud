const assert = require('assert');
const { chromium } = require('/vercel/sandbox/node_modules/playwright');
const BASE = process.env.QA_BASE || 'http://127.0.0.1:8876';
const DESKTOP = '/data/student_samed_streamlit_dashboard_v14_desktop.png';
const MOBILE = '/data/student_samed_streamlit_dashboard_v14_mobile.png';

const data = {
  name: 'منير', grade: 12, grade_label: 'الثاني عشر', overall_pct: 30,
  done: 12, selected_total: 40, xp: 1250, allowed: ['phys', 'chem'],
  physics_live: true, chemistry_live: true,
  stage_progress: { phys: [100, 40, 12, 0], chem: [0, 0, 0, 0] },
  unit_progress: { phys: 30, chem: 0 },
};

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: '/usr/local/bin/chromium', args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  await page.goto(BASE + '/index.html', { waitUntil: 'networkidle' });
  await page.evaluate(payload => window.postMessage({ type: 'streamlit:render', args: { data: payload, physics_zip: 'UEsDBA==', chemistry_zip: 'UEsDBA==' } }, '*'), data);
  await page.waitForFunction(() => document.querySelector('#heroPct')?.textContent === '30%');
  assert((await page.locator('#welcome').textContent()).includes('منير'));
  assert.strictEqual(await page.locator('#timeline .stage-card').count(), 4);
  assert.strictEqual(await page.locator('#timeline .stage-card.is-active').count(), 1);
  assert((await page.locator('#timeline .stage-card.is-active h3').textContent()).includes('مراجعة الوحدة'));
  assert((await page.locator('#timeline .stage-card.is-active .stage-meta b').textContent()).includes('40%'));
  assert.strictEqual(await page.locator('#moduleList .module-card').count(), 3);
  assert.strictEqual(await page.locator('.path-panel:empty').count(), 0);
  const heroBackground = await page.locator('.student-hero').evaluate(el => getComputedStyle(el).backgroundImage);
  assert(heroBackground.includes('linear-gradient'), heroBackground);
  const widths = await page.locator('#timeline .stage-card').evaluateAll(items => items.map(el => el.getBoundingClientRect().width));
  assert(widths[1] > widths[0] + 30, JSON.stringify(widths));
  await page.evaluate(() => {
    window.__componentMessages = [];
    window.addEventListener('message', event => {
      if (event.data && event.data.type === 'streamlit:setComponentValue') window.__componentMessages.push(event.data);
    });
  });
  await page.locator('#timeline .stage-card.is-active .stage-cta').click();
  await page.waitForFunction(() => window.__componentMessages.some(x => x.value && x.value.action === 'phys_1'));
  await page.locator('#settingsBtn').click();
  assert(await page.locator('#settingsMenu').evaluate(el => el.classList.contains('show')));
  await page.locator('#downloadBtn').click();
  assert(await page.locator('#downloadMenu').evaluate(el => el.classList.contains('show')));
  await page.locator('#downloadBtn').click();
  assert(!(await page.locator('#downloadMenu').evaluate(el => el.classList.contains('show'))));
  await page.screenshot({ path: DESKTOP, fullPage: true });

  await page.setViewportSize({ width: 390, height: 844 });
  await page.reload({ waitUntil: 'networkidle' });
  await page.evaluate(payload => window.postMessage({ type: 'streamlit:render', args: { data: payload } }, '*'), data);
  await page.waitForFunction(() => document.querySelector('#heroPct')?.textContent === '30%');
  const overflow = await page.evaluate(() => ({ doc: document.documentElement.scrollWidth, body: document.body.scrollWidth, inner: innerWidth, timeline: document.querySelector('#timeline').scrollWidth, timelineClient: document.querySelector('#timeline').clientWidth }));
  assert(overflow.doc <= overflow.inner + 1, JSON.stringify(overflow));
  assert(overflow.body <= overflow.inner + 1, JSON.stringify(overflow));
  assert(overflow.timeline > overflow.timelineClient, JSON.stringify(overflow));
  await page.screenshot({ path: MOBILE, fullPage: true });
  assert.strictEqual(errors.length, 0, errors.join('\n'));
  await browser.close();
  console.log('STREAMLIT_DASHBOARD_V14_BROWSER_QA_OK');
  console.log(JSON.stringify({ desktop: DESKTOP, mobile: MOBILE }));
})().catch(error => { console.error(error.stack || error); process.exit(1); });
