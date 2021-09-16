# ReprojectGeometry

[![tests](https://github.com/zacharyburnettNOAA/ReprojectGeometry/workflows/tests/badge.svg)](https://github.com/zacharyburnettNOAA/ReprojectGeometry/actions?query=workflow%3Atests)
[![codecov](https://codecov.io/gh/zacharyburnettNOAA/ensembleperturbation/branch/main/graph/badge.svg?token=4DwZePHp18)](https://codecov.io/gh/zacharyburnettNOAA/reprojectgeometry)
[![build](https://github.com/zacharyburnettNOAA/ReprojectGeometry/workflows/build/badge.svg)](https://github.com/zacharyburnettNOAA/ReprojectGeometry/actions?query=workflow%3Abuild)
[![version](https://img.shields.io/pypi/v/ReprojectGeometry)](https://pypi.org/project/ReprojectGeometry)
[![license](https://img.shields.io/github/license/zacharyburnettNOAA/ReprojectGeometry)](https://creativecommons.org/share-your-work/public-domain/cc0)
[![style](https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/oitnb.svg?format=raw)](https://sourceforge.net/p/oitnb/code)

reproject Shapely geometries

### Installation

```bash
git clone https://github.com/zacharyburnettNOAA/ReprojectGeometry
cd ReprojectGeometry
pip install -e .
```

### Usage

```python
from pyproj import CRS
from shapely.geometry import Polygon

from reprojectgeometry.reproject_geometry import reproject_geometry

wgs84_utm18n_polygon = Polygon(
    [
        (580733.32269, 4504690.71256),
        (580728.62269, 4504690.71256),
        (580728.62269, 4504663.81255),
        (580733.32269, 4504663.81255),
        (580733.32269, 4504690.71256),
    ]
)

print(wgs84_utm18n_polygon.exterior.xy)

wgs84_polygon = reproject_geometry(
    wgs84_utm18n_polygon,
    CRS.from_epsg(32618),
    CRS.from_epsg(4326),
)

print(wgs84_polygon.exterior.xy)
```
