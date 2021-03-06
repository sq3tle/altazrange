# AltAzRange - Calculate altitude, azimuth, distance from gps cords
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![Version](https://badge.fury.io/gh/tterb%2FHyde.svg)](https://badge.fury.io/gh/tterb%2FHyde)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fsq3tle%2Faltazrange&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

Simple tool to calculate altitude (elevation), azimuth and range between observer and object or pair of coordinates.
 
**Useful for eg. finding where to aim your antenna - no matter if it's drone, satellite, high altitude balloon.**
## Instalation 
```sh
$ pip install altazrange
```
## Basic Usage

```python
from AltAzRange import AltAzimuthRange
satellite = AltAzimuthRange()
satellite.observer(51.77021, 18.061959, 115)
satellite.target(51.681562, 17.778988, 43152)

satellite.calculate()
{'azimuth': 245.49, 'elevation': 86.86, 'distance': 430555.14}
```
###  Usage for multiple objects with single observer location
If you want to use same observer for multiple objects its recommended to use default_observer
```python
from AltAzRange import AltAzimuthRange
AltAzimuthRange.default_observer(51.773931, 18.061959, 50)
satellite_1 = AltAzimuthRange()
high_alt_balloon = AltAzimuthRange()
satellite_1.target(51.681562, 17.778988, 43152)
high_alt_balloon.target(52.30, 21.37, 190000)

satellite_1.calculate()
{'azimuth': 245.49, 'elevation': 86.86, 'distance': 430555.14}

high_alt_balloon.calculate()
{'azimuth': 74.1, 'elevation': 37.55, 'distance': 304391.38}
```
Default observer can be overwritten using observer method. 

