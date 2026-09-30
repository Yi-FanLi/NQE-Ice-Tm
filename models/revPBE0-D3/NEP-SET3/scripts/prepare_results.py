from pathlib import Path
import hashlib,json,csv
import numpy as np
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT;OUT=ROOT/'data/nep_set3';OUT.mkdir(parents=True,exist_ok=True)
archive=ROOT;sha=hashlib.sha256((ROOT/'nep.txt').read_bytes()).hexdigest();arrays={};metrics=[];sources={}
for name,n in [('training',2556),('liq',50),('ice',50)]:
 p=archive/f'evaluation/{name}';e=np.loadtxt(p/'energy_train.out.gz');f=np.loadtxt(p/'force_train.out.gz');assert e.shape==(n,2) and f.shape==(n*192,6);assert np.isfinite(e).all() and np.isfinite(f).all()
 de=e[:,0]-e[:,1];df=f[:,:3]-f[:,3:];metrics.append(dict(dataset=name,configurations=n,energy_RMSE_meV_atom=float(np.sqrt(np.mean(de**2))*1000),force_RMSE_meV_A=float(np.sqrt(np.mean(df**2))*1000)))
 if name!='training':arrays[name+'_energy']=e-156.39267947333917;arrays[name+'_force']=f
 for file in ['energy_train.out.gz','force_train.out.gz']:sources[str((p/file).relative_to(ROOT))]=hashlib.sha256((p/file).read_bytes()).hexdigest()
dens=[];blocks=[]
for phase,path,dt,end,burn in [('water',BASE/'md/water',.05,2000,200),('ice',BASE/'md/ice',.1,500,50)]:
 assert (path/'MD_COMPLETE').exists()
 t=np.loadtxt(path/'thermo.out.gz');assert t.shape==(round(end/dt),18) and np.isfinite(t).all();v=np.linalg.det(t[:,9:18].reshape(-1,3,3));assert (v>0).all()
 times=np.arange(1,len(t)+1)*dt;rho=64*18.01528*1.66053906660/v;keep=times>burn;d=rho[keep];b=d.reshape(-1,round(50/dt)).mean(axis=1)
 arrays[phase+'_density']=np.column_stack([times,rho,t[:,0],t[:,3:6].mean(axis=1)*1e4])
 dens.append(dict(phase=phase,total_ps=end,discard_ps=burn,mean_g_cm3=float(d.mean()),SEM50ps_g_cm3=float(b.std(ddof=1)/np.sqrt(len(b))),blocks50ps=len(b),first_half_g_cm3=float(d[:len(d)//2].mean()),second_half_g_cm3=float(d[len(d)//2:].mean()),temperature_K=float(t[keep,0].mean()),pressure_bar=float(t[keep,3:6].mean()*1e4)))
 for size in [5,10,20,50,100]:
  m=round(size/dt);k=len(d)//m;bb=d[:k*m].reshape(k,m).mean(axis=1);blocks.append(dict(phase=phase,block_ps=size,blocks=k,SEM_g_cm3=float(bb.std(ddof=1)/np.sqrt(k))))
 sources[str((path/'thermo.out.gz').relative_to(ROOT))]=hashlib.sha256((path/'thermo.out.gz').read_bytes()).hexdigest()
np.savez_compressed(OUT/'plot_data.npz',**arrays)
for name,rows in [('rmse.tsv',metrics),('density_statistics.tsv',dens),('density_block_sensitivity.tsv',blocks)]:
 with (OUT/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
(OUT/'provenance.json').write_text(json.dumps(dict(model_sha256=sha,energy_offset_eV_atom=-156.39267947333917,energy_plot='Both predicted and target absolute energy restored by adding the fixed training offset; no fitted alignment.',test='Independent800Ry,50water+50ice configurations; none added to training.',density='Physical masses H1.00794,O15.9994; SEM from nonoverlapping50ps blocks after200ps water /50ps ice discard; all retained samples enter mean.',source_sha256=sources),indent=2)+'\n')
print(json.dumps(dict(densities=dens,rmse=metrics,block_sensitivity=blocks),indent=2))
