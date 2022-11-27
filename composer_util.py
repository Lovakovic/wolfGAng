import random
import jellyfish

PARAMS = {
    'notes': set({}),
    'octaves': set({}),
    'modifiers': set({}),
    'max_duration': None,
    'min_duration': None
}


class MelodyIter:
    def __init__(self, melody):
        self.sounds = melody.sounds
        self.number_of_sounds = len(melody)
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index < self.number_of_sounds:
            next_sound = self.sounds[self.current_index]
            self.current_index += 1

            return next_sound
        else:
            raise StopIteration


class Melody:
    def __init__(self, genome: list[str] = None):
        if genome is None:
            self.sounds = []
        else:
            self.sounds = genome
        self.fitness = None

    def __len__(self):
        return len(self.sounds)

    def __add__(self, other):
        if isinstance(other, Melody):
            return self.sounds + other.sounds
        else:
            raise TypeError(f'Unsupported type {type(other)}')

    def __iadd__(self, other):
        if isinstance(other, Melody):
            self.sounds += other.sounds
            return self
        else:
            raise TypeError(f'Unsupported type {type(other)}')

    def __iter__(self):
        return MelodyIter(self)

    def __repr__(self):
        return f'fitness: {self.fitness}, sounds: {self.sounds}'

    def __str__(self):
        return " ".join(self.sounds)

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self))
            return Melody([self.sounds[i] for i in range(start, stop, step)])
        elif isinstance(key, int):
            return self.sounds[key]
        elif isinstance(key, tuple):
            raise NotImplementedError('Tuple as index')
        else:
            raise TypeError(f'Invalid argument type: {type(key)}')

    def __setitem__(self, key, value):
        self.sounds[key] = value

    def calculate_fitness(self, compare_to):
        compare_to_string = ''.join(compare_to)
        melody_string = ''.join(self.sounds)

        self.fitness = jellyfish.levenshtein_distance(melody_string, compare_to_string)


def set_note_gen_params(input_melody: Melody):
    min_duration = max_duration = None

    def split_sound_notation(sound: str) -> dict:
        octave = modifier = ''

        # possible inputs: C C4 C# C4# pause
        # The easiest case
        is_pause = sound.find('pause') != -1
        if is_pause:
            return {
                'note': 'pause',
                'octave': '',
                'modifier': ''
            }

        # possible inputs: C C4 C# C4#
        # Pop the note from a string
        note = sound[0]
        sound = sound[1:]

        # possible inputs: 4 # 4#
        if len(sound) > 0:
            try:
                octave = int(sound)
                octave = str(octave)
            except ValueError:

                # possible inputs: # 4#
                if len(sound) > 1:
                    octave = sound[0]
                    modifier = sound[1]

                # possible inputs: #
                else:
                    modifier = sound[0]

        return {
            'note': note,
            'octave': octave,
            'modifier': modifier
        }

    for notation in input_melody:
        spliced = notation.split(':')

        sound_notation: dict

        # Duration is noted
        if len(spliced) > 1:
            sound_notation = split_sound_notation(spliced[0])
            duration = spliced[1]

            # Init the min_duration and max_duration variables
            if min_duration is None:
                min_duration = duration
            if max_duration is None:
                max_duration = duration

            if duration < min_duration:
                min_duration = duration
            if duration > max_duration:
                max_duration = duration

        # Duration is not noted
        else:
            sound_notation = split_sound_notation(spliced[0])

        # Add the spliced sound notations in a params dict
        PARAMS['notes'].add(sound_notation['note'])
        PARAMS['octaves'].add(sound_notation['octave']) if len(sound_notation['octave']) > 0 else None
        PARAMS['modifiers'].add(sound_notation['modifier']) if len(sound_notation['modifier']) > 0 else None

    # Switch the type of dictionary values into lists because of random.choice()
    PARAMS['notes'] = list(PARAMS['notes'])
    PARAMS['octaves'] = list(PARAMS['octaves'])
    PARAMS['modifiers'] = list(PARAMS['modifiers'])
    PARAMS['min_duration'] = round(float(min_duration), 2) if min_duration is not None else None
    PARAMS['max_duration'] = round(float(max_duration), 2) if max_duration is not None else None


def generate_random_note():
    note = random.choice(PARAMS['notes'])
    duration = ''

    octave = modifier = ''
    if note != 'pause':

        # Check if octaves are noted
        if len(PARAMS['octaves']) > 0:
            octave = random.choice(PARAMS['octaves'])

        # Check if modifiers are noted
        if len(PARAMS['modifiers']) > 0:
            modifier = random.choice(PARAMS['modifiers'])

    # Check if duration is noted
    if PARAMS['min_duration'] is None and PARAMS['max_duration'] is None:
        return note + octave + modifier

    duration = round(random.uniform(PARAMS['min_duration'], PARAMS['max_duration']), 2)

    # Removing leading zero for the fitness function to work correctly
    if duration < 1:
        duration = str(duration)[1:]

    duration = str(duration)
    return note + octave + modifier + ':' + duration
