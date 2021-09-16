from typing import Union

import numpy
from pyproj import CRS, Transformer
from shapely.geometry import mapping, shape as shapely_shape
from shapely.geometry.base import BaseGeometry


def reproject_points(
    points: numpy.ndarray, input_crs: Union[CRS, str, int], output_crs: Union[CRS, str, int],
) -> numpy.array:
    """
    Reproject the given points into the given dataframe.

    :param points: NxM array of points (only the first 2 columns x and y will be reprojected)
    :param input_crs: coordinate reference system of given points
    :param output_crs: coordinate reference system of output points
    :return: NxM array of reprojected points
    """

    if not isinstance(points, numpy.ndarray):
        points = numpy.array(points)
    if not isinstance(input_crs, CRS):
        input_crs = CRS.from_user_input(input_crs)
    if not isinstance(output_crs, CRS):
        output_crs = CRS.from_user_input(output_crs)

    transformer = Transformer.from_crs(crs_from=input_crs, crs_to=output_crs,)

    reprojected_points = numpy.flip(
        numpy.stack(arrays=transformer.transform(xx=points[:, 0], yy=points[:, 1],), axis=1),
        axis=1,
    )

    if points.shape[1] > 2:
        reprojected_points = numpy.concatenate((reprojected_points, points[:, 3:]), axis=1)

    return reprojected_points


def reproject_geometry(
    geometry: BaseGeometry, input_crs: CRS, output_crs: CRS,
) -> BaseGeometry:
    """
    Reproject the given geometry with the given CRS into the desired CRS using pyproj.

    :param geometry: Shapely geometry
    :param input_crs: coordinate reference system of given geometry
    :param output_crs: coordinate reference system of output geometry
    :returns: reprojected geometry
    """

    if not isinstance(geometry, BaseGeometry):
        geometry = shapely_shape(geometry)

    geometry = mapping(geometry)

    coordinates = geometry['coordinates']
    geometry_type = geometry['type']

    if geometry_type == 'Point':
        coordinates = reproject_points(
            numpy.expand_dims(coordinates, axis=0), input_crs, output_crs,
        )[0]
    elif geometry_type in ['MultiPoint', 'LineString']:
        coordinates = reproject_points(numpy.array(coordinates), input_crs, output_crs,)
    elif geometry_type in ['MultiLineString', 'Polygon']:
        coordinates = list(coordinates)
        part_lengths = [len(part) for part in coordinates]
        reprojected_coordinates = reproject_points(
            numpy.concatenate(coordinates), input_crs, output_crs,
        )
        coordinate_index = 0
        for part_index, part_length in enumerate(part_lengths):
            coordinates[part_index] = reprojected_coordinates[
                coordinate_index : coordinate_index + part_length
            ]
            coordinate_index += part_length
    elif geometry_type == 'MultiPolygon':
        coordinates = [list(polygon) for polygon in coordinates]
        part_lengths = [[len(shell) for shell in polygon] for polygon in coordinates]
        reprojected_coordinates = reproject_points(
            numpy.concatenate(
                [shell for polygon in coordinates for shell in polygon], axis=0,
            ),
            input_crs,
            output_crs,
        )
        coordinate_index = 0
        for part_index, shell_lengths in enumerate(part_lengths):
            for shell_index in range(len(shell_lengths)):
                shell_length = shell_lengths[shell_index]
                coordinates[part_index][shell_index] = reprojected_coordinates[
                    coordinate_index : coordinate_index + shell_length
                ]
                coordinate_index += shell_length

    if 'Polygon' in geometry_type:
        coordinates = [part for part in coordinates if sum(len(shell) for shell in part) > 0]
    geometry['coordinates'] = coordinates

    return shapely_shape(geometry)
