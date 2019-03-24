# CohesiveForce
This is the place for downloading Python scripts for fitting experimental organic PDF and fitting T-dep ADPs with a Debye model.

## PDF model fit 
The PDF model fit on organic PDF follows Prill's Journal of Applied Crystallography paper (http://scripts.iucr.org/cgi-bin/paper?S1600576714026454) and uses PDF of mefenamic acid (MEF) as an example. The data was colllected at 300 K at beamline 11-ID-B at Argonne National Laboratory. The Qmax used is 24 1/A; and the r-range is 1-40 A. 

To use the scripts, download the codes <b>bin</b> and <b>data</b> located at <b>CohesiveForce/PDF_FIT_MEF/</b> to a local folder. Make sure you have installed DiffPy-CMI (http://www.diffpy.org/products/diffpycmi/). In a terminal, after <b>source activate py27</b>, navigate into <b>bin</b> and type 

<b>python MEF_300K.py</b> 

to start the run. It takes a couple of minutes to run the code on my computer; the end result is a fit that looks like something below. 

![300k_fit](https://user-images.githubusercontent.com/8492535/32331660-7a2418da-bfb1-11e7-8889-0811476c92bc.png)

## Debye model fit
The code for performing a Debye model fit is stored at <b>CohesiveForce/Debye_model/</b>. Download the code to a local folder. 

To use the code, prepare a file that contains tempeatures and ADP values similar to <b>MEF_ADPs</b> where the first column is the temperatures (here from 100 K to 300 K), the second is the ADP values in A^2. In a terminal, nagivate to the folder, and type 

<b>python debye_model.py</b>

to start the fit. In the end, one may get a fit plot similar to 
![debye_model_fit](https://user-images.githubusercontent.com/8492535/32331661-7a490ed8-bfb1-11e7-8449-19cc2d3af617.png)

For a new organic compound, in <b>debye_model.py</b>, modify line 17 to specify the molecular weight of the new molecule; line 31 to load new ADP values; and line 49 to change the name of the saved file. Optionally you may change <b>MEF</b> to your compound's acronym. 

<b>Note</b>: the code is written for Python 2.7 environment. I suggest stay at py27 environment after PDF model fit; and run this code for Debye model fit. 


