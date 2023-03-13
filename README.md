# Package neutron-source

> Calibration radionuclide neutron sources and conventional true values of associated quantities of interest.

| Last version: 0.1.0          | Source code: [GitHub](https://github.com/xandratxan/neutron-source/)             | Issues: [GitHub](https://github.com/xandratxan/neutron-source/issues/) |
|------------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------|
| **Last release: March 2023** | **Documentation : [GitHub Pages](https://xandratxan.github.io/neutron-source/)** | **License: GNU GPL 3.0**                                               |

This package allows to define calibration radionuclide neutron sources.
It also allows to compute the conventional true value of their associated quantities of interest.

Calibration radionuclide neutron sources are defined through their characteristic parameters,
as recommended in the standard ISO 8529.
These characteristics are
calibration date,
calibration strength,
half life,
anisotropy factor,
linear attenuation coefficient,
fluence-to-dose conversion factor,
neutron_effectiveness and
total air scatter component.

Conventional true value of the associated quantities of interest are computed as recommended in the standard ISO 8529.
These quantities are 
decay time on a specific date,
decay factor on a specific date,
strength on a specific date,
fluence rate on a specific date and at a specific distance and 
ambient dose equivalent rate on a specific date and at a specific distance.

This package uses the next unit convention:
calibration strength in 1/s,
half life in years,
linear attenuation coefficient in 1/cm,
fluence-to-dose conversion factor in pSv·cm²,
total air scatter component in 1/cm,
decay time in days,
strength in 1/s,
fluence rate in 1/cm²s and 
ambient dose equivalent rate in uSv/h.

## Installation

``neutron-source`` can be installed via pip after downloading the package from GitHub:

```bash
git clone git@github.com:xandratxan/neutron-source.git
cd neutron-source
pip install .
```

## Usage

### Define a neutron source

Create custom source from ``Source`` class:

```python
from magnitude import Magnitude
from source import Source

# Define neutron source from Source class
my_source = Source()
my_source.name = '252-Cf'
my_source.calibration_date = '2012/05/20'
my_source.calibration_strength = Magnitude(value=5.471E+08, unit='1/s', relative_uncertainty=0.013)
my_source.half_life = Magnitude(value=2.6470, unit='y', uncertainty=0.0026)
my_source.anisotropy_factor = Magnitude(value=1.051, unit='ND', uncertainty=0.019)
my_source.linear_attenuation_coefficient = Magnitude(value=1055e-7, unit='1/cm', relative_uncertainty=0.015)
my_source.fluence_to_dose_conversion_factor = Magnitude(value=385, unit='pSv·cm²', relative_uncertainty=0.01)
my_source.neutron_effectiveness = Magnitude(value=0.5, unit='ND', uncertainty=0.1)
my_source.total_air_scatter_component = Magnitude(value=0.00012, unit='1/cm', relative_uncertainty=0.15)
```

Create custom source from custom source class:

```python
from magnitude import Magnitude
from source import Source


# Define neutron source from custom source class
class MySource(Source):
    """252-Cf radionuclide neutron source from LPN."""

    def __init__(self):
        super().__init__()
        self.name = '252-Cf'
        self.calibration_date = '2012/05/20'
        self.calibration_strength = Magnitude(value=5.471E+08, unit='1/s', relative_uncertainty=0.013)
        self.half_life = Magnitude(value=2.6470, unit='y', uncertainty=0.0026)
        self.anisotropy_factor = Magnitude(value=1.051, unit='ND', uncertainty=0.019)
        self.linear_attenuation_coefficient = Magnitude(value=1055e-7, unit='1/cm', relative_uncertainty=0.015)
        self.fluence_to_dose_conversion_factor = Magnitude(value=385, unit='pSv·cm²', relative_uncertainty=0.01)
        self.neutron_effectiveness = Magnitude(value=0.5, unit='ND', uncertainty=0.1)
        self.total_air_scatter_component = Magnitude(value=0.00012, unit='1/cm', relative_uncertainty=0.15)


# Create you custom source class
my_source = MySource()
```
Using built-in Cf neutron source:

```python
from source import Cf

my_source = Cf()
```

### Compute neutron source associated quantities

Compute quantities associated to a neutron source using built-in neutron source:

```python
from magnitude import Magnitude
from source import Cf

# Create a Cf radionuclide neutron source
my_source = Cf()

# Define date and distance
date = '2020/05/20'
distance = Magnitude(value=100, unit='cm', uncertainty=1)

# Compute source decay time on a date
dt = my_source.decay_time(date=date)
print(f'Decay time: {dt}')

# Compute source decay time on a date
df = my_source.decay_factor(date=date)
print(f'Decay factor: {df}')

# Compute source strength on a date
s = my_source.strength(date=date)
print(f'Strength: {s}')

# Compute source fluence rate at a distance on a date
fr = my_source.fluence_rate(date=date, distance=distance)
print(f'Fluence rate: {fr}')

# Compute source ambient dose equivalent rate at a distance on a date
hr = my_source.ambient_dose_equivalent_rate(date=date, distance=distance)
print(f'Ambient dose equivalent rate: {hr}')
```

Output:

```
Decay time: 2922 ± 1 d (0.034223134839151265%)
Decay factor: 0.12307796649188105 ± 0.0002681946089174612 ND (0.21790627239129182%)
Strength: 67335955.46770813 ± 887579.6306368469 1/s (1.3181362386140014%)
Fluence rate: 563.170475934353 ± 14.906082662095244 1/cm²s (2.6468153603692817%)
Ambient dose equivalent rate: 780.5542796450133 ± 22.085178231439247 uSv/h (2.8294224767409286%)
```

## Release History

* 0.1.0
    * First release

## Authors

Xandra Campo

[@GitHub](https://github.com/xandratxan/)
[@GitHub Pages](https://xandratxan.github.io/)

xkmpera@gmail.com