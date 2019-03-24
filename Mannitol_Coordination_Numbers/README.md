# Mannitol_Coordination_Numbers
This is the place for determining the coordination number for O-O hydrogen bond in mannitol

From pair distribution function (PDF) one obtains a myraid of structural details including cooridnation number. For organic molecules, the measured/theoretical PDFs contains the contribution from single molecule and inter-molecular correlation. This is unique property of organic materials, in contrast to inorganic materials which are essentially a "giant moelcule". In this project, my goal is to isolate PDF signals from only intermolecular contribution via a simple sugar molecule--mannitol. It has the formula C6H14O6. It forms a O..O hydrogen bond at a distance of ~2.75 Anstrom.

I tried two methods to isolate this inter-PDF peak:
(a) Simulate total PDF by using a cif file; single molecule by a xyz file--Mannitol_CN_cif.py
(b) Simulate total PDF by using a xyz file (a supercell of 5 by 5 by 5 size; 13000 atoms); single molecule by a xyz file--Mannitol_CN_xyz.py

The codes for route (a) and (b), together with structure files are in the repository. 

Here are some math:

G(r) = 4 * pi * r[rou(r) - rou(0)]

R(r) = 4 * pi * r^2 * rou(r) = r[G(r) + 4 * pi * r * rou(0)]

The route (a) gives a peak position of 2.775 A and a CN of 2.640; and the plot is here.
![subtract_from_crystal](https://user-images.githubusercontent.com/8492535/29690468-b871ed20-88ec-11e7-9293-28be5bf65aea.png)

The route (a) gives a peak position of 2.773 A and a CN of 2.024; and the plot is here.
![subtact_from_supercell](https://user-images.githubusercontent.com/8492535/29690396-6ceb3eb0-88ec-11e7-8d9e-63a23e4e171b.png)

To understand this, let's take one step back and test on a simple multiple element system barium titanate (BTO). BTO has four crystal structures depending on temperatures. The example used here is the simplest cubic structure with a space group Pm-3m. For bulk BTO, this phase exsits above its Curie temperature of 120 degree C. In a BTO unit cell, eight corners are occupied by Ba atoms, six face centers by Oxygen atoms, while Ti atom sits at body center. Let's focus on Ti-O bond, which has a bond length of ~2 A. The Ti atom is surrouded by six Oxygen atoms, so the CN number should be 6. 

Let's consider three common cases (a) a BTO crystal (b) a BTO cluster with only five atoms (one molecule) (c) a BTO supercell with 4 by 4 by 4 expansion (64 molecules, 320 atoms in total). 

The RDF for crystal BTO is shown below.
![bto_cif_rdf](https://user-images.githubusercontent.com/8492535/29754813-a5b4fe26-8b52-11e7-8b88-772a5b12c6fc.png)

The RDF for cluster BTO (1_1_1 and 4_4_4) is shown below.
![bto_xyz_rdf](https://user-images.githubusercontent.com/8492535/29754816-ae84298c-8b52-11e7-82f2-09ad46198676.png)

The first RDF peak at ~2 A corresponds to Ti-O bond. If integrate it, we expect a CN of 6. Let's do it. 
The results are for crystal we get a number of 1.039; for 1_1_1 cluster we get 0.503; for 4_4_4 we get 0.880. These nubmers are all away from 6! What happened!

In fact, we need to take into account the X-ray weighting factor. It makes sense the peak is high if it involves heavy atoms such as barium. So we need to normalize the peak area by X-ray weighting factor.

Let's calculate the X-ray weighting factor for Ti-O peak

factor = f_Ti * f_O / (f_average^2 * N/2) 

f_Ti = 22

f_O = 8

f_average = (56 + 22 + 8 * 3)/5 = 20.4

N = 5 ##number of atoms in a unit cell

After doing math, we obtain a factor of 0.169.

Let's divide the integrated areas by this factor, we get a CN = 6.15, 2.98, 5.21 for crystal, 1_1_1 and 4_4_4 clusters, respectively. Now it makes sense for crystal it should have a CN of 6; for 1_1_1 cluster since there are only five atoms, the Ti atom is surrouded by three oxygen atoms, so we expect a CN of 3. Well...for a 4_4_4 cluster, since it is of finite size, at periphery of cluster there are broken bonds. Therefore the average CN should be less than 6. If we increase the size of cluster, say 8_8_8, we now get an integrated peak area for Ti-O of 0.943, corresponding to a CN of 5.58. It is larger than 5.21 but still smaller than 6. 

Instead of multiple element system, let's test on a single element system---nickel. It has a face-center cubic structure with a lattice parameter of 3.52 A. In a unit cell, there are four nickel atoms. 

Here is the RDF of nickel. 

![rdf_nickel](https://user-images.githubusercontent.com/8492535/29792940-ad2ad0bc-8c07-11e7-8409-b6378cef1d37.png)

The nearest Ni-Ni bond is between atoms sitting at corner and face-center. This bond has a length of 2.489 A, and the nickel has a CN of 12. Let's now calculate its peak area, it gives a value of 11.96. Well...we don't need a scale factor for single element system!

Back to our mannitol case, since the cluster is only a subset of a crystal, the cooridation number should be smaller than crystal case. 
If we delete all hydrogens and carbon atoms in cif file and single molecule xyz file, and simulate both PDFs, the difference PDF would give a peak at ~2.75 A, and its area has to be 2. This has to pass the test. It does! See below.

![cn_o_only](https://user-images.githubusercontent.com/8492535/29794662-902e85d8-8c0e-11e7-899e-6cff2e86b182.png)

What if we delete hydrogens only, what do we get? Here are the results.

![co](https://user-images.githubusercontent.com/8492535/29842401-5c9bf618-8cce-11e7-9170-1267645f52be.png)

For fun, what if delete C, leaving H and O. What is the coordination number? Here it is.

![oh](https://user-images.githubusercontent.com/8492535/29842475-a398f660-8cce-11e7-92db-8f3b721d08ed.png)

Here are all possible ways we can play with cif and molecule xyz file, and calculate the difference RDF. We can use both files intact, and calculate the difference RDF; or delete partially the element type. For example, "dRDF OH" means in both files we delete carbon atoms. In this particular example, we also changed the atomic density for converting PDF to RDF (i.e. rou0 = 4 x 20/822.473 instead of 4 x 26/822.473 for intact case). 

![drdf](https://user-images.githubusercontent.com/8492535/29842644-15f6ea6e-8ccf-11e7-9761-7f4ad0b60ff1.png)

Back to the top figure: If the peak at ~2.75 A corresponds to O...O, then we can find a CN by normalized by X-ray weighting factor.

factor = f_O * f_O / (f_average^2 * N/2)

f_average = (6 * 6 + 14 + 8 * 6)/26 = 3.769

N = 26

factor = 0.346

When divided by this scale factor 0.346, we get a CN of 7.63. Taking into account integration error, the closest integer number is 8. 









