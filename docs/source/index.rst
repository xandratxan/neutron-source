.. neutron-source documentation master file, created by sphinx-quickstart on Sat Mar 11 16:29:46 2023.
   You can adapt this file completely to your liking, but it should at least contain the root `toctree` directive.

Welcome to neutron-source's documentation!
==========================================

``neutron-source`` This package allows to define calibration radionuclide neutron sources.
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

.. note::
   This project is under active development.

.. toctree::
   info
   usage
   api
   :maxdepth: 4
   :caption: Contents
