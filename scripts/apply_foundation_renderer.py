from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def one(s,o,n,label):
 c=s.count(o)
 if c!=1: raise RuntimeError(f'{label}: {c}')
 return s.replace(o,n,1)

base=ROOT/'review_renderer.py'
s=base.read_text('utf-8')
extra=r'''

# FOUNDATION_LARGE_TYPE_V11
_EXTRA_LARGE_CSS = r"""
<style>
.rv-paragraph{font-size:20px!important;line-height:2.08!important}.rv-story{font-size:19px!important;line-height:2!important}.rv-card h3,.rv-example-head h3{font-size:24px!important}.rv-lesson-head h2{font-size:33px!important}.rv-lesson-head p{font-size:19px!important;line-height:1.9!important}.rv-hero h1{font-size:39px!important}.rv-hero p{font-size:19px!important;line-height:1.95!important}.rv-source{font-size:15px!important}.rv-point{font-size:17px!important;line-height:1.9!important}.rv-example-q{font-size:18px!important;line-height:2!important}.rv-plan div{font-size:16px!important;line-height:1.9!important}.rv-givens span{font-size:15px!important}.rv-formula p{font-size:17px!important;line-height:1.9!important}.rv-equation{font-size:31px!important}.rv-substitution{font-size:21px!important}.rv-field label{font-size:16px!important;line-height:1.8!important}.rv-field input{font-size:18px!important}.rv-option{font-size:17px!important;line-height:1.85!important}.rv-action,.rv-nav button{font-size:17px!important}.rv-support,.rv-memory,.rv-mistake{font-size:17px!important;line-height:1.95!important}.rv-symbol span{font-size:16px!important}.rv-symbol small{font-size:14px!important}.rv-symbol code{font-size:20px!important}.rv-solution>b{font-size:18px!important}.rv-solution-line{font-size:19px!important}.rv-interpret{font-size:17px!important;line-height:1.9!important}.rv-map button b{font-size:15px!important;line-height:1.8!important}.rv-map button small{font-size:13px!important}.rv-map-head small{font-size:14px!important}.rv-kicker,.rv-route>div{font-size:15px!important}.rv-route small{font-size:13px!important}.rv-lesson-head .tag{font-size:14px!important}.viz-caption{font-size:16px!important}.viz-label{font-size:18px!important}div[data-testid="stTextInput"] label p,div[data-testid="stSelectbox"] label p{font-size:17px!important;line-height:1.8!important}div[data-baseweb="input"] input,div[data-baseweb="select"]{font-size:18px!important}
@media(max-width:820px){.rv-paragraph{font-size:19px!important}.rv-story{font-size:18px!important}.rv-card h3,.rv-example-head h3{font-size:22px!important}.rv-lesson-head h2{font-size:28px!important}.rv-lesson-head p{font-size:18px!important}.rv-hero h1{font-size:32px!important}.rv-hero p{font-size:18px!important}.rv-equation{font-size:26px!important}.rv-substitution{font-size:19px!important}.rv-field label{font-size:16px!important}}
</style>
"""
'''
if 'FOUNDATION_LARGE_TYPE_V11' not in s:
 s=one(s,'def _esc(value: Any) -> str:',extra+'\n\ndef _esc(value: Any) -> str:','insert css')
 s=one(s,'    st.markdown(_BASE_CSS, unsafe_allow_html=True)','    st.markdown(_BASE_CSS, unsafe_allow_html=True)\n    st.markdown(_EXTRA_LARGE_CSS, unsafe_allow_html=True)','use css')
 base.write_text(s,'utf-8')

# Generate a dedicated foundation renderer from the same engine.
f=s.replace('def render_review_course(course: dict[str, Any]) -> None:','def render_foundation_course(course: dict[str, Any]) -> None:',1)
f=f.replace('page_title=f"مراجعة {course[\'title\']}"','page_title=f"تأسيس {course[\'title\']}"',1)
f=one(f,"        st.markdown(f'<div class=\"rv-topline\"><b>المرحلة 1</b><span>مراجعة الدرس</span><span>←</span><span>المرحلة 2: تمارين الكتاب</span><span>←</span><span>المرحلة 3: تدريب إضافي</span></div>', unsafe_allow_html=True)","        st.markdown('<div class=\"rv-topline\"><b>المدخل التأسيسي</b><span>مهارات الصفين 10 و11</span><span>←</span><span>1 مراجعة الوحدة</span><span>←</span><span>2 تمارين الكتاب</span><span>←</span><span>3 تدريب إضافي</span></div>', unsafe_allow_html=True)",'top path')
f=f.replace('مراجعة علاجية · ليست صفحة تمارين','جسر تأسيسي · من مهارات الصفين 10 و11').replace('تقدم المراجعة','تقدم التأسيس').replace('دروس مفاهيم','محاور تأسيسية')
f=one(f,"    st.markdown('<div class=\"rv-route\"><div class=\"rv-route-item active\"><b>1</b><span>افهم المفهوم<br><small>قصة + نموذج + علاقة</small></span></div><div class=\"rv-route-item\"><b>2</b><span>طبّق على الكتاب<br><small>بعد إتمام المراجعة</small></span></div><div class=\"rv-route-item\"><b>3</b><span>ثبّت بالتدريب<br><small>أسئلة إضافية</small></span></div></div>', unsafe_allow_html=True)","    st.markdown('<div class=\"rv-route rv-route-foundation\"><div class=\"rv-route-item active\"><b>0</b><span>أعد بناء الأساس<br><small>فكرة + نموذج + مشاركة</small></span></div><div class=\"rv-route-item\"><b>1</b><span>راجع الوحدة</span></div><div class=\"rv-route-item\"><b>2</b><span>حل تمارين الكتاب</span></div><div class=\"rv-route-item\"><b>3</b><span>تدرّب إضافيًا</span></div></div>', unsafe_allow_html=True)",'route')
f=f.replace('اختر مفهومًا للمراجعة','اختر مهارة تأسيسية')
f=f.replace('<h2>خريطة المفاهيم</h2><small>تصفحها بالترتيب أو عد إلى نقطة الضعف مباشرة</small>','<h2>خريطة الأساسيات</h2><small>ابدأ من أول فجوة أو انتقل إلى المهارة التي تحتاجها</small>')
f=f.replace('المفهوم <bdi class="rv-ltr" dir="ltr">{index+1}</bdi>','المحور التأسيسي <bdi class="rv-ltr" dir="ltr">{index+1}</bdi>')
f=f.replace('✓ اكتمل هذا الدرس: فهمت الفكرة، نفذت التعويض، وثبّت التفسير.','✓ اكتمل هذا المحور التأسيسي: فهمت الفكرة، ونفذت التطبيق، وثبّت التفسير.')
f=f.replace('→ المفهوم السابق','→ المحور السابق').replace('المفهوم التالي ←','المحور التالي ←')
f=one(f,'        st.success("أكملت مراجعة مفاهيم الوحدة. المرحلة التالية المقترحة هي حل تمارين الكتاب المدرسي.", icon="🎉")\n        if st.button("الانتقال إلى المرحلة 2: تمارين الكتاب", type="primary", use_container_width=True, key=f"{prefix}_to_book"):\n            st.switch_page(course["next_page"])','        st.success("أكملت الجسر التأسيسي. أصبحت جاهزًا للمرحلة التالية: مراجعة مفاهيم الوحدة الحالية.", icon="🎉")\n        if st.button("الانتقال إلى المرحلة 1: مراجعة الوحدة", type="primary", use_container_width=True, key=f"{prefix}_to_review"):\n            st.switch_page(course["next_page"])','finish')
f=f.replace('    st.markdown(_EXTRA_LARGE_CSS, unsafe_allow_html=True)','    st.markdown(_EXTRA_LARGE_CSS, unsafe_allow_html=True)\n    st.markdown("<style>.rv-route-foundation{grid-template-columns:repeat(4,1fr)!important}@media(max-width:820px){.rv-route-foundation{grid-template-columns:1fr 1fr!important}}</style>", unsafe_allow_html=True)',1)

# Add compact visual models for each prerequisite family.
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
insert='    foundation_visuals = {\n'+''.join(f'        {k!r}: {v!r},\n' for k,v in visuals.items())+'    }\n    if kind in foundation_visuals:\n        return \'<div class="rv-viz">\' + foundation_visuals[kind] + \'</div>\'\n'
f=one(f,'def _visual(kind: str) -> str:\n    visuals = {','def _visual(kind: str) -> str:\n'+insert+'    visuals = {','visual branch')
(ROOT/'foundation_renderer.py').write_text(f,'utf-8')

wrapper='''from pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[1]\nif str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))\nfrom foundation_content import {course}\nfrom foundation_renderer import render_foundation_course\nrender_foundation_course({course})\n'''
(ROOT/'pages'/'physics_foundation.py').write_text(wrapper.format(course='PHYSICS_FOUNDATION'),'utf-8')
(ROOT/'pages'/'chemistry_foundation.py').write_text(wrapper.format(course='CHEMISTRY_FOUNDATION'),'utf-8')
print('FOUNDATION_RENDERER_OK')
