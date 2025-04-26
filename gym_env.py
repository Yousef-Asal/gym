import gymnasium as gym
from gymnasium import spaces
import numpy as np
import os
import my_game

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

        return self.state, reward, terminated, truncated, {}

    def render(self, mode="human"):
        if not hasattr(self, 'window'):
            my_game.init()
            self.window_size = (1440, 900)
            self.window = my_game.display.set_mode(self.window_size)
            my_game.display.set_caption("Hydroponic Farm RL")
            self.font = my_game.font.SysFont(None, 24)

            # Fixed icon size
            self.icon_size = (32, 32)
            self.icons = {
                "temp": my_game.transform.scale(my_game.image.load(os.path.join("assets", "Temp.png")), self.icon_size),
                "humidity": my_game.transform.scale(my_game.image.load(os.path.join("assets", "Humidity.png")), self.icon_size),
                "light": my_game.transform.scale(my_game.image.load(os.path.join("assets", "Light.png")), self.icon_size),
                "ec": my_game.transform.scale(my_game.image.load(os.path.join("assets", "EC.png")), self.icon_size),
                "ph": my_game.transform.scale(my_game.image.load(os.path.join("assets", "PH.png")), self.icon_size),
            }

            self.plant_drawings = {
                "0_0": my_game.image.load(os.path.join("assets", "phase1.png")),
                "0_1": my_game.image.load(os.path.join("assets", "phase2.png")),
                "0_2": my_game.image.load(os.path.join("assets", "phase3.png")),
                "1_0": my_game.image.load(os.path.join("assets", "phase1.png")),
                "1_1": my_game.image.load(os.path.join("assets", "phase2.png")),
                "1_2": my_game.image.load(os.path.join("assets", "phase3.png")),
                "2_0": my_game.image.load(os.path.join("assets", "phase1.png")),
                "2_1": my_game.image.load(os.path.join("assets", "phase2.png")),
                "2_2": my_game.image.load(os.path.join("assets", "phase3.png")),
            }

        for event in my_game.event.get():
            if event.type == my_game.QUIT:
                my_game.quit()
                exit()

        self.window.fill((245, 255, 250))  # Soft background color

        # --- Observations Panel ---
        labels = {
            "temp": f"Temp: {self.state['temp'][0]:.1f}°C",
            "humidity": f"Humidity: {self.state['humidity'][0]:.1f}%",
            "light": f"Light: {self.state['light'][0]:.1f} lx",
            "ec": f"EC: {self.state['ec'][0]:.2f}",
            "ph": f"pH: {self.state['ph'][0]:.2f}",
        }

        y = 10
        for key in labels:
            icon = self.icons[key]
            self.window.blit(icon, (10, y))

            text_surface = self.font.render(labels[key], True, (0, 0, 0))
            text_y = y + (self.icon_size[1] - text_surface.get_height()) // 2
            self.window.blit(text_surface, (10 + self.icon_size[0] + 10, text_y))

            y += self.icon_size[1] + 10

        # --- Plant Visualization ---
        plant_key = f"{self.state['plant_type']}_{self.state['plant_stage']}"
        plant_img = self.plant_drawings.get(plant_key)
        if plant_img:
            center_x = self.window_size[0] // 2 - plant_img.get_width() // 2
            center_y = self.window_size[1] // 2 - plant_img.get_height() // 2
            self.window.blit(plant_img, (center_x, center_y))
        else:
            missing = self.font.render("No image for this plant stage.", True, (255, 0, 0))
            self.window.blit(missing, (self.window_size[0] // 2 - 100, self.window_size[1] // 2))

        # --- Actions & Reward Display ---
        if hasattr(self, 'last_action') and self.last_action is not None:
            formatted_action = []
            for k, v in self.last_action.items():
                if isinstance(v, np.ndarray):
                    formatted = f"{k}: {v[0]:.2f}"
                else:
                    formatted = f"{k}: {v}"
                formatted_action.append(formatted)
            action_str = " | ".join(formatted_action)
        else:
            action_str = "N/A"

        action_text = self.font.render(f"Last Action: {action_str}", True, (0, 100, 0))
        reward_val = getattr(self, 'last_reward', 0)
        reward_text = self.font.render(f"Reward: {reward_val:.2f}", True, (0, 100, 0))

        self.window.blit(action_text, (0, 550))
        self.window.blit(reward_text, (0, 570))

        my_game.display.flip()

