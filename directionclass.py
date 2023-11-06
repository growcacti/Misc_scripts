import math
import random


class Direction:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def normalize(self):
        magnitude = math.sqrt(self.x**2 + self.y**2)
        if magnitude != 0:
            self.x /= magnitude
            self.y /= magnitude

    def set_magnitude(self, magnitude):
        self.normalize()
        self.x *= magnitude
        self.y *= magnitude

    def rotate(self, degrees):
        radians = math.radians(degrees)
        cosine = math.cos(radians)
        sine = math.sin(radians)
        new_x = self.x * cosine - self.y * sine
        new_y = self.x * sine + self.y * cosine
        self.x = new_x
        self.y = new_y


# Example usage
direction = Direction(-10, 0)  # Left
direction.set_magnitude(1)  # Set magnitude to 1
print(direction.set_magnitude(10))
direction.rotate(125)  # Rotate by 45 degrees

print(
    direction.x, direction.y
)  # Prints the x and y components of the resulting direction vector
