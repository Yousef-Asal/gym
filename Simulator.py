import pygame
import os
import importlib.util
import numpy as np
import math



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
selected_stage = 0
current_stage = 0
current_day = 0
biomass = 0


def get_files(folder_path='Config', exclude_file='plant_temp.py'):
    all_files = [
        file for file in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, file)) and file != exclude_file
    ]
    
    # Base names without extensions
    base_names = [os.path.splitext(file)[0] for file in all_files]
    
    return all_files, base_names
def get_plant_images(config_folder='Config', image_folder='Plant_pics', exclude_file='plant_temp.py', default_image='Default_image.png'):
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
##################################### Growth Model ##################################################

simulated_plant = config_files[files[picked_plant]]
conditions = config_files[files[picked_plant]].OPTIMAL_CONDITIONS
optimals = config_files[files[picked_plant]].OPTIMAL_CONDITIONS
sigmas = config_files[files[picked_plant]].GROWTH_SIGMAS
low_params = simulated_plant.LOW_PARAMETERS
high_params = simulated_plant.HIGH_PARAMETERS
max_biomass = simulated_plant.MAX_BIOMASS
lifetime = simulated_plant.LIFETIME
K = simulated_plant.K
A = simulated_plant.A
damage_sensitivity = simulated_plant.DAMAGE_SENSITIVITY
stage_durations = growth_stage_durations(lifetime,num_of_stages)

def get_current_stage():
    global stage_durations
    global current_day
    if current_day < 0:
        raise ValueError("Current day must be non-negative.")

    cumulative_days = 0
    for stage_index, duration in enumerate(stage_durations):
        cumulative_days += duration
        if current_day < cumulative_days:
            return stage_index  # Stages are 0-indexed

    # If current_day exceeds total duration, return last stage
    return len(stage_durations) - 1

def calc_growth () : 
    global optimals
    global sigmas
    global conditions
    global current_day
    global current_stage
    
    #constants optimal 
    dli_optimal = optimals['DLI'][current_stage]
    tempreture_optimal = optimals['temperature'][current_stage]
    ph_optimal = optimals['PH'][current_stage]
    ec_optimal = optimals['EC'][current_stage]
    rh_optimal = optimals['RH'][current_stage]
    water_duration_optimal = optimals['water_duration'][current_stage]
    n_cycles_optimal = optimals['water_cycles'][current_stage]

    # constants sigma 
    dli_sigma = sigmas['DLI'][current_stage]
    tempreture_sigma = sigmas['temperature'][current_stage]
    ph_sigma = sigmas['PH'][current_stage]
    ec_sigma = sigmas['EC'][current_stage]
    rh_sigma = sigmas['RH'][current_stage]
    water_duration_sigma = sigmas['water_duration'][current_stage]
    n_cycles_sigma =  sigmas['water_cycles'][current_stage]

    #light 
    ppfd = conditions['light_intensity'][current_stage] * 0.0185
    DLI = ppfd * conditions['light_duration'][current_stage] * 3600/1000000

    f_light = factor_function(dli_optimal,DLI,dli_sigma)

    # tempreture 
    f_temp = factor_function(tempreture_optimal ,conditions['temperature'][current_stage] , tempreture_sigma)
    
    
    #ph 
    f_ph = factor_function(ph_optimal , conditions['PH'][current_stage], ph_sigma)

    #ec
    f_ec = factor_function(ec_optimal , conditions['EC'][current_stage] , ec_sigma)

    # rh 
    f_rh = factor_function(rh_optimal , conditions['RH'][current_stage] , rh_sigma)

    #water 
    f_water_duration = factor_function(water_duration_optimal ,conditions['water_duration'][current_stage] , water_duration_sigma)
    f_n_cycles = factor_function (n_cycles_optimal , conditions['water_cycles'][current_stage] , n_cycles_sigma)
    RUE = calculate_RUE()
    growth = RUE * f_light * f_temp * f_ph * f_ec * f_rh * f_water_duration * f_n_cycles  
    return growth

def calculate_RUE():
  global current_day
  global max_biomass
  global K
  global A
  global lifetime
  RUE_max = calc_RUE_max(max_biomass,K,A,lifetime)
  return RUE_max * math.exp(-((current_day - K) ** 2) / (2 * A ** 2))

def calc_RUE_max(max_biomass, k, a, n):
    denominator = sum(math.exp(-((x - k) ** 2) / (2 * a ** 2)) for x in range(n + 1))
    rue_max = max_biomass / denominator
    return rue_max

def factor_function (x_optimal , x , sigma_x): 
    return np.exp(-((x-x_optimal)**2)/(2*(sigma_x)**2))

def damage_loss(): 
    global conditions
    global current_stage
    D_t = (d_t(conditions['light_intensity'][current_stage],"light_I")+ d_t(conditions['light_duration'][current_stage],"light_D")+ 
           d_t(conditions['temperature'][current_stage],"temp")+ d_t(conditions['RH'][current_stage],"humidity") +d_t(conditions['PH'][current_stage],"ph")+
           d_t(conditions['EC'][current_stage],"ec")+ d_t(conditions['water_duration'][current_stage]*conditions['water_cycles'][current_stage],"TWD"))
    return D_t

def d_t(condition,condition_name:str):
    global low_params
    global high_params
    global optimals
    global current_stage
    conditions_factors={
    # light indensity
    "light_I":{
    "light_I_optimal": optimals['light_intensity'][current_stage],
    "light_I_low" : low_params['light_intensity'][current_stage] ,
    "light_I_high" : high_params['light_intensity'][current_stage]},

    # light duration
    "light_D":{
    "light_D_optimal": optimals['light_duration'][current_stage],
    "light_D_low" : low_params['light_duration'][current_stage] ,
    "light_D_high" : high_params['light_duration'][current_stage]},

    # temp
    "temp":{
    "temp_optimal": optimals['temperature'][current_stage],
    "temp_low" : low_params['temperature'][current_stage] ,
    "temp_high" : high_params['temperature'][current_stage]},
    
    # humidity
    "humidity":{
    "humidity_optimal": optimals['RH'][current_stage],
    "humidity_low" : low_params['RH'][current_stage] ,
    "humidity_high" : high_params['RH'][current_stage]},

    # ph
    "ph":{
    "ph_optimal": optimals['PH'][current_stage],
    "ph_low" : low_params['PH'][current_stage] ,
    "ph_high" : high_params['PH'][current_stage]},

    # ec
    "ec":{
    "ec_optimal": optimals['EC'][current_stage],
    "ec_low" : low_params['EC'][current_stage] ,
    "ec_high" : high_params['EC'][current_stage]},

    # total water duration (number of water cycels * hours per one cycle )
    "TWD":{
    "TWD_optimal": optimals['water_duration'][current_stage]*optimals['water_cycles'][current_stage],
    "TWD_low" : low_params['TWD'][current_stage] ,
    "TWD_high" : high_params['TWD'][current_stage]}

    }
    flag = 0
    if condition < conditions_factors[condition_name][condition_name+"_optimal"] and condition < conditions_factors[condition_name][condition_name+"_low"][0] : 
        x_critical = conditions_factors[condition_name][condition_name+"_low"][0]
        x_max = conditions_factors[condition_name][condition_name+"_low"][1]
        gamma = conditions_factors[condition_name][condition_name+"_low"][2]
        flag = 1
        # print(condition_name, {x_critical})
    elif condition > conditions_factors[condition_name][condition_name+"_optimal"] and condition > conditions_factors[condition_name][condition_name+"_high"][0]:
        x_critical=conditions_factors[condition_name][condition_name+"_high"][0]
        x_max = conditions_factors[condition_name][condition_name+"_high"][1]
        gamma = conditions_factors[condition_name][condition_name+"_high"][2]
        flag = 1

    if flag== 1: 
        f_x = max(0,((condition - x_critical) / (x_max - x_critical)) ** gamma)
    else : 
        f_x =0

    return f_x 

def calc_biomass():
    global biomass
    global current_day
    global lifetime
    global current_stage
    global damage_sensitivity
    for i in range(lifetime) :
        current_stage = get_current_stage()
        growth = calc_growth()
        damage_factor = damage_loss()
        damage = damage_factor * biomass * damage_sensitivity
        current_day += 1
        print("stage is: "+str(current_stage))
        print("growth is: "+str(growth))
        print("damage is: "+str(damage))
        biomass += (growth - damage)
    print("total biomass is: "+str(biomass))

calc_biomass()
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