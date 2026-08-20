from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]; PWA=ROOT/'static'/'pwa'; sys.path.insert(0,str(ROOT))
from foundation_content import PHYSICS_FOUNDATION,CHEMISTRY_FOUNDATION

def one(s,o,n,label):
 c=s.count(o)
 if c!=1: raise RuntimeError(f'{label}: {c}')
 return s.replace(o,n,1)

for subject,course in [('physics',PHYSICS_FOUNDATION),('chemistry',CHEMISTRY_FOUNDATION)]:
 (PWA/f'unit-{subject}-foundation-data.js').write_text('window.REVIEW_COURSE = '+json.dumps(course,ensure_ascii=False,separators=(',',':'))+';\n','utf-8')
 title='المدخل التأسيسي للميكانيكا' if subject=='physics' else 'المدخل التأسيسي لبنية الذرة'; theme='#0a3b59' if subject=='physics' else '#432b69'
 html=f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="{theme}"><title>{title}</title><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="review.css"><link rel="icon" href="icon-192.png"></head><body class="review-page foundation-page" data-theme="{subject}"><div id="reviewApp" class="rv-loading">جارٍ تحميل الدرس التأسيسي…</div><script src="unit-{subject}-foundation-data.js"></script><script src="foundation.js"></script></body></html>'
 (PWA/f'{subject}-foundation.html').write_text(html,'utf-8')

visuals={
'foundation_units':'<div class="viz-row"><span class="viz-box">km/h</span><span class="viz-arrow">÷3.6 →</span><span class="viz-box">m/s</span></div><div class="viz-caption">وحّد الوحدات قبل الحساب</div>',
'foundation_vectors':'<div class="viz-row"><span class="viz-arrow">◀ 11 N</span><span class="viz-big">📦</span><span class="viz-arrow">18 N ▶</span></div><div class="viz-caption">اجمع المتجهات بالإشارات</div>',
'foundation_motion':'<div class="viz-row"><span class="viz-box">−5 m</span><span class="viz-arrow">────▶</span><span class="viz-box">+13 m</span></div><div class="viz-caption"><bdi class="rv-ltr" dir="ltr">Δx=x_f−x_i</bdi></div>',
'foundation_acceleration':'<div class="viz-row"><span class="viz-box">4 m/s</span><span class="viz-arrow">3 s →</span><span class="viz-box">16 m/s</span></div><div class="viz-caption">تغير السرعة في كل ثانية</div>',
'foundation_newton2':'<div class="viz-row"><span class="viz-arrow">◀ 8 N</span><span class="viz-big">🛒</span><span class="viz-arrow">24 N ▶</span></div><div class="viz-caption"><bdi class="rv-ltr" dir="ltr">ΣF=ma</bdi></div>',
'foundation_newton3':'<div class="viz-row"><span class="viz-big">✋</span><span class="viz-arrow">45 N ▶</span><span class="viz-big">🧱</span><span class="viz-arrow">◀ 45 N</span></div><div class="viz-caption">قوتان على جسمين مختلفين</div>',
'foundation_energy':'<div class="viz-row"><span class="viz-label">v ×2</span><span class="viz-arrow">→</span><span class="viz-label">K ×4</span></div><div class="viz-caption"><bdi class="rv-ltr" dir="ltr">K=½mv²</bdi></div>',
'foundation_bridge':'<div class="viz-row"><span class="viz-box">FΔt</span><span class="viz-arrow">⇄</span><span class="viz-box">mΔv</span></div><div class="viz-caption">الجسر إلى الدفع والزخم</div>',
'foundation_matter':'<div class="viz-row"><span class="viz-box">H</span><span class="viz-arrow">—</span><span class="viz-box">O</span><span class="viz-arrow">—</span><span class="viz-box">H</span></div><div class="viz-caption">رموز الذرات في الجزيء</div>',
'foundation_particles':'<div class="viz-row"><span class="viz-box">p⁺</span><span class="viz-box">n⁰</span><span class="viz-arrow">نواة</span><span class="viz-box">e⁻</span></div><div class="viz-caption">الموقع والشحنة</div>',
'foundation_nuclear':'<div class="viz-row"><span class="viz-big"><bdi class="rv-ltr" dir="ltr">²⁷₁₃Al</bdi></span></div><div class="viz-caption"><bdi class="rv-ltr" dir="ltr">A</bdi> أعلى و<bdi class="rv-ltr" dir="ltr">Z</bdi> أسفل</div>',
'foundation_isotopes':'<div class="viz-row"><span class="viz-box">³⁵Cl</span><span class="viz-arrow">نفس Z</span><span class="viz-box">³⁷Cl</span></div><div class="viz-caption">نظائر العنصر نفسه</div>',
'foundation_models':'<div class="viz-row"><span class="viz-label">دالتون</span><span class="viz-arrow">→</span><span class="viz-label">طومسون</span><span class="viz-arrow">→</span><span class="viz-label">رذرفورد</span></div><div class="viz-caption">الدليل يطوّر النموذج</div>',
'foundation_ions':'<div class="viz-row"><span class="viz-box">Cl</span><span class="viz-arrow">+e⁻ →</span><span class="viz-box">Cl⁻</span></div><div class="viz-caption">اكتساب الإلكترون يعطي أيونًا سالبًا</div>',
'foundation_shells':'<div class="viz-row"><span class="viz-big">◎</span><span class="viz-label"><bdi class="rv-ltr" dir="ltr">2n²</bdi></span></div><div class="viz-caption">سعة مستويات الطاقة</div>',
'foundation_valence':'<div class="viz-row"><span class="viz-box">2</span><span class="viz-box">8</span><span class="viz-box">2</span></div><div class="viz-caption">العدد الأخير إلكترونات التكافؤ</div>'}
js=(PWA/'review.js').read_text('utf-8')
js=one(js,"const STATE_KEY='samed-review-state-'+C.id","const STATE_KEY='samed-foundation-state-'+C.id",'state')
js=one(js,"if(!C||!app){if(app)app.textContent='تعذر تحميل محتوى المراجعة.';return}","if(!C||!app){if(app)app.textContent='تعذر تحميل محتوى الدرس التأسيسي.';return}",'error')
js=one(js,'document.body.dataset.theme=C.theme;','document.body.dataset.theme=C.theme;document.body.classList.add(\'foundation-page\');','body class')
fm='const fm='+json.dumps(visuals,ensure_ascii=False,separators=(',',':'))+";if(fm[kind])return '<div class=\"rv-visual\">'+fm[kind]+'</div>';"
js=one(js,'function visual(kind){const m={','function visual(kind){'+fm+'const m={','visuals')
old="const finish=P.done===C.lessons.length?`<section class=\"rv-finish\"><h3>🎉 اكتملت مراجعة الوحدة</h3><p>المرحلة التالية هي تطبيق الفهم على تمارين الكتاب المدرسي.</p><a href=\"${C.theme==='physics'?'physics-textbook.html':'chemistry-textbook.html'}\">المرحلة 2: تمارين الكتاب ←</a></section>`:'';"
new="const finish=P.done===C.lessons.length?`<section class=\"rv-finish\"><h3>🎉 اكتمل الجسر التأسيسي</h3><p>أصبحت جاهزًا لمراجعة مفاهيم الوحدة الحالية.</p><a href=\"${esc(C.next_href)}\">المرحلة 1: مراجعة الوحدة ←</a></section>`:'';"
js=one(js,old,new,'finish')
old='<header class="rv-top"><a class="rv-back" href="${C.theme===\'physics\'?\'physics-hub.html\':\'chemistry-hub.html\'}">→ مسار الوحدة</a><div class="rv-breadcrumb"><bdi class="rv-ltr" dir="ltr">1</bdi> مراجعة الدرس ← <bdi class="rv-ltr" dir="ltr">2</bdi> تمارين الكتاب ← <bdi class="rv-ltr" dir="ltr">3</bdi> تدريب إضافي</div></header><section class="rv-hero"><div class="rv-hero-copy"><span class="rv-kicker">${esc(C.icon)} مراجعة علاجية · ليست صفحة تمارين</span>'
new='<header class="rv-top"><a class="rv-back" href="${C.theme===\'physics\'?\'physics-hub.html\':\'chemistry-hub.html\'}">→ مسار الوحدة</a><div class="rv-breadcrumb">مدخل تأسيسي ← <bdi class="rv-ltr" dir="ltr">1</bdi> مراجعة الوحدة ← <bdi class="rv-ltr" dir="ltr">2</bdi> تمارين الكتاب ← <bdi class="rv-ltr" dir="ltr">3</bdi> تدريب إضافي</div></header><section class="rv-hero"><div class="rv-hero-copy"><span class="rv-kicker">${esc(C.icon)} جسر تأسيسي · من مهارات الصفين 10 و11</span>'
js=one(js,old,new,'header')
js=one(js,'<span>تقدم المراجعة</span>','<span>تقدم التأسيس</span>','progress')
js=one(js,'دروس مفاهيم</small>','محاور تأسيسية</small>','progress units')
old='<div class="rv-route"><div class="active"><b>1</b><span>افهم المفهوم<br><small>قصة + نموذج + علاقة</small></span></div><div><b>2</b><span>طبّق على الكتاب</span></div><div><b>3</b><span>ثبّت بالتدريب</span></div></div><div class="rv-map-head"><h2>خريطة المفاهيم</h2><small>انتقل إلى نقطة الضعف مباشرة</small></div><nav class="rv-map" aria-label="خريطة المفاهيم">'
new='<div class="rv-route rv-route-foundation"><div class="active"><b>0</b><span>أعد بناء الأساس<br><small>فكرة + نموذج + مشاركة</small></span></div><div><b>1</b><span>راجع الوحدة</span></div><div><b>2</b><span>حل تمارين الكتاب</span></div><div><b>3</b><span>تدرّب إضافيًا</span></div></div><div class="rv-map-head"><h2>خريطة الأساسيات</h2><small>انتقل إلى المهارة التي تحتاجها</small></div><nav class="rv-map" aria-label="خريطة الأساسيات">'
js=one(js,old,new,'route')
js=one(js,'<span class="tag">المفهوم ','<span class="tag">المحور التأسيسي ','tag')
js=one(js,'✓ اكتمل هذا الدرس: فهمت الفكرة، نفذت التعويض، وثبّت التفسير.','✓ اكتمل هذا المحور التأسيسي: فهمت الفكرة، ونفذت التطبيق، وثبّت التفسير.','complete')
js=one(js,'→ المفهوم السابق','→ المحور السابق','prev'); js=one(js,'المفهوم التالي ←','المحور التالي ←','next')
(PWA/'foundation.js').write_text(js,'utf-8')

css=PWA/'review.css'; s=css.read_text('utf-8')
if 'FOUNDATION_LARGE_TYPE_V11' not in s:
 s+=r'''\n/* FOUNDATION_LARGE_TYPE_V11 */\nbody.review-page{font-size:18px!important}.rv-paragraph{font-size:20px!important;line-height:2.08!important}.rv-story{font-size:19px!important;line-height:2!important}.rv-card h3,.rv-example-head h3{font-size:24px!important}.rv-lesson-head h2{font-size:33px!important}.rv-lesson-head p{font-size:19px!important;line-height:1.9!important}.rv-hero h1{font-size:39px!important}.rv-hero p{font-size:19px!important;line-height:1.95!important}.rv-source{font-size:15px!important}.rv-point{font-size:17px!important;line-height:1.9!important}.rv-example-q{font-size:18px!important;line-height:2!important}.rv-plan div{font-size:16px!important;line-height:1.9!important}.rv-givens span{font-size:15px!important}.rv-formula p{font-size:17px!important;line-height:1.9!important}.rv-equation{font-size:31px!important}.rv-substitution{font-size:21px!important}.rv-field label{font-size:16px!important;line-height:1.8!important}.rv-field input{font-size:18px!important}.rv-option{font-size:17px!important;line-height:1.85!important}.rv-action,.rv-nav button{font-size:17px!important}.rv-support,.rv-memory,.rv-mistake{font-size:17px!important;line-height:1.95!important}.rv-symbol span{font-size:16px!important}.rv-symbol small{font-size:14px!important}.rv-symbol code{font-size:20px!important}.rv-solution>b{font-size:18px!important}.rv-solution-line{font-size:19px!important}.rv-interpret{font-size:17px!important;line-height:1.9!important}.rv-map button b{font-size:15px!important;line-height:1.8!important}.rv-map button small{font-size:13px!important}.rv-map-head small{font-size:14px!important}.rv-kicker,.rv-route>div{font-size:15px!important}.rv-route small{font-size:13px!important}.rv-lesson-head .tag{font-size:14px!important}.viz-caption{font-size:16px!important}.viz-label{font-size:18px!important}.foundation-page .rv-route-foundation{grid-template-columns:repeat(4,1fr)!important}@media(max-width:820px){.rv-paragraph{font-size:19px!important}.rv-story{font-size:18px!important}.rv-card h3,.rv-example-head h3{font-size:22px!important}.rv-lesson-head h2{font-size:28px!important}.rv-lesson-head p{font-size:18px!important}.rv-hero h1{font-size:32px!important}.rv-hero p{font-size:18px!important}.rv-equation{font-size:26px!important}.rv-substitution{font-size:19px!important}.foundation-page .rv-route-foundation{grid-template-columns:1fr 1fr!important}}\n'''
 css.write_text(s,'utf-8')

app=PWA/'app.js'; a=app.read_text('utf-8')
a=one(a,"['./physics-hub.html','./physics-review.html'","['./physics-hub.html','./physics-foundation.html','./physics-review.html'",'physics html')
a=one(a,"'./unit-physics-review-data.js'","'./unit-physics-foundation-data.js','./unit-physics-review-data.js'",'physics data')
a=one(a,"['./chemistry-hub.html','./chemistry-review.html'","['./chemistry-hub.html','./chemistry-foundation.html','./chemistry-review.html'",'chem html')
a=one(a,"'./unit-chemistry-review-data.js'","'./unit-chemistry-foundation-data.js','./unit-chemistry-review-data.js'",'chem data')
# foundation.js belongs to both unit caches.
a=a.replace("'./review.js','./review.css'","'./review.js','./foundation.js','./review.css'")
app.write_text(a,'utf-8')
sw=PWA/'service-worker.js'; w=sw.read_text('utf-8').replace('samed-core-v10','samed-core-v11').replace('samed-units-v10','samed-units-v11'); sw.write_text(w,'utf-8')
print('FOUNDATION_PWA_BUILT')
