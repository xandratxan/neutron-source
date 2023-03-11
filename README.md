# Package neutron-source

> Calibration radionuclide neutron sources and conventional true values of associated quantities of interest.
 
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

## Usage examples

### How to define a calibration radionuclide neutron source

### Conventional true value of associated quantities of interest

## Release History

* 0.1.0
    * First release

## Source code, license and author

Source code of the package available on [GitHub.](https://github.com/xandratxan/neutron-source)
Distributed under the GNU General Public license. See ``LICENSE`` for more information.

Xandra Campo [@GitHub](https://github.com/xandratxan) – xkmpera@gmail.com