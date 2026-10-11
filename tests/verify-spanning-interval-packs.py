"""Accept three distinct problem objectives and unfinished learner file boundaries."""
import argparse
import datetime
import functools
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import re
import signal
import subprocess
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[1]
ORIGINALS={'UG15-Superbull/solution/Main.java': 'f291eaa17772ad022a1264fcdbf0ccddf01d64a52a3eb6db59756669ecba87ff', 'UG17-Moocast/solution/Main.java': '8768cea738dd0ce9a1d6a7964167d4c825c0edcb252ddb065074f49c02cceda6', 'UG6-248/solution/Main.java': '90d7c092c32678bcf2573244fcc44bfcbdf1b31472a01036f951c815708e7713'}
MOOCAST_LEGACY='01e14364b63831bd8f98df4db8bd33ef661b2c437ddce9dec5a9f4883fccb556'
parser=argparse.ArgumentParser()
parser.add_argument('--javac',default='javac');parser.add_argument('--java',default='java')
args=parser.parse_args()

def cancel(sig,frame): raise KeyboardInterrupt('Spanning and interval source acceptance cancelled')
signal.signal(signal.SIGTERM,cancel)
def run(command,cwd,success=True,timeout=30):
 child=subprocess.Popen(command,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
 record=dict(event='spanning-interval-command',parentTaskId=os.environ.get('CLASSES_FAMILY_TASK_ID','gold-spanning-interval'),cwd=str(cwd),command=command,pid=child.pid,startTime=datetime.datetime.now(datetime.timezone.utc).isoformat(),timeoutSeconds=timeout,childProcessGroupCleanup=False)
 try: stdout,stderr=child.communicate(timeout=timeout)
 except BaseException:
  os.killpg(child.pid,signal.SIGTERM)
  try:child.communicate(timeout=5)
  except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.communicate()
  record['childProcessGroupCleanup']=True
  raise
 finally:
  record.update(endTime=datetime.datetime.now(datetime.timezone.utc).isoformat(),exitCode=child.returncode);print(json.dumps(record),flush=True)
 if success and child.returncode:raise AssertionError((command,child.returncode,stdout[-1000:],stderr[-1000:]))
 return subprocess.CompletedProcess(command,child.returncode,stdout,stderr)
def compile_role(directory,probe=False):run([args.javac,'--release','17','-encoding','UTF-8','-Xlint:all','-Werror','Main.java',*(['Probe.java'] if probe else [])],directory)
def execute(directory,success=True):return run([args.java,'-ea','-Xmx256m','Main'],directory,success)
def encoded(values):return str(len(values))+'\n'+'\n'.join(str(x) for x in values)+'\n'
def cow_input(values):return str(len(values))+'\n'+'\n'.join(str(x)+' '+str(y) for x,y in values)+'\n'
def elimination_score(ids):
 @functools.lru_cache(None)
 def best(remaining):
  if len(remaining)<=1:return 0
  return max((ids[a]^ids[b])+max(best(tuple(x for x in remaining if x!=a)),best(tuple(x for x in remaining if x!=b))) for a,b in itertools.combinations(remaining,2))
 return best(tuple(range(len(ids))))
def threshold_power(cows):
 distances=[[ (x-a)**2+(y-b)**2 for a,b in cows] for x,y in cows]
 for threshold in sorted({d for row in distances for d in row}):
  seen={0};queue=[0]
  while queue:
   v=queue.pop()
   for u,d in enumerate(distances[v]):
    if d<=threshold and u not in seen:seen.add(u);queue.append(u)
  if len(seen)==len(cows):return threshold
 raise AssertionError('No connected threshold')
def reachable_tile(values):
 initial=tuple(values);seen={initial};queue=[initial];answer=max(initial)
 while queue:
  state=queue.pop()
  for i in range(len(state)-1):
   if state[i]!=state[i+1]:continue
   merged=state[:i]+(state[i]+1,)+state[i+2:];answer=max(answer,state[i]+1)
   if merged not in seen:seen.add(merged);queue.append(merged)
 return answer
rng=random.Random(1110202607)
superbull=[[3,6,9,10],[1],[1,1073741823],[1073741823,1073741822,1,2],[1,2,3,4,5,6]]
superbull += [rng.sample(range(1,100),rng.randint(1,7)) for _ in range(20)]
moocast=[[(1,3),(5,4),(7,2),(6,1)],[(0,0)],[(0,0),(0,0)],[(0,0),(25000,25000)],[(0,0),(1,0),(2,0)]]
moocast += [[(rng.randrange(9),rng.randrange(9)) for _ in range(rng.randint(1,8))] for _ in range(20)]
merge=[[1,1,1,2],[1,1],[1,2],[40,40],[1]*8,[3,2,2,3],[2,1,2]]
merge += [[rng.randint(1,4) for _ in range(rng.randint(2,8))] for _ in range(20)]
ids=list(range(1,2000))+[1073741823]
line=[(25*i,0) for i in range(1000)];grid=[(500*x,500*y) for x in range(20) for y in range(50)]
specs={
 'UG15-Superbull':dict(stem='superbull',tiny=[(encoded(v),elimination_score(v),v) for v in superbull],full=[(encoded(ids),1999*1073741823-1999*2000//2,ids)],bad=['0\n','2001\n','2\n1\n1\n','1\n0\n','1\n1073741824\n','2\n1\n','1\n1\nextra\n','x\n','1\nx\n',None],type='int[]',display='Arrays.toString(input)',parse=lambda v:str(v),invalid=[-1,1999*1073741823+1]),
 'UG17-Moocast':dict(stem='moocast',tiny=[(cow_input(v),threshold_power(v),v) for v in moocast],full=[(cow_input([(0,0)]*1000),0,[(0,0)]*1000),(cow_input(line),625,line),(cow_input(grid),250000,grid)],bad=['0\n','1001\n','1\n-1 0\n','1\n25001 0\n','1\n0 -1\n','1\n0 25001\n','1\n0\n','1\n0 0 extra\n','x\n','1\nx 0\n',None],type='int[][]',display='Arrays.deepToString(input)',parse=lambda v:str([list(x) for x in v]),invalid=[-1,1250000001]),
 'UG6-248':dict(stem='248',tiny=[(encoded(v),reachable_tile(v),v) for v in merge],full=[(encoded([40]*248),47,[40]*248),(encoded([1,2]*124),2,[1,2]*124),(encoded([i%40+1 for i in range(248)]),40,[i%40+1 for i in range(248)])],bad=['1\n1\n','249\n','2\n0\n1\n','2\n41\n1\n','2\n1\n','2\n1\n1\nextra\n','x\n','2\nx\n1\n',None],type='int[]',display='Arrays.toString(input)',parse=lambda v:str(v),invalid=[0,48])}
assert [specs[f]['tiny'][0][1] for f in specs]==[37,17,3]
tracked={p:p.read_bytes() for f in specs for p in (ROOT/f).rglob('*') if p.is_file() and p.suffix in ['.java','.md','.in','.out']}
for folder,s in specs.items():
 pack=ROOT/folder;learner=(pack/'starter/Main.java').read_text();reference=(pack/'solution/Main.java').read_text()
 assert learner.count('// TODO ')==4 and learner!=reference
 assert (pack/'starter'/(s['stem']+'.in')).read_bytes()==(pack/'solution'/(s['stem']+'.in')).read_bytes()
 assert (pack/'solution'/(s['stem']+'.in')).read_text().strip()==s['tiny'][0][0].strip()
 assert (pack/'solution'/(s['stem']+'.out')).read_text()==str(s['tiny'][0][1])+'\n'
 for role in ['starter','solution']:
  guide=(pack/role/'README.md').read_text()
  assert all(v in guide for v in ['## Contract','## Prediction','## Tasks and walkthrough','## State and reasoning','## Build and run','## Independent checks','JDK 17','PowerShell','exit status',s['stem']+'.in',s['stem']+'.out'])
 if folder=='UG17-Moocast':
  original=(pack/'legacy/Main.java').read_bytes();assert hashlib.sha256(original).hexdigest()==MOOCAST_LEGACY
  def tokens(t):return re.sub(r'\s+','',re.sub(r'/\*.*?\*/|//[^\n]*','',t,flags=re.S))
  assert tokens(original.decode().replace('\r\n','\n')).replace('==Long.MAX_VALUE','==Integer.MAX_VALUE')==tokens(reference)
  assert reference.count('CHANGED:')==3
 else:assert hashlib.sha256((pack/'solution/Main.java').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==ORIGINALS[folder+'/solution/Main.java']
counts=dict(compiledRoles=0,independentTinyCases=0,constructedFullLimitCases=0,unfinishedLearnerRuns=0,refusedLearnerInputs=0,parserProbes=0,invalidResultProbes=0,zipRoles=0)
with tempfile.TemporaryDirectory(prefix='gold-spanning-interval-') as temporary:
 work=Path(temporary)
 for folder,s in specs.items():
  source=ROOT/folder;stem=s['stem'];dirs={}
  for role in ['starter','solution']:
   directory=work/folder/role;directory.mkdir(parents=True)
   # Compile and run actual native source copied from the role ZIP, not a substitute solver.
   archive=directory/'role.zip'
   with zipfile.ZipFile(archive,'w') as z:
    for p in sorted((source/role).iterdir()):
     if p.is_file() and p.suffix in ['.java','.md','.in','.out']:z.write(p,p.name)
   with zipfile.ZipFile(archive) as z:
    assert all('/' not in name and name not in ['.','..'] for name in z.namelist());z.extractall(directory)
    for p in (source/role).iterdir():
     if p.is_file() and p.suffix in ['.java','.md','.in','.out']:assert (directory/p.name).read_bytes()==p.read_bytes()
   counts['zipRoles']+=1;compile_role(directory);counts['compiledRoles']+=1;dirs[role]=directory
  directory=dirs['solution'];input_file=directory/(stem+'.in');output_file=directory/(stem+'.out')
  for data,expected,_ in s['tiny']+s['full']:
   input_file.write_text(data);output_file.unlink(missing_ok=True);process=execute(directory)
   assert not process.stdout and not process.stderr
   assert output_file.read_text()==str(expected)+'\n'
  counts['independentTinyCases']+=len(s['tiny']);counts['constructedFullLimitCases']+=len(s['full'])
  directory=dirs['starter'];input_file=directory/(stem+'.in');output_file=directory/(stem+'.out');previous=b'preserve the earlier learner answer\n'
  for data,_,_ in [s['tiny'][0],s['full'][0]]:
   input_file.write_text(data)
   for existing in [False,True]:
    if existing:output_file.write_bytes(previous)
    else:output_file.unlink(missing_ok=True)
    process=execute(directory,False);assert process.returncode==2 and not process.stdout and 'Complete the four' in process.stderr
    assert output_file.read_bytes()==previous if existing else not output_file.exists();counts['unfinishedLearnerRuns']+=1
  for data in s['bad']:
   output_file.write_bytes(previous)
   if data is None:input_file.unlink(missing_ok=True)
   else:input_file.write_text(data)
   process=execute(directory,False);assert process.returncode==2 and not process.stdout and 'Complete the four' not in process.stderr
   assert output_file.read_bytes()==previous;counts['refusedLearnerInputs']+=1
  # The helper reads and serializes the supplied parser and calls the output guard.
  # It does not fill in a learner algorithm or judge an attempted implementation.
  probe='import java.util.Arrays;\nclass Probe { public static void main(String[] args) throws Exception { __TYPE__ input=Main.readInput(); if(args[0].equals("parse"))System.out.println(__DISPLAY__);else System.out.print(Main.output(input,Long.parseLong(args[0]))); } }\n'
  probe=probe.replace('__TYPE__',s['type']).replace('__DISPLAY__',s['display']);(directory/'Probe.java').write_text(probe);compile_role(directory,True)
  for data,_,values in [s['tiny'][0],s['tiny'][-1],*s['full']]:
   input_file.write_text(data);process=run([args.java,'-ea','-Xmx256m','Probe','parse'],directory)
   assert process.stdout.strip()==s['parse'](values) and not process.stderr;counts['parserProbes']+=1
  input_file.write_text(s['full'][0][0])
  for value in s['invalid']:
   process=run([args.java,'-ea','-Xmx256m','Probe',str(value)],directory,False)
   assert process.returncode!=0 and not process.stdout and 'Result outside documented feasible bounds' in process.stderr;counts['invalidResultProbes']+=1
for path,before in tracked.items():assert path.read_bytes()==before
assert counts==dict(compiledRoles=6,independentTinyCases=77,constructedFullLimitCases=7,unfinishedLearnerRuns=12,refusedLearnerInputs=30,parserProbes=13,invalidResultProbes=6,zipRoles=6),counts
print(json.dumps(dict(event='verified-spanning-interval-packs',packs=3,jdk=args.java,independentModels=['Elimination game sequences','Threshold flood-fill connectivity','Reachable adjacent merge sequences'],sourceUnchanged=True,moocastExecutableEdits=1,**counts)),flush=True)
