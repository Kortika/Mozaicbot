import sys, json, math, random

def move(commands):
    record = { 'moves': commands }
    print(json.dumps(record))
    sys.stdout.flush()

def euclideanDist(x1, y1, x2, y2):
    return math.sqrt( math.pow(x1-x2, 2) + math.pow(y1-y2,2))

def movablePlanets(my_planets, lower_limit):
    return [p for p in my_planets if p['ship_count'] >= lower_limit]
    
def getClosestPlanets(my_planet, other_planets, k): 
    x2 = my_planet['x']
    y2 = my_planet['y']
    distances =  []
    targets = []
    for i in range(len(other_planets)): 
        dest_planet = other_planets[i] 
        x1 = dest_planet['x']  
        y1 = dest_planet['y']
        distances.append([euclideanDist(x1,y1,x2,y2), i])
    distances = sorted(distances)
    
    for i in range(k): 
        index = distances[i][1]
        targets.append(other_planets[index])
    
    return targets

def getCommand(source, dest, count):
    return {
            'origin': source['name'],
            'destination': dest['name'],
            'ship_count': count
        }

lower_limit = 10
for line in sys.stdin:
    state = json.loads(line)
    # find planet with most ships
    my_planets = [p for p in state['planets'] if p['owner'] == 1]
    other_planets = [p for p in state['planets'] if p['owner'] != 1]
    attacking_planets = movablePlanets(my_planets, lower_limit)
    
    if not my_planets or not other_planets or not attacking_planets:
        move(None)
    else:
        commands = []

        k = len(attacking_planets)

        if len(attacking_planets) > len(other_planets):
            k = len(other_planets)

        attack_point = random.choice(attacking_planets)
        destinations = getClosestPlanets(attack_point, other_planets, k)
        commands.append(getCommand(attack_point,destinations[0],attack_point['ship_count']))
        attack_point['ship_count'] = 0 
        attacking_planets =  movablePlanets(attacking_planets, lower_limit)
        index = 0 
        for dest in  destinations[1:]:
            attkr =  attacking_planets[index]
            index += 1
            commands.append(getCommand(attkr, dest, attkr['ship_count']))
        move(commands)
        