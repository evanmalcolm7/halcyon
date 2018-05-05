from tags import add_tags
from task import Task

class Creature():
    '''Base class for all creatures.
    Contains statistics, tag information, and position.
    Also handles adding the creature to the occupants of its octant.'''
    def __init__(self, name, on_planet, in_octant, health=5, move=0, player=0):
        self.tags = {'Material' : [], 'Structure' : [], 'Function' : []}
        self.name = name
        self.health = health
        self.move = move
        self.player = player
        self.planet = on_planet
        self.octant = in_octant
        #Add the creature to the contents of the octant
        self.octant.add_occupant(self)

    def __str__(self):
        return 'a Creature named %s' % self.name

class Laborer(Creature):

    def __init__(self, name, on_planet, in_octant, harvest_rate=0, build_rate=0):
        super().__init__(name, on_planet, in_octant, move=1/5, health=5)
        self.harvest_rate = harvest_rate
        self.build_rate = build_rate

    def __str__(self):
        return 'a Laborer named %s' % self.name

    def harvest_resource(self, resource):
        '''starts a Task() of harvesting the given resource if the resource is in the same octant'''
        #check if the resource is in the same octant
        if resource in self.octant.resources:
            #calculate the number of hours needed to finish the Task
            hours = (1/self.harvest_rate)
            #start the Task object with the given number of hours
            #at the end of the hours, will call gain_resource(on self)
            harvest_task = Task(self, hours, self.player.gain_resource(resource))
            return '%s is now harvesting %s' % (self.name, resource)
        return 'there is no %s in %s' % (resource, self.octant)

    def construct_building(self, building_plan):
        if building_plan in self.octant.contents:
            print('%s is now building %s' % (self.name, building_plan))
        print('there is no unfinished %s in %s' % (building_plan, self.octant))


class CrewMember(Laborer):

    def __init__(self, name, on_planet, in_octant):
        super().__init__(name, on_planet, in_octant, harvest_rate=1/12)
        #add the Flesh material to the material tags
        add_tags(self, 'Flesh')

class Engineer(CrewMember):

    def __init__(self, name, on_planet, in_octant):
        super().__init__(name, on_planet, in_octant)

    def make_building_plan(self):
        return self.octant

class Soldier(CrewMember):

    def __init__(self, name, on_planet, in_octant):
        super().__init__(name, on_planet, in_octant)

class Researcher(CrewMember):

    def __init__(self, name, on_planet, in_octant):
        super().__init__(name, on_planet, in_octant)

class Artist(CrewMember):

    def __init__(self, name, on_planet, in_octant):
        super().__init__(name, on_planet, in_octant)

class Automaton(Laborer):

    def __init__(self, name, on_planet, in_octant):
        super().__init__(name, on_planet, in_octant, harvest_rate=1/6, build_rate=1/3)
        self.tags['Material'].append('Metal')
