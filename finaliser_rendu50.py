from pathlib import Path
import json,time,subprocess,sys
O=Path('dq6-fr/v0.50')
while not (O/'qa-render-fixtures.json').exists():time.sleep(2)
initial=json.loads((O/'qa-render-fixtures.json').read_text())
(O/'qa-rendu-preliminaire.json').write_text(json.dumps(dict(result_sha256=initial['result_sha256'],pages=len(initial['rows']),accepted_as_final=False,reason='Audit du handler DF : il ne produit pas vous. Correction de752 avant validation et recapture complète.'),ensure_ascii=False,indent=2))
f=O/'revue-lot-v050.json';r=json.loads(f.read_text())
for x in r:
 if x['id']==752:
  for k in ['native_plan','original_body','adaptation_body']:x[k]=x[k].replace('Tiens... {DF}','Tiens... Vous{DF}')
  for k in ['review','adaptation_review']:x[k]='DF natif appelle011C (vide en français) seulement au pluriel ; Vous reste littéral, commun au singulier de politesse et au pluriel. Ne pas confondre avec E0 qui imprime vous/vous tous. Huit tours du prêtre et tous les AF conservés.'
f.write_text(json.dumps(r,ensure_ascii=False,indent=2));f=O/'native_plan.py';f.write_text(f.read_text().replace('0xdf:9','0xdf:0'))
subprocess.run([sys.executable,'dq6-fr/pass50.py'],check=True)
for f in ['prepare.py','build.py','verify.py']:
 with open('final50-'+f+'.log','w') as out:subprocess.run([sys.executable,str(O/f)],stdout=out,stderr=subprocess.STDOUT,check=True)
for f,log in [('test_render.py','render50-final.log'),('test_runtime.py','runtime50.log')]:
 args=[sys.executable,'-u',str(O/f)]
 if f=='test_render.py':args+=['--camp-state','/workspace/scratch/fc8c8cdec832/work-v026/dq6-fr/emulator-tests/v026-camp.state']
 with open(log,'w') as out:subprocess.run(args,stdout=out,stderr=subprocess.STDOUT,check=True)
print('Final render/runtime50 passed')
