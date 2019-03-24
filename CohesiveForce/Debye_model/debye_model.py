"""
    The file coded by Chenyang Shi at AbbVie;
    Send him an email at chenyang.shi@abbvie.com for questions and suggestions.
    Fitting experimentally determined ADPs with a Debye model to extract Debye temperature and offset
    The Debye equation is:
    (1) u^2 = 3*h^2*T/(4*pi^2*m*kb*thetaD^2)*[phi(thetaD/T) + 1./4.(thetaD/T)] + A
    (2) phi(x) = 1/x int_0^xi[(xi/exp(xi)-1)]dxi
    we use the curve_fit module from scipy to do the minimization

"""
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt
h = 6.62606957e-34 # Planck's constant m^2kg/s
kb = 1.3806488e-23 # Boltzmann's constant m^2kgs^-2K^-1
amu = 1.66053892e-27 # atomic mass unit kg
m = 241.285*amu   # atmoic mass of mefanamic acid


def __integral(x):
    return x/(np.exp(x)-1)

def __phi(x):
    a = np.array([quad(__integral, 0, i)[0] for i in x]) # TURNS OUT quad function can not integrate an array, so we need a for loop
    return (1/x)*a # quad(func, 0, x) usually gives two values, i.e. integration and error, we only need former

def __adp(T, thetaD, A):
    u = ((3*h**2*T)/(4*np.pi**2*m*kb*thetaD**2))*(__phi(thetaD/T)+0.25*(thetaD/T))
    return u*1e20+A

data = np.loadtxt("MEF_ADPs", skiprows=0).transpose()
T = data[0]
thermal = data[1]
from scipy.optimize import curve_fit
popt, pcov = curve_fit(__adp, T, thermal)#, p0)#, sigma = error) # sigma = error, p0 = guess, guess not used here
uncertainty = np.sqrt(pcov.diagonal())
print "Debye temperature of MEF is %3f K"%popt[0]
print "Zero point energy of MEF is %3f $\AA^{2}$"%popt[1]
print "The uncertainty on Debye temperature of MEF is %3f K"% uncertainty[0]
print "The uncertainty on zero point energy of MEF is %3f $\AA^{2}$"% uncertainty[1]

plt.plot(T, thermal, "bo", markersize = 10)
plt.plot(T, __adp(T, *popt), "r-", lw=3)
plt.xlabel("T (K)", fontsize = 15)
plt.ylabel("Intermolecular ADPs $(\AA^{2})$", fontsize = 15)
plt.title("Debye model fit of ADPs from MEF", fontsize = 15)
plt.show()

np.savetxt("MEF_Debye_model_Fit.txt", zip(T, thermal, __adp(T, *popt))) # the 1st, 2nd columns are experimental data while the 3rd one is the fit results






