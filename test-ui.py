import asyncio,subprocess,json
from playwright.async_api import async_playwright
async def main():
 proc=subprocess.Popen(['python3','server.py'],stdout=open('/tmp/server.log','w'),stderr=subprocess.STDOUT)
 try:
  async with async_playwright() as p:
   b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox']);page=await b.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   await page.goto('http://localhost:3000/')
   result=await page.evaluate('''()=>{const sent=[];ws={readyState:1,send:s=>sent.push(JSON.parse(s))};basePrompt='base';answerTimer=VivaCore.answerTimer(15,expireAnswer);expireAnswer();const muted=answerMuted;replyActive=true;lastEvent='reply.started';finishTimeout();const held=answerMuted;replyActive=false;lastEvent='reply.done';playbackDrained=true;finishTimeout();const modelRequested=timeoutModelRequested;replyActive=false;lastEvent='reply.done';playbackDrained=true;finishTimeout();clearTimeout(timeoutFallback);ws=null;return {sent,muted,held,reopened:!answerMuted};}''')
   assert result['muted'] and result['held'] and result['reopened'];assert len(result['sent'])==3;assert 'expired' in result['sent'][0]['session']['system_prompt'];assert result['sent'][2]['session']['system_prompt']=='base';assert result['sent'][1]['type']=='reply.create';assert 'model answer' in result['sent'][1]['instructions'];assert not errors
   print(json.dumps({'mock_timeout':'pass','errors':errors}));await b.close()
 finally:proc.terminate();proc.wait()
asyncio.run(main())
