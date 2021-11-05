# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 16:36:46 2021

@author: daimi
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pyevtk.hl import gridToVTK

#read the magnetization from the file
filename = 'm000399.ovf'
netfile = open(filename,'r')

count = 0
lstart = 28
lend = 4124
input_net = []
lines = netfile.readlines()
for line in lines[lstart:lend]:
    input_net.append([float(item) for item in line.split()])

#put the data from the input magnetization into an array    
Nx = 64
Ny = 64
net = np.empty((Nx,Ny,3))
for j in range(Ny):
    for i in range(Nx):
        net[i][j][0:3] = input_net[j*Nx+i][0:3]
        
n_x = np.arange(0,64,1)
n_y = np.arange(0,32,0.5)
N_Y,N_X = np.meshgrid(n_y,n_x)

netx=net[:,:,0]
nety=net[:,:,1]
netz=net[:,:,2]

fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(111)
xstart=26
xend=38
ystart=22
yend=42
ax.set_aspect('equal','box')
ax.quiver(N_X[xstart:xend,ystart:yend],N_Y[xstart:xend,ystart:yend],netx[xstart:xend,ystart:yend],nety[xstart:xend,ystart:yend],netz[xstart:xend,ystart:yend],pivot='mid',cmap=cm.bwr,clim=(-1,1))

Nx_new = xend - xstart + 1
Ny_new = yend - ystart + 1
# below code are from https://github.com/pyscience-projects/pyevtk/blob/master/examples/structured.py
x = np.zeros((Nx_new,Ny_new,1))
y = np.zeros((Nx_new,Ny_new,1))
z = np.zeros((Nx_new,Ny_new,1))
netx_new = np.zeros((Nx_new,Ny_new,1))
nety_new = np.zeros((Nx_new,Ny_new,1))
netz_new = np.zeros((Nx_new,Ny_new,1))

dx = 1
dy = 0.5
for k in range(1):
    for j in range(Ny_new):
        for i in range(Nx_new):
            x[i,j,k] = (i + xstart)*dx
            y[i,j,k] = (j + ystart)*dy
            z[i,j,k] = k
            netx_new[i,j,k] = netx[i + xstart,j + ystart]
            nety_new[i,j,k] = nety[i + xstart,j + ystart]
            netz_new[i,j,k] = netz[i + xstart,j + ystart]

gridToVTK("./central_part_net",x,y,z,pointData={"m": (netx_new,nety_new,netz_new)})
            

