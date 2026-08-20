from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PWA = ROOT / "static" / "pwa"
MARK = "FINAL_UI_V13"


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def add_once(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker not in text:
        path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


# 1) Streamlit dashboard integration.
app_path = ROOT / "app.py"
app = app_path.read_text(encoding="utf-8")
app = app.replace('DASHBOARD_UX_VERSION = "dashboard-ux-v10-ultra-simple-inline"', 'DASHBOARD_UX_VERSION = "final-ui-v13-figma-rtl"')
if "from ui_theme_v13 import apply_ui_theme" not in app:
    app = app.replace("import streamlit.components.v1 as components\n", "import streamlit.components.v1 as components\nfrom ui_theme_v13 import apply_ui_theme\n", 1)
start_anchor = '    st.markdown("""\n    <style>'
fn_start = app.index("def _render_dashboard():")
start = app.index(start_anchor, fn_start)
end = app.index("    st.stop()", start)
new_dashboard = '''    from streamlit_dashboard_v13 import render_dashboard_v13
    stage_progress = {
        "phys": [
            round(100 * physics_foundation_done / 8),
            round(100 * physics_review_done / 7),
            round(100 * physics_book_done / 10),
            round(100 * physics_lesson_done / 15),
        ],
        "chem": [
            round(100 * chemistry_foundation_done / 8),
            round(100 * chemistry_review_done / 8),
            round(100 * chemistry_book_done / 20),
            round(100 * chemistry_lesson_done / 15),
        ],
    }
    unit_progress = {"phys": physics_pct, "chem": chemistry_pct}
    display_xp = max(xp, done * 100 + 50 if done else 0)
    action = render_dashboard_v13(
        profile=profile,
        safe_name=safe_name,
        grade_label=grade_label,
        overall_pct=pct,
        done=done,
        selected_total=selected_total,
        xp=display_xp,
        allowed=allowed,
        physics_live=physics_live,
        chemistry_live=chemistry_live,
        stage_progress=stage_progress,
        unit_progress=unit_progress,
        unit_bytes=_unit_download_bytes,
    )
    if action == "edit":
        st.session_state["samed_view"] = "onboarding"
        st.rerun()
    if action == "home":
        st.session_state["samed_view"] = "home"
        st.rerun()
    if action:
        routes = {
            "phys_0": ("physics_foundation", "pages/physics_foundation.py"),
            "phys_1": ("physics_review", "pages/physics_unit_review.py"),
            "phys_2": ("physics_book", "pages/physics_textbook_exercises.py"),
            "chem_0": ("chemistry_foundation", "pages/chemistry_foundation.py"),
            "chem_1": ("chemistry_review", "pages/chemistry_unit_review.py"),
            "chem_2": ("chem_book", "pages/chemistry_textbook_exercises.py"),
            "chem_3": ("chem_app", "pages/chemistry_unit_1.py"),
        }
        if action == "phys_3":
            st.session_state["samed_view"] = "app"
            st.rerun()
        if action in routes:
            view, page = routes[action]
            st.session_state["samed_view"] = view
            st.switch_page(page)
'''
app = app[:start] + new_dashboard + app[end:]
# Make the final theme available to the in-app physics practice route.
if "# FINAL_UI_V13_EXERCISE_THEME" not in app:
    app += '\n\n# FINAL_UI_V13_EXERCISE_THEME\nif st.session_state.get("samed_view") == "app":\n    apply_ui_theme("exercise")\n'
app_path.write_text(app, encoding="utf-8")

# 2) Streamlit learning pages share the final visual language.
for filename, anchor, kind in [
    ("foundation_renderer.py", "    st.markdown(_FOUNDATION_SIMPLE_CSS_V12, unsafe_allow_html=True)\n", "foundation"),
    ("review_renderer.py", "    st.markdown(_EXTRA_LARGE_CSS, unsafe_allow_html=True)\n", "review"),
]:
    path = ROOT / filename
    text = path.read_text(encoding="utf-8")
    if "from ui_theme_v13 import apply_ui_theme" not in text:
        text = text.replace("import streamlit as st\n", "import streamlit as st\nfrom ui_theme_v13 import apply_ui_theme\n", 1)
    call = f'    apply_ui_theme("{kind}")\n'
    if call not in text:
        if anchor not in text:
            raise RuntimeError(f"missing renderer anchor: {filename}")
        text = text.replace(anchor, anchor + call, 1)
    path.write_text(text, encoding="utf-8")

for rel in ["pages/physics_textbook_exercises.py", "pages/chemistry_textbook_exercises.py", "pages/chemistry_unit_1.py"]:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if "from ui_theme_v13 import apply_ui_theme" not in text:
        text = text.replace("import streamlit.components.v1 as components\n", "import streamlit.components.v1 as components\nfrom ui_theme_v13 import apply_ui_theme\n", 1)
    if "# FINAL_UI_V13_EXERCISE_THEME" not in text:
        text += '\n\n# FINAL_UI_V13_EXERCISE_THEME\napply_ui_theme("exercise")\n'
    path.write_text(text, encoding="utf-8")

# 3) PWA cache and manifest.
write(PWA / "service-worker.js", """const CORE='samed-core-v13',UNITS='samed-units-v13';
const ASSETS=['./','./index.html','./app.js','./styles.css','./dashboard-v13.css','./manifest.webmanifest','./icon-192.png','./icon-512.png','./offline.html'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CORE).then(cache=>cache.addAll(ASSETS)).then(()=>self.skipWaiting())));
self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>![CORE,UNITS].includes(key)).map(key=>caches.delete(key)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',event=>{if(event.request.method!=='GET')return;event.respondWith(caches.match(event.request).then(hit=>hit||fetch(event.request).then(response=>{const copy=response.clone();caches.open(CORE).then(cache=>cache.put(event.request,copy));return response}).catch(()=>caches.match('./offline.html'))))});
""")
manifest = (PWA / "manifest.webmanifest").read_text(encoding="utf-8").replace("#082f49", "#245e65")
write(PWA / "manifest.webmanifest", manifest)

# 4) PWA hubs, using the same dashboard design language.
def hub(subject: str) -> str:
    physics = subject == "physics"
    icon = "⚛️" if physics else "🧪"
    label = "الفيزياء" if physics else "الكيمياء"
    title = "الزخم الخطي والدفع" if physics else "البناء الإلكتروني للذرة"
    total = 40 if physics else 51
    keys = ["physics12-foundation-momentum", "physics12-review-momentum", "physics12-textbook-momentum", "physics12-momentum"] if physics else ["chemistry12-foundation-atom", "chemistry12-review-unit1", "chemistry12-textbook-unit1", "chemistry12-atomic-structure"]
    hrefs = [f"{subject}-foundation.html", f"{subject}-review.html", f"{subject}-textbook.html", "unit.html" if physics else "chemistry-unit.html"]
    counts = ["8 محاور", "7 دروس" if physics else "8 دروس", "10 أسئلة" if physics else "20 تمرينًا", "15 تمرينًا"]
    stages = [("🧱", "مدخل تأسيسي", "استرجع الأساس المطلوب من الصفين 10 و11"), ("🧭", "مراجعة الوحدة", "افهم المفاهيم والعلاقات بهدوء"), ("📘", "تمارين الكتاب", "طبّق بخطوات كاملة دون اختصار"), ("🎯", "تدريب إضافي", "ثبّت الفهم بأسئلة جديدة")]
    cards = []
    for i, ((stage_icon, stage_title, desc), href, count) in enumerate(zip(stages, hrefs, counts)):
        cards.append(f'''<article class="hub-course-card" id="hubCard{i}"><span class="hub-chip">المرحلة {i+1}</span><span class="module-icon">{stage_icon}</span><h2>{stage_title}</h2><p>{desc}</p><div class="stage-progress"><i id="bar{i}" style="width:0%"></i></div><div class="stage-meta"><span>{count}</span><b id="pct{i}">0%</b></div><a class="stage-cta" href="{href}">{'ابدأ' if i == 0 else 'فتح'} المرحلة ←</a></article>''')
    key_js = ",".join(repr(k) for k in keys)
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#245e65"><title>مسار {label} — {title}</title><link rel="icon" href="icon-192.png"><link rel="stylesheet" href="dashboard-v13.css"></head><body class="hub-ui"><header class="student-header"><div class="ui-container student-header-inner"><div class="student-brand"><span class="brand-shield">{icon}</span><span><b>{label} · الصف الثاني عشر</b><small>مسار علاجي يبدأ من الأساس</small></span></div><div class="header-actions"><a id="back" class="ui-control" href="index.html">لوحة الطالب</a></div></div></header><main class="ui-container hub-main"><section class="hub-hero"><div><span class="hero-label">{icon} الوحدة الأولى</span><h1>{title}</h1><p>مسار واضح يحمي الطالب من القفز إلى الإجابة: تأسيس، ثم مراجعة، ثم تمارين الكتاب، ثم تدريب إضافي.</p></div><div class="hub-stats"><div class="hub-stat"><b>{total}</b><small>محتوى تعليمي</small></div><div class="hub-stat"><b>4</b><small>مراحل متدرجة</small></div><div class="hub-stat"><b>أوفلاين</b><small>بعد تحميل الوحدة</small></div></div></section><div class="section-title ui-section"><div><h2>خريطة الوحدة</h2><p>تُبرز المرحلة التالية تلقائيًا حسب تقدمك</p></div><span class="title-side">لا قفز إلى النتيجة</span></div><section class="hub-stage-grid">{''.join(cards)}</section></main><script>(()=>{{let progress={{}};try{{progress=JSON.parse(localStorage.getItem('samed-offline-progress-v1')||'{{}}')}}catch(e){{}}const keys=[{key_js}];const values=keys.map(key=>Math.max(0,Math.min(100,Number((progress[key]||{{}}).percent||0))));let active=values.findIndex(value=>value<100);if(active<0)active=3;values.forEach((value,index)=>{{document.getElementById('pct'+index).textContent=Math.round(value)+'%';document.getElementById('bar'+index).style.width=value+'%';const card=document.getElementById('hubCard'+index);if(value>=100)card.classList.add('is-done');if(index===active)card.classList.add('is-current')}});if(location.protocol==='file:')document.getElementById('back').style.display='none'}})();</script></body></html>'''

write(PWA / "physics-hub.html", hub("physics"))
write(PWA / "chemistry-hub.html", hub("chemistry"))

# 5) Existing PWA lesson/exercise pages receive the same surfaces and palette.
content_css = r'''/* FINAL_UI_V13_CONTENT */
:root{--navy:#173f44;--navy2:#245e65;--teal:#347d78;--gold:#f5c65a;--bg:#f8fafc;--ink:#173b3d;--muted:#71847f;--line:#dfe7e5;--shadow:0 16px 42px rgba(23,63,68,.09)}
body{background:#f8fafc;color:#173b3d}.top{background:linear-gradient(125deg,#245e65,#3e8179 62%,#6a9679)!important}.card,.statement,.qnav{border-color:#dfe7e5!important;border-radius:19px!important;box-shadow:0 7px 22px rgba(23,63,68,.055)!important}.hero{border-radius:24px!important}.qbtn,.step-tile,.dock-panel,.formula,.solution,.law{border-radius:14px!important}.btn.primary{background:#236b78!important;border-color:#236b78!important}.step-tile.current{border-color:#347d78!important;box-shadow:0 0 0 3px rgba(52,125,120,.10)!important}.step-number{background:#e8f4f0!important}.notice{border-radius:15px!important}
'''
add_once(PWA / "styles.css", "FINAL_UI_V13_CONTENT", content_css)
review_css = r'''/* FINAL_UI_V13_REVIEW */
:root{--rv-accent:#347d78;--rv-deep:#1d5156;--rv-soft:#eef8f4;--rv-ink:#173b3d;--rv-muted:#71847f;--rv-line:#dfe7e5}body.review-page{background:#f8fafc}.rv-shell{max-width:1220px}.rv-hero{background:linear-gradient(125deg,#245e65 0%,#3e8179 58%,#6a9679 115%);border-radius:28px;box-shadow:0 20px 46px rgba(28,88,87,.18)}.rv-ring:after{background:#37736f}.rv-card,.rv-lesson-head,.rv-visual,.rv-viz{border-radius:20px;border-color:#dfe7e5;box-shadow:0 7px 22px rgba(23,63,68,.055)}.rv-formula{background:linear-gradient(135deg,#1d5156,#286a6d);border-radius:19px;box-shadow:0 12px 28px rgba(29,81,86,.13)}.rv-route>div,.rv-map button{border-radius:14px}.rv-route .active{background:#eef8f4;border-color:#9fc5bb}.rv-route .active b{background:#347d78}.rv-action{background:#236b78;border-radius:12px}.foundation-page .rv-simple-sentence{background:#eef8f4;border-color:#b9dacf}.foundation-page .rv-inline-input{border-bottom-color:#347d78}
'''
add_once(PWA / "review.css", "FINAL_UI_V13_REVIEW", review_css)

# 6) Landing palette follows the dashboard while preserving its structure.
landing = ROOT / "landing_component" / "index.html"
text = landing.read_text(encoding="utf-8")
text = text.replace('content="#08345f"', 'content="#245e65"')
text = text.replace('--navy:#082c4c;--navy2:#0c3e68;--ink:#0c2036;--muted:#60758a;', '--navy:#173f44;--navy2:#245e65;--ink:#173b3d;--muted:#71847f;')
text = text.replace('--teal:#08a98a;--teal2:#07856e;--violet:#7554e8;--amber:#f6bb42;', '--teal:#347d78;--teal2:#286a6d;--violet:#8460b8;--amber:#f5c65a;')
landing.write_text(text, encoding="utf-8")

# 7) Release notes.
readme = ROOT / "README_AR.md"
section = '''\n\n## التصميم النهائي للمنصة v13\n- لوحة طالب RTL مستوحاة من نموذج Figma المرفق: هيدر هادئ، Hero زيتي/زمردي، مؤشر إنجاز أصفر، وإحصاءات سريعة.\n- مسار أفقي من أربع مراحل يتسع فيه العنصر النشط تلقائيًا.\n- الوحدات تعرض كبطاقات مطوية مع وسوم حالة ومؤشر دائري صغير.\n- اعتماد نظام بصري موحد على صفحات التأسيس والمراجعة وتمارين الكتاب والتدريب.\n- جميع الأنماط محلية بلا Tailwind CDN حتى يبقى التشغيل دون اتصال حقيقيًا.\n'''
if "التصميم النهائي للمنصة v13" not in readme.read_text(encoding="utf-8"):
    readme.write_text(readme.read_text(encoding="utf-8").rstrip() + section, encoding="utf-8")
write(ROOT / "RELEASE_V13_AR.txt", """منصة الطالب الصامد — الإصدار v13 للتصميم النهائي\n================================================\n\n- Dashboard عربي RTL مطابق للهوية البصرية المرفقة.\n- خلفية #F8FAFC وتدرج زيتي/زمردي وظلال خفيفة.\n- Hero بثلاث مناطق: الترحيب، الإنجاز، الإحصاءات.\n- Learning Timeline من أربع مراحل وبطاقة نشطة عريضة.\n- Course Modules كبطاقات Accordions مع Tags ومؤشرات دائرية.\n- توحيد الهوية في صفحات المسارات والتأسيس والمراجعة والتمارين.\n- CSS محلي بأسلوب Tailwind/Figma بلا مكتبات خارجية، للحفاظ على الأوفلاين.\n""")

print("FINAL_UI_V13_APPLIED")
