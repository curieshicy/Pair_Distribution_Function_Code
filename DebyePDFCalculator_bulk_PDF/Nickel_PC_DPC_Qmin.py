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
            'rmax' : 100,
            'rstep': 0.01}

cfg_dpc2 = {'qmax' : 100,
            'qmin' : 0.5,
            'rmin' : 0,
            'rmax' : 100,
            'rstep': 0.01}

cfg_dpc3 = {'qmax' : 100,
            'qmin' : 1,
             'rmin' : 0,
            'rmax' : 100,
            'rstep': 0.01}

# calculate PDF by real-space summation
pc0 = PDFCalculator(**cfg_pc)
r0, g0 = pc0(nkl_crystal)

# calcualte PDF by DPC
pc1 = DebyePDFCalculator(**cfg_dpc1)
r1, g1 = pc1(nkl_crystal)

pc2 = DebyePDFCalculator(**cfg_dpc2)
r2, g2 = pc2(nkl_crystal)

pc3 = DebyePDFCalculator(**cfg_dpc3)
r3, g3 = pc3(nkl_crystal)

plt.plot(r0, g0, "b-", lw=2, label = "PC")
plt.plot(r1, g1 + 30, "r-", lw=2, label = "DPC, Qmin = 0 1/A")
plt.plot(r2, g2 + 60, "k-", lw=2, label = "DPC, Qmin = 0.5 1/A")
plt.plot(r3, g3 + 90, "m-", lw=2, label = "DPC, Qmin = 1.0 1/A")

plt.legend(loc=0)
plt.xlabel("Radial Distance", fontsize = 15)
plt.ylabel("PDF, G(r), 1/A^2", fontsize = 15)
plt.xlim([0, 20])
plt.title("Nickel cif PDF via PC and DPC")
plt.show()










