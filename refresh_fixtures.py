#!/usr/bin/env python3
"""Daily lightweight fixture cache. The browser still queries ESPN live for user-selected dates."""
from datetime import datetime
from zoneinfo import ZoneInfo
import json, os, urllib.request

LEAGUES=['bra.1','arg.1','per.1','col.1','usa.1','mex.1','ecu.1','chi.1','uru.1','par.1','bel.1','ned.1','ned.2','nor.1','ita.1','ita.2','fra.1','fra.2','eng.1','eng.2','esp.1','esp.2','ger.1','ger.2','por.1','tur.1','ksa.1','uefa.champions','uefa.europa','fifa.world','fifa.worldq.conmebol','fifa.worldq.uefa','fifa.worldq.concacaf','fifa.worldq.afc','fifa.friendly','concacaf.gold']
TODAY=datetime.now(ZoneInfo('America/Sao_Paulo')).strftime('%Y%m%d')
out={'generated_at':datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat(),'timezone':'America/Sao_Paulo','date':TODAY,'source':'ESPN public scoreboard API','leagues':{}}
for league in LEAGUES:
    url=f'https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard?dates={TODAY}'
    try:
        with urllib.request.urlopen(url,timeout=20) as response: data=json.load(response)
        out['leagues'][league]={'name':(data.get('leagues') or [{}])[0].get('name'), 'events':data.get('events',[]), 'ok':True}
    except Exception as exc:
        out['leagues'][league]={'events':[],'ok':False,'error':str(exc)}
os.makedirs('data',exist_ok=True)
with open('data/fixtures-today.json','w',encoding='utf8') as f: json.dump(out,f,ensure_ascii=False,separators=(',',':'))
print('Date',TODAY,'leagues',len(out['leagues']),'fixtures',sum(len(x.get('events',[])) for x in out['leagues'].values()),'failed',sum(not x.get('ok') for x in out['leagues'].values()))
