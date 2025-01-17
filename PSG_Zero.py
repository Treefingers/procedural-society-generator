# PSG Zero
# Procedurally Generated Society, Barebones Variant
# by Christopher Fryer
# 

# =============================================================
# Imported Libraries

import numpy    # for normal distribution
import random   # for other randoms


# =============================================================
# Variables

koppen_types = {
    "Af":   "tropical rainforest",
    "Am":   "tropical monsoon", 
    "Aw":   "tropical savanna (dry winter)", 
    "As":   "tropical savanna (dry summer)",
    "BWh":  "desert (dry and hot)", 
    "BWk":  "desert (dry and cold)", 
    "BSh":  "steppe (dry and hot)",
    "BSk":  "steppe (dry and cold)", 
    "Csa":  "temperate (dry, hot summer)", 
    "Csb":  "temperate (dry, warm summer)", 
    "Csc":  "temperate (dry, cold summer)", 
    "Cwa":  "temperate (dry winter, hot summer)", 
    "Cwb":  "temperate (dry winter, warm summer)", 
    "Cwc":  "temperate (dry winter, cold summer)", 
    "Cfa":  "temperate (hot summer, no dry season)", 
    "Cfb":  "temperate (warm summer, no dry season)", 
    "Csc":  "temperate (cold summer, no dry season)",
    "Dsa":  "continental (dry, hot summer)",  
    "Dsb":  "continental (dry, warm summer)",
    "Dsc":  "continental (dry, cold summer)",
    "Dsd":  "continental (dry summer, very cold winter)", 
    "Dwa":  "continental (dry winter, hot summer)", 
    "Dwb":  "continental (dry winter, warm summer)", 
    "Dwc":  "continental (dry winter, cold summer)", 
    "Dwd":  "continental (dry, very cold winter)", 
    "Dfa":  "continental (no dry season, hot summer)", 
    "Dfb":  "continental (no dry season, warm summer)", 
    "Dfc":  "continental (no dry season, cold summer)",
    "Dfd":  "continental (no dry season, very cold winter)", 
    "ET":   "tundra", 
    "EF":   "frozen", # "ice cap" in koppen; changed here to avoid a/an switching
    }


# =============================================================
# Function Defenitions

def rand():
    rng = numpy.random.default_rng()
    generated = rng.random()
    return 2 * generated - 1


def norm(standev, *args): # TODO: currently, nothing uses this
# Use instead of rand() when you want the new generated value to be
# influenced by already set values. args are one or more values of 
# generated characteristics. Standev values around 0.5 are a 
# reasonable starting point.
    mean = numpy.mean(args)
    result = numpy.random.normal(mean, standev)
    while(result < -1 or result > 1):
        result = numpy.random.normal(mean, standev)
    return result


def rand_koppen():
    return random.choice(koppen_types)


def dicprint(dictionary):
    # sort characteristics by decreasing absolute value
    # i.e. from most to least extreme.
    dictionary = dict(sorted(dictionary.items(), key=lambda item: abs(item[1]), reverse=True))
    output = ""
    for key in dictionary:
        value = dictionary[key]
        pre = 10 + int(value * 10)
        post = 10 - int(value * 10)
        output += "{:<16}{:+.3f}  {}|{}\n".format(key, value, "-" * pre, "-" * post)
    return output


def assess_chars(chars):
    chars = dict(sorted(chars.items(), key=lambda item: item[1], reverse=True))
    for key in chars:
        value = chars[key]
        if value >= 0.9:
            print("  -", key, "is extremely high.")
        elif value >= 0.8:
            print("  -", key, "is unusually high.")
        elif value > 0.5:
            print("  -", key, "is notably high.")
        elif value <= -0.9:
            print("  -", key, "is extremely low.")
        elif value <= -0.8:
            print("  -", key, "is unusually low.")
        elif value < -0.5:
            print("  -", key, "is notably low.")
    return


# =============================================================
# Classes

class Species:
    def __init__(self):
        self.chars = {
            'fecundity': rand(),
            'strength': rand(),
            'lifespan': rand(),
            'hardiness': rand(),
            'polymorphism': rand(),
            'sociality': rand(),
            'beligerence': rand(),
            'migratoriness': rand(),
            'familialness': rand(),
            'territoriality': rand(),
            }
        self.home_climate = random.choice(list(koppen_types.keys()))
        self.migrate_climate = random.choice(list(koppen_types.keys()))
        while(self.migrate_climate == self.home_climate):
        # ensures migration climate is not the same as the home climate
            self.migrate_climate = random.choice(list(koppen_types.keys()))

    def __str__(self):
        return dicprint(self.chars)


class Culture:
    def __init__(self, species):
        self.species = species
        self.chars = {
            'memorialism': norm(0.5, self.species.chars['lifespan'], self.species.chars['sociality']),
            'introspection': rand(),
            'stratification': rand(),
            'traditionalism': rand(),
            'asceticism': rand(),
            'spiritualism': rand(),
            'nomadism': rand(),
            'generosity': rand(),
            'individualism': rand(),
            'wastefulness': rand(),
            }

    def __str__(self):
        return dicprint(self.chars)


class Politic:
    def __init__(self, culture):
        self.culture = culture
        self.chars = {
            'hierarchy': rand(),
            'formality': rand(),
            'xenophobia': rand(),
            'egalitarianism': rand(),
            'tolerance': rand(),
            'militarism': rand(),
            }

    def __str__(self):
        return dicprint(self.chars)


class Society:
    def __init__(self):
        self.species = Species()
        self.culture = Culture(self.species)
        self.politic = Politic(self.culture)

    def __str__(self):
        return "{}\n{}\n{}".format(self.species, self.culture, self.politic)

    def print_assessment(self):
        print("\nAssessment:")
        print("\nAs a species, they are adapted to a\n" + koppen_types[self.species.home_climate] + " climate.")
        print("\nIf they migrate, it is to a\n" + koppen_types[self.species.migrate_climate] + " climate.")
        print("\nCompared to other species,")
        assess_chars(self.species.chars)
        print("\nCompared to other cultures,")
        assess_chars(self.culture.chars)
        print("\nCompared to other polities,")
        assess_chars(self.politic.chars)
        print("")
        return
        

# =============================================================
# Main

society = Society()
print(society)
society.print_assessment()

input("Press <Enter> to exit . . .")