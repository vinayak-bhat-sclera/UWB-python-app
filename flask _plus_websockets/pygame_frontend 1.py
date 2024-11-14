import pygame
import requests
import threading
import time

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Map dimensions
ROOM_WIDTH = 800
ROOM_HEIGHT = 600

# qorvo and 2 ble Beacon coordinates (fixed points)
BEACONS = [(500, 250), (350, 180), (700, 180)]

# iphone coordinates (initializing with a default values)
iphone_x = 300
iphone_y = 200

# Fetching coordinates from the Flask API
def fetch_coordinates():
    global iphone_x, iphone_y
    while True:
        try:
            # Send GET request to fetch the latest coordinates from flask
            response = requests.get('http://localhost:5000/get_coordinates')
            if response.status_code == 200:
                data = response.json()
                iphone_x = data.get('x', iphone_x)  # Fallback to current position if there is no data
                iphone_y = data.get('y', iphone_y)
        except Exception as e:
            print(f"Error fetching coordinates: {e}")
        time.sleep(0.1)  # Fetch every 0.1 second for smoother real-time updates

# Initializing Pygame
pygame.init()
screen = pygame.display.set_mode((ROOM_WIDTH, ROOM_HEIGHT))
pygame.display.set_caption("UWB Bluetooth Beacon Navigation")

# Load and scale the background image
background_image = pygame.image.load("floor2.png")
background_image = pygame.transform.scale(background_image, (ROOM_WIDTH, ROOM_HEIGHT))


# Run coordinate fetching in a background thread
thread = threading.Thread(target=fetch_coordinates)
thread.daemon = True
thread.start()

# Main loop
running = True
while running:
    # Fill background
    #screen.fill(WHITE) incase if there is no map , plain white background image

    # Drawing the background image
    screen.blit(background_image, (0, 0))

    # Drawing beacons
    for beacon in BEACONS:
        pygame.draw.circle(screen, BLUE, beacon, 7)

    # Drawing the iphone marker (based on fetched coordinates)
    pygame.draw.circle(screen, RED, (int(iphone_x), int(iphone_y)), 9)

    # Updating the display
    pygame.display.flip()

    # Event handling (checking for quit event)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limit the frame rate to 60 FPS for smoother rendering
    pygame.time.Clock().tick(60)

pygame.quit()


#python3 flask_server.py
#python3 pygame_frontend.py