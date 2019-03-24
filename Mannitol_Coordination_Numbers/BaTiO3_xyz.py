import numpy as np
import matplotlib.pyplot as plt
from diffpy.Structure import loadStructure
from diffpy.srreal.pdfcalculator import PDFCalculator
from diffpy.srfit.pdf import PDFContribution
from scipy.integrate import simps

bto_cluster_1 = loadStructure("BaTiO3.xyz")
bto_cluster_2 = loadStructure("BaTiO3_4_4_4.xyz")
bto_cluster_3 = loadStructure("BaTiO3_8_8_8.xyz")

bto_cluster_1.Uisoequiv = 0.005
bto_cluster_2.Uisoequiv = 0.005
bto_cluster_3.Uisoequiv = 0.005


cfg = { 'qmax' : 25,
        'qmin' :0,
        'rmin' : 0,
        'rmax' : 20,
        'rstep': 0.01,
        'qdamp': 0.045,
        'qbroad': 0.069}

# calculate PDF by real-space summation
pc0 = PDFCalculator(**cfg)
r1, g1 = pc0(bto_cluster_1)
r2, g2 = pc0(bto_cluster_2)
r3, g3 = pc0(bto_cluster_3)

## convert to RDF from G(r)
g1_new = r1*g1
g2_new = r2*g2
g3_new = r3*g3

plt.plot(r1, g1_new, "m-", lw=2, label = "R(r) 1_1_1")
plt.plot(r2, g2_new, "r-", lw=2, label = "R(r) 4_4_4")

plt.legend(loc=0)
plt.xlabel("radial distance", fontsize = 15)
plt.ylabel("RDF, R(r), 1/A", fontsize = 15)
plt.title("BaTiO3 clusters RDF")
plt.show()


##Ti-O bond
##
f_ave = (56 + 22 + 24)/5.
f_TiO = 22*8

scale_f = f_TiO/f_ave**2/2.5

print simps(g1_new[170:230], r1[170:230])
print simps(g2_new[170:230], r2[170:230])
print simps(g3_new[170:230], r3[170:230])

print scale_f


#print simps(g1_new[220:310], r1[220:310])/0.95








