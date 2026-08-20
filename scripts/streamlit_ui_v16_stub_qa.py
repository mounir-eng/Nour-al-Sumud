from __future__ import annotations
import base64,importlib,sys,types
from pathlib import Path
markdown_calls=[];component_calls=[]
streamlit=types.ModuleType('streamlit');streamlit.session_state={};streamlit.markdown=lambda body,**kwargs:markdown_calls.append(str(body))
components_pkg=types.ModuleType('streamlit.components');components_v1=types.ModuleType('streamlit.components.v1')
def declare_component(name,path):
    assert name=='student_samed_dashboard_v16',name
    p=Path(path);assert (p/'index.html').is_file();assert (p/'dashboard.css').is_file()
    def component(**kwargs):component_calls.append(kwargs);return None
    return component
components_v1.declare_component=declare_component;components_pkg.v1=components_v1;streamlit.components=components_pkg
sys.modules['streamlit']=streamlit;sys.modules['streamlit.components']=components_pkg;sys.modules['streamlit.components.v1']=components_v1
module=importlib.import_module('streamlit_dashboard_v13');assert module.DASHBOARD_UI_VERSION=='streamlit-dashboard-v16-navigation-account'
result=module.render_dashboard_v13(profile={'name':'منير','grade':12,'subjects':['phys','chem']},safe_name='منير',grade_label='الثاني عشر',overall_pct=30,done=12,selected_total=40,xp=1250,allowed=['phys','chem'],physics_live=True,chemistry_live=True,stage_progress={'phys':[100,40,12,0],'chem':[0,0,0,0]},unit_progress={'phys':30,'chem':0},unit_bytes=lambda name:b'PK\x03\x04')
assert result is None and len(component_calls)==1
call=component_calls[0];assert call['key']=='student_samed_dashboard_v16';assert base64.b64decode(call['physics_zip'])==b'PK\x03\x04';assert 'streamlit-dashboard-v16-parent' in '\n'.join(markdown_calls)
app=Path('app.py').read_text('utf-8');landing=Path('landing_component/index.html').read_text('utf-8');dash=Path('dashboard_component/index.html').read_text('utf-8');account=Path('onboarding_component/index.html').read_text('utf-8');pwa=Path('static/pwa/index.html').read_text('utf-8');pwa_js=Path('static/pwa/app.js').read_text('utf-8')
assert 'student_samed_onboarding_v16' in app and 'passwordHash' in app and 'تأكيدها غير متطابقين' in app
onboarding=app[app.index('def _render_onboarding():'):app.index('\ndef _unit_download_bytes')]
assert 'رمز PIN' not in onboarding and 'PWA' not in onboarding and 'back_home' in onboarding
for token in ['landing-ui-v16','howModal','howWorksBtn','جميع المواد ستتوفر قريبًا','parentScrollContext','measuredLandingHeight']:assert token in landing,token
for token in ['dashboardParentContext','أونلاين','أوفلاين','سطح المكتب','اللوحات','الهاتف','UI v16']:assert token in dash,token
footer=dash[dash.index('<footer'):dash.index('</footer>')+9];assert 'ZIP' not in footer
for token in ['كلمة المرور','تأكيد كلمة المرور','الرجوع إلى الرئيسية','تعمل حتى عند انقطاع الإنترنت','جميع المواد قريبًا']:assert token in account,token
assert 'رمز PIN' not in pwa and 'confirmPassword' in pwa and 'passwordDigest' in pwa_js and "samed-units-v16" in pwa_js
for path in [Path('app.py'),Path('landing_component/index.html'),Path('dashboard_component/index.html'),Path('onboarding_component/index.html'),Path('static/pwa/index.html'),Path('static/pwa/app.js')]:assert '\ufffd' not in path.read_text('utf-8'),path
print('STREAMLIT_UI_V16_NAVIGATION_ACCOUNT_STUB_QA_OK')
