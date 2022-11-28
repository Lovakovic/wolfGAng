import time

from composer_util import Melody
from composer import Composer
from improvements import play

Note = str
Melody = Melody


def main(melody: str = ''):

    if len(melody) == 0:
        print('Please enter the melody:')
        melody = Melody(input().split())

    else:
        melody = melody.split()


    composer = Composer(melody)

    start_time = time.time()

    # Do the thing
    solution, generation_count = composer.compose(10000)

    end_time = time.time()

    print(f'Solution found in {generation_count} generations.')
    print(f'Printing solution: {solution}')
    print(f'Took {round(end_time - start_time, 2)} s to compose this masterpiece!')
    time.sleep(1.5)

    print('Playing solution...')
    play(str(solution))

    return 0


melody = 'C4:.45 C4:.15 D4:.60 C4:.60 F4:.60 E4:1.2 C4:.45 C4:.15 D4:.60 C4:.60 ' \
         'G4:.60 F4:1.2 C4:.45 C4:.15 C5:.60 A4:.60 F4:.60 E4:.60 D4:1.20 B4b:.45 ' \
         'B4b:.15 A4:.60 F4:.60 G4:.60 F4:1.20'

main(melody)