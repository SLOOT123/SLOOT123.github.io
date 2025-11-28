import dash
import os, sys
# Asegurar que la raíz del proyecto está en sys.path para resolver imports relativos
ROOT = r"c:\Users\slotzs\Desktop\dashtv"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
PAGES = os.path.join(ROOT, "pages")
app = dash.Dash(__name__, use_pages=True, pages_folder=PAGES)
print('Dash pages folder:', app.config.pages_folder)
print('Registered pages:')
for key, page in dash.page_registry.items():
    print('-', key, 'name=', page.get('name'), 'path=', page.get('path'), 'module=', page.get('module'))
    # indicate whether module has layout attribute
    try:
        mod = __import__(page.get('module'), fromlist=['*'])
        print('   -> module has layout:', hasattr(mod, 'layout'))
    except Exception as e:
        print('   -> import error:', e)
