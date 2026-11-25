import asyncio, os, shutil
from playwright.async_api import async_playwright
from PIL import Image
B=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','brand')); R=os.path.abspath(os.path.join(B,'..'))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':512,'height':512})
        open(f'{B}/_fav.html','w').write('<body style="margin:0;background:transparent"><img src="favicon.svg" style="width:512px;height:512px;display:block"></body>')
        await pg.goto(f'file://{B}/_fav.html'); await pg.wait_for_timeout(300)
        await pg.screenshot(path=f'{B}/favicon-512.png',omit_background=True)
        pg2=await b.new_page(viewport={'width':1200,'height':630})
        html=f'''<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,800,100;1,9..144,600,100&family=Manrope:wght@700&display=swap" rel="stylesheet"><body style="margin:0;width:1200px;height:630px;background:url(file://{R}/img/og-base.jpg) right center/cover;position:relative">
        <div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(20,29,13,.96) 0%,rgba(20,29,13,.82) 50%,rgba(20,29,13,.1) 100%)"></div>
        <img src="file://{B}/logo-horizontal-dark.svg" style="position:absolute;left:60px;top:56px;height:78px">
        <div style="position:absolute;left:60px;top:220px;color:#F4EFE2;font:800 76px/1 Fraunces,serif;letter-spacing:-2px">From the crown<br>down to the <i style="color:#D8662C;font-weight:600">stump.</i></div>
        <div style="position:absolute;left:60px;bottom:58px;color:#F4EFE2;font:700 25px Manrope,sans-serif">★ 5.0 · 22 Google reviews · Free estimates · (352) 857-9472</div></body>'''
        open(f'{B}/_og.html','w').write(html)
        await pg2.goto(f'file://{B}/_og.html'); await pg2.wait_for_timeout(2500)
        await pg2.screenshot(path=f'{R}/img/og.jpg',type='jpeg',quality=86)
        await b.close()
asyncio.run(main())
im=Image.open(f'{B}/favicon-512.png').convert('RGBA')
for s in (16,32,180): im.resize((s,s),Image.LANCZOS).save(f'{B}/favicon-{s}.png')
im.resize((180,180),Image.LANCZOS).save(f'{R}/apple-touch-icon.png')
im.save(f'{R}/favicon.ico',sizes=[(16,16),(32,32),(48,48)])
shutil.copy(f'{B}/favicon.svg',f'{R}/favicon.svg')
os.remove(f'{B}/_og.html'); os.remove(f'{B}/_fav.html'); print('ok')
