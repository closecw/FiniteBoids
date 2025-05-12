import tkinter as tk
import math
import random
import Boid as b

class BoidApp:
    """
    Class for the main application.
    Defines the window, boids, and configuration.
    This is the file that should be run.
    """
    def __init__(self, root, width=800, height=600, num_boids=75):
        """
        Constructor for the BoidApp, the main application.
        :param root: Root window, everything will be drawn on this.
        :param width: Width of the window.
        :param height: Height of the window.
        :param num_boids: Number of boids to create.
        """
        self.root = root
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(root, width=width, height=height, bg="black")
        self.canvas.pack(fill="both", expand=True)

        # Boid creation
        self.boids = []
        for _ in range (num_boids):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            self.boids.append(b.Boid(random.uniform(0, width), random.uniform(0, height), speed * math.cos(angle), speed * math.sin(angle)))

        # Property configuration
        self.resize_event_count = 0
        self.root.bind("<Configure>", self.on_resize)
        self.update_frame()

    def on_resize(self, event):
        """
        Resize event handler.
        :param event: Resize event.
        :return: New width and height.
        """
        self.resize_event_count += 1
        if self.resize_event_count <= 10:
            return
        self.width = event.width
        self.height = event.height
        #print(f"New Width: {self.width}, New Height: {self.height}")
        self.canvas.config(width=self.width, height=self.height)

    def update_frame(self):
        """
        Method for updating the frame.
        Calls the next method for each boid and draws them.
        :return: New frame every 17 ms.
        """
        self.canvas.delete("all")       # Potential optimization?
        for i, boid in enumerate(self.boids):
            boid.next(self.boids, self.width, self.height)
            self.draw_boid(boid, i)
        self.root.after(17, self.update_frame)  # ~60 FPS

    @staticmethod
    def color(fatigue):
        """
        Color gradient state machine.
        Takes in each Boid's fatigue, will gradient color based on that.
        :param fatigue: Fatigue of the Boid object.
        :return: Color values in hex format.
        """
        if fatigue < 20:
            ratio = fatigue / 20
            r = 255
            g = 255
            b = int(255 * (1 - ratio))
        elif fatigue < 50:
            ratio = (fatigue - 20) / 30
            r = 255
            g = int(255 * (1 - ratio))
            b = 0
        else:
            r, g, b = 255, 0, 0

        return f"#{r:02x}{g:02x}{b:02x}"

    def draw_boid(self, boid, i):
        """
        Method for drawing a boid.
        :param boid: Boid object that will be drawn.
        :param i: Index of the boid for coloring.
        :return: Triangle drawn for the specified boid.
        """
        x, y = boid.position.x, boid.position.y
        angle = math.atan2(boid.velocity.y, boid.velocity.x)
        size = 8
        points = self.get_triangle_points(x, y, angle, size)
        color = self.color(boid.fatigue)
        self.canvas.create_polygon(points, fill=color)

    @staticmethod
    def get_triangle_points(x, y, angle, size):
        """
        Triangle point generator; acts as a helper method.
        :param x: X (horizontal) coordinate.
        :param y: Y (vertical) coordinate.
        :param angle: Angle of the triangle.
        :param size: Size of the triangle.
        :return: List of triangle points.
        """
        front = (x + size * math.cos(angle), y + size * math.sin(angle))
        left = (x + size * math.cos(angle + 2.5), y + size * math.sin(angle + 2.5))
        right = (x + size * math.cos(angle - 2.5), y + size * math.sin(angle - 2.5))
        return [front, left, right]

# Run
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Boids Simulation")
    app = BoidApp(root)
    root.mainloop()