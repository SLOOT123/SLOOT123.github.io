import sys
ROOT = r"c:\Users\slotzs\Desktop\dashtv"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import dina
app = dina.app
client = app.server.test_client()
resp = client.get('/')
print('Status:', resp.status_code)
print(resp.data.decode('utf-8')[:2000])
