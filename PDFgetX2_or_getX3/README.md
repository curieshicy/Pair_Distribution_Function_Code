# PDFgetX2_or_getX3
This article compares the two commonly used PDF reduction programs PDFgetX2 and PDFgetX3.

The X-ray total scattering is a powerful technique for studying local structure of materials. The popular softwares used for data reduction include PDFgetX2 (https://web.pa.msu.edu/cmp/billinge-group/programs/PDFgetX2/) and a later version PDFgetX3 (http://www.diffpy.org/products/pdfgetx3.html), both developed by Prof. Simon Billinge's group. GetX2 performs a rigorous data treatment following scattering theory, correcting a number of parameters including Compton scattering, absorption, multiple scattering, and self-scattering from same elements. As such, GetX2 has many parameters to fine tune, thus requiring great familarity of X-ray scattering theory which is usually in the domain of an expert. To make the data reduction step straightforward and easily-manageable by a wider group of users, the Biillinge group developed and released GetX3, which uses an ad hoc algorithm for rapid data reduction. In this article I tested both programs on a diffraction data of indomethacin recently collected at beamline 11-ID-B at Argonne National Lab. The experiment was done at 300 K, using a ~58 keV beam (wavelength is 0.2113 Angstrom) and a sample-to-detector distance of ~24 cm.

The raw diffraction is first converted to I(Q). Starting from I(Q), one obtains total structure factor S(Q) via S(Q) = 1 + [I(Q) - <f^2> ]/< f>^2. This step is a major data reduction step, it corrects many experimental artifacts including Oblique Incidence and Compton Scattering. Also it eliminates the self scattering from same elements and normalizes the measured coherent scattering intensity by average X-ray form factor squared. Then F(Q) is obtain by a simple relation F(Q) = Q[S(Q) - 1]. A sine Fourier transform gives PDF, G(r) by G(r) = Integral Q[S(Q) -1]sin(Qr)dQ. 

Here are the results on IMC by using GetX2 and GetX3. First the I(Q), this is consistent in both programs. The I(Q) is just a preliminary basic treatment of raw intensity data, i.e. subtracting container scattering from total scattering, (if necessary) converting two-theta to Q via Q = 4 * Pi * sin(theta)/lambda. 
![iq23](https://user-images.githubusercontent.com/8492535/30458967-8d9b57f2-9973-11e7-8081-205d43ab34fc.png)

A next comparision is on S(Q). Both S(Q)s show a fluctuation around unitiy at high Q (truncated at 20 1/A) and overrall both patterns show great similarity. However, we notice two major differences. One is the scale. GetX2 S(Q) is ~5 times that of GetX3 counterpart. The normalization in GetX2 goes through rigorous procedure, and therefore is absolute. In contrast, the algorithm used in GetX3 makes the scale an abitrary number, although we noticed it is ~20% of GetX2 scale from sevearl of test samples. Another difference is S(0). According to S(Q) = 1 + [I(Q) - <f^2> ]/< f>^2, S(0) for IMC is calculated to be -0.53. The S(0) from GetX2 does give a number ~-0.5 but GetX3 S(0) shows a positive number at ~0.62. Even if we shift and scale the S(Q) of GetX3, i.e. [S(Q) - 1] * scale + 1, we obtain a value of -1.09 (using a scale fator of 5.5), it is still off from the right value.  

![sq2](https://user-images.githubusercontent.com/8492535/30458963-8d864d30-9973-11e7-9133-0da1f9eebfb0.png)
![sq3](https://user-images.githubusercontent.com/8492535/30458965-8d97199e-9973-11e7-8282-78255fdddfe1.png)

F(Q)s from both programs are overlaid as below. The peaks are aligned with the small difference in peak intensities. 
![fq23](https://user-images.githubusercontent.com/8492535/30458964-8d956aea-9973-11e7-8835-2dbcbf8ec520.png)

The PDFs are plotted up to 100 A and compared as below. The inset shows the first 5 A region. Both PDFs give a pronounced peak at 1.4 A. Small differences in peaks are observed in an r-range from 3 to 5 A. Overall both PDFs show agreement. 
![gr23](https://user-images.githubusercontent.com/8492535/30458966-8d999390-9973-11e7-84d1-c2fae70408a5.png)

Base on the comparison made above, the conclusion is (1) Overall both programs generate PDFs of high similarity. In many cases, both PDFs should give same scientific conclusions. (2) There is an issue with GetX3 S(Q) at low-Q region, for example, S(0) value is not correct. (3) GetX3 uses an arbitrary scale factor while GetX2 uses an "absolute" scale (within experimental error). Although in GetX3 case, one may obtain a scale by performing a PDF model fit on crystalline sample, it is not possible for amorphous sample or heavily disordered sample where one cannot find a good structural model to explain the measured PDF. For these samples, GetX2 with an absolute scale will show advantage. My personal recommendation is that we should use GetX2 whenever possible.



