#!/usr/bin/env python3
"""Oxygen displacement and global Q6 diagnostics; inspect alongside density drift."""
from pathlib import Path
import argparse,shlex,csv
import numpy as np

def frames(path):
    with path.open() as f:
        while line:=f.readline():
            n=int(line);info=dict(t.split('=',1) for t in shlex.split(f.readline()) if '=' in t)
            cell=np.array(list(map(float,info['Lattice'].split()))).reshape(3,3)
            props=info['Properties'].split(':');cols={};k=0
            for i in range(0,len(props),3):cols[props[i]]=slice(k,k+int(props[i+2]));k+=int(props[i+2])
            data=[f.readline().split() for _ in range(n)]
            pos=np.array([r[cols['pos']] for r in data if r[cols['species']][0]=='O'],float)
            assert pos.shape==(64,3)
            yield cell,pos

def main(root,phases=('water','ice')):
    rows=[]
    for phase,burn in [('water',200),('ice',50)]:
        if phase not in phases: continue
        cells=[];scaled=[];q6=[]
        for i,(cell,pos) in enumerate(frames(root/f'md/{phase}/dump.xyz')):
            frac=pos@np.linalg.inv(cell);scaled.append(frac);cells.append(cell)
            if (i+1)%10==0 and i+1>burn:
                d=frac[:,None,:]-frac[None,:,:];d-=np.rint(d);d=d@cell
                r=np.linalg.norm(d,axis=2);np.fill_diagonal(r,np.inf)
                near=np.argsort(r,axis=1)[:,:4];bonds=np.take_along_axis(d,near[:,:,None],axis=1).reshape(-1,3)
                bonds/=np.linalg.norm(bonds,axis=1)[:,None]
                x=np.clip(bonds@bonds.T,-1,1);p6=(231*x**6-315*x**4+105*x*x-5)/16
                q6.append(np.sqrt(max(0,np.mean(p6))))
        expected=2000 if phase=='water' else 500
        assert len(scaled)==expected,(phase,'incomplete trajectory',len(scaled),expected)
        scaled=np.array(scaled);cells=np.array(cells)
        assert np.isfinite(scaled).all() and np.isfinite(cells).all()
        delta=np.diff(scaled,axis=0);delta-=np.rint(delta)
        dr=np.einsum('tni,tij->tnj',delta,(cells[1:]+cells[:-1])/2)
        path=np.concatenate([np.zeros((1,64,3)),np.cumsum(dr,axis=0)],axis=0)
        path-=path.mean(axis=1,keepdims=True);path=path[burn:]
        row={'phase':phase,'trajectory_frames':len(scaled),'discard_ps':burn,'mean_global_oxygen_Q6':np.mean(q6),'first_half_Q6':np.mean(q6[:len(q6)//2]),'second_half_Q6':np.mean(q6[len(q6)//2:])}
        for lag in [10,50,100]:row[f'oxygen_MSD_lag{lag}ps_A2']=np.mean(np.sum((path[lag:]-path[:-lag])**2,axis=2))
        rows.append(row)
    suffix='' if len(phases)==2 else '_'+phases[0]
    with (root/f'structure_diagnostics{suffix}.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
    print(rows)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path)
    p.add_argument('--phase',choices=['water','ice'])
    args=p.parse_args();main(args.root,(args.phase,) if args.phase else ('water','ice'))
