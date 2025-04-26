import gymnasium as gym
from gymnasium import spaces
import numpy as np
import os
import pygame

class HydroponicEnv(gym.Env):
    def __init__(self):
        super(HydroponicEnv, self).__init__()

        # Observation space
        self.observation_space = spaces.Dict({
            "plant_stage": spaces.Discrete(5),   
            "day":  spaces.Discrete(365),
            "watering_cycles": spaces.Discrete(11), 
            "watering_period": spaces.Discrete(1411),  
            "temp": spaces.Discrete(51),
            "RH": spaces.Discrete(61),
            "light_intensity": spaces.Discrete(21),
            "light_duration": spaces.Discrete(1441),
            "ec": spaces.Discrete(51),
            "ph": spaces.Discrete(51)
        })

        # Action space
        self.action_space = spaces.Dict({
            "watering_cycles": spaces.Discrete(11), 
            "watering_period": spaces.Discrete(1411),  
            "temp": spaces.Discrete(51),
            "RH": spaces.Discrete(61),
            "light_intensity": spaces.Discrete(21),
            "light_duration": spaces.Discrete(1441),
            "ec": spaces.Discrete(51),
            "ph": spaces.Discrete(51)
        })

        self.state = None
        self.episode_length = 1000
        self.current_step = 0

        #pygame init 
        
        pygame.init()
        self.screen = pygame.display.set_mode((1440, 900))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.font_path = os.path.join('assets', 'Lucida_Handwriting_Italic.ttf')
        self.font = pygame.font.Font(self.font_path, 32)
        self.x_space = 310
        self.y_space = 83
        self.mid_position = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.background = pygame.image.load(os.path.join("assets", "background.png")).convert()
        self.progress_bar_full = pygame.image.load(os.path.join("assets", "progress_bar_full.png")).convert()
        self.plant_stages = [pygame.image.load(os.path.join("assets", "stage-1.png")).convert(),
                        pygame.image.load(os.path.join("assets", "stage-2.png")).convert(),
                        pygame.image.load(os.path.join("assets", "stage-3.png")).convert(),
                        pygame.image.load(os.path.join("assets", "stage-4.png")).convert(),
                        pygame.image.load(os.path.join("assets", "stage-5.png")).convert()]
        self.GREEN = (44, 149, 65)
        self.PURPLE = (143,125,183)
        # Rectangle properties
        self.rect_width = 38
        self.max_height = 405  
        self.current_height = 0  
        self.fixed_bottom = 670 
        self.rect_x = 1357

    def reset(self, seed=None, options=None):
        self.Done = False
        super().reset(seed=seed)
        self.state = {
            "plant_stage": 0,                                  # min=0 (Discrete(5): 0-4
            "day": 0,                                          # min=0 (Discrete(365): 0-364
            "watering_cycles": 0,                              # min=0 (Discrete(11): 0-10
            "watering_period": 0,                              # min=0 (Discrete(1411): 0-1410
            "temp": np.array([0], dtype=np.int32),             # min=0 (Discrete(51): 0-50 → maps to 10°C
            "RH": np.array([0], dtype=np.int32),               # min=0 (Discrete(61): 0-60 → maps to 30% RH
            "light_intensity": np.array([0], dtype=np.int32),  # min=0 (Discrete(21): 0-20 → maps to 0 units
            "light_duration": np.array([0], dtype=np.int32),   # min=0 (Discrete(1441): 0-1440
            "ec": np.array([0], dtype=np.int32),               # min=0 (Discrete(51): 0-50 → maps to 0.0
            "ph": np.array([0], dtype=np.int32)                # min=0 (Discrete(51): 0-50 → maps to 5.0
        }
        self.current_step = 0
        return self.state, {}

    def step(self, action):
        self.current_step += 1

        # Dummy reward function: you’ll replace this later with a real optimization goal
        reward = np.random.rand()

        terminated = self.current_step >= self.episode_length
        truncated = False
        self.last_action = action
        self.last_reward = reward
        # Apply action to the state (later we can define how it affects plant growth)
        # For now, we skip state transitions to keep it simple
        #pygame loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        #Background and plant
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.plant_stages[4], self.mid_position-pygame.Vector2(100,200))

        #Progress bar
        self.current_height = min(self.current_height + 10, self.max_height)
        self.rect_y = self.fixed_bottom - self.current_height
        self.growing_rect = pygame.Rect(self.rect_x, self.rect_y, self.rect_width, self.current_height)
        pygame.draw.rect(self.screen, self.PURPLE, self.growing_rect)
        pygame.draw.line(self.screen, self.PURPLE, (self.rect_x, self.fixed_bottom), 
                        (self.rect_x + self.rect_width, self.fixed_bottom), 3)
        if self.current_height == self.max_height:
            self.screen.blit(self.progress_bar_full, (1356,250))


        #Environment
        #1 Temp
        self.temp_ts = self.font.render("32.6", True, self.GREEN)
        self.temp_tr = self.temp_ts.get_rect()
        self.temp_tr.center = (pygame.Vector2(250,60))
        self.screen.blit(self.temp_ts, self.temp_tr)

        #2 RH
        self.rh_ts = self.font.render("32.6", True, self.GREEN)
        self.rh_tr = self.rh_ts.get_rect()
        self.rh_tr.center = (pygame.Vector2(250,60+self.y_space))
        self.screen.blit(self.rh_ts, self.rh_tr)

        #3 PH
        self.ph_ts = self.font.render("32.6", True, self.GREEN)
        self.ph_tr = self.ph_ts.get_rect()
        self.ph_tr.center = (pygame.Vector2(250+self.x_space,60))
        self.screen.blit(self.ph_ts, self.ph_tr)

        #4 EC
        self.ec_ts = self.font.render("32.6", True, self.GREEN)
        self.ec_tr = self.ec_ts.get_rect()
        self.ec_tr.center = (pygame.Vector2(250+self.x_space,60+self.y_space))
        self.screen.blit(self.ec_ts, self.ec_tr)

        #5 Light Intensity
        self.light_intensity_ts = self.font.render("32.6", True, self.GREEN)
        self.light_intensity_tr = self.light_intensity_ts.get_rect()
        self.light_intensity_tr.center = (pygame.Vector2(250+2*self.x_space,60))
        self.screen.blit(self.light_intensity_ts, self.light_intensity_tr)

        #6 Light duration
        self.light_duration_ts = self.font.render("32.6", True, self.GREEN)
        self.light_duration_tr = self.light_duration_ts.get_rect()
        self.light_duration_tr.center = (pygame.Vector2(250+2*self.x_space,60+self.y_space))
        self.screen.blit(self.light_duration_ts, self.light_duration_tr)

        #7 Water duration/period
        self.water_duration_ts = self.font.render("32.6", True, self.GREEN)
        self.water_duration_tr = self.water_duration_ts.get_rect()
        self.water_duration_tr.center = (pygame.Vector2(250+3*self.x_space,60))
        self.screen.blit(self.water_duration_ts, self.water_duration_tr)

        #8 Num of water periods
        self.water_periods_ts = self.font.render("32.6", True, self.GREEN)
        self.water_periods_tr = self.water_periods_ts.get_rect()
        self.water_periods_tr.center = (pygame.Vector2(250+3*self.x_space,60+self.y_space))
        self.screen.blit(self.water_periods_ts, self.water_periods_tr)

        #8 Day
        self.day_ts = self.font.render("4", True, self.GREEN)
        self.day_tr = self.water_periods_ts.get_rect()
        self.day_tr.center = (pygame.Vector2(725,221))
        self.screen.blit(self.day_ts, self.day_tr)

        #Actions
        #1 Temp
        self.action_temp_ts = self.font.render("32.6", True, self.GREEN)
        self.action_temp_tr = self.action_temp_ts.get_rect()
        self.action_temp_tr.center = (pygame.Vector2(250,765))
        self.screen.blit(self.action_temp_ts, self.action_temp_tr)

        #2 RH
        self.action_rh_ts = self.font.render("32.6", True, self.GREEN)
        self.action_rh_tr = self.action_rh_ts.get_rect()
        self.action_rh_tr.center = (pygame.Vector2(250,765+self.y_space))
        self.screen.blit(self.action_rh_ts, self.action_rh_tr)

        #3 PH
        self.action_ph_ts = self.font.render("32.6", True, self.GREEN)
        self.action_ph_tr = self.action_ph_ts.get_rect()
        self.action_ph_tr.center = (pygame.Vector2(250+self.x_space,765))
        self.screen.blit(self.action_ph_ts, self.action_ph_tr)

        #4 EC
        self.action_ec_ts = self.font.render("32.6", True, self.GREEN)
        self.action_ec_tr = self.action_ec_ts.get_rect()
        self.action_ec_tr.center = (pygame.Vector2(250+self.x_space,765+self.y_space))
        self.screen.blit(self.action_ec_ts, self.action_ec_tr)

        #5 Light Intensity
        self.action_light_intensity_ts = self.font.render("32.6", True, self.GREEN)
        self.action_light_intensity_tr = self.action_light_intensity_ts.get_rect()
        self.action_light_intensity_tr.center = (pygame.Vector2(250+2*self.x_space,765))
        self.screen.blit(self.action_light_intensity_ts, self.action_light_intensity_tr)

        #6 Light duration
        self.action_light_duration_ts = self.font.render("32.6", True, self.GREEN)
        self.action_light_duration_tr = self.action_light_duration_ts.get_rect()
        self.action_light_duration_tr.center = (pygame.Vector2(250+2*self.x_space,765+self.y_space))
        self.screen.blit(self.action_light_duration_ts, self.action_light_duration_tr)

        #7 Water duration/period
        self.action_water_duration_ts = self.font.render("32.6", True, self.GREEN)
        self.action_water_duration_tr = self.action_water_duration_ts.get_rect()
        self.action_water_duration_tr.center = (pygame.Vector2(250+3*self.x_space,765))
        self.screen.blit(self.action_water_duration_ts, self.action_water_duration_tr)

        #8 Num of water periods
        self.action_water_periods_ts = self.font.render("32.6", True, self.GREEN)
        self.action_water_periods_tr = self.action_water_periods_ts.get_rect()
        self.action_water_periods_tr.center = (pygame.Vector2(250+3*self.x_space,765+self.y_space))
        self.screen.blit(self.action_water_periods_ts, self.action_water_periods_tr)

        #Equations
        #1 Biomass
        self.biomass_ts = self.font.render("32.6", True, self.GREEN)
        self.biomass_tr = self.biomass_ts.get_rect()
        self.biomass_tr.center = (pygame.Vector2(192,370))
        self.screen.blit(self.biomass_ts, self.biomass_tr)

        #2 Height
        self.height_ts = self.font.render("32.6", True, self.GREEN)
        self.height_tr = self.height_ts.get_rect()
        self.height_tr.center = (pygame.Vector2(192,516))
        self.screen.blit(self.height_ts, self.height_tr)

        pygame.display.flip()

        self.dt = self.clock.tick(60) / 1000
        return self.state, reward, terminated, truncated, {}