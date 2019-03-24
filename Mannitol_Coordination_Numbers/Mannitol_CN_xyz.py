import numpy as np
import matplotlib.pyplot as plt
from diffpy.Structure import loadStructure
from diffpy.srreal.pdfcalculator import PDFCalculator
from diffpy.srfit.pdf import PDFContribution
from scipy.integrate import simps
##load structure files including single molecule, supercell in xyz format 
mannitol_SM = loadStructure("Mannitol_Single_Molecule.xyz")
mannitol_supercell = loadStructure("Mannitol_5_5_5.xyz")

##assign them thermal factors
mannitol_SM.Uisoequiv = 0.005
mannitol_supercell.Uisoequiv = 0.005

cfg = { 'qmax' : 25,
        'qmin' :0,
        'rmin' : 0,
        'rmax' : 20,
        'rstep': 0.01,
        'qdamp': 0.045,
        'qbroad': 0.069}

# calculate PDF by real-space summation
pc0 = PDFCalculator(**cfg)
r0, g0 = pc0(mannitol_SM)
r1, g1 = pc0(mannitol_supercell)

###define a Gaussian function
def Gauss(r, r0, Gamma, scale):
    return scale*(np.sqrt(np.log(2.)/np.pi))*(2./Gamma)*np.exp((-1)*(r-r0)**2*4.*np.log(2.)/Gamma**2)

##from G(r) to R(r) by R(r) = G(r)*r
dif_x = r0
dif_y = dif_x*(g1 - g0)

##chose the top region to fit Gaussian function, 2.7 A~2.9 A
select_x = dif_x[270:290]
select_y = dif_y[270:290]
plt.plot(select_x, select_y, "g-", lw=2)

##do a fit to find optimum parameters for Gaussian
from scipy.optimize import curve_fit
p0 = [2.74, 0.5, 2.3]
popt, pcov = curve_fit(Gauss, select_x, select_y, p0)
print popt
CN = simps(Gauss(dif_x[250:310], popt[0], popt[1], popt[2]), dif_x[250:310])

plt.plot(dif_x[:350], dif_y[:350], "m-", lw=2, label = "DifferencePDF")
plt.plot(dif_x[250:310], Gauss(dif_x[250:310], popt[0], popt[1], popt[2]), "r-", lw=2, label = "Gauss fit \n peak position %.3f A \n peak area %.3f"%(popt[0], CN))

plt.legend()
plt.xlabel("radial distance: A", fontsize = 15)
plt.ylabel("R(r): 1/A", fontsize = 15)
plt.title("subtract a molecule from a supercell", fontsize = 15)
#
plt.show()

##print out the coordination number
print "The peak position for O...O is at {}".format(popt[0])
print "The coordination number for O...O is {}".format(CN)


np.savetxt("supercell_RDF", zip(r0, r0*g1))






