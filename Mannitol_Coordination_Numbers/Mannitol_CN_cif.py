import numpy as np
import matplotlib.pyplot as plt
from diffpy.Structure import loadStructure
from diffpy.srreal.pdfcalculator import PDFCalculator
from diffpy.srfit.pdf import PDFContribution
from scipy.integrate import simps
##load structure files including single molecule, in xyz format and crystal cif
mannitol_SM = loadStructure("Mannitol_Single_Molecule.xyz")
mannitol_crystal = loadStructure("DMANTL01_alpha_RT.cif")
##assign them thermal factors
mannitol_SM.Uisoequiv = 0.005
mannitol_crystal.Uisoequiv = 0.005


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
r1, g1 = pc0(mannitol_crystal)

plt.plot(r0, g0, "b-")
plt.plot(r1, g1, "r-")

##rou0 can be estimated from unit cell
rou0 = 4*26/822.473 ## atoms per A^3
###define a Gaussian function
def Gauss(r, r0, Gamma, scale):
    return scale*(np.sqrt(np.log(2.)/np.pi))*(2./Gamma)*np.exp((-1)*(r-r0)**2*4.*np.log(2.)/Gamma**2)

##from G(r) to R(r) by R(r) = [G(r) + 4*pi*r*rou0]*r
diff = g1 - g0
dif_x = r0
dif_y = (diff + 4*np.pi*r0*rou0)*r0

plt.plot(dif_x, dif_y, "g-", lw=2)
plt.show()

##chose the top region to fit Gaussian function, 2.7 A~2.9 A
select_x = dif_x[270:290]
select_y = dif_y[270:290]
plt.plot(select_x, select_y, "k-", lw=2)

##do a fit to find optimum parameters for Gaussian
from scipy.optimize import curve_fit
p0 = [2.74, 0.5, 2.3]
popt, pcov = curve_fit(Gauss, select_x, select_y, p0)
print popt

CN = simps(Gauss(dif_x[250:310], popt[0], popt[1], popt[2]), dif_x[250:310])

plt.plot(dif_x[:350], dif_y[:350], "m-", lw=2, label = "DifferencePDF")
plt.plot(dif_x[250:310], Gauss(dif_x[250:310], popt[0], popt[1], popt[2]), "r-", lw=2,
         label = "Gauss fit \n peak position %.3f A \n peak area %.3f"%(popt[0], CN))


plt.legend()
plt.xlabel("radial distance: A", fontsize = 15)
plt.ylabel("R(r): 1/A", fontsize = 15)
plt.title("subtract a molecule from a crystal", fontsize = 15)
#
plt.show()

##print out the coordination number
print "The peak position for O...O is at {}".format(popt[0])
print "The coordination number for O...O is {}".format()


np.savetxt("crystal_RDF", zip(r0, (g1 + 4*np.pi*r0*rou0)*r0))









