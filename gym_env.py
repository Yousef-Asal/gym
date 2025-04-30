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
            "watering_period": spaces.Discrete(49),  
            "temp": spaces.Discrete(51),
            "RH": spaces.Discrete(61),
            "light_intensity": spaces.Discrete(41),
            "light_duration": spaces.Discrete(49),
            "ec": spaces.Discrete(51),
            "ph": spaces.Discrete(51)
        })

        # Action space
        self.action_space = spaces.Dict({
            "watering_cycles": spaces.Discrete(11), 
            "watering_period": spaces.Discrete(49),  
            "temp": spaces.Discrete(51),
            "RH": spaces.Discrete(61),
            "light_intensity": spaces.Discrete(41),
            "light_duration": spaces.Discrete(49),
            "ec": spaces.Discrete(51),
            "ph": spaces.Discrete(51)
        })

        self.state = None
        self.episode_length = 1000
        self.current_step = 0
        self.max_days = 150
        self.height = 0
        self.biomass = 0
        self.max_biomass = 450  #lesa hn7dedha
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
        self.plant_stages_assets = [pygame.image.load(os.path.join("assets", "stage-1.png")).convert(),
                             pygame.image.load(os.path.join("assets", "stage-2.png")).convert(),
                             pygame.image.load(os.path.join("assets", "stage-3.png")).convert(),
                             pygame.image.load(os.path.join("assets", "stage-4.png")).convert(),
                             pygame.image.load(os.path.join("assets", "stage-5.png")).convert()]
        self.plant_dead_asset = pygame.image.load(os.path.join("assets", "dead.png")).convert()
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
        self.plant_died = False
        super().reset(seed=seed)
        self.state = {
            "plant_stage": 0,                                  # min=0 (Discrete(5): 0-4
            "day": 0,                                          # min=0 (Discrete(365): 0-364
            "watering_cycles": np.array([0], dtype=np.int32),  # min=0 (Discrete(11): 0-10
            "watering_period": np.array([0], dtype=np.int32),  # min=0 (Discrete(1411): 0-49
            "temp": np.array([0], dtype=np.int32),             # min=0 (Discrete(51): 0-50 → maps to 10°C
            "RH": np.array([0], dtype=np.int32),               # min=0 (Discrete(61): 0-60 → maps to 30% RH
            "light_intensity": np.array([0], dtype=np.int32),  # min=0 (Discrete(41): 0-41 → maps to 0 units
            "light_duration": np.array([0], dtype=np.int32),   # min=0 (Discrete(1441): 0-49
            "ec": np.array([0], dtype=np.int32),               # min=0 (Discrete(51): 0-50 → maps to 0.0
            "ph": np.array([0], dtype=np.int32)                # min=0 (Discrete(51): 0-50 → maps to 5.0
        }
        self.current_step = 0
        return self.state, {}

    def retreive_data(self):
        
        self.day += 1

        self.plant_stage = self.calculate_stage()
        
        self.watering_cycles = self.state['watering_cycles'][0]  # Direct mapping (0-10)

        # Watering period: 0-24 → maps to 0-24 hr (discrete 30-minute intervals)
        self.watering_period = 30 * self.state['watering_period'][0]  

        # Temperature: 0-50 → maps to 10°C-60°C (0.5°C increments)
        self.temp = 10 + self.state['temp'][0]

        # Relative Humidity: 0-60 → maps to 30%-90% (1% increments)
        self.RH = 30 + self.state['RH'][0]

        # Light Intensity: 0-40 → maps to 0-20000 µmol/m²/s (500 units per step)
        self.light_intensity = self.state['light_intensity'][0] * 500

        # Light Duration: 0-49 → maps to 0-24 hours (30-minute increments)
        self.light_duration = self.state['light_duration'][0] * 30  

        # EC (Electrical Conductivity): 0-50 → maps to 0.0-5.0 dS/m (0.1 increments)
        self.ec = self.state['ec'][0] * 0.1

        # pH: 0-50 → maps to 4.0-9 (0.1 increments)
        self.ph = 4.0 + (self.state['ph'][0] * 0.1)

    def _get_observation_state(self):
      return {
          'plant_stage': self.plant_stage,
          'day': self.day,
          'watering_cycles': np.array([int(self.watering_cycles)], dtype=np.int32),
          'watering_period': np.array([int(self.watering_period // 30)], dtype=np.int32),
          'temp': np.array([int(self.temp - 10)], dtype=np.int32),
          'RH': np.array([int(self.RH - 30)], dtype=np.int32),
          'light_intensity': np.array([int(self.light_intensity // 500)], dtype=np.int32),
          'light_duration': np.array([int(self.light_duration // 30)], dtype=np.int32),
          'ec': np.array([int(self.ec // 0.1)], dtype=np.int32),
          'ph': np.array([int((self.ph - 4.0) // 0.1)], dtype=np.int32)
    }

    def calculate_stage(self):
        if self.day < 10: return 0
        elif 10 <= self.day < 30: return 1
        elif 30 <= self.day < 60: return 2
        elif 60 <= self.day < 90: return 3
        else: return 4

    def _apply_actions(self, action):
      self.state['watering_cycles'][0] = action['watering_cycles']
      self.state['watering_period'][0] = action['watering_period']
      self.state['temp'][0] = action['temp']
      self.state['RH'][0] = action['RH']
      self.state['light_intensity'][0] = action['light_intensity']
      self.state['light_duration'][0] = action['light_duration']
      self.state['ec'][0] = action['ec']
      self.state['ph'][0] = action['ph']

    def calculate_reward():
        #El model Hykoon hena 
        # calculate_growth_rate()
        # calculate_penality()
        # calculate_height()
        # reward logic
        return np.random.rand()

    def step(self, action):
        self.current_step += 1

        self._apply_actions(action)
        self.retreive_data()
        self.reward = self.calculate_reward()
        self.state = self._get_observation_state()

        #implement it inside the calculate reward function
        if self.plant_died:
            self.Done = True
            self.reward = -10

        terminated = self.current_step >= self.episode_length
        truncated = False
        self.last_action = action
        self.last_reward = self.reward
        # Apply action to the state (later we can define how it affects plant growth)
        # For now, we skip state transitions to keep it simple

        #pygame loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
        #Background and plant
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.plant_stages_assets[self.plant_stage], self.mid_position-pygame.Vector2(100,200))
        if self.plant_died:
              self.screen.blit(self.plant_dead_asset, self.mid_position-pygame.Vector2(100,200))

        #Progress bar
        self.current_height = min((self.biomass/self.max_biomass)*self.max_height, self.max_height)
        self.rect_y = self.fixed_bottom - self.current_height
        self.growing_rect = pygame.Rect(self.rect_x, self.rect_y, self.rect_width, self.current_height)
        pygame.draw.rect(self.screen, self.PURPLE, self.growing_rect)
        pygame.draw.line(self.screen, self.PURPLE, (self.rect_x, self.fixed_bottom), 
                        (self.rect_x + self.rect_width, self.fixed_bottom), 3)
        if self.current_height == self.max_height:
            self.screen.blit(self.progress_bar_full, (1356,250))


        #Environment
        #1 Temp
        self.temp_ts = self.font.render(f"{self.temp} C", True, self.GREEN)
        self.temp_tr = self.temp_ts.get_rect()
        self.temp_tr.center = (pygame.Vector2(250,60))
        self.screen.blit(self.temp_ts, self.temp_tr)

        #2 RH
        self.rh_ts = self.font.render(f"{self.RH}%", True, self.GREEN)
        self.rh_tr = self.rh_ts.get_rect()
        self.rh_tr.center = (pygame.Vector2(250,60+self.y_space))
        self.screen.blit(self.rh_ts, self.rh_tr)

        #3 PH
        self.ph_ts = self.font.render(f"{self.ph}", True, self.GREEN)
        self.ph_tr = self.ph_ts.get_rect()
        self.ph_tr.center = (pygame.Vector2(250+self.x_space,60))
        self.screen.blit(self.ph_ts, self.ph_tr)

        #4 EC
        self.ec_ts = self.font.render(f"{self.ec}", True, self.GREEN)
        self.ec_tr = self.ec_ts.get_rect()
        self.ec_tr.center = (pygame.Vector2(250+self.x_space,60+self.y_space))
        self.screen.blit(self.ec_ts, self.ec_tr)

        #5 Light Intensity
        self.light_intensity_ts = self.font.render(f"{self.light_intensity} LUX", True, self.GREEN)
        self.light_intensity_tr = self.light_intensity_ts.get_rect()
        self.light_intensity_tr.center = (pygame.Vector2(250+2*self.x_space,60))
        self.screen.blit(self.light_intensity_ts, self.light_intensity_tr)

        #6 Light duration
        self.light_duration_ts = self.font.render(f"{self.light_duration} mins", True, self.GREEN)
        self.light_duration_tr = self.light_duration_ts.get_rect()
        self.light_duration_tr.center = (pygame.Vector2(250+2*self.x_space,60+self.y_space))
        self.screen.blit(self.light_duration_ts, self.light_duration_tr)

        #7 Water duration/period
        self.water_duration_ts = self.font.render(f"{self.watering_period} mins", True, self.GREEN)
        self.water_duration_tr = self.water_duration_ts.get_rect()
        self.water_duration_tr.center = (pygame.Vector2(250+3*self.x_space,60))
        self.screen.blit(self.water_duration_ts, self.water_duration_tr)

        #8 Num of water periods
        self.water_periods_ts = self.font.render(f"{self.watering_cycles}", True, self.GREEN)
        self.water_periods_tr = self.water_periods_ts.get_rect()
        self.water_periods_tr.center = (pygame.Vector2(250+3*self.x_space,60+self.y_space))
        self.screen.blit(self.water_periods_ts, self.water_periods_tr)

        #9 Day
        self.day_ts = self.font.render(f"{self.day}", True, self.GREEN)
        self.day_tr = self.water_periods_ts.get_rect()
        self.day_tr.center = (pygame.Vector2(725,221))
        self.screen.blit(self.day_ts, self.day_tr)

        #Actions
        #1 Temp
        self.action_temp_ts = self.font.render(f"{action['temp']+10} C", True, self.GREEN)
        self.action_temp_tr = self.action_temp_ts.get_rect()
        self.action_temp_tr.center = (pygame.Vector2(250,765))
        self.screen.blit(self.action_temp_ts, self.action_temp_tr)

        #2 RH
        self.action_rh_ts = self.font.render(f"{action['RH']+30}%", True, self.GREEN)
        self.action_rh_tr = self.action_rh_ts.get_rect()
        self.action_rh_tr.center = (pygame.Vector2(250,765+self.y_space))
        self.screen.blit(self.action_rh_ts, self.action_rh_tr)

        #3 PH
        self.action_ph_ts = self.font.render(f"{4.0 + (action['ph'] * 0.1)}", True, self.GREEN)
        self.action_ph_tr = self.action_ph_ts.get_rect()
        self.action_ph_tr.center = (pygame.Vector2(250+self.x_space,765))
        self.screen.blit(self.action_ph_ts, self.action_ph_tr)

        #4 EC
        self.action_ec_ts = self.font.render(f"{action['ec'] * 0.1}", True, self.GREEN)
        self.action_ec_tr = self.action_ec_ts.get_rect()
        self.action_ec_tr.center = (pygame.Vector2(250+self.x_space,765+self.y_space))
        self.screen.blit(self.action_ec_ts, self.action_ec_tr)

        #5 Light Intensity
        self.action_light_intensity_ts = self.font.render(f"{action['light_intensity'] * 500}", True, self.GREEN)
        self.action_light_intensity_tr = self.action_light_intensity_ts.get_rect()
        self.action_light_intensity_tr.center = (pygame.Vector2(250+2*self.x_space,765))
        self.screen.blit(self.action_light_intensity_ts, self.action_light_intensity_tr)

        #6 Light duration
        self.action_light_duration_ts = self.font.render(f"{action['light_duration'] * 30}", True, self.GREEN)
        self.action_light_duration_tr = self.action_light_duration_ts.get_rect()
        self.action_light_duration_tr.center = (pygame.Vector2(250+2*self.x_space,765+self.y_space))
        self.screen.blit(self.action_light_duration_ts, self.action_light_duration_tr)

        #7 Water duration/period
        self.action_water_duration_ts = self.font.render(f"{30 * action['watering_period'] }", True, self.GREEN)
        self.action_water_duration_tr = self.action_water_duration_ts.get_rect()
        self.action_water_duration_tr.center = (pygame.Vector2(250+3*self.x_space,765))
        self.screen.blit(self.action_water_duration_ts, self.action_water_duration_tr)

        #8 Num of water periods
        self.action_water_periods_ts = self.font.render(f"{action['watering_cycles']}", True, self.GREEN)
        self.action_water_periods_tr = self.action_water_periods_ts.get_rect()
        self.action_water_periods_tr.center = (pygame.Vector2(250+3*self.x_space,765+self.y_space))
        self.screen.blit(self.action_water_periods_ts, self.action_water_periods_tr)

        #Equations
        #1 Biomass
        self.biomass_ts = self.font.render(f"{self.biomass} KG", True, self.GREEN)
        self.biomass_tr = self.biomass_ts.get_rect()
        self.biomass_tr.center = (pygame.Vector2(192,370))
        self.screen.blit(self.biomass_ts, self.biomass_tr)

        #2 Height
        self.height_ts = self.font.render(f"{self.height} CM", True, self.GREEN)
        self.height_tr = self.height_ts.get_rect()
        self.height_tr.center = (pygame.Vector2(192,516))
        self.screen.blit(self.height_ts, self.height_tr)

        pygame.display.flip()

        self.dt = self.clock.tick(60) / 1000
        return self.state, self.reward, terminated, truncated, {}