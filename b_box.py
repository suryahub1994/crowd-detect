from dataclasses import dataclass

@dataclass
class Box:
    x_left_top: int
    y_left_top: int
    x_right_bottom: int
    y_right_bottom: int
    x_centroid: int
    y_centroid: int
    centroid_class: int