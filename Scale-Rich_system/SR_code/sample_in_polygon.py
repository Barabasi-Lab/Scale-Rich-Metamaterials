import numpy as np
from shapely.geometry import Polygon, Point

def sort_vertices(vertices):
    """
    Sorts the vertices of the polygon based on their polar angles with respect to a reference point.

    Returns:
        List[Tuple[float, float]]: The sorted list of vertices.
    """
    def polar_angle(point, reference_point) -> float:
        """
        Calculates the polar angle of a point with respect to a reference point.

        Args:
            point (Tuple[float, float]): The coordinates (x, y) of the point for which to calculate the polar angle.
            reference_point (Tuple[float, float]): The coordinates (x, y) of the reference point.

        Returns:
            float: The polar angle in radians.
        """
        dx = point[0] - reference_point[0]
        dy = point[1] - reference_point[1]
        return np.arctan2(dy, dx)

    reference_point = min(vertices, key=lambda point: point[1])
    return sorted(vertices, key=lambda point: polar_angle(point, reference_point))

def sample_in_polygon(vertices):
    
    vertices = sort_vertices(vertices)
    
    # Create a Shapely polygon from the given vertices
    polygon = Polygon(vertices)
    
    # Find the bounding box of the polygon
    min_x, min_y, max_x, max_y = polygon.bounds
        
    # Generate random points within the bounding box
    while True:
        random_point = Point(np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y))
        
        # Check if the random point is inside the polygon
        if polygon.contains(random_point):
            return random_point.x, random_point.y
        
def is_inside_polygon(vertices, point):
    vertices = sort_vertices(vertices)
    polygon = Polygon(vertices)
    point = Point(point[0], point[1])
    if polygon.contains(point):
        return True
    else:
        return False