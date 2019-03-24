"""
    This is an example script for modeling organic PDF.
    File coded by Chenyang Shi at AbbVie.
    For questions and suggestions, send him an email at chenyang.shi@abbvie.com.
"""
import os
import numpy
from numpy import pi
from pyobjcryst.crystal import CreateCrystalFromCIF
from diffpy.srfit.pdf import DebyePDFGenerator, PDFParser, PDFGenerator
from diffpy.srfit.fitbase import Profile
from diffpy.srfit.fitbase import FitContribution, FitRecipe
from diffpy.srfit.fitbase import FitResults

####### Example Code
_plot = True
_parallel = 0

def makeRecipe(stru1, stru2, stru3, datname):
    """Create a fitting recipe for crystalline PDF data."""

    ## The Profile
    profile = Profile()

    # Load data and add it to the profile
    parser = PDFParser()
    parser.parseFile(datname)
    profile.loadParsedData(parser)
    profile.setCalculationRange(xmin=1, xmax = 40, dx = 0.01)

    ## The ProfileGenerator
    generator_MEF_Cryst_B = PDFGenerator("G_MEF_Cryst_B")
    generator_MEF_Cryst_B.setStructure(stru1, periodic = True)
    generator_MEF_Mole_B = DebyePDFGenerator("G_MEF_Mole_B")
    generator_MEF_Mole_B.setStructure(stru2, periodic = False)
    generator_MEF_Intra = DebyePDFGenerator("G_MEF_Intra")
    generator_MEF_Intra.setStructure(stru3, periodic = False)

    ## The FitContribution
    # Add both generators to the FitContribution. Add the Profile. This will
    # send the metadata to the generators.
    contribution = FitContribution("MEF")
    contribution.addProfileGenerator(generator_MEF_Cryst_B)
    contribution.addProfileGenerator(generator_MEF_Mole_B)
    contribution.addProfileGenerator(generator_MEF_Intra)
    contribution.setProfile(profile, xname = "r")
    #write down the fit equation:
    #(G_MEF_Cryst_B - G_MEF_Mole_B) gives the intermolecular PDF, using a larger atomic displacement parameter
    #G_MEF_Intra gives intramolecular PDF, using a smaller atomic displacement parameter.
    #The sum of both parts gives the total PDF.
    contribution.setEquation("scale * (G_MEF_Cryst_B - G_MEF_Mole_B + G_MEF_Intra)")

    # Make the FitRecipe and add the FitContribution.
    recipe = FitRecipe()
    recipe.addContribution(contribution)

    qdamp = 0.02902
    generator_MEF_Cryst_B.qdamp.value = qdamp
    generator_MEF_Mole_B.qdamp.value = qdamp
    generator_MEF_Intra.qdamp.value = qdamp

    # Vary the gloabal scale as well.
    recipe.addVar(contribution.scale, 1) 

#############################################################################################
############### First the MEF_Cryst_B parameters ############################################
#############################################################################################
    phase_MEF_Cryst_B = generator_MEF_Cryst_B.phase

    lat = phase_MEF_Cryst_B.getLattice()
    atoms = phase_MEF_Cryst_B.getScatterers()
    
    recipe.newVar("Uiso_Inter", 0.05, tag = "T1")
    recipe.newVar("lat_a", 14.556, tag = "lat")
    recipe.newVar("lat_b", 6.811, tag = "lat")
    recipe.newVar("lat_c", 7.657, tag = "lat")
    recipe.newVar("alpha", 119.57, tag = "lat")
    recipe.newVar("beta", 103.93, tag = "lat")
    recipe.newVar("gamma", 91.30, tag = "lat")

    recipe.constrain(lat.a, "lat_a")
    recipe.constrain(lat.b, "lat_b")
    recipe.constrain(lat.c, "lat_c")
    recipe.constrain(lat.alpha, "alpha")
    recipe.constrain(lat.beta, "beta")
    recipe.constrain(lat.gamma, "gamma")
    
    for atom in atoms:
    	if atom.element.title() == "N":
             recipe.constrain(atom.Uiso, "Uiso_Inter")
             
    	elif atom.element.title() == "O":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    	elif atom.element.title() == "C":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    	elif atom.element.title() == "H":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    generator_MEF_Cryst_B.delta2.value = 0


#############################################################################################
############### Second the MEF_Mole_B parameters ############################################
#############################################################################################
    phase_MEF_Mole_B = generator_MEF_Mole_B.phase
    generator_MEF_Mole_B.setQmin(0.0)
    generator_MEF_Mole_B.setQmax(24.0)
    recipe.newVar("zoom_Mole_B", 1, tag = "lat2") 

    lat = phase_MEF_Mole_B.getLattice()
    recipe.constrain(lat.a, "zoom_Mole_B")
    recipe.constrain(lat.b, "zoom_Mole_B")
    recipe.constrain(lat.c, "zoom_Mole_B")
   # Constrain fractional xyz parameters
    atoms = phase_MEF_Mole_B.getScatterers()
   # Constrain ADPs

    for atom in atoms:
    	if atom.element.title() == "C":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    	elif atom.element.title() == "O":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    	elif atom.element.title() == "N":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    	elif atom.element.title() == "H":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    generator_MEF_Mole_B.delta2.value = 0

#############################################################################################
############### Third the intra molecule parameters##########################################
#############################################################################################
    phase_MEF_Intra = generator_MEF_Intra.phase
    generator_MEF_Intra.setQmin(0.0)
    generator_MEF_Intra.setQmax(24.0)
    recipe.newVar("zoom_Intra", 1, tag = "lat3") 

    lat = phase_MEF_Intra.getLattice()
    recipe.constrain(lat.a, "zoom_Intra")
    recipe.constrain(lat.b, "zoom_Intra")
    recipe.constrain(lat.c, "zoom_Intra")
   # Constrain fractional xyz parameters
    atoms = phase_MEF_Intra.getScatterers()
   # Constrain ADPs
    recipe.newVar("Uiso_Intra", 0.005, tag = "T2") 
    
    for atom in atoms:
    	if atom.element.title() == "C":
             recipe.constrain(atom.Uiso, "Uiso_Intra")

    	elif atom.element.title() == "O":
             recipe.constrain(atom.Uiso, "Uiso_Intra")

    	elif atom.element.title() == "N":
             recipe.constrain(atom.Uiso, "Uiso_Intra")

    	elif atom.element.title() == "H":
             recipe.constrain(atom.Uiso, "Uiso_Intra")

    generator_MEF_Intra.delta2.value = 0

    # Give the recipe away so it can be used!
    return recipe

def plotResults(recipe):
    """Plot the results contained within a refined FitRecipe."""

    r = recipe.MEF.profile.x

    g = recipe.MEF.profile.y
    gcalc = recipe.MEF.profile.ycalc
    diffzero = -0.8 * max(g) * numpy.ones_like(g)
    diff = g - gcalc + diffzero

    import pylab
    pylab.plot(r,g,'bo',label="G(r) Data")
    pylab.plot(r, gcalc,'r-',label="G(r) Fit")
    pylab.plot(r,diff,'g-',label="G(r) diff")
    pylab.plot(r,diffzero,'k-')
    pylab.xlabel("$r (\AA)$")
    pylab.ylabel("$G (\AA^{-2})$")
    pylab.legend(loc=1)

    pylab.show()
    return
   
    
def main():

    # Make the data and the recipe
    data = "../data/MEF_300-00000.gr"
    basename = "MEF_300K_LS"
    print basename

    # Make the recipe
    from diffpy.Structure import Structure
    stru1 = Structure(filename='../data/MEF.cif')
    stru2 = Structure(filename='../data/MEF.xyz')
    stru3 = Structure(filename='../data/MEF.xyz')
    recipe = makeRecipe(stru1, stru2, stru3, data)
    if _plot:
        from diffpy.srfit.fitbase.fithook import PlotFitHook
        recipe.pushFitHook(PlotFitHook())
    recipe.fithooks[0].verbose = 3

    from scipy.optimize import leastsq
    leastsq(recipe.residual, recipe.values)

    # Save structures
    stru1.write(basename + "_Cryst_B_zoomed.stru", "pdffit")
    stru2.write(basename + "_Mole_B_zoomed.xyz", "xyz")
    stru2.write(basename + "_Intra_zoomed.xyz", "xyz")

    profile = recipe.MEF.profile
    
    #import IPython.Shell; IPython.Shell.IPShellEmbed(argv=[])()
    profile.savetxt(basename + ".fit")

    # Generate and print the FitResults
    res = FitResults(recipe)
    res.printResults()

    header = "MEF Organic PDF fit.\n"
    res.saveResults(basename + ".res", header=header)
    
    # Plot!
    if _plot:
        plotResults(recipe)

if __name__ == "__main__":

    main()
# End of file
