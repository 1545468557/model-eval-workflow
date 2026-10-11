#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path

def audit(d):
    cases=d['case_ids']
    if not cases or len(cases)!=len(set(cases)):raise ValueError('case_ids empty or duplicate')
    summaries=[]
    for model in d['models']:
        rows=model['results'];seen=[r['case_id'] for r in rows]
        if len(seen)!=len(set(seen)) or set(seen)!=set(cases):raise ValueError('missing/duplicate/unexpected case in '+model['id'])
        counts={k:0 for k in ('pass','fail','pending')};veto=[]
        for r in rows:
            if r['verdict'] not in counts:raise ValueError('invalid verdict')
            counts[r['verdict']]+=1
            if r.get('hard_veto'):veto.append(r['case_id'])
        summaries.append({'model':model['id'],'counts':counts,'pass_rate':counts['pass']/len(cases),'veto_cases':veto,'eligible':not veto and not counts['pending'] and counts['fail']==0,'cost':model.get('cost',{'status':'unknown'})})
    return {'summaries':summaries,'limits':'Recorded judgments only; no model API called. Pending never counted as passing; eligibility is separate from ranking.'}
def main():
    p=argparse.ArgumentParser();p.add_argument('input',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    try:
        result=audit(json.loads(a.input.read_text()))
        with a.output.open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2)
        return 0
    except (ValueError,KeyError,OSError) as e:print(e,file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
