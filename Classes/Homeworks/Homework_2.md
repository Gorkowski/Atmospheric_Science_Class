# Homework 2 Due, Tuesday 10/18/22 11:59 PM
Email a pdf or code of your homework to kjgorkow@mtu.edu
If you have written work, scan it with an app like camscanner to generate a pdf.
Include your name.


## PyMieScatt
Using the `PyMieScatt` python package create the following plots. Use the Part2/LecMie.ipynb notebook to help you.

# Single particle
1a. [10 pt] For the three refractive indices m = 1.5 + 0j, m = 2 + 0j, m = 2.5 + 0j. Plot the wavelength of the maximum Mie extinction efficiency (Qext) as a function of particle radius (Dp = 10 nm to 1000 nm, step_size = 10 nm). Within the 100 nm to 5,000nm wavelength range.
1b. [5 pt] comment on and summarize the relationship between the maximum Mie extinction efficiency and the particle radius. How does the refractive index change this relationship?

2a. [10 pt] For the three refractive indices m = 1.5 + 0.1j, m = 1.5 + 0.5j, m = 1.5 + 1.5j,  m = 2 + 1.5j. Create similar plots as in problem 1 but for each of the Mie efficiencies (Qext, Qsca, Qabs) as a function of particle radius (Dp = 10 nm to 1000 nm, step_size = 10 nm). Within the 100 nm to 5,000nm wavelength range. I'm expecting 3 plots, one for each of the efficiencies.
2b. [5 pt] comment on and summarize the relationship between the wavelength and size there maximum absorption? How does the refractive index change this relationship? [I might change these values after I test this problem]

# Distribution of particles [to be updated]
3a. [15 pt] For a lognormal distribution of particles calculate the wavelength of maximum extinction, scattering, and absorption coefficients (Bext, Bsac, Babs) for the following parameters.

-3 plots with 3 lines in each.

    * m = 1.5 + 0j
    * distribution mean = 50 to 500 nm, step_size = 10 nm
    * distribution geometric sigma = 1.25, 1.5, 2 
    * max (Bext, Bsac, Babs) value within the 100 nm to 5,000 nm wavelength range.

-3 plots with 4 lines in each.

    * m = 1.5 + 0j, 1.5 + 0.5j, 2.0 + 0.5j, 2.0 + 0j
    * distribution mean = 50 to 500 nm, step_size = 10 nm
    * distribution geometric sigma = 1.5
    * max (Bext, Bsac, Babs) value within the 100 nm to 5,000 nm wavelength range.

3b [5 pt] comment on and summarize the relationship between these plots. Also compare the results to problem 1.
