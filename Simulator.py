import pygame
import sys
from collections import deque
import os


screen_width = 1440
screen_height = 1024
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Custom Sliders Panel")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
current_page = 'start'


bg1 = pygame.image.load(os.path.join("sim_assets", "bg_1.png")).convert()
bg2 = pygame.image.load(os.path.join("sim_assets", "bg_2.png")).convert()
bg3 = pygame.image.load(os.path.join("sim_assets", "bg_3.png")).convert()
button1_img = pygame.image.load(os.path.join("sim_assets", "project_overview.png")).convert_alpha() 
button1_rect = button1_img.get_rect(center=(368, 822))
button2_img = pygame.image.load(os.path.join("sim_assets", "simulation.png")).convert_alpha() 
button2_rect = button2_img.get_rect(center=(1046, 822))
button3_img = pygame.image.load(os.path.join("sim_assets", "get_started.png")).convert_alpha() 
button3_rect = button3_img.get_rect(center=(screen_width//2, 805))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1_rect.collidepoint(event.pos):
                print("Button clicked!") 
            if button2_rect.collidepoint(event.pos):
                current_page = 'pre_sim'
            if button3_rect.collidepoint(event.pos):
                current_page = 'simulation'
    if current_page == 'start':
        screen.blit(bg1, (0,0))
        screen.blit(button1_img, button1_rect)
        screen.blit(button2_img, button2_rect)
    elif current_page == 'pre_sim':
        screen.blit(bg2, (0,0))
        screen.blit(button3_img, button3_rect)
    elif current_page == 'simulation':
        screen.blit(bg3, (0,0))
    pygame.display.flip()
    clock.tick(60)