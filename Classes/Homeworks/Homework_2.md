# Homework 2 Due, Tuesday 10/18/22 11:59 PM
Email a pdf or code of your homework to kjgorkow@mtu.edu
If you have written work, scan it with an app like camscanner to generate a pdf.
Include your name.


## PyMieScatt
Using the `PyMieScatt` python package create the following plots. Use the [Mie_lecture](https://github.com/Gorkowski/Atmospheric_Science_Class/blob/main/Classes/Part2/Lec_Mie.ipynb) notebook to help you.

# Single particle
1a. [10 pt] For the three refractive indices m = 1.5 + 0j, m = 2 + 0j, m = 2.5 + 0j. Plot the wavelength of the maximum Mie extinction efficiency (Qext) as a function of particle diameter (Dp = 10 nm to 1000 nm, step_size = 10 nm). Within the 100 nm to 5,000nm wavelength range.
Note: The plot should be wavelength on the y-axis (corresponding to the max Qext) and particle diameter on the x-axis.

1b. [5 pt] comment on and summarize the relationship between the maximum Mie extinction efficiency and the particle diameter. How does the refractive index change this relationship?

2a. [10 pt] For the three refractive indices m = 1.5 + 0.1j, m = 1.5 + 0.5j, m = 1.7 + 0.5j. Create similar plots as in problem 1 but for each of the Mie efficiencies (Qext, Qsca, Qabs) as a function of particle diameter (Dp = 10 nm to 1000 nm, using 100 steps). Within the 10 nm to 2,500nm wavelength range, 200 wavelength samples, and logW=True.

In addition add a 1:1 line to the plot. I'm expecting 3 plots, one for each of the efficiencies.
Note: This took 1 minute to run on my computer, for debugging purposes you can reduce the number of diameter steps.

2b. [5 pt] comment on and summarize the relationship between the wavelength and size there for these three cases? How does the refractive index change this relationship?

# Distribution of particles
3a. [15 pt] For a lognormal distribution of particles calculate the wavelength of maximum extinction, scattering, or absorption coefficients (Bext, Bsac, Babs) for the following parameters.

- 3 plots with 3 lines (plus 1:1 line).
    * m = 1.5 + 0.1j
    * distribution geometric sigma = 1.25, 1.5, 2 


- 3 plots with 3 lines in each (plus 1:1 line).
    * m = 1.5 + 0.1j, 1.5 + 0.5j, 1.7 + 0.5j
    * distribution geometric sigma = 1.5

- Parameters
    * wavelength: logspace 10 nm to 1000 nm with 100 steps
    * distribution: lognormal 
    * distribution mean: linspace, 50 to 500 nm, with 20 steps
    * number of particles: 1000
    * distribution lower size limit: 10 nm, distribution upper size limit: 5000 nm

- Note: For both of these sets, my code took 2.5 minutes to run, for debugging purposes you can reduce the number of steps.


3b [5 pt] comment on and summarize the relationship between these plots. Also compare the results to problem 1 and 2.
