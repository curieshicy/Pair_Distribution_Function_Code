import numpy as np
import matplotlib.pyplot as plt
from diffpy.Structure import loadStructure
from diffpy.srreal.pdfcalculator import PDFCalculator
from diffpy.srfit.pdf import PDFContribution
from scipy.integrate import simps

nkl_crystal = loadStructure("Nickel.cif")
nkl_crystal.Uisoequiv = 0.005


cfg = { 'qmax' : 25,
        'qmin' :0,
        'rmin' : 0,
        'rmax' : 20,
        'rstep': 0.01,
        'qdamp': 0.045,
        'qbroad': 0.069}

# calculate PDF by real-space summation
pc0 = PDFCalculator(**cfg)
r1, g1 = pc0(nkl_crystal)
#plt.plot(r1, g1, "r-", lw = 2, label = "G(r)")

#rou0 can be estimated from unit cell
rou0 = 4./3.52**3 ## atoms per A^3

##from G(r) to R(r) by R(r) = [G(r) + 4*pi*r*rou0]*r
g1_new = (g1 + 4*np.pi*r1*rou0)*r1

plt.plot(r1, g1_new, "m-", lw=2, label = "R(r)")
plt.legend(loc=0)
plt.xlabel("radial distance", fontsize = 15)
plt.ylabel("RDF, R(r), 1/A", fontsize = 15)
plt.title("Nickel cif RDF")
plt.show()

print simps(g1_new[200:300], r1[200:300])









