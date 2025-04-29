import tkinter as tk
import math
import random
import Boid as b
import Vec as vec

class BoidApp:
    def __init__(self, root, width=800, height=600, num_boids=50, boid_turn_margin=0.5):
        self.root = root
        self.width = width
        self.height = height
        self.center = vec.Vec(self.width / 2, self.height / 2)
        self.canvas = tk.Canvas(root, width=width, height=height, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.boids = [b.Boid(random.randint(0, 50) + width / 2, random.randint(0, 50) + height / 2) for _ in range(num_boids)]
        self.boid_turn_margin = boid_turn_margin

        self.resize_event_count = 0
        self.root.bind("<Configure>", self.on_resize)
        self.update_frame()

    def on_resize(self, event):
        self.resize_event_count += 1
        if self.resize_event_count <= 10:
            return
        self.width = event.width
        self.height = event.height
        print(f"New Width: {self.width}, New Height: {self.height}")
        self.canvas.config(width=self.width, height=self.height)

    def update_frame(self):
        self.canvas.delete("all")

        for boid in self.boids:
            boid.next(self.boids, self.width, self.height, self.boid_turn_margin)
            self.draw_boid(boid)
        self.root.after(16, self.update_frame)  # ~60 FPS

    def draw_boid(self, boid):
        x, y = boid.position.x, boid.position.y
        angle = math.atan2(boid.velocity.y, boid.velocity.x)
        size = 10
        points = self.get_triangle_points(x, y, angle, size)
        self.canvas.create_polygon(points, fill="white")

    @staticmethod
    def get_triangle_points(x, y, angle, size):
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