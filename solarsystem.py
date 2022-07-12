import turtle
import math


class SolarSystemBody(turtle.Turtle):
    # Need a min size so that small mass planets still show up
    min_display_size = 20
    # Log scale so that suns are not extremely large
    display_log_base = 1.1

    def __init__(
        self,
        solar_system,
        mass,
        charge,
        position=(0, 0),
        velocity=(0, 0),
    ):
        super().__init__()
        self.mass = mass
        self.charge = charge
        self.setposition(position)
        self.velocity = velocity
        self.display_size = max(
            math.log(self.mass, self.display_log_base),
            self.min_display_size,
        )

        self.penup()
        self.hideturtle()
        solar_system.add_body(self)

    def draw(self):
        self.clear()
        self.dot(self.display_size)

    def move(self):
        self.setx(self.xcor() + self.velocity[0])
        self.sety(self.ycor() + self.velocity[1])

    def print_position(self):
        print(f"{self.__class__.__name__} position: {self.xcor(), self.ycor()}")


class Sun(SolarSystemBody):
    def __init__(
            self,
            solar_system,
            mass,
            charge,
            position=(0, 0),
            velocity=(0, 0),
    ):
        super().__init__(solar_system, mass, charge, position, velocity)
        self.color("yellow")


class Planet(SolarSystemBody):
    def __init__(
            self,
            solar_system,
            mass,
            charge,
            position=(0, 0),
            velocity=(0, 0),
    ):
        super().__init__(solar_system, mass, charge, position, velocity)
        self.color("blue")

    def __str__(self):
        return "Position: {0}".format(self.color)


class SolarSystem:
    def __init__(self, width, height):
        self.solar_system = turtle.Screen()
        self.solar_system.tracer(0)
        self.solar_system.setup(width, height)
        self.solar_system.bgcolor("black")
        self.bodies = []

    def add_body(self, body):
        self.bodies.append(body)

    def remove_body(self, body):
        self.bodies.remove(body)

    def update_all(self):
        for body in self.bodies:
            body.move()
            body.draw()
            # if type(body) == Planet:
            #     body.print_position()
        self.solar_system.update()

    @staticmethod
    def accelerate_due_to_gravity(
            first: SolarSystemBody,
            second: SolarSystemBody,
            timer: int,
    ):
        omega = 50
        G = 6.67408 * 10 ** -11
        k = 100
        angle = first.towards(second)
        newtonian_force = \
            G * first.mass * second.mass / first.distance(second) ** 3 \
            - first.charge * second.charge / first.distance(second) ** 3
        reverse = 1
        for body in first, second:
            force_x = newtonian_force * \
                (2 * body.xcor() * (math.sin(omega * timer) ** 2) \
                - 4 * body.xcor() * (math.cos(omega * timer) ** 2) \
                - 2 * body.ycor() * math.sin(2 * omega * timer))

            force_y = newtonian_force * \
                (2 * body.ycor() * (math.cos(omega * timer) ** 2) \
                - 4 * body.ycor() * (math.sin(omega * timer) ** 2) \
                - 2 * body.xcor() * math.sin(2 * omega * timer))

            acc_x = force_x / body.mass
            acc_y = force_y / body.mass
            body.velocity = (
                body.velocity[0] + (reverse * acc_x),
                body.velocity[1] + (reverse * acc_y),
            )
            reverse = -1
            print(body.xcor())

    def calculate_all_body_interactions(self, timer):
        bodies_copy = self.bodies.copy()
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                self.accelerate_due_to_gravity(first, second, timer)
