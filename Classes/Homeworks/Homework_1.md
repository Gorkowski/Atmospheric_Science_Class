# Homework 1 Due, Tuesday 9/27/22 11:59 PM

## 1. Air Parcels and Skew-T

Download the radiosonde data from Spokane Washington (OTX), on August 9, 2019 at 00:00 UTC, using the following python snip from the jupyter notebook `skew_T_parcels_plots.ipynb` https://github.com/Gorkowski/Atmospheric_Science_Class/blob/main/Classes/Part1/skew_T_parcels_plots.ipynb
or your own download method.

```python
date = datetime(2019, 8, 9, 0)
station = 'OTX' # stations at https://weather.uwyo.edu/upperair/sounding.html
data = WyomingUpperAir.request_data(site_id=station, time=date)
```

Create the skew-t plot (with temperature and dew point temperature) and answer the following questions: 
1. What is the mean lapse rate form 1000 hPa to 600 hPa? and is this layer of the atmosphere stable or unstable or neutral?
2. From 600 hPa to 300 hPa, does and air parcel follow a moist adiabatic path or a dry adiabatic path?
3. In the dew point temperature curve, what process is occurring in the the dip in temperature at 500 hPa (650 hPa to 450 hPa)?
4. In the dew point temperature curve, what process is occurring in the the dip in temperature at 300 hPa?

Calculate the potential temperature curve form the temperature and pressure data. Plot the potential temperature and temperature curve on a new skew-t plot. Why does the potential temperature curve not follow the temperature curve but instead diverges from it after 600 hPa?



## S&P Ch01 problem 1.5 (plus add-ons)
You consume 500 gallons of gasoline per year in your car (1 gal = 3.7879L).
Assume that gasoline can be represented as consisting entirely of C8H18. Gasoline
has a density of 0.85 g cm- 3 . Assume that combustion of CgH18 leads to CO2 and
H2O. How many kilograms of CO2 does your driving contribute to the atmosphere
each year?

**b.** If you drive an electric car, how many kilograms of CO2 does your driving contribute to the atmosphere each year?
Assume that the electric car is 80% efficient in converting electricity to motion and that the gasoline car is 20% efficient in converting gasoline to motion.
Calculate based on two different energy sources for the electric car: 100% coal or 100% natural gas. 
*State the sources of the possible missing information you used to make your calculations.*

## S&P Ch21 problem 21.1
Compute the magnitude of the geostrophic windspeed (westerly) at 40°N latitude
and 5000 m altitude assuming that the pressure at this latitude and altitude
decreases from south to north by 400 Pa over a distance of 200 km.

## S&P Ch21 problem 21.2
The total mass of water in the atmosphere is 1.3 Χ 10^16 kg, and the global mean
rate of precipitation is estimated to be 0.2 cm day-1. Estimate the global mean
residence time of a molecule of water in the atmosphere.

## Methane
Using the following methane data from https://www.methanelevels.org/ (download at the bottom of the page)
And temperature data https://github.com/Gorkowski/Atmospheric_Science_Class/blob/main/Classes/Part1/temperature_dataset.xlsx

For the 800,000 years ago to 1000 year ago dataset answer the flowing questions:
1. Is methane a leading or lagging indicator of temperature?
2. Is methane and temperature correlated?
3. What is the correlation coefficient?
4. What is the mean methane concentration for this period? and how does it compare to current concentration?
