from solarsystem import SolarSystem, Sun, Planet
solar_system = SolarSystem(width=600, height=400)
suns = (
    Sun(solar_system,
        mass=10 ** 10,
        charge=100,
        position=(-200, 0),
        velocity=(0, 3.5)),
    Sun(solar_system,
        mass=10 ** 10,
        charge=100,
        position=(200, 0),
        velocity=(0, -3.5)),
)
planets = (
    Planet(
        solar_system,
        mass=1,
        charge=1,
        position=(0, 0),
        velocity=(0, 0),
    )
)
timer = 0
while True:
    solar_system.calculate_all_body_interactions(timer)
    solar_system.update_all()
    timer += 1
