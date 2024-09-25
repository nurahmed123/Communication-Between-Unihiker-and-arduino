import pygame
import serial
import time

# Setup PySerial to communicate with Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust this to your correct port
time.sleep(2)  # Give time for the connection to establish

# Initialize pygame
pygame.init()

# Set up display (240x320 resolution for landscape Unihiker)
screen = pygame.display.set_mode((240, 320), pygame.FULLSCREEN)
pygame.display.set_caption("Arduino Control")

# Define colors
WHITE = (255, 255, 255)
GREEN = (76, 175, 80)   # Modern green color
RED = (244, 67, 54)     # Modern red color
LIGHT_GREY = (240, 240, 240)  # Light background color
DARK_GREY = (50, 50, 50)
SHADOW = (169, 169, 169)

# Button dimensions and animation scaling factor
button_width = 80
button_height = 50
button_scale_factor = 1.05  # Scaling factor for hover animation

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Calculate center of the screen for landscape mode
screen_width, screen_height = 240, 320
center_y = screen_height // 2  # Centered vertically

# Button and title positions (aligned horizontally, rotate screen)
title_rect = pygame.Rect(10, center_y - 75, 220, 40)

# Adjust spacing between buttons to 5 pixels
button_spacing = 10  # Space between buttons
on_button_rect = pygame.Rect(60, center_y - 25, button_width, button_height)
off_button_rect = pygame.Rect(on_button_rect.x + button_width + button_spacing, center_y - 25, button_width, button_height)

# Button state tracking for animation
on_button_hovered = False
off_button_hovered = False

# Functions to send commands to Arduino
def send_on_command():
    arduino.write(b'ON\n')  # Sending 'ON' command to Arduino

def send_off_command():
    arduino.write(b'OFF\n')  # Sending 'OFF' command to Arduino

# Draw rounded rectangle
def draw_rounded_rect(surface, color, rect, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

# Draw button with animation and modern styling
def draw_button(rect, color, text, hovered):
    if hovered:
        # Apply scaling effect when hovered
        scaled_rect = rect.inflate(button_width * (button_scale_factor - 1), button_height * (button_scale_factor - 1))
    else:
        scaled_rect = rect
    
    shadow_rect = scaled_rect.move(3, 3)  # Create shadow by offsetting the button
    draw_rounded_rect(screen, SHADOW, shadow_rect, 15)
    draw_rounded_rect(screen, color, scaled_rect, 15)

    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=scaled_rect.center)
    screen.blit(text_surface, text_rect)

# Main loop
running = True
while running:
    screen.fill(LIGHT_GREY)  # Fill background with light grey for a modern look

    # Draw title (horizontally aligned to the left in landscape mode)
    title_text = font.render("Arduino Control", True, DARK_GREY)
    title_text_rect = title_text.get_rect(center=title_rect.center)
    screen.blit(title_text, title_text_rect)

    # Track mouse position to detect hover state
    mouse_pos = pygame.mouse.get_pos()

    on_button_hovered = on_button_rect.collidepoint(mouse_pos)
    off_button_hovered = off_button_rect.collidepoint(mouse_pos)

    # Draw "ON" and "OFF" buttons with hover animation
    draw_button(on_button_rect, GREEN, "ON", on_button_hovered)
    draw_button(off_button_rect, RED, "OFF", off_button_hovered)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if on_button_rect.collidepoint(event.pos):
                send_on_command()
            elif off_button_rect.collidepoint(event.pos):
                send_off_command()

    # Update display
    pygame.display.flip()

# Close the serial connection when the GUI closes
arduino.close()
pygame.quit()
