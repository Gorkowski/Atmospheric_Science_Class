# %% [markdown]
# # Mie Theory in Python
# 
# In this notebook, we will practice using PyMieScatt to calculate the scattering properties of a sphere. We will also look at distributions of spheres.
# Uncomment the code below to install the two packages we will need.
# 
# The documentation in the PyMieScatt is good, You can find it here: https://pymiescatt.readthedocs.io/en/latest/

# %%
# !pip install shapely
# !pip install PyMieScatt

# %%
import numpy as np
import matplotlib.pyplot as plt
import json as json # for printing dictionaries

import PyMieScatt as ps # the main package


# %%
ps.__version__ # check the version, we need 1.8.1 for one of the examples.

# %% [markdown]
# ## Single particles 
# For Mie theory you'll need some basic inputs:
# * The size of the particle
# * The wavelength of the light
# * The refractive index of the particle and the medium (usually =1)
# 
# We use `AutoMieQ` to simplify the calculation and transitions from a mie calcualtion to a rayleigh calculation. The `AutoMieQ` function takes the following inputs:
# 
# `AutoMieQ(m, wavelength, diameter, nMedium=1.0, crossover=0.01, asDict=False, asCrossSection=False)`
# 
# The inputs that have an `= XX`, are optional. The default value is given.

# %%
diameter = 150 # nm 
wavelength = 589 # nm 
m = 1.5 + 0.0001j


single_particle = ps.AutoMieQ(m, wavelength, diameter, asDict=True)
# the asDict=True option returns a dictionary instead of individual variables
# the alternative is to use the following syntax
# Qext, Qsca, Qabs, g, Qpr, Qback, Qratio = ps.AutoMieQ(m, wavelength, diameter, asDict=False)
# or
# Qarray = ps.AutoMieQ(m, wavelength, diameter, asDict=False)

#print single_particle dictionary
print(json.dumps(single_particle, indent=4))

# %% [markdown]
# How about some absorption, so lets increase that imaginary part of the refractive index.

# %%
m_absorption = 1.5 + 0.5j # some absorption

single_particle_absorption = ps.AutoMieQ(m_absorption, wavelength, diameter, asDict=True)
print('Absorption coefficient: ',str(m), ', ', single_particle['Qabs'])
print('Absorption coefficient: ',str(m_absorption), ', ', single_particle_absorption['Qabs'])


# %%
# scattering efficiency and extinction efficiency
print('Scattering efficiency: ',str(m), ', ', single_particle['Qsca'])
print('Scattering efficiency: ',str(m_absorption), ', ', single_particle_absorption['Qsca'])
print('')
print('Ectinction efficiency: ',str(m), ', ', single_particle['Qext'])
print('Ectinction efficiency: ',str(m_absorption), ', ', single_particle_absorption['Qext'])

# %% [markdown]
# Note the same real part of the refractive index, does not result in the same Mie efficiency. 
# 
# Why might that be? 
# try some other particle sizes, add/subtract 100 nm from the diameter.

# %% [markdown]
# ## Particle size scans
# We can explore these dipenedences by scanning over a range of sizes. Here we use the `np.linspace` function to create a range of sizes. We can then use a for loop to calculate the Mie efficiency for each size.

# %%
diameter = np.linspace(10, 5000, 500) # nm
m = 1.5 + 0.001j # some absorption
wavelength = 589 # nm 

Qsca = np.zeros(len(diameter))
Qext = np.zeros(len(diameter))
Qabs = np.zeros(len(diameter))
ssa = np.zeros(len(diameter))
for Dp_i, Dp in enumerate(diameter):
    single_particle = ps.AutoMieQ(m, wavelength, Dp, asDict=True)
    Qsca[Dp_i] = single_particle['Qsca']
    Qext[Dp_i] = single_particle['Qext']
    Qabs[Dp_i] = single_particle['Qabs']
    ssa[Dp_i] = single_particle['Qsca']/single_particle['Qext']

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.plot(diameter, Qsca, label='Qsca')
ax.plot(diameter, Qext, label='Qext')
ax.plot(diameter, Qabs, label='Qabs')
ax.set_xlabel('Diameter (nm)', fontsize=14)
ax.set_ylabel('Mie Q Efficiency', fontsize=14)
ax.legend(fontsize=14)
ax.set_title('Mie Q Efficiency', fontsize=14)


# %% [markdown]
# We can look at the net effect by plotting scattering / extinction. This is the single scattering albedo.

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(diameter, ssa, label='SSA')
ax.set_xlabel('Diameter (nm)', fontsize=14)
ax.set_ylabel('Single Scattering Albedo', fontsize=14)
ax.legend()

# %% [markdown]
# Writing *for* loops is good for clarity, but we can let PyMieScatt do the work for us. Using `MieQ_withDiameterRange(m, wavelength, nMedium=1.0, diameterRange=(10,1000), nd=1000, logD=False)`
#  https://pymiescatt.readthedocs.io/en/latest/forward.html#MieQ_withDiameterRange
# 
# The return will be a tuple of arrays. The first array is the diameter, then Mie efficiencies. We can plot this directly.

# %%
# https://pymiescatt.readthedocs.io/en/latest/forward.html#MieQ_withDiameterRange

m = 1.5 + 0.001j # some absorption
wavelength = 589 # nm
# tuple output order
# diameters, qext, qsca, qabs, g, qpr, qback, qratio 
simulation_low_abs = ps.MieQ_withDiameterRange(m, wavelength, diameterRange=(10, 10000), nd=500, logD=False)

m = 1.5 + 0.5j # some absorption
simulation_abs = ps.MieQ_withDiameterRange(m, wavelength, diameterRange=(10, 10000), nd=500, logD=False)

m = 2 + 0.001j # some absorption
simulation_scat = ps.MieQ_withDiameterRange(m, wavelength, diameterRange=(10, 10000), nd=500, logD=False)

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(simulation_low_abs[0], simulation_low_abs[1], label='Qext')
ax.plot(simulation_low_abs[0], simulation_low_abs[2], label='Qsca', linestyle='dashed')
ax.plot(simulation_low_abs[0], simulation_low_abs[3], label='Qabs')
ax.set_xlabel('Diameter (nm)', fontsize = 14)
ax.set_ylabel('Mie Q Efficiency', fontsize = 14)
ax.set_title('Low abs simulation', fontsize = 14)
ax.legend(fontsize = 14)

# %% [markdown]
# Lets look at the comparison based on refractive index. 

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(simulation_low_abs[0], simulation_low_abs[1], label='low abs')
ax.plot(simulation_abs[0], simulation_abs[1], label='more imaginary')
ax.plot(simulation_scat[0], simulation_scat[1], label='more real', alpha = 0.7) # alpha changes the transparency of the line 
ax.set_xlabel('Diameter (nm)', fontsize = 14)
ax.set_ylabel('Mie Q Efficiency', fontsize = 14)
ax.set_title('Extinction', fontsize = 14)
ax.legend(fontsize = 14)

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(simulation_low_abs[0], simulation_low_abs[2], label='low abs')
ax.plot(simulation_abs[0], simulation_abs[2], label='more imaginary')
ax.plot(simulation_scat[0], simulation_scat[2], label='more real', alpha = 0.7) # alpha changes the transparency of the line 
ax.set_xlabel('Diameter (nm)', fontsize = 14)
ax.set_ylabel('Mie Q Efficiency', fontsize = 14)
ax.set_title('Scattering', fontsize = 14)
ax.legend(fontsize = 14)

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(simulation_low_abs[0], simulation_low_abs[3], label='low abs')
ax.plot(simulation_abs[0], simulation_abs[3], label='more imaginary')
ax.plot(simulation_scat[0], simulation_scat[3], label='more real', alpha = 0.7) # alpha changes the transparency of the line 
ax.set_xlabel('Diameter (nm)', fontsize = 14)
ax.set_ylabel('Mie Q Efficiency', fontsize = 14)
ax.set_title('Absroption', fontsize = 14)
ax.legend( fontsize = 14)

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(simulation_low_abs[0], simulation_low_abs[2]/simulation_low_abs[1], label='low abs')
ax.plot(simulation_abs[0], simulation_abs[2]/simulation_abs[1], label='more imaginary')
ax.plot(simulation_scat[0], simulation_scat[2]/simulation_scat[1], label='more real', alpha = 0.7) # alpha changes the transparency of the line 
ax.set_xlabel('Diameter (nm)', fontsize = 14)
ax.set_ylabel('single scattering albedo = SSA', fontsize = 14)
ax.set_title('SSA', fontsize = 14)
ax.legend(fontsize = 14)

# %% [markdown]
# ## Constant diameter, vary wavelength.
# Similar to before, we could just write a for loop...but I'll skip to the function that does the loop for us.
# 
# `MieQ_withWavelengthRange(m, diameter, nMedium=1.0, wavelengthRange=(100,1600), nw=1000, logW=False)`
# 
# https://pymiescatt.readthedocs.io/en/latest/forward.html#MieQ_withWavelengthRange

# %%
lambda_range  = (10, 1500)
diameter = 200 #nm 
m = 1.5 + 0.001j # some absorption 

simulation_low_abs = ps.MieQ_withWavelengthRange(m, diameter, nMedium=1.0, wavelengthRange=lambda_range, nw=500, logW=False)

m = 1.5 + 0.5j # more imaginary
simulation_abs = ps.MieQ_withWavelengthRange(m, diameter, nMedium=1.0, wavelengthRange=lambda_range, nw=500, logW=False)

m = 2 + 0.001j # more real
simulation_scat = ps.MieQ_withWavelengthRange(m, diameter, nMedium=1.0, wavelengthRange=lambda_range, nw=500, logW=False)

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(simulation_low_abs[0], simulation_low_abs[1], label='low abs')
ax.plot(simulation_abs[0], simulation_abs[1], label='more imaginary')
ax.plot(simulation_scat[0], simulation_scat[1], label='more real', alpha = 0.7) # alpha changes the transparency of the line 
ax.set_xlabel('Wavelength (nm)', fontsize = 14)
ax.set_ylabel('Mie Q Efficiency', fontsize = 14)
ax.set_title('Extinction', fontsize = 14)
ax.legend(fontsize = 14)

# %% [markdown]
# The Mie ressonance look a bit different on this scale.

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(simulation_low_abs[0], simulation_low_abs[2], label='low abs')
ax.plot(simulation_abs[0], simulation_abs[2], label='more imaginary')
ax.plot(simulation_scat[0], simulation_scat[2], label='more real', alpha = 0.7) # alpha changes the transparency of the line 
ax.set_xlabel('Wavelength (nm)', fontsize = 14)
ax.set_ylabel('Mie Q Efficiency', fontsize = 14)
ax.set_title('Scattering', fontsize = 14)
ax.legend(fontsize = 14)

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(simulation_low_abs[0], simulation_low_abs[3], label='low abs')
ax.plot(simulation_abs[0], simulation_abs[3], label='more imaginary')
ax.plot(simulation_scat[0], simulation_scat[3], label='more real', alpha = 0.7) # alpha changes the transparency of the line 
ax.set_xlabel('Wavelength (nm)', fontsize = 14)
ax.set_ylabel('Mie Q Efficiency', fontsize = 14)
ax.set_title('Absorption', fontsize = 14)
ax.legend(fontsize = 14)

# %% [markdown]
# On the above graphs:
# * How does the peak depend on the particle size?
# * How does the refractive index change the position the peak?
# * What does the effect of absoprtion have on the resonances?

# %% [markdown]
# # Whispering Gallery Modes
# Let's zoom in on those resonances. To find a interesting measurement tool. 
# 
# First we'll start with a large droplet relative to the wavelength and see what the Q ext looks like.

# %%
lambda_range  = (650, 700)
diameter = 10000 #nm 
m = 1.4 + 0.0001j # some absorption 

WGMs_dp1 = ps.MieQ_withWavelengthRange(m, diameter, nMedium=1.0, wavelengthRange=lambda_range, nw=2000, logW=False)

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(WGMs_dp1[0], WGMs_dp1[1], label='base WGMs')
ax.set_xlabel('Wavelength (nm)', fontsize = 14)
ax.set_ylabel('Mie Q Efficiency', fontsize = 14)
ax.set_title('Whispering Gallery Modes', fontsize = 14)
ax.legend( fontsize = 14)

# %% [markdown]
# All right, now lets change the size of the droplet a little.

# %%
size_delta = 10
WGMs_plus = ps.MieQ_withWavelengthRange(m, diameter+size_delta, nMedium=1.0, wavelengthRange=lambda_range, nw=2000, logW=False)
WGMs_minus = ps.MieQ_withWavelengthRange(m, diameter-size_delta, nMedium=1.0, wavelengthRange=lambda_range, nw=2000, logW=False)

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(WGMs_dp1[0], WGMs_dp1[1], label='base', alpha = 0.8)
ax.plot(WGMs_minus[0], WGMs_minus[1], label='minus', alpha = 0.6)
ax.plot(WGMs_plus[0], WGMs_plus[1], label='plus')
ax.set_xlabel('Wavelength (nm)', fontsize = 14)
ax.set_ylabel('Mie Q Efficiency', fontsize = 14)
ax.set_title('Whispering Gallery Modes', fontsize = 14)
# ax.set_xlim(650, 670)
# ax.set_xlim(667, 668)
ax.legend(fontsize = 14)

# %% [markdown]
# So we got a noticable change in the resonance position. 10 nm on a 10000 nm droplet is a 0.1% change, quite impressive measurement sensitivity.
# 
# We can rerun the above code and zoom in on a resonance.
# * What is happening here? Why is the resonance position changing?
# * Is this a real effect? What is the physical reason for this?
# * What might the size limitations be for this measurement?

# %% [markdown]
# ## Distribution of particles
# 
# For a collections of particles, as long as the multiple scattering is small, we can use the Mie theory to calculate the scattering of the collection. Each particles scattering and absorption is added together.
# 
# $$ b_{Mie} = \frac{\pi D_p^2}{4} ~ Q_{Mie} ~ N_{number}$$
# The optical depth 
# $$ \tau =  b_{Mie} z_{path~length}$$
# 
# First we'll need a distribution of particles. This can be normal, but lognormal is more typical in the atmosphere.

# %%

mu, sigma = 200, 75 # mean and standard deviation
s = np.random.normal(mu, sigma, 2000)
s = np.abs(s)

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
count, bins, ignored = plt.hist(s, 50)
ax.set_xlabel('Particle Diameter (Dp = nm)', fontsize = 14)
ax.set_ylabel('Bin count #/cc', fontsize = 14)
ax.set_title('Particle Counts', fontsize = 14)

# %% [markdown]
# Ok, lets calculate the Qext for each particle and calculate Bext from the size and number in that bin.

# %%
ndp = count
diameter = bins[:-1]+np.diff(bins)/2
m = 1.5 + 0.001j # some absorption
wavelength = 589 #nm


Qext_manual = np.zeros(len(diameter))
for Dp_i, Dp in enumerate(diameter):
    single_particle = ps.AutoMieQ(m, wavelength, Dp, asDict=True)
    Qext_manual[Dp_i] = single_particle['Qext']

# scaling of 1e-6 to cast in units of inverse megameters - see docs
aSDn = np.pi*((diameter/2)**2)*ndp*(1e-6)
Bext_dp = Qext_manual*aSDn

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.bar(diameter, Bext_dp, width=10)
ax.set_xlabel('Particle Diameter (Dp = nm)', fontsize = 14)
ax.set_ylabel('Bext (1/Mm)', fontsize = 14)
ax.set_title('Extinction coefficient', fontsize = 14)

# %% [markdown]
# We can get the total Bext from the sum of the Bext for each bin.

# %%
Bext = np.sum(Qext_manual*aSDn)

print('Total Extinction Coefficient = ', Bext)

# %% [markdown]
# The Bext graph looked a little shifted from the size distribution, lets compare the two.

# %%
fig, ax = plt.subplots(1, 1, figsize=(8, 6))

ax.bar(diameter, Bext_dp/Bext_dp.max(), width=5, label='particle Bext')
ax.bar(diameter, ndp/ndp.max(), width=5, alpha=0.5, label='particle count')

ax.set_xlabel('Particle Diameter (Dp = nm)', fontsize = 14)
ax.set_ylabel('Normalized Bext or particle count', fontsize = 14)
ax.set_title('Compared size vs Bext', fontsize = 14)
ax.legend(fontsize = 14)

# %% [markdown]
# * What is happening here?
# * Why is the max of the Bext not at the peak of the size distribution?

# %% [markdown]
# Instead of using the for loop manually, we can use the `Mie_SD` function. 
# 
# `Mie_SD(m, wavelength, dp, ndp, nMedium=1.0, SMPS=True, interpolate=False, asDict=False)`
# 
# https://pymiescatt.readthedocs.io/en/latest/forward.html#Mie_SD
# 

# %%
B_built_in = ps.Mie_SD(m, wavelength, diameter, ndp, SMPS=True, asDict=True) # this needs pymiescat v 1.8.1
print(json.dumps(B_built_in, indent=4))

print('Manual Bext = ', Bext)

# %% [markdown]
# We can see compare the manual method and the `Mie_SD` function, and they give the same results.

# %% [markdown]
# Now lets look at a Lognormal distribution.

# %%
m = 1.5 + 0.001j # some absorption
wavelength = 589 #nm

mu = 200
sigma = 1.5
total_count = 2000

Bext, Bsca, Babs, bigG, Bpr, Bback, Bratio, dp, ndp, = ps.Mie_Lognormal(m, wavelength, geoStdDev=sigma, geoMean=mu, numberOfParticles=total_count, numberOfBins=250, upper=1000, returnDistribution=True)

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.bar(dp, ndp, label='particle count', width = 5)
ax.set_xlabel('Particle Diameter (Dp = nm)', fontsize = 14)
ax.set_ylabel('Bin count #/cc', fontsize = 14)
ax.set_title('Whispering Gallery Modes', fontsize = 14)

# %% [markdown]
# Now with the lognormal distribution, lets do a wavelength scan, like we did before for a single particle.

# %%
m = 1.5 + 0.001j # some absorption

mu = 200
sigma = 1.5
total_count = 2000

wavelength_vector = np.arange(10, 1500, 25)


Bext_vector = np.zeros(len(wavelength_vector))
Bsca_vector = np.zeros(len(wavelength_vector))

for i, wavelength in enumerate(wavelength_vector):
    Bext_vector[i], Bsca_vector[i], _, _, _, _, _, = ps.Mie_Lognormal(m, wavelength, geoStdDev=sigma, geoMean=mu, numberOfParticles=total_count, numberOfBins=250, upper=1000, returnDistribution=False)


fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(wavelength_vector, Bext_vector, label='Bext')
ax.plot(wavelength_vector, Bsca_vector, label='Bsca')
ax.set_xlabel('Wavelength (nm)', fontsize = 14)
ax.set_ylabel('Bext or Bsca (1/Mm)', fontsize = 14)
ax.set_title('Extinction and Scattering Coefficients', fontsize = 14)
ax.legend(fontsize = 14)

# %% [markdown]
# What happened to our Mie resonances?

# %%
lambda_range  = (10, 1500)
diameter = mu #nm 

simulation_low_abs = ps.MieQ_withWavelengthRange(m, diameter, nMedium=1.0, wavelengthRange=lambda_range, nw=500, logW=False)


fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(wavelength_vector, Bext_vector, label='Bext')
ax.plot(simulation_low_abs[0], simulation_low_abs[1]*100, label='single particle 100x scaled')
ax.set_xlabel('Wavelength (nm)', fontsize = 14)
ax.set_ylabel('Bext or Qext x100', fontsize = 14)
ax.set_title('Extinction and Scattering Coefficients', fontsize = 14)
ax.legend(fontsize = 14)

# %% [markdown]
# * What is the limiting case to get the resonances back?
# * Size?
# * Sigma of the lognormal distribution?
# * Refractive index?

# %% [markdown]
# ## Fixed wavelength, vary the mean of the lognormal distribution.
# Let's look at the size effect on the Mie resonances.

# %%
m = 1.5 + 0.001j # some absorption
wavelength = 589 #nm

sigma = 1.5
total_count = 2000

diameter = np.arange(50, 2000, 50)


Bext_vector = np.zeros(len(diameter))
Bsca_vector = np.zeros(len(diameter))

for i, mu in enumerate(diameter):
    Bext_vector[i], Bsca_vector[i], _, _, _, _, _, = ps.Mie_Lognormal(m, wavelength, geoStdDev=sigma, geoMean=mu, numberOfParticles=total_count, numberOfBins=250, upper=20000, returnDistribution=False)


fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.plot(diameter, Bext_vector, label='Bext')
ax.plot(diameter, Bsca_vector, label='Bsca')
ax.set_xlabel('Geo-mean diameter (nm)', fontsize = 14)
ax.set_ylabel('Bext or Bsca (1/Mm)', fontsize = 14)
ax.set_title('Distribution change of Coefficients', fontsize = 14)
ax.legend(fontsize = 14)

# %% [markdown]
# What could be the limiting case to get the resonances back?
# * Size?
# * Sigma of the lognormal distribution?
# * Refractive index?

# %% [markdown]
# # Rayleigh to Mie Scattering Phase Function
# 
# We can use the `ScatteringFunction` function to calculate the phase function for a single particle.
# 
# `ScatteringFunction(m, wavelength, diameter, nMedium=1.0, minAngle=0, maxAngle=180, angularResolution=0.5, space='theta', angleMeasure='radians', normalization=None)`
# 
# http://pymiescatt.readthedocs.io/en/latest/forward.html#ScatteringFunction

# %%
m = 1.5 + 0.001j # some absorption
wavelength = 589 #nm
dp = 200 #nm.


theta,SL,SR,SU = ps.ScatteringFunction(m,wavelength,dp)


fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 6))
ax.plot(theta, SU, label='unplolarized', linewidth=2)
ax.plot(theta+np.pi, np.flip(SU), label='unplolarized', linewidth=2)
ax.set_rmax(max(SU))
ax.set_rlabel_position(-40)  # Move radial labels away from plotted line
ax.grid(True)
ax.set_title("Scattering angular dependence", va='bottom')
plt.show()

# %% [markdown]
# * What would be the Rayleigh phase function?
# * How about the result for a cloud droplet?
# * How does the refractive index change the phase function? 
# * More absorption?

# %% [markdown]
# # Core - Shell particles
# 
# What about particles with a coating? We can use the `MieQCoreShell` function to calculate the scattering properties of a core-shell particle.
# 
# Why would this change the optical properties of the particle?

# %%
m_core = 1.6 + 0.001j # some absorption
m_shell = 1.45 + 0.001j # some absorption

wavelength = 589 #nm
dp_shell = 200
dp_core = 150 #nm.

particle_core_shell = ps.MieQCoreShell(m_core, m_shell, wavelength, dp_core, dp_shell, asDict=True)
print('core_shell only Qext ', particle_core_shell['Qext'])

particle_shell = ps.MieQ(m_shell, wavelength, dp_shell, asDict=True)
particle_shell_core_to_remove = ps.MieQ(m_shell, wavelength, dp_core, asDict=True)
particle_shell_Qext_minus_core = particle_shell['Qext'] - particle_shell_core_to_remove['Qext']
print('shell Qext ', particle_shell['Qext'])
print('shell Qext minus core approx.', particle_shell_Qext_minus_core)

# %% [markdown]
# Lets do some calculations, to see if the scattering properties are additive.

# %%
particle_core = ps.MieQ(m_core, wavelength, dp_core, asDict=True)
print('core only Qext ', particle_core['Qext'])
print('shell only Qext ', particle_shell_Qext_minus_core)

print('')
print('core + shell Qext ', particle_core['Qext'] + particle_shell_Qext_minus_core)
print('core_shell Qext ', particle_core_shell['Qext'])

# %% [markdown]
# * When is the sum more than the parts?
# * When is it less than the parts?


