#!/usr/bin/env python3
"""Daily lightweight fixture cache. The browser still queries ESPN live for user-selected dates."""
from datetime import datetime
from zoneinfo import ZoneInfo
import json, os, urllib.request, concurrent.futures

LEAGUES=['bra.1', 'arg.1', 'per.1', 'col.1', 'usa.1', 'mex.1', 'ecu.1', 'chi.1', 'uru.1', 'par.1', 'bel.1', 'ned.1', 'ned.2', 'nor.1', 'ita.1', 'ita.2', 'fra.1', 'fra.2', 'eng.1', 'eng.2', 'esp.1', 'esp.2', 'ger.1', 'ger.2', 'por.1', 'tur.1', 'ksa.1', 'uefa.champions', 'uefa.europa', 'uefa.nations', 'fifa.world', 'fifa.worldq.conmebol', 'fifa.worldq.uefa', 'fifa.worldq.concacaf', 'fifa.worldq.afc', 'fifa.friendly', 'concacaf.gold', 'sui.1', 'sui.2', 'eng.3', 'eng.4', 'eng.5', 'sco.1', 'sco.2', 'sco.3', 'sco.4', 'irl.1', 'swe.1', 'swe.2', 'nor.2', 'usa.usl.1', 'usa.usl.l1', 'conmebol.libertadores', 'conmebol.sudamericana', 'bra.2', 'arg.2', 'arg.3', 'mex.2', 'jpn.1', 'eng.fa', 'eng.league_cup', 'eng.trophy', 'eng.fa_qual', 'ger.dfb_pokal', 'sco.tennents', 'sco.cis', 'sco.challenge', 'fra.coupe_de_france', 'arg.copa', 'bra.copa_do_brazil', 'esp.copa_del_rey', 'ned.cup', 'por.taca.portugal']
TODAY=datetime.now(ZoneInfo('America/Sao_Paulo')).strftime('%Y%m%d')
out={'generated_at':datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat(),'timezone':'America/Sao_Paulo','date':TODAY,'source':'ESPN public scoreboard API','leagues':{},'teams':{},'window':{}}
def fetch_teams(league):
    team_url=f'https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/teams?limit=500'
    try:
        with urllib.request.urlopen(team_url,timeout=20) as response: team_data=json.load(response)
        teams=[]
        for sport in team_data.get('sports',[]):
            for league_data in sport.get('leagues',[]):
                for item in league_data.get('teams',[]):
                    team=item.get('team',item)
                    teams.append({'id':team.get('id'),'name':team.get('displayName') or team.get('name'),'abbreviation':team.get('abbreviation')})
        return league,{'teams':teams,'ok':True}
    except Exception as exc:
        return league,{'teams':[],'ok':False,'error':str(exc)}
def fetch_today(league):
    url=f'https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard?dates={TODAY}'
    try:
        with urllib.request.urlopen(url,timeout=20) as response: data=json.load(response)
        return league,{'name':(data.get('leagues') or [{}])[0].get('name'),'events':data.get('events',[]),'ok':True}
    except Exception as exc:
        return league,{'events':[],'ok':False,'error':str(exc)}
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
    for league,data in pool.map(fetch_teams,LEAGUES): out['teams'][league]=data
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
    for league,data in pool.map(fetch_today,LEAGUES): out['leagues'][league]=data
os.makedirs('data',exist_ok=True)
with open('data/fixtures-today.json','w',encoding='utf8') as f: json.dump(out,f,ensure_ascii=False,separators=(',',':'))
print('Date',TODAY,'leagues',len(out['leagues']),'fixtures',sum(len(x.get('events',[])) for x in out['leagues'].values()),'failed',sum(not x.get('ok') for x in out['leagues'].values()))

# Cache upcoming fixtures over the next 31 BRT dates (today + 30 days), enabling team-first search across leagues.
def fetch_day(item):
    league, day = item
    url=f'https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard?dates={day}'
    try:
        with urllib.request.urlopen(url,timeout=18) as response: data=json.load(response)
        return league,day,data.get('events',[]),None
    except Exception as exc:
        return league,day,[],str(exc)
now=datetime.now(ZoneInfo('America/Sao_Paulo'))
days=[(now+__import__('datetime').timedelta(days=i)).strftime('%Y%m%d') for i in range(0,31)]
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
    for league,day,events,error in pool.map(fetch_day,[(l,d) for l in LEAGUES for d in days]):
        block=out['window'].setdefault(league,{'days':{},'errors':0})
        block['days'][day]=events
        if error: block['errors']+=1
window_count=sum(len(events) for block in out['window'].values() for events in block['days'].values())
with open('data/fixtures-window.json','w',encoding='utf8') as f: json.dump({'generated_at':out['generated_at'],'timezone':out['timezone'],'days':days,'source':out['source'],'window':out['window']},f,ensure_ascii=False,separators=(',',':'))
print('Window days',len(days),'upcoming fixtures',window_count,'window file bytes',os.path.getsize('data/fixtures-window.json'))
