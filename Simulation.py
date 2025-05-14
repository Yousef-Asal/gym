import pygame
import sys
import random
import math
from collections import deque
import colorsys
import os


screen_width = 1440
screen_height = 1024
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Custom Sliders Panel")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
current_page = 'start'

class Slider:
    def __init__(self, x, y, width, min_val, max_val, step, label, initial_value=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = 8
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.label = label
        self.value = initial_value if initial_value is not None else min_val
        self.handle_radius = 10
        self.handle_x = self.get_pos_from_val(self.value)
        self.dragging = False

    def get_val_from_pos(self, pos_x):
        relative_x = pos_x - self.x
        percent = max(0, min(1, relative_x / self.width))
        raw_val = self.min_val + percent * (self.max_val - self.min_val)
        stepped_val = round(raw_val / self.step) * self.step
        return max(self.min_val, min(self.max_val, round(stepped_val, 2)))

    def get_pos_from_val(self, value):
        percent = (value - self.min_val) / (self.max_val - self.min_val)
        return self.x + percent * self.width

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.pos[0] - self.handle_x) ** 2 + (event.pos[1] - self.y) ** 2 < self.handle_radius ** 2:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

    def update(self):
        if self.dragging:
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_x = max(self.x, min(self.x + self.width, mouse_x))
            self.value = self.get_val_from_pos(mouse_x)
            self.handle_x = self.get_pos_from_val(self.value)

    def draw(self, surface):
        val_display = f"{self.value:.2f}" if isinstance(self.value, float) else str(self.value)
        label_surf = font.render(f"{self.label} {val_display}", True, (0, 0, 0))
        surface.blit(label_surf, (self.x, self.y - 25))
        pygame.draw.rect(surface, (180, 180, 180), (self.x, self.y - self.height // 2, self.width, self.height))
        pygame.draw.circle(surface, (0, 120, 255), (int(self.handle_x), self.y), self.handle_radius)

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False

    def draw(self, surface):
        color = (100, 200, 100) if self.hovered else (80, 180, 80)
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surf = font.render(self.text, True, (255, 255, 255))
        surface.blit(text_surf, (self.rect.centerx - text_surf.get_width() // 2,
                                 self.rect.centery - text_surf.get_height() // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

def draw_biomass_bar(surface, x, y, height, percent, biomass_value):
    bar_width = 30
    fill_height = int(height * (percent / 100))
    pygame.draw.rect(surface, (200, 200, 200), (x, y, bar_width, height))  # background
    pygame.draw.rect(surface, (0, 180, 0), (x, y + (height - fill_height), bar_width, fill_height))  # filled

    # Draw percentage
    percent_text = font.render(f"{percent:.1f}%", True, (0, 0, 0))
    surface.blit(percent_text, (x - percent_text.get_width() // 2 + 15, y - 25))

    # Draw actual biomass value
    biomass_text = font.render(f"{biomass_value}g", True, (0, 0, 0))
    surface.blit(biomass_text, (x - biomass_text.get_width() // 2 + 15, y + height + 10))

# Initial biomass values
biomass_percent = 0
biomass_actual = 0
show_biomass = False

show_save = False


# Plant cache and ID system
plant_cache = {}
current_plant_id = 0

def draw_procedural_plant(surface, biomass_percent, center_x=None, base_y=None, *, 
                         plant_id=None, wind_effect=0, target_height=250):
    """Beautiful procedural plant with perfect growth pacing and visual appeal."""
    global current_plant_id, plant_cache
    
    # Initialize defaults
    if center_x is None:
        center_x = surface.get_width() // 2
    if base_y is None:
        base_y = surface.get_height() - 100
    
    # Get or create plant state
    if plant_id is None:
        plant_id = current_plant_id
        current_plant_id += 1
    
    if plant_id not in plant_cache:
        rng = random.Random(plant_id)
        plant_cache[plant_id] = {
            'segments': deque(),
            'leaves': deque(),
            'flowers': deque(),
            'rng': rng,
            'max_biomass': 0,
            'colors': generate_plant_colors(rng),
            'last_flower_time': 0,
            'base_x': center_x,
            'base_y': base_y
        }
    
    state = plant_cache[plant_id]
    
    # Only grow if biomass increased
    if biomass_percent <= state['max_biomass']:
        draw_cached_plant(surface, state, wind_effect)
        return
    
    state['max_biomass'] = biomass_percent
    growth_factor = biomass_percent / 100
    
    # Adjusted growth stages with better pacing
    if growth_factor <= 0.1:
        draw_seed(surface, center_x, base_y, growth_factor)
    else:
        grow_plant(state, growth_factor, target_height)
    
    draw_cached_plant(surface, state, wind_effect)

def generate_plant_colors(rng):
    """Generates harmonious color schemes for the plant."""
    base_hue = rng.uniform(0.25, 0.4)  # Greens
    accent_hue = (base_hue + rng.uniform(0.15, 0.25)) % 1.0
    
    return {
        'stem': hsv_to_rgb(base_hue, 0.8, 0.5),
        'young_stem': hsv_to_rgb(base_hue, 0.7, 0.7),
        'leaf': hsv_to_rgb(base_hue, rng.uniform(0.6, 0.9), rng.uniform(0.7, 0.9)),
        'flower': hsv_to_rgb(accent_hue, rng.uniform(0.7, 0.9), rng.uniform(0.8, 1.0)),
        'fruit': hsv_to_rgb((accent_hue + 0.1) % 1.0, 0.8, 0.7)
    }

def hsv_to_rgb(h, s, v):
    """Converts HSV to RGB (all values 0-1)."""
    rgb = colorsys.hsv_to_rgb(h, s, v)
    return tuple(int(c * 255) for c in rgb)

def draw_seed(surface, x, y, growth_factor):
    """Draws the seed in early growth stages."""
    seed_size = 3 + (growth_factor / 0.1) * 5
    pygame.draw.circle(surface, (139, 69, 19), (x, y), int(seed_size))

def grow_plant(state, growth_factor, target_height):
    """Handles the plant's growth logic."""
    rng = state['rng']
    colors = state['colors']
    center_x, base_y = state['base_x'], state['base_y']
    
    # Initial stem
    if len(state['segments']) == 0:
        add_stem_segment(
            state,
            start_x=center_x,
            start_y=base_y,
            length=target_height * 0.15,
            angle=0,
            width=6,
            color=colors['young_stem']
        )
    
    # Growth phases with better pacing
    if growth_factor > 0.15 and len(state['segments']) < 5:
        extend_main_stem(state, target_height * 0.25, colors)
    
    if growth_factor > 0.3:
        add_leaves(state, growth_factor, colors)
        
    if growth_factor > 0.5 and len(state['segments']) < 12:
        create_branches(state, target_height * 0.2, colors)
    
    if growth_factor > 0.7:
        add_more_leaves(state, colors)
        
    if growth_factor > 0.8 and pygame.time.get_ticks() - state['last_flower_time'] > 1500:
        add_flowers(state, colors)
        state['last_flower_time'] = pygame.time.get_ticks()

def add_stem_segment(state, start_x, start_y, length, angle, width, color):
    """Adds a new stem segment to the plant."""
    angle_rad = math.radians(angle)
    end_x = start_x + math.sin(angle_rad) * length
    end_y = start_y - math.cos(angle_rad) * length
    
    state['segments'].append({
        'start_x': start_x,
        'start_y': start_y,
        'end_x': end_x,
        'end_y': end_y,
        'width': width,
        'color': color,
        'angle': angle
    })

def extend_main_stem(state, length, colors):
    """Extends the main stem upwards."""
    if len(state['segments']) == 0:
        return
    
    last_seg = state['segments'][-1]
    rng = state['rng']
    
    new_angle = last_seg['angle'] + rng.uniform(-10, 10)
    new_length = length * (0.8 + rng.random() * 0.4)
    new_width = max(2, last_seg['width'] * 0.9)
    
    add_stem_segment(
        state,
        start_x=last_seg['end_x'],
        start_y=last_seg['end_y'],
        length=new_length,
        angle=new_angle,
        width=new_width,
        color=colors['stem']
    )

def add_leaves(state, growth_factor, colors):
    """Adds leaves at appropriate growth stages."""
    rng = state['rng']
    segments = list(state['segments'])
    
    # Add leaves to newest segments
    for seg in segments[-min(3, len(segments)):]:
        if rng.random() < 0.7 * growth_factor and len(state['leaves']) < 3 + int(growth_factor * 10):
            add_leaf(
                state,
                x=seg['end_x'],
                y=seg['end_y'],
                angle=seg['angle'] + (35 if rng.random() > 0.5 else -35),
                color=colors['leaf'],
                size=12 + rng.random() * 16,
                curve=rng.uniform(10, 25)
            )

def add_leaf(state, x, y, angle, color, size, curve):
    """Adds a leaf to the plant state."""
    state['leaves'].append({
        'x': x,
        'y': y,
        'angle': angle,
        'color': color,
        'size': size,
        'curve': curve
    })

def create_branches(state, length, colors):
    """Creates beautiful branching patterns."""
    rng = state['rng']
    segments = list(state['segments'])
    
    # Create primary branches on older segments
    for seg in segments[-min(6, len(segments)):-2]:
        if rng.random() < 0.6:
            branch_angle = seg['angle'] + rng.uniform(30, 60) * (1 if rng.random() > 0.5 else -1)
            add_stem_segment(
                state,
                start_x=seg['end_x'],
                start_y=seg['end_y'],
                length=length * rng.uniform(0.6, 0.9),
                angle=branch_angle,
                width=max(1.5, seg['width'] * 0.6),
                color=colors['stem']
            )

def add_more_leaves(state, colors):
    """Adds more leaves to mature plants."""
    rng = state['rng']
    for seg in state['segments']:
        if seg['width'] > 2 and rng.random() < 0.4 and len(state['leaves']) < 15:
            add_leaf(
                state,
                x=seg['end_x'],
                y=seg['end_y'],
                angle=seg['angle'] + (40 if rng.random() > 0.5 else -40),
                color=colors['leaf'],
                size=15 + rng.random() * 20,
                curve=rng.uniform(15, 30)
            )

def add_flowers(state, colors):
    """Adds flowers to branch tips."""
    rng = state['rng']
    for seg in state['segments']:
        if seg['width'] < 3 and rng.random() < 0.5:
            state['flowers'].append({
                'x': seg['end_x'],
                'y': seg['end_y'],
                'size': 6 + rng.random() * 8,
                'color': colors['flower'],
                'petals': 5 + rng.randint(0, 3),
                'phase': rng.random() * 6.28
            })

def draw_cached_plant(surface, state, wind_effect):
    """Draws the plant with beautiful rendering."""
    time = pygame.time.get_ticks()
    wind_offset = math.sin(time * 0.001) * 15 * wind_effect
    center_x, base_y = state['base_x'], state['base_y']
    
    # Draw stems with organic taper
    for i, seg in enumerate(state['segments']):
        width = seg['width'] * (0.9 + 0.1 * math.sin(time * 0.002 + i))
        sway = wind_offset * (i / max(1, len(state['segments'])))
        
        pygame.draw.line(
            surface, seg['color'],
            (seg['start_x'] + sway * 0.3, seg['start_y']),
            (seg['end_x'] + sway, seg['end_y']),
            max(1, int(width))
        )
    
    # Draw leaves with subtle movement
    for leaf in state['leaves']:
        draw_leaf(
            surface,
            leaf['x'] + wind_offset * 0.5,
            leaf['y'] + math.sin(time * 0.0015 + leaf['x']) * 3,
            leaf['size'],
            leaf['angle'],
            leaf['curve'],
            leaf['color']
        )
    
    # Draw flowers with animation
    for flower in state['flowers']:
        draw_flower(
            surface,
            flower['x'] + wind_offset * 0.7,
            flower['y'],
            flower['size'] * (1 + 0.1 * math.sin(time * 0.003 + flower['phase'])),
            flower['color'],
            flower['petals']
        )

def draw_leaf(surface, x, y, size, angle, curve, color):
    """Draws a beautiful organic leaf."""
    angle_rad = math.radians(angle)
    curve_rad = math.radians(curve)
    
    # Main leaf vein
    end_x = x + math.sin(angle_rad) * size
    end_y = y - math.cos(angle_rad) * size
    
    # Control point for curve
    ctrl_x = x + math.sin(angle_rad + curve_rad) * size * 0.7
    ctrl_y = y - math.cos(angle_rad + curve_rad) * size * 0.7
    
    # Create bezier curve points
    points = []
    for t in (i/10 for i in range(11)):
        px = (1-t)**2 * x + 2*(1-t)*t * ctrl_x + t**2 * end_x
        py = (1-t)**2 * y + 2*(1-t)*t * ctrl_y + t**2 * end_y
        points.append((px, py))
    
    # Mirror for other side
    mirror_points = [(x - (p[0] - x), p[1]) for p in reversed(points)]
    all_points = points + mirror_points
    
    # Draw leaf
    pygame.draw.polygon(surface, color, all_points)
    pygame.draw.aalines(surface, (color[0]//2, color[1]//2, color[2]//2), False, all_points)
    pygame.draw.line(surface, (color[0]//2, color[1]//2, color[2]//2), (x, y), (end_x, end_y), 1)

def draw_flower(surface, x, y, size, color, petals):
    """Draws a gorgeous multi-petal flower."""
    center_color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 30))
    
    for i in range(petals):
        angle = math.radians(i * (360 / petals))
        petal_length = size * 1.1
        petal_width = size * 0.6
        
        # Position each petal
        pygame.draw.ellipse(
            surface, color,
            (
                x + math.sin(angle) * petal_length - petal_width/2,
                y - math.cos(angle) * petal_length - size/3,
                petal_width, size * 0.66
            )
        )
    
    # Sparkling center
    pygame.draw.circle(surface, center_color, (x, y), size * 0.25)
    pygame.draw.circle(surface, (255, 255, 200), (x, y), size * 0.15)

def on_button_click():
    global biomass_percent, biomass_actual, show_biomass, show_save
    
    biomass_percent = min(100,biomass_percent+0.1)
    biomass_actual += 15
    show_biomass = True
    show_save = True
show_popup = False

# Function to restart the program
def restart_program():
    pygame.quit()
    pygame.init()
    return pygame.display.set_mode((1440, 900))

# Function called when the "Save" button is clicked
def on_save_click():
    global show_popup
    show_popup = True

def draw_popup():
    # Create the pop-up surface (a rectangle)
    popup_width = 400
    popup_height = 200
    popup_x = (screen.get_width() - popup_width) // 2
    popup_y = (screen.get_height() - popup_height) // 2
    
    pygame.draw.rect(screen, (255, 255, 255), (popup_x, popup_y, popup_width, popup_height))  # White background
    pygame.draw.rect(screen, (0, 0, 0), (popup_x, popup_y, popup_width, popup_height), 5)  # Black border

    # Display text on pop-up
    font = pygame.font.SysFont(None, 36)
    text = font.render("Data saved successfully!", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 40))
    screen.blit(text, text_rect)

    # Draw Restart button
    button_width = 120
    button_height = 40
    button_x = (screen.get_width() - button_width) // 2
    button_y = screen.get_height() // 2 + 20
    pygame.draw.rect(screen, (0, 120, 255), (button_x, button_y, button_width, button_height))  # Button background
    pygame.draw.rect(screen, (0, 0, 0), (button_x, button_y, button_width, button_height), 2)  # Button border

    # Button text
    button_text = font.render("Restart", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 40))
    screen.blit(button_text, button_text_rect)
# Button settings
button_width = 180
button_height = 40
button_x = screen.get_width() // 2 - button_width // 2
button_y = screen.get_height() - 60
submit_button = Button(button_x, button_y, button_width, button_height, "Submit", on_button_click)
save_button = Button(1300, 835, 120, 35, "Save", on_save_click)

# Customize slider settings individually
slider_settings = [
    {"min": 10, "max": 60, "step": 1, "label": "Temp:"},
    {"min": 20, "max": 90, "step": 1, "label": "RH:"},
    {"min": 2, "max": 12, "step": 0.1, "label": "PH:"},
    {"min": 0, "max": 15, "step": 0.1, "label": "EC:"},
    {"min": 0, "max": 40000, "step": 500, "label": "Light Intensity:"},
    {"min": 0, "max": 24, "step": 0.5, "label": "Light Duration:"},
    {"min": 0, "max": 15, "step": 1, "label": "Num of Water Periods:"},
    {"min": 0, "max": 24, "step": 0.5, "label": "Water Duration/Period:"}
]

# Create sliders
sliders = []
x_start = 30
y_start = 150
spacing = 80
slider_width = 300

for i, setting in enumerate(slider_settings):
    sliders.append(Slider(
        x=x_start,
        y=y_start + i * spacing,
        width=slider_width,
        min_val=setting["min"],
        max_val=setting["max"],
        step=setting["step"],
        label=setting["label"]
    ))

plant_id = 1
# Main loop

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
        for slider in sliders:
            slider.handle_event(event)
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
    else:
      for slider in sliders:
          slider.update()

      screen.fill((255, 255, 255))
      for slider in sliders:
          slider.draw(screen)
      # Draw button and biomass bar
      submit_button.draw(screen)
      submit_button.handle_event(event)
      if show_save:
          draw_procedural_plant(screen, biomass_percent, plant_id=plant_id, wind_effect=0.2)
          save_button.draw(screen)
          save_button.handle_event(event)
      draw_biomass_bar(screen, x=screen.get_width() - 60, y=200, height=300, percent=biomass_percent, biomass_value=biomass_actual)
      if show_popup:
          draw_popup()
    pygame.display.flip()
    clock.tick(60)
