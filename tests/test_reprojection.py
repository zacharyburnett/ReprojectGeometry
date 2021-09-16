from pyproj import CRS
from shapely.geometry import (
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)

from reprojectgeometry.reproject_geometry import reproject_geometry

WGS84 = CRS.from_epsg(4326)
NAD83 = CRS.from_epsg(4269)
WGS84_UTM18N = CRS.from_epsg(32618)
NAD83_UTM18N = CRS.from_epsg(26918)


def test_reproject_point():
    wgs84_utm18n_point = Point((580733.32269, 4504690.71256))
    wgs84_utm18n_multipoint = MultiPoint(
        [(580733.32269, 4504690.71256), (580728.62269, 4504663.81255)]
    )

    wgs84_point = Point((-74.04453072, 40.68916014))
    wgs84_multipoint = MultiPoint([(-74.04453072, 40.68916014), (-74.0445898, 40.6889183)])

    reprojected_point = reproject_geometry(wgs84_utm18n_point, WGS84_UTM18N, WGS84,)
    reprojected_multipoint = reproject_geometry(wgs84_utm18n_multipoint, WGS84_UTM18N, WGS84,)

    assert reprojected_point.almost_equals(wgs84_point, decimal=5,)
    assert reprojected_multipoint.almost_equals(wgs84_multipoint, decimal=5,)


def test_reproject_linestring():
    wgs84_utm18n_linestring = LineString(
        [(580733.32269, 4504690.71256), (580728.62269, 4504663.81255)]
    )
    wgs84_utm18n_multilinestring = MultiLineString(
        [
            [(580733.32269, 4504690.71256), (580728.62269, 4504663.81255)],
            [(580728.62269, 4504690.71256), (580733.32269, 4504663.81255)],
        ]
    )

    wgs84_linestring = LineString([(-74.04453072, 40.68916014), (-74.0445898, 40.6889183)])
    wgs84_multilinestring = MultiLineString(
        [
            [(-74.04453072, 40.68916014), (-74.0445898, 40.6889183)],
            [(-74.0445898, 40.68916014), (-74.04453072, 40.6889183)],
        ]
    )

    reprojected_linestring = reproject_geometry(wgs84_utm18n_linestring, WGS84_UTM18N, WGS84,)
    reprojected_multilinestring = reproject_geometry(
        wgs84_utm18n_multilinestring, WGS84_UTM18N, WGS84,
    )

    assert reprojected_linestring.almost_equals(wgs84_linestring, decimal=5,)
    assert reprojected_multilinestring.almost_equals(wgs84_multilinestring, decimal=5,)


def test_reproject_polygon():
    wgs84_utm18n_polygon = Polygon(
        [
            (580733.32269, 4504690.71256),
            (580728.62269, 4504690.71256),
            (580728.62269, 4504663.81255),
            (580733.32269, 4504663.81255),
            (580733.32269, 4504690.71256),
        ]
    )
    wgs84_utm18n_multipolygon = MultiPolygon(
        [
            [
                [
                    (580733.32269, 4504663.81255),
                    (580753.32269, 4504663.81255),
                    (580743.32269, 4504690.71256),
                    (580728.62269, 4504690.71256),
                    (580733.32269, 4504663.81255),
                ],
                [],
            ],
            [
                [
                    (580763.32269, 4504663.81255),
                    (580783.32269, 4504663.81255),
                    (580773.32269, 4504690.71256),
                    (580758.62269, 4504690.71256),
                    (580763.32269, 4504663.81255),
                ],
                [],
            ],
        ]
    )

    wgs84_polygon = Polygon(
        [
            (-74.0445307243618, 40.68916014235889),
            (-74.0445863409444, 40.68916060265818),
            (-74.04458980179766, 40.688918301595706),
            (-74.04453418541644, 40.688917841300324),
            (-74.0445307243618, 40.68916014235889),
        ]
    )
    wgs84_multipolygon = MultiPolygon(
        [
            [
                [
                    (-74.04453418541644, 40.688917841300324),
                    (-74.04429751997884, 40.6889158822971),
                    (-74.04441239121161, 40.68915916290957),
                    (-74.0445863409444, 40.68916060265818),
                    (-74.04453418541644, 40.688917841300324),
                ],
                [],
            ],
            [
                [
                    (-74.04417918726875, 40.68891490261359),
                    (-74.04394252186606, 40.68891294288276),
                    (-74.04405739179592, 40.68915622383406),
                    (-74.04423134150306, 40.689157664117424),
                    (-74.04417918726875, 40.68891490261359),
                ],
                [],
            ],
        ]
    )

    reprojected_polygon = reproject_geometry(wgs84_utm18n_polygon, WGS84_UTM18N, WGS84,)
    reprojected_multipolygon = reproject_geometry(
        wgs84_utm18n_multipolygon, WGS84_UTM18N, WGS84,
    )

    assert reprojected_polygon.almost_equals(wgs84_polygon, decimal=5,)
    assert reprojected_multipolygon.almost_equals(wgs84_multipolygon, decimal=5,)
