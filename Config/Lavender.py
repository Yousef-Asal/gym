# General parameters

MAX_BIOMASS = 1500                          # Maximum biomass in grams
LIFETIME = 250                             # Maximum life time of the plant in days
MANUAL_STAGES = False                      # If you want to enter the days of each stage manually
NUMBER_OF_DAYS_PER_STAGE = [0,0,0,0,0]     # Only fill this when the MANUAL_STAGES is set to true, the sum of all values must equal to the LIFETIME

OPTIMAL_CONDITIONS = {
    "light_intensity": [10000, 11000, 11500, 12000, 12500],  # µmol/m²/s, increasing as plant matures
    "light_duration": [5, 6, 7, 8, 9],                       # hours per day, increasing
    "DLI": [8.0, 9.0, 9.5, 10.0, 10.5],                      # mol/m²/day, increasing slightly
    "temperature": [32, 30, 28, 27, 26],                     # °C, cooling as plant grows
    "RH": [75, 70, 65, 60, 55],                              # %, decreasing humidity gradually
    "PH": [6.7, 6.5, 6.4, 6.3, 6.2],                         # slightly acidic trend
    "EC": [4.3, 4.1, 3.9, 3.8, 3.7],                         # mS/cm, decreasing as plant grows
    "water_duration": [120, 110, 100, 90, 80],               # minutes per cycle, less watering later
    "water_cycles": [5, 4, 4, 3, 3]                          # cycles per day, slight decrease
}

# Growth parameters
GROWTH_SIGMAS = {
    "DLI": [1.2, 1.0, 0.8, 0.7, 0.6],            # decreasing variability as plant stabilizes
    "temperature": [1.6, 1.4, 1.2, 1.0, 0.8],    
    "RH": [4.5, 4.0, 3.5, 3.0, 2.5],              
    "PH": [0.5, 0.4, 0.3, 0.3, 0.2],             
    "EC": [0.7, 0.6, 0.5, 0.4, 0.4],              
    "water_duration": [8, 7, 6, 5, 5], 
    "water_cycles": [0.2, 0.15, 0.1, 0.1, 0.05]      
}

K = 100      # Parameter to tune the growth curve  (peak day)
A = 50      # Parameter to tune the growth curve  (controls the spread)

# Damage parameters
DAMAGE_SENSITIVITY = 0.1

LOW_PARAMETERS = {
    "light_intensity": [
        [5000, 0, 6],                                   #[Critical low, minimum, sigma]  
        [4000, 100, 5],
        [3000, 200, 4],
        [2000, 300, 3],
        [1000, 400, 2]
    ],
    "light_duration": [
        [5000, 0, 6],
        [4500, 50, 5],
        [4000, 100, 4],
        [3500, 150, 3],
        [3000, 200, 2]
    ],
    "temperature": [
        [5000, 0, 6],
        [4800, 20, 5],
        [4600, 40, 4],
        [4400, 60, 3],
        [4200, 80, 2]
    ],
    "RH": [
        [5000, 0, 6],
        [4700, 30, 5],
        [4400, 60, 4],
        [4100, 90, 3],
        [3800, 120, 2]
    ],
    "PH": [
        [5000, 0, 6],
        [4900, 10, 5],
        [4800, 20, 4],
        [4700, 30, 3],
        [4600, 40, 2]
    ],
    "EC": [
        [5000, 0, 6],
        [4800, 20, 5],
        [4600, 40, 4],
        [4400, 60, 3],
        [4200, 80, 2]
    ],
    # TWD(total water duration) represents the total time that the plant is emerged in water in
    "TWD": [
        [5000, 0, 6],
        [4700, 30, 5],
        [4400, 60, 4],
        [4100, 90, 3],
        [3800, 120, 2]
    ],
}

HIGH_PARAMETERS = {
    "light_intensity": [
        [7000, 12000, 6],                                    #[Critical high, maximum, sigma]
        [7200, 12500, 5],
        [7400, 13000, 4],
        [7600, 13500, 3],
        [7800, 14000, 2]
    ],
    "light_duration": [
        [6000, 11000, 6],
        [6200, 11500, 5],
        [6400, 12000, 4],
        [6600, 12500, 3],
        [6800, 13000, 2]
    ],
    "temperature": [
        [7000, 12000, 6],
        [6800, 11800, 5],
        [6600, 11600, 4],
        [6400, 11400, 3],
        [6200, 11200, 2]
    ],
    "RH": [
        [7000, 12000, 6],
        [6900, 11900, 5],
        [6800, 11800, 4],
        [6700, 11700, 3],
        [6600, 11600, 2]
    ],
    "PH": [
        [7000, 12000, 6],
        [7100, 12100, 5],
        [7200, 12200, 4],
        [7300, 12300, 3],
        [7400, 12400, 2]
    ],
    "EC": [
        [7000, 12000, 6],
        [6800, 11800, 5],
        [6600, 11600, 4],
        [6400, 11400, 3],
        [6200, 11200, 2]
    ],
    "TWD": [
        [7000, 12000, 6],
        [6900, 11900, 5],
        [6800, 11800, 4],
        [6700, 11700, 3],
        [6600, 11600, 2]
    ],
}