class Entity:
    def __init__(self, name):
        self.name = name
        self.health = 100

    def taunt(self):
        return f"{self.name} glares at you silently."
    
class Wizard(Entity):
    def __init__(self, name):
        super().__init__(name)
    
    def taunt(self):
        return "You shall not pass!"
    
class Robot(Entity):
    def __init__(self, name):
        super().__init__(name)

    def taunt(self):
        return "Beep Boop. Exterminate."