const assert = require('assert');
const { chromium } = require('/vercel/sandbox/node_modules/playwright');
const base = 'http://127.0.0.1:8765/';
const exe = '/usr/local/bin/chromium';

function track(page){
  const errors=[];
  page.on('pageerror',e=>errors.push('page:'+e.message));
  page.on('console',m=>{if(m.type()==='error') errors.push('console:'+m.text())});
  page.on('requestfailed',r=>errors.push('request:'+r.url()+':'+(r.failure()?.errorText||'')));
  return errors;
}

async function checkFoundation(browser, subject){
  const context=await browser.newContext({viewport:{width:1440,height:1000}});
  const page=await context.newPage(); const errors=track(page);
  await page.goto(base+subject+'-foundation.html',{waitUntil:'networkidle'});
  await page.waitForSelector('.rv-hero');
  assert.equal(await page.locator('#reviewApp').evaluate(e=>e.classList.contains('rv-loading')),false);
  assert.equal(await page.locator('body').evaluate(e=>getComputedStyle(e).direction),'rtl');
  assert.equal(await page.locator('.rv-route>div').count(),4);
  assert.equal(await page.locator('.rv-map button').count(),8);
  assert.equal(await page.locator('.rv-paragraph').first().evaluate(e=>getComputedStyle(e).fontSize),'20px');
  assert.equal(await page.locator('.rv-equation').first().evaluate(e=>getComputedStyle(e).direction),'ltr');
  assert.equal(await page.locator('.rv-solution').count(),0,'solution must be hidden before participation');
  const bodyText=await page.locator('body').innerText();
  assert(!bodyText.includes('<div class='),'raw HTML is visible');
  const titles=[];
  for(let i=0;i<8;i++){
    await page.locator('.rv-map button').nth(i).click();
    await page.waitForSelector('form#exampleForm');
    const data=await page.evaluate(i=>{const L=window.REVIEW_COURSE.lessons[i];return {id:L.id,title:L.title,fields:L.example.fields.map(f=>({key:f.key,answer:f.answer})),result:L.example.result.answer}},i);
    titles.push(data.title);
    assert.equal(await page.locator('.rv-solution').count(),0,subject+' '+data.id+' revealed solution early');
    for(const f of data.fields) await page.locator('form#exampleForm input[name="'+f.key+'"]').fill(String(f.answer));
    await page.locator('form#exampleForm input[name="__result"]').fill(String(data.result));
    await page.locator('form#exampleForm button[type="submit"]').click();
    await page.waitForSelector('.rv-solution');
    assert((await page.locator('.rv-solution-line').count())>=3,subject+' '+data.id+' solution too short');
    assert.equal(await page.locator('.rv-equation').first().evaluate(e=>getComputedStyle(e).direction),'ltr');
    const mixedBad=await page.locator('.rv-paragraph,.rv-story,.rv-example-q,.rv-point').evaluateAll(els=>els.filter(e=>/[\u0600-\u06ff]/.test(e.textContent)&&/[A-Za-z]/.test(e.textContent)&&!e.querySelector('bdi[dir="ltr"]')).length);
    assert.equal(mixedBad,0,subject+' '+data.id+' has unisolated RTL/LTR text');
  }
  assert.equal(new Set(titles).size,8);
  await page.screenshot({path:'/data/'+subject+'_foundation_desktop.png',fullPage:true});
  assert.equal(errors.length,0,errors.join('\n'));
  await context.close();
  console.log(subject.toUpperCase()+'_FOUNDATION_8_LESSONS_OK');
}

async function checkMobile(browser, file, expectedFont){
  const context=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1});
  const page=await context.newPage(); const errors=track(page);
  await page.goto(base+file,{waitUntil:'networkidle'});
  if(file.includes('foundation')||file.includes('review')){
    await page.waitForSelector('.rv-paragraph');
    assert.equal(await page.locator('.rv-paragraph').first().evaluate(e=>getComputedStyle(e).fontSize),expectedFont);
  } else await page.waitForSelector('.card');
  const dims=await page.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth}));
  assert(dims.sw<=dims.cw,'mobile overflow '+file+' '+JSON.stringify(dims));
  assert.equal(errors.length,0,errors.join('\n'));
  await context.close();
}

async function checkHubsAndReview(browser){
  for(const subject of ['physics','chemistry']){
    const page=await browser.newPage();const errors=track(page);
    await page.goto(base+subject+'-hub.html',{waitUntil:'networkidle'});
    assert.equal(await page.locator('.card').count(),4);
    assert.equal(await page.locator('a[href="'+subject+'-foundation.html"]').count(),1);
    assert((await page.locator('body').innerText()).includes('تأسيس سابق'));
    assert.equal(errors.length,0,errors.join('\n')); await page.close();
    const review=await browser.newPage();const reviewErrors=track(review);
    await review.goto(base+subject+'-review.html',{waitUntil:'networkidle'});await review.waitForSelector('.rv-paragraph');
    assert.equal(await review.locator('.rv-paragraph').first().evaluate(e=>getComputedStyle(e).fontSize),'20px');
    assert.equal(reviewErrors.length,0,reviewErrors.join('\n'));await review.close();
  }
}

async function checkOffline(browser){
  const context=await browser.newContext({viewport:{width:1000,height:800}});const page=await context.newPage();const errors=track(page);
  await page.goto(base+'index.html',{waitUntil:'networkidle'});
  await page.evaluate(()=>navigator.serviceWorker.ready.then(()=>true));
  await page.goto(base+'physics-foundation.html',{waitUntil:'networkidle'});await page.waitForSelector('.rv-hero');
  await context.setOffline(true);await page.reload({waitUntil:'domcontentloaded'});await page.waitForSelector('.rv-hero');
  assert((await page.locator('.rv-map button').count())===8);
  await context.setOffline(false);
  const caches=await page.evaluate(()=>window.caches?caches.keys():[]);
  assert(caches.some(x=>x.includes('v12')),'v12 cache missing');
  assert.equal(errors.filter(x=>!x.includes('ERR_INTERNET_DISCONNECTED')).length,0,errors.join('\n'));
  await context.close();console.log('PWA_OFFLINE_FOUNDATION_OK');
}

(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:exe,args:['--no-sandbox']});
  try{
    await checkFoundation(browser,'physics');
    await checkFoundation(browser,'chemistry');
    await checkHubsAndReview(browser);
    for(const f of ['physics-foundation.html','chemistry-foundation.html','physics-review.html','chemistry-review.html']) await checkMobile(browser,f,'19px');
    for(const f of ['physics-hub.html','chemistry-hub.html']) await checkMobile(browser,f,'');
    await checkOffline(browser);
    console.log('FOUNDATION_BROWSER_QA_OK');
  }finally{await browser.close()}
})().catch(e=>{console.error(e.stack||e);process.exit(1)});
