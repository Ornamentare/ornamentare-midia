import json, sys, base64, pathlib
from playwright.sync_api import sync_playwright

ART = pathlib.Path('/tmp/claude-0/sp/art')
P = json.load(open(ART / 'louças.json'))

def b64(p):
    return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()

MONO = b64(ART / 'mono_w.png'); LOGOS = b64(ART / 'logos_w.png')
def img(i): return b64(ART / f'img/t_{i}.png')

def brl(v):
    s = f'{v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return s

# nome curto e linha de acabamento
INFO = {
 '42723': ('Cuba de apoio quadrada com mesa', 'VANILLA'),
 '42394': ('Cuba de apoio Trapez', 'ÉBANO FOSCO'),
 '23884': ('Cuba de apoio cilíndrica', 'BRANCO'),
 '41081': ('Cuba de apoio quadrada com mesa', 'BRANCO'),
 '45508': ('Cuba de sobrepor redonda', 'BRANCO FOSCO'),
 '38579': ('Cuba de apoio retangular com mesa', 'ÉBANO'),
 '39815': ('Bacia convencional Deca Wish', 'BRANCO'),
 '43632': ('Cuba de apoio triangular Jader Almeida', 'BRANCA'),
 '44382': ('Cuba de sobrepor redonda bicolor', 'MARROM FOSCO · BRANCO FOSCO'),
 '44374': ('Cuba de sobrepor redonda Seda texturizada', 'BRANCO FOSCO'),
 '1099': ('Lavatório de sobrepor quadrado', 'BRANCO'),
 '42719': ('Cuba de sobrepor retangular', 'KALE GREEN'),
 '16088': ('Cuba de sobrepor redonda', 'BRANCO'),
 '37525': ('Cuba de apoio redonda com mesa', 'BRANCO'),
 '15741': ('Cuba de apoio quadrada', 'BRANCO'),
 '39174': ('Cuba de apoio Trapez', 'BRANCO'),
 '51517': ('Cuba de sobrepor retangular 50 cm', 'CINZA ANTRACITE'),
}
NOVOS = ['43632','44382','44374','1099','42719','16088','37525','15741','39174','51517']

def off(i):
    p = P[i]; return round(100 * (1 - p['cartao'] / p['de']))

BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Montserrat;color:#1d1c1a;-webkit-font-smoothing:antialiased}
.c{position:relative;overflow:hidden;background:radial-gradient(120% 70% at 50% 35%,#e3dfd9 0%,#d6d1ca 55%,#cdc8c0 100%)}
.floor{position:absolute;left:0;right:0;background:linear-gradient(180deg,rgba(255,255,255,0) 0%,rgba(244,242,238,.85) 45%,rgba(222,218,212,0) 100%)}
.mul{mix-blend-mode:multiply}
.bf{font-weight:500;letter-spacing:.42em;text-align:center}
.dt{font-weight:400;letter-spacing:.3em;color:#6f6b66;text-align:center}
.tag{display:inline-block;border:1.5px solid #1d1c1a;border-radius:40px;font-weight:600;letter-spacing:.22em}
.red{color:#a3222b}
s{text-decoration:line-through;color:#7a766f}
"""

def story(i):
    nome, acab = INFO[i]; p = P[i]
    return f"""<html><head><style>{BASE_CSS}
.c{{width:1080px;height:1920px}}</style></head><body><div class=c>
<div class=floor style="top:1040px;height:420px"></div>
<img class=mul src="{MONO}" style="position:absolute;left:469px;top:300px;width:142px">
<div class=bf style="position:absolute;top:425px;width:100%;font-size:40px">BLACK FRIDAY</div>
<div class=dt style="position:absolute;top:488px;width:100%;font-size:22px">LOUÇAS DECA · ATÉ 15/12</div>

<div style="position:absolute;left:150px;top:640px;width:780px;height:640px;display:flex;align-items:center;justify-content:center">
<img class=mul src="{img(i)}" style="max-width:780px;max-height:640px"></div>
<div style="position:absolute;left:84px;top:1330px;width:560px">
 <div style="font-size:33px;font-weight:400;line-height:1.15">{nome}</div>
 <div style="font-size:19px;letter-spacing:.28em;color:#6f6b66;margin-top:8px">{acab}</div>
 <div style="margin-top:14px"><span class=red style="font-size:66px;font-weight:700;letter-spacing:-.02em">{off(i)}%</span> <span class=red style="font-size:36px;font-weight:400">OFF</span></div>
</div>
<div style="position:absolute;right:84px;top:1352px;text-align:right">
 <div style="font-size:30px">de <s>R$ {brl(p['de'])}</s> por</div>
 <div style="font-size:62px;font-weight:300;margin-top:4px">R$ <b style="font-weight:700">{brl(p['pix'])}</b></div>
 <div style="font-size:17px;letter-spacing:.2em;color:#6f6b66;margin-top:8px">NO PIX · OU R$ {brl(p['cartao'])} EM ATÉ 10X</div>
</div>
<div style="position:absolute;top:1612px;width:100%;text-align:center;font-size:32px;font-weight:500;letter-spacing:.42em">LOJA.ORNAMENTARE.COM.BR</div>
<img class=mul src="{LOGOS}" style="position:absolute;left:270px;top:1672px;width:540px">
<div style="position:absolute;left:510px;top:1800px;width:60px;height:2px;background:#1d1c1a"></div>
<div class=bf style="position:absolute;top:1828px;width:100%;font-size:30px">COMPRE AGORA</div>
</div></body></html>"""

def tile(i, w, h):
    p = P[i]; nome, acab = INFO[i]
    return f"""<div style="width:{w}px;height:{h}px;background:rgba(255,255,255,.55);border-radius:18px;position:relative;overflow:hidden">
 <div style="position:absolute;top:10px;right:10px;background:#a3222b;color:#fff;font-weight:700;font-size:19px;padding:4px 10px;border-radius:20px">-{off(i)}%</div>
 <div style="height:{h-104}px;display:flex;align-items:center;justify-content:center;padding:18px"><img class=mul src="{img(i)}" style="max-width:100%;max-height:100%"></div>
 <div style="position:absolute;bottom:14px;left:14px;right:14px">
  <div style="font-size:15.5px;line-height:1.15;height:36px;overflow:hidden">{nome}</div>
  <div style="font-size:24px;font-weight:700;margin-top:6px">R$ {brl(p['pix'])} <span style="font-size:13px;font-weight:500;color:#6f6b66;letter-spacing:.1em">PIX</span></div>
 </div></div>"""

def colecao(hero, tiles):
    p = P[hero]; nome, acab = INFO[hero]
    t = ''.join(tile(x, 234, 300) for x in tiles)
    return f"""<html><head><style>{BASE_CSS}
.c{{width:1080px;height:1350px}}</style></head><body><div class=c>
<div class=floor style="top:560px;height:300px"></div>
<img class=mul src="{MONO}" style="position:absolute;left:60px;top:52px;width:96px">
<div style="position:absolute;left:176px;top:62px"><div class=bf style="text-align:left;font-size:34px">BLACK FRIDAY</div>
<div class=dt style="text-align:left;font-size:19px;margin-top:8px">LOUÇAS DECA · ATÉ 15/12</div></div>

<div style="position:absolute;left:60px;top:200px;width:1px"></div>
<div style="position:absolute;left:40px;top:170px;width:620px;height:640px;display:flex;align-items:center;justify-content:center"><img class=mul src="{img(hero)}" style="max-width:600px;max-height:600px"></div>
<div style="position:absolute;right:60px;top:300px;width:380px;text-align:right">
 <div class=red style="font-size:104px;font-weight:700;line-height:1;letter-spacing:-.03em">{off(hero)}%</div>
 <div class=red style="font-size:30px;letter-spacing:.3em;margin-top:4px">OFF</div>
 <div style="font-size:26px;margin-top:36px;line-height:1.2">{nome}</div>
 <div style="font-size:16px;letter-spacing:.26em;color:#6f6b66;margin-top:8px">{acab}</div>
 <div style="font-size:24px;margin-top:26px">de <s>R$ {brl(p['de'])}</s></div>
 <div style="font-size:54px;font-weight:300">R$ <b style="font-weight:700">{brl(p['pix'])}</b></div>
 <div style="font-size:15px;letter-spacing:.18em;color:#6f6b66;margin-top:6px">NO PIX</div>
</div>
<div style="position:absolute;left:60px;right:60px;top:838px;display:flex;justify-content:space-between">{t}</div>
<div style="position:absolute;left:60px;right:60px;top:1172px;height:1px;background:rgba(0,0,0,.15)"></div>
<img class=mul src="{LOGOS}" style="position:absolute;left:50px;top:1200px;width:470px">
<div style="position:absolute;right:60px;top:1222px;text-align:right"><div style="font-size:22px;font-weight:600;letter-spacing:.24em">COMPRE AGORA →</div>
<div style="font-size:16px;letter-spacing:.2em;color:#6f6b66;margin-top:8px">LOJA.ORNAMENTARE.COM.BR</div></div>
</div></body></html>"""

def capa(hero):
    p = P[hero]
    return f"""<html><head><style>{BASE_CSS}
.c{{width:1080px;height:1080px}}</style></head><body><div class=c>
<div class=floor style="top:640px;height:300px"></div>
<img class=mul src="{MONO}" style="position:absolute;left:478px;top:56px;width:124px">
<div class=bf style="position:absolute;top:168px;width:100%;font-size:38px">BLACK FRIDAY</div>
<div style="position:absolute;top:226px;width:100%;text-align:center;font-size:64px;font-weight:700;letter-spacing:-.01em">Louças Deca até <span class=red>{max(off(x) for x in INFO)}% OFF</span></div>
<div class=dt style="position:absolute;top:318px;width:100%;font-size:20px">CUBAS E BACIAS · ESTOQUE LIMITADO · ATÉ 15/12</div>
<div style="position:absolute;left:190px;top:380px;width:700px;height:540px;display:flex;align-items:center;justify-content:center"><img class=mul src="{img(hero)}" style="max-width:640px;max-height:520px"></div>
<div style="position:absolute;top:960px;width:100%;text-align:center"><span class=tag style="font-size:18px;padding:9px 24px">LOJA.ORNAMENTARE.COM.BR</span></div>
</div></body></html>"""

jobs = []
ONLY = sys.argv[1:] or list(INFO)
for i in ONLY: jobs.append((f'story-{i}', story(i), 1080, 1920))
if not sys.argv[1:]: jobs.append(('colecao-feed-1', colecao('42723', ['42394', '23884', '41081', '45508']), 1080, 1350))
if not sys.argv[1:]: jobs.append(('colecao-feed-2', colecao('42394', ['38579', '42723', '39815', '23884']), 1080, 1350))
jobs.append(('colecao-feed-3', colecao('43632', ['44382', '42719', '37525', '51517']), 1080, 1350))
if not sys.argv[1:]: jobs.append(('colecao-capa', capa('42723'), 1080, 1080))

with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(device_scale_factor=1)
    for name, html, w, h in jobs:
        pg.set_viewport_size({'width': w, 'height': h}); pg.set_content(html); pg.wait_for_timeout(150)
        pg.screenshot(path=str(ART / 'out' / f'{name}.jpg'), type='jpeg', quality=92, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
    b.close()
print('ok', len(jobs))
