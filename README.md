# ReprojectGeometry

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
