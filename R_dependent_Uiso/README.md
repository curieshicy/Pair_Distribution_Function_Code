# R dependent Uiso
This is to test r-dependent Uiso in PDF model fit in some organic materials. The relavant discussion was already done almost 20 years ago in http://pubs.acs.org/doi/pdf/10.1021/jp9836978. 

## Motivation
It is the known fact that in inorganics and metallic compounds, due to correlated motions of atoms, the PDFs of these compounds show sharp first few peaks and broadened peaks at high-r region because the atoms are uncorrelated there. A quick demonstration of this can be seen on nickel. The red feature is the peak width (as it is) for nickel where we see a strong r dependent Uiso and it goes up quickly up to 30 Angstroms and plateaued beyond 40 Angstroms. 

![nickel](https://user-images.githubusercontent.com/8492535/34116727-05488bac-e3df-11e7-9289-8142c1783d3e.png)

To explain a bit more about how we obtain these red dots in the plot, we rely on the PDF modeling software, PDfgui (DiffPy-CMI can do the same job with no problem; actutally it is more versatile). If we take a look at the PDF peak width calculation in PDFgui, 

![equation](https://user-images.githubusercontent.com/8492535/34116723-037b082c-e3df-11e7-8904-943537f3676e.png)

it can be seen the measured PDF peak width, Sigma, is modeled by three factors, i.e. Delta 1, Delta 2, and Qbroad, while the intrinsic peak width Sigma Prime is the prefactor. To extract Simga, in the PDF model fit, Delta 1, Delta 2 and Qbroad has to be set to 0, and this is exactly what we did to get red dots in the above figure.

To account for correlated/uncorrelated motions at different r-range, Qbroad and delta 2 parameters are allowed to vary in the fits. The final Uiso value (i.e. Sigma Prime) is plotted as black squares and we can see the r-dependent Uisos effect is suppressed to a large extent. 

## Is r dependent Uisos also true for organics?

The same practices as in nickel case are performed. To explore if Uisos are r dependent or not, one need to extract peak width (Sigma Prime in the above equation) by setting Qbroad, delta1, delta 2 values to 0 in the PDF fit. For organics, a three-phase fit is carried out to account for PDF contributions from intra- and intermolecular correlations (Details see Prill et al., 2015 J. Applied Crystallography paper). The results are summarized in the following plots. Both mefenamic acid and mannitol show a strong r-dependent Uisos for Uiso-inter. The r-dependence is not obvious for Uiso-intra. To account for the atoms correlations in organics, the delta 2 and Qbroad parameters have to be turned on during the fit (or fix Qbroad to that from the fit to the PDF of a standard calibrant).    

![mef_man](https://user-images.githubusercontent.com/8492535/34126279-a44c7500-e3fe-11e7-8e03-df86460e7315.png)

## Does the fit improve for manitol measured at 300 K?

We noticed for mannitol data collected at 300 K, if we fix delta2 values and Qbroad to 0 (while fixing Qdamp value to calibrant value), we see the fit is in general OK but the low-r disagreement is quite pronounced (see top panel of the figure below). If we fix Qdamp and Qbroad using values from calibrant, and free delta2 values, the fit gives a lower Rw value (bottom panel), and an improvement in the low-r fit. Still there are some difference, which I don't know why yet, but likely come from the inprecision of the molecular model. The extracted Uiso values are in general larger for the bottom panel (i.e. free delta2 in the fit). This makes sense because in the equation, Sigma Prime is multiplied by a value (square root term) less than 1. While in the top panel, it doesn't. 

![man](https://user-images.githubusercontent.com/8492535/34129237-0576658e-e409-11e7-8d21-0dc082de4181.png)

## Conclusions
(0) In the formal practice of a PDF experiment, before measuring actutal samples, one always measures a standard calibrant sample such as nickel, cerium oxide or lanthanum hexaboride. The purpose is two-fold, one is to calibrate the sample-to-detector distance for integration of sample 2D diffraction image later. The other is to perform a PDF model fit to extract Qdamp and Qbroad parameters, which will be fixed in the later fits to the actual samples. These two parameters take into account the instrument resolutions--fixing them at the values from calibrant will decouple actual structural results from resolution effects. For example, Qdamp parameter explains how PDF peak intensity drops with increasing r distance. Even for a bulk calibrant, the peak vanishes at certain r distance; however, there are also effects from samples that cause the drop of peak intensity such as nanopartice effect, internal structural disorders etc. In this case, fixing Qdamp to the value from calibrant somehow removes or takes care of the effect from finite instrument resolution. 

(1) The formal procedure for fitting of PDF from organic materials is the same as in inorganics. First extract Qdamp, Qbroad numbers from fit to the standard at same r-range desired; then fix them in organic PDF fit; free delta 2 parameters to account for r-dependent Uiso.

(2) Alternative way but less rigid is to treat measured bulk organic PDF as standard samples. In other words, free Qdamp, Qbroad and delta2 in the fit. This is only done when there is no calibration data. 





