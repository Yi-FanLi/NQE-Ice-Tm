"""Create fresh GPUMD work directories; does not submit or run jobs."""
from pathlib import Path
import argparse,gzip,shutil
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('destination',type=Path);args=p.parse_args()
args.destination.mkdir(parents=True,exist_ok=False)
def unpack(source,target):
 with gzip.open(source,'rb') as s,target.open('wb') as t:shutil.copyfileobj(s,t)
for kind,names in [('training',['fresh']),('evaluation',['training','liq','ice']),('md',['water','ice'])]:
 for name in names:
  d=args.destination/kind/name;d.mkdir(parents=True)
  if kind=='training':
   shutil.copy2(ROOT/'training/nep.in',d/'nep.in')
   for f in ['train.xyz','test.xyz']:unpack(ROOT/'training'/(f+'.gz'),d/f)
  elif kind=='evaluation':
   shutil.copy2(ROOT/'nep.txt',d/'nep.txt');shutil.copy2(ROOT/'evaluation'/name/'nep.in',d/'nep.in')
   source=ROOT/('training/train.xyz.gz' if name=='training' else f'evaluation/{name}/train.xyz.gz')
   unpack(source,d/'train.xyz')
  else:
   for f in ['run.in','model.xyz']:shutil.copy2(ROOT/'md'/name/f,d/f)
   shutil.copy2(ROOT/'nep.txt',d/'nep.txt')
print(args.destination.resolve())
