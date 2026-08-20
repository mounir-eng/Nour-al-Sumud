from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; PWA=ROOT/'static'/'pwa'

def one(s,o,n,label):
 c=s.count(o)
 if c!=1: raise RuntimeError(f'{label}: {c}')
 return s.replace(o,n,1)

def hub(subject):
 phy=subject=='physics'; ar='الفيزياء' if phy else 'الكيمياء'; unit='الزخم الخطي والدفع' if phy else 'البناء الإلكتروني للذرة'; icon='⚛️' if phy else '🧪'; p='physics' if phy else 'chemistry';
 c1,c2,ink,line=('#073b62','#0e78ad','#17324b','#d5e4ef') if phy else ('#43266f','#8052bd','#2f2540','#e3dbee')
 total=40 if phy else 51; counts=(8,7,10,15) if phy else (8,8,20,15)
 ids=('physics12-foundation-momentum','physics12-review-momentum','physics12-textbook-momentum','physics12-momentum') if phy else ('chemistry12-foundation-atom','chemistry12-review-unit1','chemistry12-textbook-unit1','chemistry12-atomic-structure')
 practice='unit.html' if phy else 'chemistry-unit.html'
 css=f'''*{{box-sizing:border-box}}body{{margin:0;background:#f5f8fc;font-family:"Noto Sans Arabic",Tahoma,Arial,sans-serif;direction:rtl;color:{ink}}}.hub{{max-width:1240px;margin:auto;padding:27px 20px 58px}}.top{{display:flex;justify-content:space-between;align-items:center;gap:14px;margin-bottom:18px}}.brand{{display:flex;align-items:center;gap:13px}}.brand>span{{width:56px;height:56px;border-radius:17px;background:linear-gradient(135deg,{c1},{c2});display:grid;place-items:center;font-size:30px;color:white}}.brand b{{display:block;font-size:20px}}.brand small{{font-size:14px;opacity:.7}}.hero{{background:linear-gradient(135deg,{c1},{c2});color:white;border-radius:27px;padding:31px;box-shadow:0 18px 40px #17324b24}}.hero h1{{margin:0 0 9px;font-size:35px}}.hero p{{margin:0;font-size:18px;line-height:2;color:#ffffffe8}}.stats{{display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin-top:19px}}.stat{{background:#ffffff1f;border:1px solid #ffffff2b;border-radius:15px;padding:13px}}.stat b{{display:block;font-size:23px}}.stat small{{font-size:14px}}.flow{{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin:15px 0}}.flow div{{background:white;border:1px solid {line};border-radius:14px;padding:12px;display:flex;align-items:center;gap:9px;font-size:15px;font-weight:850}}.flow b{{width:31px;height:31px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(135deg,{c1},{c2});color:white}}.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:13px}}.card{{background:white;border:1px solid {line};border-radius:20px;padding:20px;box-shadow:0 9px 27px #0d3a5a0f;display:flex;flex-direction:column;min-height:345px;position:relative}}.card.foundation{{border-top:6px solid #e17d2f;background:linear-gradient(180deg,#fff9f1,#fff 36%)}}.card.review{{border-top:6px solid #159b88}}.card.book{{border-top:6px solid #e2a022}}.card.practice{{border-top:6px solid #5477c7}}.tag{{position:absolute;left:14px;top:13px;font-size:12px;font-weight:900;background:#eef3f6;padding:5px 8px;border-radius:99px}}.ico{{width:55px;height:55px;border-radius:16px;display:grid;place-items:center;font-size:28px;background:#eef7fb}}.card h2{{font-size:23px;margin:14px 0 8px}}.card p{{font-size:16px;line-height:1.95;color:#617584;margin:0 0 13px}}.recommend{{display:inline-block;width:max-content;background:#fff0dc;color:#9c4d0f;border-radius:99px;padding:5px 9px;font-size:12px;font-weight:900;margin-bottom:8px}}.meta{{display:flex;gap:6px;flex-wrap:wrap;margin:auto 0 13px}}.meta span{{background:#f2f5f7;border-radius:99px;padding:6px 9px;font-size:12px;font-weight:800}}.progress{{height:9px;background:#e8eef2;border-radius:99px;overflow:hidden;margin-bottom:14px}}.progress i{{display:block;height:100%;background:linear-gradient(135deg,{c1},{c2})}}.btn{{display:block;text-decoration:none;text-align:center;border-radius:12px;padding:12px 14px;font-size:16px;font-weight:850;background:linear-gradient(135deg,{c1},{c2});color:white}}.btn.outline{{background:white;color:{c1};border:1px solid {line}}}@media(max-width:1100px){{.grid{{grid-template-columns:1fr 1fr}}}}@media(max-width:760px){{.grid,.flow,.stats{{grid-template-columns:1fr}}.hero{{padding:24px 19px}}.hero h1{{font-size:29px}}.hero p{{font-size:17px}}.card{{min-height:0}}.brand b{{font-size:17px}}.hub{{padding:19px 13px 40px}}}}'''
 def card(cls,tag,ico,title,desc,meta,href,cta,extra=''):
  return f'<article class="card {cls}"><span class="tag">{tag}</span><span class="ico">{ico}</span><h2>{title}</h2>{extra}<p>{desc}</p><div class="meta"><span>{meta}</span><span id="{cls}Pct">0% مكتمل</span></div><div class="progress"><i id="{cls}Bar" style="width:0%"></i></div><a class="btn" href="{href}">{cta} ←</a></article>'
 cards=''.join([
 card('foundation','المدخل','🧱','الدرس التأسيسي','استرجع مهارات الصفين العاشر والحادي عشر التي تحتاجها الوحدة، مع شرح هادئ ومثال تشارك في تعويضه.',f'{counts[0]} محاور · من المرفق',f'{p}-foundation.html','بدء التأسيس','<span class="recommend">ابدأ من هنا أولًا</span>'),
 card('review','المرحلة 1','🧭','مراجعة مفاهيم الوحدة','ابنِ مفاهيم الصف الثاني عشر بالعلاقات الكاملة والأمثلة الموجهة بعد تثبيت الأساس.',f'{counts[1]} دروس مراجعة',f'{p}-review.html','بدء المراجعة'),
 card('book','المرحلة 2','📘','حل تمارين الكتاب','طبّق المفاهيم على أسئلة الكتاب بخطوات كاملة من القانون إلى التعويض والنتيجة.',f'{counts[2]} تمرينًا',f'{p}-textbook.html','فتح تمارين الكتاب'),
 card('practice','المرحلة 3','🎯','تدريب إضافي','ثبّت الفهم بأسئلة جديدة متدرجة، وارجع إلى العلاقة اللازمة دون كشف الإجابة.',f'{counts[3]} تمرينًا',practice,'بدء التدريب')])
 script=f'''<script>(()=>{{let x={{}};try{{x=JSON.parse(localStorage.getItem('samed-offline-progress-v1')||'{{}}')}}catch(e){{}}const a=[['foundation','{ids[0]}'],['review','{ids[1]}'],['book','{ids[2]}'],['practice','{ids[3]}']];for(const [n,k] of a){{const v=(x[k]||{{}}).percent||0;document.getElementById(n+'Pct').textContent=v+'% مكتمل';document.getElementById(n+'Bar').style.width=v+'%'}}if(location.protocol==='file:')document.getElementById('back').style.display='none'}})();</script>'''
 return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="{c1}"><title>مسار {ar} — {unit}</title><link rel="stylesheet" href="styles.css"><link rel="icon" href="icon-192.png"><style>{css}</style></head><body><main class="hub"><div class="top"><div class="brand"><span>{icon}</span><div><b>{ar} · الصف الثاني عشر</b><small>مسار علاجي يبدأ من الأساس</small></div></div><a id="back" class="btn outline" href="index.html">لوحة الطالب</a></div><section class="hero"><h1>{unit}</h1><p>لأن الانقطاع الطويل يترك فجوات، يبدأ المسار بدرس تأسيسي من مقررات السنوات السابقة، ثم ينتقل إلى مراجعة الوحدة وتمارينها.</p><div class="stats"><div class="stat"><b>{total}</b><small>محورًا ودرسًا وتمرينًا</small></div><div class="stat"><b>4</b><small>مراحل متدرجة واضحة</small></div><div class="stat"><b>أوفلاين</b><small>المسار كامل بعد التحميل</small></div></div></section><div class="flow"><div><b>0</b> تأسيس سابق</div><div><b>1</b> مراجعة الوحدة</div><div><b>2</b> تمارين الكتاب</div><div><b>3</b> تدريب إضافي</div></div><section class="grid">{cards}</section></main>{script}</body></html>'''

(PWA/'physics-hub.html').write_text(hub('physics'),'utf-8'); (PWA/'chemistry-hub.html').write_text(hub('chemistry'),'utf-8')

# Dashboard totals, progress and entry buttons.
path=ROOT/'app.py'; s=path.read_text('utf-8')
s=one(s,'DASHBOARD_UX_VERSION = "dashboard-ux-v8-rtl-readable-review"','DASHBOARD_UX_VERSION = "dashboard-ux-v9-foundation-large-type"','version')
s=one(s,'    physics_review_completed = st.session_state.get("physreview_completed_questions", set()) or set()','    physics_review_completed = st.session_state.get("physreview_completed_questions", set()) or set()\n    physics_foundation_completed = st.session_state.get("physfoundation_completed_questions", set()) or set()','physics set')
s=one(s,'    chemistry_review_completed = st.session_state.get("chemreview_completed_questions", set()) or set()','    chemistry_review_completed = st.session_state.get("chemreview_completed_questions", set()) or set()\n    chemistry_foundation_completed = st.session_state.get("chemfoundation_completed_questions", set()) or set()','chem set')
s=one(s,'    physics_review_done = sum(1 for qid in physics_review_completed if str(qid).startswith("pr"))\n    physics_done = physics_review_done + physics_book_done + physics_lesson_done','    physics_review_done = sum(1 for qid in physics_review_completed if str(qid).startswith("pr"))\n    physics_foundation_done = sum(1 for qid in physics_foundation_completed if str(qid).startswith("pf"))\n    physics_done = physics_foundation_done + physics_review_done + physics_book_done + physics_lesson_done','physics count')
s=one(s,'    chemistry_review_done = sum(1 for qid in chemistry_review_completed if str(qid).startswith("cr"))\n    chemistry_done = chemistry_review_done + chemistry_book_done + chemistry_lesson_done','    chemistry_review_done = sum(1 for qid in chemistry_review_completed if str(qid).startswith("cr"))\n    chemistry_foundation_done = sum(1 for qid in chemistry_foundation_completed if str(qid).startswith("cf"))\n    chemistry_done = chemistry_foundation_done + chemistry_review_done + chemistry_book_done + chemistry_lesson_done','chem count')
s=one(s,'    physics_total, chemistry_total = 32, 43','    physics_total, chemistry_total = 40, 51','totals')
s=one(s,'    xp = st.session_state.get("total_xp", 0) + st.session_state.get("physbook_total_xp", 0) + st.session_state.get("physreview_total_xp", 0) + st.session_state.get("chem_total_xp", 0) + st.session_state.get("book_total_xp", 0) + st.session_state.get("chemreview_total_xp", 0)','    xp = st.session_state.get("total_xp", 0) + st.session_state.get("physbook_total_xp", 0) + st.session_state.get("physfoundation_total_xp", 0) + st.session_state.get("physreview_total_xp", 0) + st.session_state.get("chem_total_xp", 0) + st.session_state.get("book_total_xp", 0) + st.session_state.get("chemfoundation_total_xp", 0) + st.session_state.get("chemreview_total_xp", 0)','xp')
s=one(s,'<p>1 مراجعة 7 دروس · 2 حلول 10 أسئلة · 3 تدريب 15 تمرينًا</p>','<p>مدخل تأسيسي 8 محاور · 1 مراجعة 7 دروس · 2 حلول 10 أسئلة · 3 تدريب 15 تمرينًا</p>','physics copy')
s=s.replace('المسار المقترح: 1 مراجعة الدرس ← 2 تمارين الكتاب ← 3 تدريب إضافي.','المسار المقترح: مدخل تأسيسي ← 1 مراجعة الوحدة ← 2 تمارين الكتاب ← 3 تدريب إضافي.',1)
old='''                if st.button("1️⃣ مراجعة الدرس والمفاهيم", use_container_width=True, key="dashboard_review_physics"):
                    st.session_state["samed_view"] = "physics_review"
                    st.switch_page("pages/physics_unit_review.py")'''
new='''                if st.button("0️⃣ الدرس التأسيسي للصفين 10 و11", use_container_width=True, key="dashboard_foundation_physics"):
                    st.session_state["samed_view"] = "physics_foundation"
                    st.switch_page("pages/physics_foundation.py")
                if st.button("1️⃣ مراجعة الوحدة الحالية", use_container_width=True, key="dashboard_review_physics"):
                    st.session_state["samed_view"] = "physics_review"
                    st.switch_page("pages/physics_unit_review.py")'''
s=one(s,old,new,'physics button')
s=one(s,'<p>1 مراجعة 8 دروس · 2 حلول 20 تمرينًا · 3 تدريب 15 تمرينًا</p>','<p>مدخل تأسيسي 8 محاور · 1 مراجعة 8 دروس · 2 حلول 20 تمرينًا · 3 تدريب 15 تمرينًا</p>','chem copy')
s=one(s,'المسار المقترح: 1 مراجعة الدرس ← 2 تمارين الكتاب ← 3 تدريب إضافي.','المسار المقترح: مدخل تأسيسي ← 1 مراجعة الوحدة ← 2 تمارين الكتاب ← 3 تدريب إضافي.','chem path')
old='''                if st.button("1️⃣ مراجعة الدرس والمفاهيم", use_container_width=True, key="dashboard_review_chemistry"):
                    st.session_state["samed_view"] = "chemistry_review"
                    st.switch_page("pages/chemistry_unit_review.py")'''
new='''                if st.button("0️⃣ الدرس التأسيسي للصفين 10 و11", use_container_width=True, key="dashboard_foundation_chemistry"):
                    st.session_state["samed_view"] = "chemistry_foundation"
                    st.switch_page("pages/chemistry_foundation.py")
                if st.button("1️⃣ مراجعة الوحدة الحالية", use_container_width=True, key="dashboard_review_chemistry"):
                    st.session_state["samed_view"] = "chemistry_review"
                    st.switch_page("pages/chemistry_unit_review.py")'''
s=one(s,old,new,'chem button'); path.write_text(s,'utf-8')

# Add all foundation assets to unit packages.
pack=Path('/data/package_professional_review_final.py'); x=pack.read_text('utf-8')
x=one(x,"common=['review.js','review.css'","common=['review.js','foundation.js','review.css'",'package common')
x=one(x,"['physics-hub.html','physics-review.html'","['physics-hub.html','physics-foundation.html','physics-review.html'",'package physics html')
x=one(x,"'unit-physics-review-data.js'","'unit-physics-foundation-data.js','unit-physics-review-data.js'",'package physics data')
x=one(x,"['chemistry-hub.html','chemistry-review.html'","['chemistry-hub.html','chemistry-foundation.html','chemistry-review.html'",'package chem html')
x=one(x,"'unit-chemistry-review-data.js'","'unit-chemistry-foundation-data.js','unit-chemistry-review-data.js'",'package chem data')
pack.write_text(x,'utf-8')

readme=ROOT/'README_AR.md'; md=readme.read_text('utf-8')
if '## المدخل التأسيسي للسنوات السابقة' not in md:
 md+='''\n\n## المدخل التأسيسي للسنوات السابقة\n\nتبدأ الوحدة الأولى في الفيزياء والكيمياء بمرحلة تأسيسية مستقلة من مفاهيم الصفين العاشر والحادي عشر، ثم مراجعة الوحدة الحالية، ثم تمارين الكتاب، ثم التدريب الإضافي. يشمل تأسيس الفيزياء الوحدات والمتجهات والحركة وقوانين نيوتن والطاقة، ويشمل تأسيس الكيمياء بنية الذرة والجسيمات والنظائر والأيونات والأغلفة وإلكترونات التكافؤ. تعمل المرحلة دون اتصال بعد تحميل الوحدة، وخطوط الشرح والحقول مكبرة بوضوح.\n'''
 readme.write_text(md,'utf-8')
print('FOUNDATION_JOURNEY_INTEGRATED')
