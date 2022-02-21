# Made By Tristan Prater
# Heavily Inspired by Tech With Tim :D Link to Video https://www.youtube.com/watch?v=WTLPmUHTPqo&t=3100s

import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 38, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")


class Planet:
    AU = 149.6e6 * 1000  # The Distance from the Sun to Earth
    G = 6.67428e-11  # Attraction of gravity
    SCALE = 200 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 Day in seconds

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2  # (x of planet) * (SCALE of Planet) + 400 Pixel
        y = self.y * self.SCALE + HEIGHT / 2  # (y of planet) * (SCALE of Planet) + 400 Pixel
        if len(self.orbit) >= 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x,y))
            pygame.draw.lines(win, self.color, False, updated_points, 2)
            pygame.draw.circle(win, self.color, (x, y), self.radius)
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_width() / 2))
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)  # The distance of the planet from the sun.

        if other.sun:
            self.distance_to_sun = distance
        force = self.G * self.mass * other.mass / distance ** 2  # f= G(m1 * m2)/(r^2) (hypotenuse)
        theta = math.atan2(distance_y, distance_x)  # angle of the triangle from sun to planet = tan-1 (y/x)
        force_X = math.cos(theta) * force  # force of x (base of triangle) = cosine(angle)
        force_Y = math.sin(theta) * force  # force of y (height of triangle) = Sin(theta)
        return force_X, force_Y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx / self.mass * self.TIMESTEP  # a= F/M, Vf = V0 + a * ∆Time
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP  # Distance = Velocity * Time
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    Sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30)
    Sun.sun = True

    Earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10 ** 24)
    Earth.y_vel = 29.783 * 1000  # Km converting to Meters

    Mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10 ** 23)
    Mars.y_vel = 24.077 * 1000

    Mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 0.330 * 10 ** 24)
    Mercury.y_vel = -47.4 * 1000

    Venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10 ** 24)
    Venus.y_vel = -35.02 * 1000

    planets = [Sun, Earth, Mars, Mercury, Venus]

    while run:
        clock.tick(60)  # 60FPS
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets=planets)
            planet.draw(WIN)
        pygame.display.update()
    pygame.quit()


main()
