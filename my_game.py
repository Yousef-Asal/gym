import pygame
import os

pygame.init()
screen = pygame.display.set_mode((1440, 900))
clock = pygame.time.Clock()
running = True
dt = 0
font_path = os.path.join('assets', 'Lucida_Handwriting_Italic.ttf')
font = pygame.font.Font(font_path, 32)
x_space = 310
y_space = 83
mid_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
background = pygame.image.load(os.path.join("assets", "background.png")).convert()
progress_bar_full = pygame.image.load(os.path.join("assets", "progress_bar_full.png")).convert()
plant_stages = [pygame.image.load(os.path.join("assets", "stage-1.png")).convert(),
                pygame.image.load(os.path.join("assets", "stage-2.png")).convert(),
                pygame.image.load(os.path.join("assets", "stage-3.png")).convert(),
                pygame.image.load(os.path.join("assets", "stage-4.png")).convert(),
                pygame.image.load(os.path.join("assets", "stage-5.png")).convert()]
GREEN = (44, 149, 65)
PURPLE = (143,125,183)
# Rectangle properties
rect_width = 38
max_height = 405  # Maximum possible height
current_height = 10  # Starting height
fixed_bottom = 670  # Fixed bottom position
rect_x = 1357
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    #Background and plant
    screen.blit(background, (0,0))
    screen.blit(plant_stages[4], mid_position-pygame.Vector2(100,200))

    #Progress bar
    current_height = min(current_height + 10, max_height)
    rect_y = fixed_bottom - current_height
    growing_rect = pygame.Rect(rect_x, rect_y, rect_width, current_height)
    pygame.draw.rect(screen, PURPLE, growing_rect)
    pygame.draw.line(screen, PURPLE, (rect_x, fixed_bottom), 
                    (rect_x + rect_width, fixed_bottom), 3)
    if current_height == max_height:
        screen.blit(progress_bar_full, (1356,250))


    #Environment
    #1 Temp
    temp_ts = font.render("32.6", True, GREEN)
    temp_tr = temp_ts.get_rect()
    temp_tr.center = (pygame.Vector2(250,60))
    screen.blit(temp_ts, temp_tr)

    #2 RH
    rh_ts = font.render("32.6", True, GREEN)
    rh_tr = rh_ts.get_rect()
    rh_tr.center = (pygame.Vector2(250,60+y_space))
    screen.blit(rh_ts, rh_tr)

    #3 PH
    ph_ts = font.render("32.6", True, GREEN)
    ph_tr = ph_ts.get_rect()
    ph_tr.center = (pygame.Vector2(250+x_space,60))
    screen.blit(ph_ts, ph_tr)

    #4 EC
    ec_ts = font.render("32.6", True, GREEN)
    ec_tr = ec_ts.get_rect()
    ec_tr.center = (pygame.Vector2(250+x_space,60+y_space))
    screen.blit(ec_ts, ec_tr)

    #5 Light Intensity
    light_intensity_ts = font.render("32.6", True, GREEN)
    light_intensity_tr = light_intensity_ts.get_rect()
    light_intensity_tr.center = (pygame.Vector2(250+2*x_space,60))
    screen.blit(light_intensity_ts, light_intensity_tr)

    #6 Light duration
    light_duration_ts = font.render("32.6", True, GREEN)
    light_duration_tr = light_duration_ts.get_rect()
    light_duration_tr.center = (pygame.Vector2(250+2*x_space,60+y_space))
    screen.blit(light_duration_ts, light_duration_tr)

    #7 Water duration/period
    water_duration_ts = font.render("32.6", True, GREEN)
    water_duration_tr = water_duration_ts.get_rect()
    water_duration_tr.center = (pygame.Vector2(250+3*x_space,60))
    screen.blit(water_duration_ts, water_duration_tr)

    #8 Num of water periods
    water_periods_ts = font.render("32.6", True, GREEN)
    water_periods_tr = water_periods_ts.get_rect()
    water_periods_tr.center = (pygame.Vector2(250+3*x_space,60+y_space))
    screen.blit(water_periods_ts, water_periods_tr)

    #8 Day
    day_ts = font.render("4", True, GREEN)
    day_tr = water_periods_ts.get_rect()
    day_tr.center = (pygame.Vector2(725,221))
    screen.blit(day_ts, day_tr)

    #Actions
    #1 Temp
    action_temp_ts = font.render("32.6", True, GREEN)
    action_temp_tr = action_temp_ts.get_rect()
    action_temp_tr.center = (pygame.Vector2(250,765))
    screen.blit(action_temp_ts, action_temp_tr)

    #2 RH
    action_rh_ts = font.render("32.6", True, GREEN)
    action_rh_tr = action_rh_ts.get_rect()
    action_rh_tr.center = (pygame.Vector2(250,765+y_space))
    screen.blit(action_rh_ts, action_rh_tr)

    #3 PH
    action_ph_ts = font.render("32.6", True, GREEN)
    action_ph_tr = action_ph_ts.get_rect()
    action_ph_tr.center = (pygame.Vector2(250+x_space,765))
    screen.blit(action_ph_ts, action_ph_tr)

    #4 EC
    action_ec_ts = font.render("32.6", True, GREEN)
    action_ec_tr = action_ec_ts.get_rect()
    action_ec_tr.center = (pygame.Vector2(250+x_space,765+y_space))
    screen.blit(action_ec_ts, action_ec_tr)

    #5 Light Intensity
    action_light_intensity_ts = font.render("32.6", True, GREEN)
    action_light_intensity_tr = action_light_intensity_ts.get_rect()
    action_light_intensity_tr.center = (pygame.Vector2(250+2*x_space,765))
    screen.blit(action_light_intensity_ts, action_light_intensity_tr)

    #6 Light duration
    action_light_duration_ts = font.render("32.6", True, GREEN)
    action_light_duration_tr = action_light_duration_ts.get_rect()
    action_light_duration_tr.center = (pygame.Vector2(250+2*x_space,765+y_space))
    screen.blit(action_light_duration_ts, action_light_duration_tr)

    #7 Water duration/period
    action_water_duration_ts = font.render("32.6", True, GREEN)
    action_water_duration_tr = action_water_duration_ts.get_rect()
    action_water_duration_tr.center = (pygame.Vector2(250+3*x_space,765))
    screen.blit(action_water_duration_ts, action_water_duration_tr)

    #8 Num of water periods
    action_water_periods_ts = font.render("32.6", True, GREEN)
    action_water_periods_tr = action_water_periods_ts.get_rect()
    action_water_periods_tr.center = (pygame.Vector2(250+3*x_space,765+y_space))
    screen.blit(action_water_periods_ts, action_water_periods_tr)

    #Equations
    #1 Biomass
    biomass_ts = font.render("32.6", True, GREEN)
    biomass_tr = biomass_ts.get_rect()
    biomass_tr.center = (pygame.Vector2(192,370))
    screen.blit(biomass_ts, biomass_tr)

    #2 Height
    height_ts = font.render("32.6", True, GREEN)
    height_tr = height_ts.get_rect()
    height_tr.center = (pygame.Vector2(192,516))
    screen.blit(height_ts, height_tr)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()