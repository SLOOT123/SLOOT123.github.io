import sys, os
ROOT = r"c:\Users\slotzs\Desktop\dashtv"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import dina
app = dina.app
print('Index string (truncated):')
print(app.index_string[:2000])
