import numpy as np
from time import time
import os
from scipy.stats import gaussian_kde
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str)
args = parser.parse_args()

path = args.path

def exclude_elements(arr2d, arr1d):
    # Create an empty list to hold the resulting rows
    result = []

    # Iterate over each row in the 2D array and corresponding element in the 1D array
    for row, exclude in zip(arr2d, arr1d):
        # Create a boolean mask where the condition is True for elements not equal to the element to exclude
        mask = row != exclude
        # Apply the mask to the row
        filtered_row = row[mask]
        # Append the filtered row to the result list
        result.append(filtered_row)
    
    # Convert the result list back to a numpy array
    return np.array(result)

t0 = time()

nO=432
nH=432*2

nbead = 1
nstep = 2001
natom = 432*3
traj_liq = np.zeros([nbead, nstep, natom, 6])
cell_liq = np.zeros([nbead, nstep, 3])
for ibead in range(nbead):
    with open(os.path.join(path, f"{ibead:02d}.xyz"), "r") as f:
        for istep in range(nstep):
            for iline in range(5):
                f.readline()
            for iline in range(3):
                line = f.readline().split()
                cell_liq[ibead][istep][iline] = float(line[1]) - float(line[0])
            f.readline()
            for iline in range(natom):
                line = f.readline().split()
                traj_liq[ibead][istep][iline] = np.array(line[2:8], dtype=float)

t1 = time()
print(f"{t1-t0:.2f} s: Reading trajectory done")

typeO = np.arange(nO)
typeH = np.arange(nO, nO+nH)

coord_O = traj_liq[:, :, typeO, :3]
coord_H = traj_liq[:, :, typeH, :3]

O_bonded = ((typeH - nO)//2).astype(int)
O_all = np.tile(typeO, (nH, 1))
O_nonbonded = exclude_elements(O_all, O_bonded)

idx_frame = np.arange(200, 2000, 4)
nsamp_ = idx_frame.shape[0]

r_O2H_list = np.zeros([nsamp_, 1, nH, nO-1])
r_O2O1_list = np.zeros([nsamp_, 1, nH, nO-1])
beta_list = np.zeros([nsamp_, 1, nH, nO-1])

X_list = np.zeros([nsamp_, 1, nH, nO-1])
Y_list = np.zeros([nsamp_, 1, nH, nO-1])

# for isamp in range(traj_liq.shape[1]):
for iframe in range(len(idx_frame)):
    isamp = idx_frame[iframe]
    H = coord_H[:, isamp, :]
    O1 = coord_O[:, isamp, O_bonded, :]
    O2 = coord_O[:, isamp, O_nonbonded, :]
    prd = cell_liq[:, isamp]
    
    d_O2H = H[:, :, None, :] - O2
    d_O2H = (d_O2H/prd-np.floor(d_O2H/prd+0.5))*prd
    r_O2H = np.linalg.norm(d_O2H, axis=3)
    r_O2H_list[iframe] = r_O2H
    
    d_O2O1 = O1[:, :, None, :] - O2
    d_O2O1 = (d_O2O1/prd-np.floor(d_O2O1/prd+0.5))*prd
    
    d_HO1 = O1 - H
    d_HO1 = (d_HO1/prd-np.floor(d_HO1/prd+0.5))*prd
    
#     print(d_O2O1.shape)
#     print(d_HO1.shape)
    beta = np.arccos(np.sum(d_O2O1 * d_HO1[:, :, None, :], axis=-1) / np.linalg.norm(d_O2O1, axis=-1) / np.linalg.norm(d_HO1, axis=-1)[:, :, None]) / np.pi * 180
    beta_list[iframe] = beta
    
    n1 = np.cross(d_O2O1, d_O2H, axis=-1)
    n2 = np.cross(n1, d_O2O1, axis=-1)
    n2_norm = np.linalg.norm(n2, axis=-1)
    n2 = n2 / n2_norm[:, :, :, None]
    
# #     print(n2.shape)
    d_O2H_n2 = np.sum(d_O2H*n2, axis=-1) / np.linalg.norm(n2, axis=-1)
# #     print(np.where(d_O2H_n2 > 0))
# #     print(d_O2H_n2.shape)
# #     print(np.linalg.norm(n2, axis=-1))
    r_O2O1 = np.linalg.norm(d_O2O1, axis=3)
    r_O2O1_list[iframe] = r_O2O1    

# #     print(d_O2H.shape)
    X = np.sum(d_O2H * d_O2O1, axis=-1) / r_O2O1
# #     print(d_O2O1.shape)
    Y = d_O2H_n2

    X_list[iframe] = X
    Y_list[iframe] = Y

t2 = time()
print(f"{t2-t0:.2f} s: Calculation done")

r_O2O1 = r_O2O1_list.flatten()
beta = beta_list.flatten()
X = X_list.flatten()
Y = Y_list.flatten()

mask = ((r_O2O1 > 2.5) & (r_O2O1 < 3.6) & (beta < 100))

X = X[mask]
Y = Y[mask]

t3 = time()
print(f"{t3-t0:.2f} s: Masking done")

data = np.vstack([X, Y])
kde_xy = gaussian_kde(data)

# Create a grid for evaluation
xmin, xmax = X.min() - 0.1, X.max() + 0.1
ymin, ymax = Y.min() - 0.01, Y.max() + 0.01
X_grid, Y_grid = np.meshgrid(np.linspace(xmin, xmax, 100), np.linspace(ymin, ymax, 100))
positions = np.vstack([X_grid.ravel(), Y_grid.ravel()])
Zxy = np.reshape(kde_xy(positions).T, X_grid.shape)

t4 = time()
print(f"{t4-t0:.2f} s: KDE done")

np.savez(os.path.join(path, "out_Zxy.npy"), X_grid=X_grid, Y_grid=Y_grid, Zxy=Zxy)