import numpy as np
import matplotlib.pyplot as plt
from diffpy.Structure import loadStructure
from diffpy.srreal.pdfcalculator import PDFCalculator, DebyePDFCalculator
from diffpy.srfit.pdf import PDFContribution
from scipy.integrate import simps

nkl_crystal = loadStructure("Nickel.cif")
nkl_crystal.Uisoequiv = 0.005


cfg_pc = {'rmin' : 0,
         'rmax' : 20,
         'rstep': 0.01}

cfg_dpc1 = {'qmax' : 100,
            'qmin' : 0,
            'rmin' : 0,
            'rmax' : 40,
            'rstep': 0.01}

#cfg_dpc2 = {'qmax' : 100,
#            'qmin' : 0,
#            'rmin' : 0,
#            'rmax' : 70,
#            'rstep': 0.01}
#
#cfg_dpc3 = {'qmax' : 100,
#            'qmin' : 0,
#             'rmin' : 0,
#            'rmax' : 100,
#            'rstep': 0.01}

# calculate PDF by real-space summation
pc0 = PDFCalculator(**cfg_pc)
r0, g0 = pc0(nkl_crystal)

# calcualte PDF by DPC
pc1 = DebyePDFCalculator(**cfg_dpc1)
r1, g1 = pc1(nkl_crystal)

#pc2 = DebyePDFCalculator(**cfg_dpc2)
#r2, g2 = pc2(nkl_crystal)
#
#pc3 = DebyePDFCalculator(**cfg_dpc3)
#r3, g3 = pc3(nkl_crystal)
rou = 4/3.52**3 ## atomic density

plt.plot(r0, g0, "b-", lw=2, label = "PC")
plt.plot(r1, g1, "r-", lw=2, label = "DPC, rmax = 40 A")
plt.plot(r1, g1 - 4*np.pi*rou*r1, "k-", label = "DPC, minus 4*pi*rou*r")
#plt.plot(r2, g2 + 60, "k-", lw=2, label = "DPC, rmax = 70 A")
#plt.plot(r3, g3 + 90, "m-", lw=2, label = "DPC, rmax = 100 A")

plt.legend(loc=0)
plt.xlabel("Radial Distance (r)", fontsize = 15)
plt.xlim([0, 20])
plt.ylabel("PDF, G(r), 1/A^2", fontsize = 15)
plt.title("Nickel cif PDF via PC and DPC")
plt.show()










