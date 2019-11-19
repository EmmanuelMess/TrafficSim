import pygame
from pygame.constants import K_SPACE
from pygame.rect import Rect

from simulator.simulator import Simulator, TrafficLight, YELLOW
from thinker import Thinker
from utils import vec, toPairI, scale

WIDTH = 700
HEIGHT = 500
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

CAR_RECT = Rect(0, 0, 5, 5)

if __name__ == '__main__':
    SIMULATOR = Simulator([
        vec(50, 40), vec(100, 44), vec(300, 36), vec(450, 40),
        vec(50, 160), vec(100, 180), vec(200, 160), vec(450, 160),
        vec(200, 10), vec(200, 40), vec(150, 172), vec(200, 400)
    ], [
        [1], [9], [3], [7],
        [5], [10], [7], [11],
        [9], [10, 2], [11, 6], [7, 10, 6]
    ], {
        0: TrafficLight(2, 1, 2),
        1: TrafficLight(2, 1, 2),
        2: TrafficLight(2, 1, 2),
        3: TrafficLight(2, 1, 2),
        4: TrafficLight(2, 1, 2),
        5: TrafficLight(2, 1, 2),
        6: TrafficLight(2, 1, 2)
    }, [
        (vec(70, 200), 1, 4)
    ])

    SIMULATOR.createCar(Thinker(), 0)
    SIMULATOR.createCar(Thinker(), 1)

    # initialize pygame and create window
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    transparent_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    pygame.display.set_caption("Traffic Simulator")
    clock = pygame.time.Clock()

    running = True
    paused = False
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    paused = not paused
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        transparent_surface.fill((0, 0, 0, 255))

        for carPos in SIMULATOR.getCarPositions():
            rect = CAR_RECT.copy()
            rect.center = carPos.x, carPos.y
            #pygame.draw.circle(transparent_surface, (143, 235, 52, 20), toPairI(carPos), 20)

        screen.blit(transparent_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        for street in SIMULATOR.map.streets:
            pygame.draw.line(screen, WHITE, toPairI(street.start), toPairI(street.end), 1)

        for street in SIMULATOR.map.streets:
            middlePoint = (street.start + street.end)/2
            normal = scale(street.getDefaultVector().rotate(90), 4)
            middleVertex = scale(street.getDefaultVector(), 4)
            opposite = scale(street.getDefaultVector().rotate(-90), 4)
            pygame.draw.lines(screen, WHITE, False,
                              [toPairI(middlePoint + normal), toPairI(middlePoint + middleVertex), toPairI(middlePoint + opposite)])

        for intersection in SIMULATOR.map.intersections:
            pygame.draw.circle(screen, (100, 255, 50), toPairI(intersection), 5)

        for (intersectionId, light) in SIMULATOR.map.trafficLightsByIntersectionId.items():
            state = light.getState()
            if state == RED:
                color = RED
            elif state == YELLOW:
                color = (255, 255, 0)
            else:
                color = GREEN

            position = SIMULATOR.map.intersections[intersectionId] + vec(10, -10)

            pygame.draw.circle(screen, color, toPairI(position), 4)

        for sourceNode in SIMULATOR.map.sourceNodes:
            pygame.draw.circle(screen, (100, 255, 50), toPairI(sourceNode.position), 5)
            pygame.draw.circle(screen, (255, 0, 0), toPairI(sourceNode.position), 2)

        for carPos in SIMULATOR.getCarPositions():
            rect = CAR_RECT.copy()
            rect.center = carPos.x, carPos.y
            pygame.draw.rect(screen, RED, rect)

        pygame.display.flip()

        if not paused:
            SIMULATOR.step(1/60)


    pygame.quit()
