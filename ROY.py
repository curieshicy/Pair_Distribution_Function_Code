#!/usr/bin/env python
########################################################################
#
# diffpy.srfit      by DANSE Diffraction group
#                   Simon J. L. Billinge
#                   (c) 2009 Trustees of the Columbia University
#                   in the City of New York.  All rights reserved.
#
# File coded by:    Chenyang Shi
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
########################################################################
"""Example of a PDF refinement of three-phase structure.

Like the ones before, this example uses PDFGenerator to refine a structure to
PDF data. However, for a multi-phase structure one must use multiple
PDFGenerators. This example refines a physical mixture of CdS and ZnS to
find the structures and phase fractions.

"""

########this file calculates PDFs from two molecular crystals#######
import os
import numpy
from numpy import pi

from pyobjcryst.crystal import CreateCrystalFromCIF
from diffpy.srfit.pdf import DebyePDFGenerator, PDFParser, PDFGenerator
from diffpy.srfit.fitbase import Profile
from diffpy.srfit.fitbase import FitContribution, FitRecipe
from diffpy.srfit.fitbase import FitResults

#from gaussianrecipe import scipyOptimize

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
    profile.setCalculationRange(xmin=1, xmax = 20, dx = 0.01)

    ## The ProfileGenerator
    generator_ROY_Cryst_B = PDFGenerator("G_ROY_Cryst_B")
    generator_ROY_Cryst_B.setStructure(stru1, periodic = True)
    generator_ROY_Mole_B = DebyePDFGenerator("G_ROY_Mole_B")
    generator_ROY_Mole_B.setStructure(stru2, periodic = False)
    generator_ROY_Intra = DebyePDFGenerator("G_ROY_Intra")
    generator_ROY_Intra.setStructure(stru3, periodic = False)

    ## The FitContribution
    # Add both generators to the FitContribution. Add the Profile. This will
    # send the metadata to the generators.
    contribution = FitContribution("ROY")
    contribution.addProfileGenerator(generator_ROY_Cryst_B)
    contribution.addProfileGenerator(generator_ROY_Mole_B)
    contribution.addProfileGenerator(generator_ROY_Intra)
    contribution.setProfile(profile, xname = "r")

    # Write the fitting equation. We want to sum the PDFs from each phase and
    # multiply it by a scaling factor. We also want a certain phase scaling
    # relationship between the PDFs which we will enforce with constraints in
    # the FitRecipe.
    #from diffpy.srfit.pdf.characteristicfunctions import sphericalCF
    #contribution.registerFunction(sphericalCF, name = "f_IMC")
    contribution.setEquation("scale * (G_ROY_Cryst_B - G_ROY_Mole_B + G_ROY_Intra)")

    # Make the FitRecipe and add the FitContribution.
    recipe = FitRecipe()
    recipe.addContribution(contribution)

    qdamp = 0.02902
    generator_ROY_Cryst_B.qdamp.value = qdamp
    generator_ROY_Mole_B.qdamp.value = qdamp
    generator_ROY_Intra.qdamp.value = qdamp
    
    qbroad = 0.017315
    generator_ROY_Cryst_B.qbroad.value = qbroad
    generator_ROY_Mole_B.qbroad.value = qbroad 
    generator_ROY_Intra.qbroad.value = qbroad 

    # Vary the gloabal scale as well.
    recipe.addVar(contribution.scale, 1) 

#############################################################################################
############### First the ROY_Cryst_B parameters ############################################
#############################################################################################
    phase_ROY_Cryst_B = generator_ROY_Cryst_B.phase

    lat = phase_ROY_Cryst_B.getLattice()
    atoms = phase_ROY_Cryst_B.getScatterers()
    
    recipe.newVar("Uiso_Inter", 0.05, tag = "T1")
    recipe.newVar("lat_a", 3.9453, tag = "lat")
    recipe.newVar("lat_b", 18.685, tag = "lat")
    recipe.newVar("lat_c", 16.3948, tag = "lat")
    #recipe.newVar("alpha", 90, tag = "lat")
    recipe.newVar("beta", 93.83, tag = "lat")
    #recipe.newVar("gamma", 90, tag = "lat")

    recipe.constrain(lat.a, "lat_a")
    recipe.constrain(lat.b, "lat_b")
    recipe.constrain(lat.c, "lat_c")
    #recipe.constrain(lat.alpha, "alpha")
    recipe.constrain(lat.beta, "beta")
    #recipe.constrain(lat.gamma, "gamma")
    
    for atom in atoms:
    	if atom.element.title() == "N":
             recipe.constrain(atom.Uiso, "Uiso_Inter")
             
    	elif atom.element.title() == "O":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    	elif atom.element.title() == "C":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    	elif atom.element.title() == "H":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

        elif atom.element.title() == "S":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    generator_ROY_Cryst_B.delta2.value = 0
#    recipe.addVar(generator_IMC_Cryst_B.delta2, name = "delta2_IMC_Cryst_B", value =
#            0, tag = "delta") 


#############################################################################################
############### Second the ROY_Mole_B parameters ############################################
#############################################################################################
    phase_ROY_Mole_B = generator_ROY_Mole_B.phase
    generator_ROY_Mole_B.setQmin(0.0)
    generator_ROY_Mole_B.setQmax(24.0)
    recipe.newVar("zoom_Mole_B", 1, tag = "lat2") 

    lat = phase_ROY_Mole_B.getLattice()
    recipe.constrain(lat.a, "zoom_Mole_B")
    recipe.constrain(lat.b, "zoom_Mole_B")
    recipe.constrain(lat.c, "zoom_Mole_B")
   # Constrain fractional xyz parameters
    atoms = phase_ROY_Mole_B.getScatterers()
   # Constrain ADPs
    #recipe.newVar("Uiso_Inter", 0.05, tag = "T2") 
    
    for atom in atoms:
    	if atom.element.title() == "C":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    	elif atom.element.title() == "O":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    	elif atom.element.title() == "N":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    	elif atom.element.title() == "H":
             recipe.constrain(atom.Uiso, "Uiso_Inter")
             
        elif atom.element.title() == "S":
             recipe.constrain(atom.Uiso, "Uiso_Inter")

    generator_ROY_Mole_B.delta2.value = 0

#    recipe.addVar(generator_IMC_Mole_B.delta2, name = "delta2_IMC_Mole_B", value
#            = 5.66086478091, tag = "delta") 

#############################################################################################
############### Third the intra molecule parameters##########################################
#############################################################################################
    phase_ROY_Intra = generator_ROY_Intra.phase
    generator_ROY_Intra.setQmin(0.0)
    generator_ROY_Intra.setQmax(24.0)
    recipe.newVar("zoom_Intra", 1, tag = "lat3") 

    lat = phase_ROY_Intra.getLattice()
    recipe.constrain(lat.a, "zoom_Intra")
    recipe.constrain(lat.b, "zoom_Intra")
    recipe.constrain(lat.c, "zoom_Intra")
   # Constrain fractional xyz parameters
    atoms = phase_ROY_Intra.getScatterers()
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
             
        elif atom.element.title() == "S":
             recipe.constrain(atom.Uiso, "Uiso_Intra")

    generator_ROY_Intra.delta2.value = 0

    # Give the recipe away so it can be used!
    return recipe

def plotResults(recipe, basename):
    """Plot the results contained within a refined FitRecipe."""

    r = recipe.ROY.profile.x
    g = recipe.ROY.profile.y
    gcalc = recipe.ROY.profile.ycalc
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
    pylab.savefig('{}.png'.format(basename))

    pylab.show()
    return
   
    
def main():

    # Make the data and the recipe
    data = "../data/ON_RT_5-00000.gr"
    basename = "ROY_Least_Squares"
    print basename

    # Make the recipe
    from diffpy.Structure import Structure
    stru1 = Structure(filename='../data/QAXMEH_ON.cif')
    stru2 = Structure(filename='../data/QAXMEH_ON.xyz') # this is non-distorted structure, keep it fixed.
    stru3 = Structure(filename='../data/QAXMEH_ON.xyz')

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

    profile = recipe.ROY.profile    
    profile.savetxt(basename + ".fit")

    res = FitResults(recipe)
    res.printResults()

    header = "A+B-C.\n"
    res.saveResults(basename + ".res", header=header)
    
    # Plot!
    if _plot:
        plotResults(recipe, basename)

if __name__ == "__main__":

    main()
# End of file
