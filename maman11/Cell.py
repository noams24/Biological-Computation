from random import randint

SEA = 'S'
LAND = 'L'
GLACIER = 'G'
FOREST = 'F'
CITY = 'C'

cell_properties = {
    SEA: ('cyan', 15),
    LAND: ('yellow', 40),
    GLACIER: ('white', -15),
    FOREST: ('forestgreen', 10),
    CITY: ('darkgrey', 20)
}

wind_direction = {
    0: "↑",  # NORTH
    1: "↓",  # SOUTH
    2: "→",  # EAST
    3: "←",  # WEST
    4: ''  # NO WIND
}

MAX_TEMPERATURE = 70
MAX_AIR_POLLUTION = 100
MAX_CLOUDINESS = 100



ALL_TEMP_STATS = []
ALL_AIR_POLLUTION_STATS = []

AVG_TEMP_STATS = []
AVG_AIR_POLLUTION_STATS = []

'''
Cell: object of cell. 
      contains 6 attributes:  type, color, wind direction, cloudiness, air pollution, temperature
'''

class Cell():
    def __init__(self, cell_type, starting_air_pollution, air_pollution_factor):
        self.type = cell_type  # land, sea, glacier, forest, city
        self.color = cell_properties[cell_type][0]
        self.wind_direction = wind_direction[randint(0, 4)]  # choose between 4 directions
        self.cloudiness = randint(0, 100)  # from 0 to 100%, when it's 100% - will rain
        self.air_pollution = 0
        self.air_pollution = starting_air_pollution
        self.temperature = cell_properties[cell_type][1]

        ALL_TEMP_STATS.append(self.temperature)
        ALL_AIR_POLLUTION_STATS.append(self.air_pollution)
        self.air_pollution_factor = air_pollution_factor

    '''
    update_values: updates the cell attributes, according to my algorithm
        Input
            > 'neighbors': list that contains 4 objects of cell
    '''

    def update_values(self, neighbors):
        self.update_type()
        self.values_changes_with_wind(neighbors, self.air_pollution_factor)
        self.update_cloudiness()
        self.update_air_pollution()
        self.update_temperature()
        self.update_wind()

        ALL_TEMP_STATS.append(self.temperature)
        ALL_AIR_POLLUTION_STATS.append(self.air_pollution)

    '''
    update_type: updates the attribute 'type' according to the current type and temperature of cell
    '''

    def update_type(self):
        if self.type == 'G' and self.temperature > 0:  # high temperature evaporates the glacier
            self.type = 'S'
            self.color = 'cyan'

        elif self.type == 'S' and self.temperature < 0:  # low temperature freezes the sea
            self.type = 'G'
            self.color = 'white'

        elif self.type == 'F' and self.temperature > 30:  # high temperature change's forest into land
            self.type = 'L'
            self.color = 'yellow'

        elif self.type == 'L' and self.temperature < 30:  # low temperature change's land into forest
            self.type = 'F'
            self.color = 'forestgreen'

    '''
    values_changes_with_wind: update the cell attribute of cloudiness and air pollution.
                              the values calculated according to the neighbors cells.
        Input
            > 'neighbors': list of 4 objects of cell
            > 'air_pollution_factor' - parameter that determines the spread speed of air pollution
    '''

    def values_changes_with_wind(self, neighbors, air_pollution_factor):
        tmp = self.air_pollution
        if neighbors[0].wind_direction == '←':
            self.cloudiness += neighbors[0].cloudiness / 2
            self.air_pollution += neighbors[0].air_pollution * air_pollution_factor

        if neighbors[1].wind_direction == '→':
            self.cloudiness += neighbors[1].cloudiness / 2
            self.air_pollution += neighbors[1].air_pollution * air_pollution_factor

        if neighbors[2].wind_direction == '↓':
            self.cloudiness += neighbors[2].cloudiness / 2
            self.air_pollution += neighbors[2].air_pollution * air_pollution_factor

        if neighbors[3].wind_direction == '↑':
            self.cloudiness += neighbors[3].cloudiness / 2
            self.air_pollution += neighbors[3].air_pollution * air_pollution_factor

        if self.type == 'C':
            self.air_pollution = tmp  # the city is not infected by the neighbors

    '''
    update_cloudiness: updates the attribute 'cloudiness' if the cell is sea.
    '''

    def update_cloudiness(self):
        if self.type == 'S':
            rand = randint(0, 1)  # 50% to add cloudiness
            if rand:
                self.cloudiness += 0.5

    '''
    update_air_pollution: updates the attribute 'pollution' according to algorithm
    '''

    def update_air_pollution(self):
        if (self.type == 'F') and self.air_pollution > 2:
            self.air_pollution -= 1

        elif self.type == 'C':
            self.air_pollution += 2

        if self.cloudiness >= MAX_CLOUDINESS :  # raining
            self.cloudiness = 0
            self.air_pollution = 0.3 * self.air_pollution
            self.temperature -= 1

        if self.air_pollution > MAX_AIR_POLLUTION:
            self.air_pollution = MAX_AIR_POLLUTION

    '''
    update_temperature: updates the attribute 'temperature' according to algorithm
    '''
    def update_temperature(self):

        if self.air_pollution > 30:
            self.temperature += 1
        else:
            if self.temperature < cell_properties[self.type][1]:
                self.temperature += 0.25
            else:
                self.temperature -= 0.25

        if self.temperature > MAX_TEMPERATURE:
            self.temperature = MAX_TEMPERATURE

    '''
    update_wind: updates the attribute 'wind_direction' 
    '''
    def update_wind(self):
        rand = randint(0, 2)
        if rand == 0: # 33% to change wind direction
            self.wind_direction = wind_direction[randint(0, 4)]
