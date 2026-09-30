"""Execute the authoritative notebooks from the release directory."""
from pathlib import Path
import json,os
ROOT=Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLBACKEND','Agg');os.chdir(ROOT)
(ROOT/'figures').mkdir(exist_ok=True)
for name in ['nep_set3_test_parity','nep_set3_density_trajectories']:
 scope={'__name__':'__main__'}
 for cell in json.loads((ROOT/'scripts'/f'{name}.ipynb').read_text())['cells']:
  if cell['cell_type']=='code':exec(compile(''.join(cell['source']),name,'exec'),scope)
