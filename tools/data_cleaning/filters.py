"""Module containing various filtering functions.

Todo:
    * Handle missing keys (for flags)
"""
from osgeo import ogr
# Spatial

# .............................................................................
def get_bounding_box_filter(x_index, y_index, min_x, min_y, max_x, max_y):
    """Get a filter function for the specified bounding box.

    Args:
        x_index (str or int): The index of the 'x' value for each point.
        y_index (str or int): The index of the 'y' value for each point.
        min_x (numeric): The minimum 'x' value for the bounding box.
        min_y (numeric): The minimum 'y' value for the bounding box.
        max_x (numeric): The maximum 'x' value for the bounding box.
        max_y (numeric): The maximum 'y' value for the bounding box.

    Returns:
        function - A function that takes a point as input and returns a boolean
            output indicating if the point is valid according to this filter.
    """
    # .......................
    def bounding_box_filter(point):
        """Bounding box filter function."""
        return (min_x <= point[x_index] <= max_x and
                min_y <= point[y_index] <= max_y)
    return bounding_box_filter


# .............................................................................
def get_data_flag_filter(flag_field_index, filter_flags):
    """Get a filter function for the specified flags.

    Args:
        flag_field_index (str or int): The index of the flag field for each
            point.
        filter_flags (list): A list of flag values that should be considered to
            be invalid.

    Returns:
        function - A function that takes a point as input and returns a boolean
            output indicating if the point is valid according to this filter.
    """
    # .......................
    def flag_filter(point):
        """Data flag filter function."""
        test_flags = point[flag_field_index]
        if not isinstance(test_flags, (list, tuple)):
            test_flags = [test_flags]
        return not any([flag in filter_flags for flag in test_flags])
    return flag_filter


# .............................................................................
def get_intersect_geometries_filter(x_index, y_index, geometries):
    """Get a filter function for intersecting the provided shapefiles.

    Args:
        x_index (str or int): The index of the 'x' value for each point.
        y_index (str or int): The index of the 'y' value for each point.
        geometries (list of ogr.Geometry): A list of geometries to check for
            intersection.

    Returns:
        function - A function that takes a point as input and returns a boolean
            output indicating if the point is valid according to this filter.
    """
    # .......................
    def intersect_geometry_filter(point):
        """Intersect geometry filter function."""
        point_geometry = ogr.Geometry(ogr.wkbPoint)
        point_geometry.AddPoint(point[x_index], point[y_index])
        return any([geom.Intersection(point_geometry) for geom in geometries])
    return intersect_geometry_filter



# .............................................................................
def get_unique_localities_filter(x_index, y_index):
    """Get a filter function that only allows unique (x, y) values.

    Args:
        x_index (str or int): The index of the 'x' value for each point.
        y_index (str or int): The index of the 'y' value for each point.

    Returns:
        function - A function that takes a point as input and returns a boolean
            output indicating if the point is valid according to this filter.
    """
    unique_values = []
    # .......................
    def unique_localities_filter(point):
        """Unique localities filter function."""
        test_val = (point[x_index], point[y_index])
        if test_val in unique_values:
            return False
        unique_values.append(test_val)
        return True
    return unique_localities_filter