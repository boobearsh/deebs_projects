# Pokédex Project from Codédex📟

# Class definition
class Pokemon:
    def __init__(self, entry, name, types, description, is_caught):
        self.entry = entry
        self.name = name
        self.types = types
        self.description = description
        self.is_caught = is_caught

    def speak(self):
        print(self.name + ', ' + self.name + '!')

    def display_details(self):
        print('Entry Number: ' + str(self.entry))
        print('Name: ' + self.name)

        if len(self.types) == 1:
            print('Type: ' + self.types[0])
        else:
            print('Type: ' + self.types[0] + '/' + self.types[1])

        print('Description: ' + self.description)

        if self.is_caught:
            print(self.name + ' has already been caught!')
        else:
            print(self.name + ' hasn\'t been caught yet.')


# Pokémon objects
pikachu = Pokemon(
    25,
    'Pikachu',
    ['Electric'],
    'It is a yellow rat',
    True)
charizard = Pokemon(
    6,
    'Charizard',
    ['Fire', 'Flying'],
    'It is a flying red rat',
    False)
gyarados = Pokemon(
    130,
    'Gyarados',
    ['Water', 'Flying'],
    'It is a giant blue sea worm',
    False)

pikachu.speak()
charizard.speak()
gyarados.speak()
