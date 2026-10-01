import sys,unittest,os,asyncio
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parent))
from fastapi.testclient import TestClient
import server
class Tests(unittest.TestCase):
 def setUp(self): self.client=TestClient(server.app)
 def test_health(self):self.assertEqual(self.client.get('/health').json()['backend'],'FastAPI')
 def test_assets(self):
  for p in ['/','/app.js','/core.js','/styles.css']:
   r=self.client.get(p);self.assertEqual(r.status_code,200);self.assertEqual(r.headers['cache-control'],'no-store')
 def test_clean_ui(self):
  s=self.client.get('/').text;self.assertNotIn('Powered by',s);self.assertNotIn('Hackathon',s);self.assertIn('Audio and transcripts go to AssemblyAI',s)
 def test_proxy_frontend(self):
  s=self.client.get('/app.js').text;self.assertIn("new URL('/voice'",s);self.assertNotIn("fetch('/token')",s)
 def test_features(self):
  ui=self.client.get('/').text
  for token in ['pdf-notes','model-panel','maxlength="48000"','answer-limit','value="15" selected','history-list','No audio is recorded']:
   self.assertIn(token,ui)
  self.assertIn('historyStore',self.client.get('/core.js').text)
  self.assertIn('answerTimer',self.client.get('/core.js').text)
 def test_context_limits(self):
  import json
  server.validate_browser_message(json.dumps({'type':'session.update','session':{'system_prompt':'A'*64000}}))
  with self.assertRaises(ValueError):
   server.validate_browser_message(json.dumps({'type':'session.update','session':{'system_prompt':'A'*64001}}))
 def test_404(self):self.assertEqual(self.client.get('/missing').status_code,404)
 def test_origin(self):
  with self.assertRaises(Exception):
   with self.client.websocket_connect('/voice',headers={'origin':'https://evil.invalid'}):pass
 def test_missing_key(self):
  key=os.environ.pop('ASSEMBLYAI_API_KEY',None)
  try:
   with self.client.websocket_connect('/voice',headers={'origin':'http://testserver'}) as ws:self.assertIn('not configured',ws.receive_json()['message'])
  finally:
   if key:os.environ['ASSEMBLYAI_API_KEY']=key
 def test_rate_limit(self):
  os.environ['ASSEMBLYAI_API_KEY']='fictional-test-value';old=server.requests.copy();server.requests.clear();server.requests.extend([__import__('time').monotonic()]*20)
  try:
   with self.client.websocket_connect('/voice',headers={'origin':'http://testserver'}) as ws:self.assertIn('limit',ws.receive_json()['message'])
  finally:server.requests.clear();server.requests.extend(old);os.environ.pop('ASSEMBLYAI_API_KEY',None)
unittest.main()
