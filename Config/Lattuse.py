# General parameters

MAX_BIOMASS = 700                          # Maximum biomass in grams
LIFETIME = 190                             # Maximum life time of the plant in days
NUMBER_OF_STAGES = 1                       # Number of growth stages can take values 1:5
NUMBER_OF_DAYS_PER_STAGE = [190,0,0,0,0]   # Leave it empty if the number of stages is 1, the sum of the values must be equal to the lifetime

OPTIMAL_CONDITIONS = {
    "light_intensity": [10000,0,0,0,0],   # Light intensity in µmol/m²/s
    "light_duration": [5,0,0,0,0],        # Number of light hours per day
    "DLI": [8.0,0,0,0,0],                 # Daily Light Integral in mol/m²/day
    "temperature": [32,0,0,0,0],          # Temperature in °C
    "RH": [75,0,0,0,0],                   # Relative Humidity in %
    "PH": [6.7,0,0,0,0],                  # pH level
    "EC": [4.3,0,0,0,0],                  # Electrical Conductivity in mS/cm
    "water_duration": [120,0,0,0,0],      # In minutes per cycle
    "water_cycles": [5,0,0,0,0]           # Number of cycles per day
}

# Growth parameters
GROWTH_SIGMAS = {
    "DLI": [1.2,0,0,0,0],             
    "temperature": [1.6,0,0,0,0],    
    "RH": [4.5,0,0,0,0],              
    "PH": [0.5,0,0,0,0],             
    "EC": [0.7,0,0,0,0],              
    "water_duration": [8,0,0,0,0], 
    "water_cycles": [0.2,0,0,0,0]      
}

K = 5      # Parameter to tune the growth curve
A = 3      # Parameter to tune the growth curve

# Damage parameters
LOW_PARAMETERS = {
    "light_intensity": [[5000,0,6],[],[],[],[]],    #[Critical low, minimum, sigma]
    "light_duration": [[5000,0,6],[],[],[],[]],  
    "temperature": [[5000,0,6],[],[],[],[]],    
    "RH": [[5000,0,6],[],[],[],[]],              
    "PH": [[5000,0,6],[],[],[],[]],             
    "EC": [[5000,0,6],[],[],[],[]],              
    "TWD": [[5000,0,6],[],[],[],[]],                # TWD(total water duration) represents the total time that the plant is emerged in water in
}

HIGH_PARAMETERS = {
    "light_intensity": [[5000,0,6],[],[],[],[]],    #[Critical high, maximum, sigma]
    "light_duration": [[5000,0,6],[],[],[],[]],  
    "temperature": [[5000,0,6],[],[],[],[]],    
    "RH": [[5000,0,6],[],[],[],[]],              
    "PH": [[5000,0,6],[],[],[],[]],             
    "EC": [[5000,0,6],[],[],[],[]],              
    "TWD": [[5000,0,6],[],[],[],[]], 
}