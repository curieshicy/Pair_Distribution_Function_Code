# DebyePDFCalculator_bulk_PDF
This project is to demonstrate how to use DebyePDFCalculator in DiffPy-CMI program to calculate PDF for crystals.

Given a crystal structure it is straightforward to simulate its PDF using PDFCalculator (PC) either by using PDFgui or DiffPy-CMI programs. The essential equation is G(r) = 4* Pi *r * [rou(r) - rou0]. The summation is done in real space. The background term -4 * Pi * r * rou0 gives rise to a negative slope in the simulated PDF. For example, let's consider simple face-center cubic nickel. It has a lattice constant of 3.52 A and 4 atoms in a unit cell. It's PDF can be generated as shown in the blue curve below. As expected the PDF peaks are sitting on top of a negative backgroud with an intial linear slope.

Let's move on to calculate the PDF of nickel using DebyePDFCalculator (DPC). DPC first sums up the scattering intensities of each atomic pair in Q space using the sinc function, i.e. f_i * f_j * sin(Q.r_ij)/Q.r_ij, then does the normalization by <f(Q)>^2 to obtain structure factor S(Q) before a sine Fourier transform to obtain PDF in real space. Another difference between PC and DPC is that PC uses Q independent X-ray form factor, i.e. uses atomic number as a replacement while DPC uses Q-dependent X-ray form factor (from Waasmaier and Kirfel, Acta Cryst. A, 51, 416-431, 1995). However, for simple element system, both calculators should agree. OK, now the test is that we should be able to reproduce PDF calculated by PC using DPC. 

PC takes paramters such as rmin and rmax; DPC is a bit more complicated, taking in rmin, rmax, qmin and qmax. rmax is the largest radial distance it would sum up in Q space. qmin and qmax are for Fourier transform. To make life easier, let's fix rmin=0 and qmax=100 A-1. A large qmax would reduce termination ripple in PDF after Fourier transform. Let's test first fix qmin=0, and set rmax = 40 A, 70 A, and 100 A. The results are shown in the figures below.
![nickel_qmin 0](https://user-images.githubusercontent.com/8492535/30351095-5dba5708-97df-11e7-9291-360d31fbac2b.png)
The PDFs by DPC are relatively flat at low-r (e.g. below 5 A) but takes off quickly at high r. The difference between different rmax is subtle at least for nickel case.

Let's now fix rmax = 100 A and vary qmin = 0, 0.5 and 1 A-1. The results are shown in the figures below.
![nickel_rmax 100](https://user-images.githubusercontent.com/8492535/30351094-5dba19b4-97df-11e7-9a3f-ed86c931514d.png)
It is seen that by choosing a small qmin value, the tilted-up PDFs go down, and the high r PDFs fluctuate close to 0 (not there yet). It is seen in the literature that people use a qmin cutoff trick to simulate PDF and compares with measured one. However, neither of these three qmin gives an PDF exact as the one produced by PC (blue curve). This is no good. 

Why don't they agree? The qmin cutoff logic is partially correct in that it needs to subtract certain portion from the qmin = 0 PDF to bring the tilted up part down. A small qmin cutoff does this job. A simulation with q-range 0-0.5 1/A and 0-1.0 1/A is shown.

![qmin_cutoff](https://user-images.githubusercontent.com/8492535/30352405-4ec06fd4-97e5-11e7-9e36-db7db005764b.png)

However, this doesn't seem correct as the dfifference between flat low-r part in qmin=0 PDF and the non-linear feature shown in the figure above won't give a linear negative slope. So we guess that the subtract term must be in the form of constant * r. Indeed a constant of ~1.1 gives a good agreement. What does this value mean? It acutally corresponds to 4 * Pi * atomic_density_of_nickel = 4 * 3.1415 * 4/3.52^3 = 1.153. OK, by subtracting 4 * Pi * rou0 * r term from qmin=0 PDF by DPC we achieve an exact same PDF as from PC, see below.

![nickel_pc_dpc](https://user-images.githubusercontent.com/8492535/30351093-5dae5c50-97df-11e7-90dd-dab000e55965.png)

The same methodology works well for BaTiO3 and indomethacin. Note the difference in PDFs from PC and DPC that comes from different treatment of X-ray form factor. BaTiO3 has distinctively different elements, so it is expected to see larger difference when compared with indomethacin where C, O, N are close in scattering behavior. 

![bto_pc_dpc](https://user-images.githubusercontent.com/8492535/30351098-5dbfd8fe-97df-11e7-87b0-77ccd60943ed.png)
![imc_pc_dpc](https://user-images.githubusercontent.com/8492535/30351097-5dbd787a-97df-11e7-83e8-2bc7244279d6.png)

