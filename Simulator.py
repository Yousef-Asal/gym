import pygame
import os
import importlib.util



screen_width = 1440
screen_height = 1024
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Custom Sliders Panel")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
current_page = 'start'
num_of_stages = 1
picked_plant = 1



def get_files(folder_path='Config', exclude_file='plant_temp.py'):
    all_files = [
        file for file in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, file)) and file != exclude_file
    ]
    
    # Base names without extensions
    base_names = [os.path.splitext(file)[0] for file in all_files]
    
    return all_files, base_names
def get_plant_images(config_folder='Config', image_folder='Plant_pics', exclude_file='plant_temp.py', default_image='Default_image'):
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.webp']

    config_files = [
        file for file in os.listdir(config_folder)
        if os.path.isfile(os.path.join(config_folder, file)) and file != exclude_file
    ]

    plant_names = [os.path.splitext(f)[0] for f in config_files]

    available_images = os.listdir(image_folder)

    result = {}
    for name in plant_names:
        matched_image = next(
            (img for img in available_images if os.path.splitext(img)[0] == name and os.path.splitext(img)[1].lower() in image_extensions),
            default_image
        )
        result[name] = matched_image

    return result

def load_config_files(file_list, config_folder='Config'):
    configs = {}
    for file_name in file_list:
        try:
            module = load_config_module(file_name, config_folder)
            configs[file_name] = module
        except Exception as e:
            print(f"Failed to load {file_name}: {e}")
    return configs

def load_config_module(file_name, config_folder='Config'):
    if not file_name.endswith('.py'):
        raise ValueError("Expected a .py file name")

    module_name = os.path.splitext(file_name)[0]
    file_path = os.path.join(config_folder, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file '{file_path}' does not exist.")

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module

files, plant_names = get_files()
print(files)
print(plant_names)
plant_image_map = get_plant_images()
print(plant_image_map)
default_data = load_config_module('plant_temp.py')
plant_data = load_config_module(files[picked_plant])
print(default_data.MAX_BIOMASS)   
print(plant_data.MAX_BIOMASS)   
config_files = load_config_files(files)
print(config_files[files[picked_plant]].OPTIMAL_CONDITIONS)

##################################### Growth Model ##################################################

conditions = config_files[files[picked_plant]].OPTIMAL_CONDITIONS
def growth_stage_durations(lifetime_days: int, num_stages: int):
    if not (1 <= num_stages <= 5):
        raise ValueError("Number of stages must be between 1 and 5.")
    
    stage_ratios_dict = {
        1: [1.0],                                
        2: [0.4, 0.6],                            
        3: [0.15, 0.55, 0.30],                    
        4: [0.1, 0.35, 0.35, 0.2],                
        5: [0.05, 0.20, 0.35, 0.25, 0.15]         
    }

    ratios = stage_ratios_dict[num_stages]
    durations = [round(r * lifetime_days) for r in ratios]

    difference = lifetime_days - sum(durations)
    if difference != 0:
        durations[-1] += difference

    return durations
print(growth_stage_durations(153,5))
#***************************************************************************************************#

bg1 = pygame.image.load(os.path.join("sim_assets", "bg_1.png")).convert()
bg2 = pygame.image.load(os.path.join("sim_assets", "bg_2.png")).convert()
bg3 = pygame.image.load(os.path.join("sim_assets", "bg_3.png")).convert()
button1_img = pygame.image.load(os.path.join("sim_assets", "project_overview.png")).convert_alpha() 
button1_rect = button1_img.get_rect(center=(368, 822))
button2_img = pygame.image.load(os.path.join("sim_assets", "simulation.png")).convert_alpha() 
button2_rect = button2_img.get_rect(center=(1046, 822))
button3_img = pygame.image.load(os.path.join("sim_assets", "get_started.png")).convert_alpha() 
button3_rect = button3_img.get_rect(center=(screen_width//2, 805))
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if button1_rect.collidepoint(event.pos):
#                 print("Button clicked!") 
#             if button2_rect.collidepoint(event.pos):
#                 current_page = 'pre_sim'
#             if button3_rect.collidepoint(event.pos):
#                 current_page = 'simulation'
#     if current_page == 'start':
#         screen.blit(bg1, (0,0))
#         screen.blit(button1_img, button1_rect)
#         screen.blit(button2_img, button2_rect)
#     elif current_page == 'pre_sim':
#         screen.blit(bg2, (0,0))
#         screen.blit(button3_img, button3_rect)
#     elif current_page == 'simulation':
#         screen.blit(bg3, (0,0))
#     pygame.display.flip()
#     clock.tick(60)