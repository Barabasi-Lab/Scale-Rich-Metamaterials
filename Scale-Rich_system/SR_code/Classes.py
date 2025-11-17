import copy
import matplotlib.axes._axes as axes
from matplotlib.patches import Polygon as polgon
import numpy as np
from typing import List, Tuple, Union, Optional

class Line:
    """
    Represents a line segment by its location and direction.

    Attributes:
    - location (Tuple[float, float]): The starting point of the line.
    - direction (Tuple[float, float]): The direction vector of the line.
    - id (Optional[Union[str, int]]): Identifier for the line segment.
    """
    
    def __init__(self, location: Tuple[float, float], direction: Tuple[float, float], id: Optional[Union[str, int]] = None, neighbors_initial={}, neighbors={}):
        self.location = location
        self.direction = direction
        self.id = id
        self.neighbors_initial = neighbors_initial
        self.neighbors = neighbors
        

    def draw(self, ax: axes.Axes, color: str = 'black', alpha: float = 1.0, label: bool = False, linewidth=1):
        """
        Draw the line segment on a given axes.

        Args:
        - ax (axes.Axes): Matplotlib axes on which to draw the line segment.
        - color (str): Color of the line segment (default is 'black').
        - alpha (float): Alpha (transparency) value (default is 1.0).
        """
        
        x1, y1 = np.array(self.location[0]) - np.array(self.direction) / np.linalg.norm(self.direction) * 100
        x2, y2 = np.array(self.location[1]) - np.array(self.direction) / np.linalg.norm(self.direction) * 100
        ax.plot([x1, x2], [y1, y2], color=color, alpha=alpha, linewidth=linewidth)
        
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2, self.id, fontsize=12)
            
        ax.set(xlim=(0, 1), ylim=(0, 1))

class LineSegment:
    """
    Represents a line segment defined by its start and end points.

    Attributes:
    - start (Tuple[float, float]): Starting point of the line segment.
    - end (Tuple[float, float]): Ending point of the line segment.
    - id (Optional[Union[str, int]]): Identifier for the line segment.
    """
    
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], id: Optional[Union[str, int]] = None, neighbors_initial={}, neighbors={}):
        self.start = start
        self.end = end
        self.id = id
        self.neighbors_initial = neighbors_initial
        self.neighbors = neighbors
        
    def length(self) -> float:
        return np.linalg.norm(np.array(self.start) - np.array(self.end))

    def draw(self, ax: axes.Axes, color: str = 'black', alpha: float = 1.0, label: bool = False, linewidth=1):
        """
        Draw the line segment on a given axes.

        Args:
        - ax (axes.Axes): Matplotlib axes on which to draw the line segment.
        - color (str): Color of the line segment (default is 'black').
        - alpha (float): Alpha (transparency) value (default is 1.0).
        """
        
        x1, y1 = self.start
        x2, y2 = self.end
        ax.plot([x1, x2], [y1, y2], color=color, alpha=alpha, linewidth=linewidth)
        
        if label:
            ax.text((x1+x2)/2, (y1+y2)/2, self.id, fontsize=12)
            
    def copy(self):
        """
        Create a copy of the LineSegment object.

        Returns:
        - LineSegment: A new LineSegment object with the same attributes.
        """
        return copy.deepcopy(self)
    
class Polygon:
    """
    Represents a polygon defined by a list of vertices.

    Args:
        vertices (List[Tuple[float, float]]): A list of (x, y) coordinates representing the vertices of the polygon.
    """

    def __init__(self, vertices: List[tuple], middle_segment=None):
        """
        Initializes a Polygon instance with the provided vertices.

        Args:
            vertices (List[Tuple[float, float]]): A list of (x, y) coordinates representing the vertices of the polygon.
        """
        self.vertices = vertices
        self.middle_line = middle_segment

    def area(self) -> float:
        """
        Calculates the area of the polygon.

        Returns:
            float: The area of the polygon.

        Raises:
            ValueError: If the polygon has less than 3 vertices.
        """
        if len(self.vertices) < 3:
            raise ValueError("A polygon must have at least 3 vertices.")

        area = 0.0

        for i in range(len(self.vertices)):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % len(self.vertices)]
            area += (x1 * y2) - (x2 * y1)

        area = abs(area) / 2.0

        return area

    def sort_vertices(self) -> List[Tuple[float, float]]:
        """
        Sorts the vertices of the polygon based on their polar angles with respect to a reference point.

        Returns:
            List[Tuple[float, float]]: The sorted list of vertices.
        """
        def polar_angle(point: Tuple[float, float], reference_point: Tuple[float, float]) -> float:
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

        reference_point = min(self.vertices, key=lambda point: point[1])
        return sorted(self.vertices, key=lambda point: polar_angle(point, reference_point))

    def draw(self, ax: axes.Axes, color='purple', alpha=0.8):
        """
        Draws a filled polygon with the given vertices on the specified Matplotlib axes.

        Args:
            ax (matplotlib.axes.Axes): The Matplotlib axes on which to draw the polygon.

        Note:
            This method sorts the vertices based on their polar angles with respect to a reference point
            (vertex with the lowest y-coordinate) before drawing the filled polygon.
        """
        sorted_vertices = self.sort_vertices()
        polygon = polgon(sorted_vertices, closed=True, alpha=alpha, facecolor=color, edgecolor='black')
        ax.add_patch(polygon)
        
    def perimeter(self):
        perimeter = 0
        for i in range(len(self.vertices)):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % len(self.vertices)]
            perimeter += np.sqrt((x1-x2)**2 + (y1-y2)**2)
        return perimeter
        
class Cycle:
    def __init__(self, vertices, id=None):
        self.vertices = vertices
        self.id = id
        
    def sort_vertices(self) -> List[Tuple[float, float]]:
        """
        Sorts the vertices of the polygon based on their polar angles with respect to a reference point.

        Returns:
            List[Tuple[float, float]]: The sorted list of vertices.
        """
        def polar_angle(point: Tuple[float, float], reference_point: Tuple[float, float]) -> float:
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

        reference_point = min(self.vertices, key=lambda point: point[1])
        return sorted(self.vertices, key=lambda point: polar_angle(point, reference_point))

    def draw(self, ax: axes.Axes, color='purple', alpha=0.8):
        sorted_vertices = self.sort_vertices()
        polygon = polgon(sorted_vertices, closed=False, alpha=alpha, color=color)
        ax.add_patch(polygon)