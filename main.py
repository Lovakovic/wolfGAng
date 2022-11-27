import time
import threading

from composer_util import Melody
from composer import Composer
from improvements import play

Note = str
Melody = Melody


def main(melody: str = '', number_of_threads: int = 1):

    if len(melody) == 0:
        print('Please enter the melody:')
        melody = Melody(input().split())

    else:
        melody = melody.split()

    # Enables multithreading for faster measuring of statistics
    def parallel_main(melody: str, instance_no: int):
        composer = Composer(melody)

        start_time = time.time()

        # Do the thing
        solution, generation_count = composer.compose(5000)

        end_time = time.time()

        print(f"Instance No. {instance_no} finished in {round(end_time - start_time, 2)} seconds "
              f"and {generation_count} generations.")

    if number_of_threads == 1:
        composer = Composer(melody)

        start_time = time.time()

        # Do the thing
        solution, generation_count = composer.compose(5000)

        end_time = time.time()

        print(f'Solution found in {generation_count} generations.')
        print(f'Printing solution: {solution}')
        print(f'Took {round(end_time - start_time, 2)} s to compose this masterpiece!')
        time.sleep(1.5)

        print('Playing solution...')
        play(str(solution))

    else:
        threads = []

        for i in range(number_of_threads):
            threads.append(threading.Thread(name=f'thread {i}', target=parallel_main, args=(melody.copy(), i)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    return 0


mary = "E D C D E E E D D D E G G E D C D E E E E D D E D C"
fur_elise = "E5:.15 D5#:.15 E5:.15 D5#:.15 E5:.15 B4:.15 D5:.15 C5:.15 A4:.15 E3:.15 A3:.15 C4:.15 E4:.15 A4:.15 B4:.15 E3:.15 G3#:.15 E4:.15 G4#:.15 B4:.15 C5:.15 E3:.15 A3:.15 E4:.15 E5:.15 D5#:.15 E5:.15 D5#:.15 E5:.15 B4:.15 D5:.15 C5:.15 A4:.15 E3:.15 A3:.15 C4:.15 E4:.15 A4:.15 B4:.15 E3:.15 G3#:.15 D4:.15 C5:.15 B4:.15 A4:.15 E3:.15 A3:.15 B4:.15 C5:.15 D5:.15 E5:.15 G3:.15 C4:.15 G4:.15 F5:.15 E5:.15 D5:.15 G3:.15 B3:.15 F4:.15 E5:.15 D5:.15 C5:.15 E3:.15 A3:.15 E4:.15 D5:.15 C5:.15 B4:.15 E3:.15 E4:.15 E4:.15 E5:.15 E4:.15 E5:.15 E5:.15 E6:.15 D5#:.15 E5:.15 D5#:.15 E5:.15 D5#:.15 E5:.15 D5#:.15 E5:.15 D5#:.15 E5:.15 D5#:.15 E5:.15 B4:.15 D5:.15 C5:.15 A4:.15 E3:.15 A3:.15 C4:.15 E4:.15 A4:.15 B4:.15 E3:.15 G3#:.15 D4:.15 C5:.15 B4:.15 A4:.15 E3:.15 A3:.15 B4:.15 C5:.15 D5:.15 E5:.15 G3:.15 C4:.15 G4:.15 F5:.15 E5:.15 D5:.15 G3:.15 B3:.15 F4:.15 E5:.15 D5:.15 C5:.15 E3:.15 A3:.15 E4:.15 D5:.15 C5:.15 B4:.15 E3:.15 E4:.15 E4:.15 E5:.15 E4:.15 E5:.15 E5:.15 E6:.15 D5#:.15 E5:.15 D5#:.15 E5:.15 D5#:.15 E5:.15 D5#:.15 E5:.15 D5#:.15 E5:.15 D5#:.15 E5:.15 B4:.15 D5:.15 C5:.15 A4:.15 E3:.15 A3:.15 C4:.15 E4:.15 A4:.15 B4:.15 E3:.15 G3#:.15 D4:.15 C5:.15 B4:.15 A4:1.2"
tetris = "E5:.4 B4:.2 C5:.2 D5:.4 C5:.2 B4:.2 A4:.4 A4:.2 C5:.2 E5:.4 D5:.2 C5:.2 B4:.4 B4:.2 C5:.2 D5:.4 E5:.4 C5:.4 A4:.4 A4:.4 pause:.4 pause:.2 D5:.4 F5:.2 A5:.4 G5:.2 F5:.2 E5:.6 C5:.2 E5:.4 D5:.2 C5:.2 B4:.4 B4:.2 C5:.2 D5:.4 E5:.4 C5:.4 A4:.4 A4:.4 pause:.4 E4:.8 C4:.8 D4:.8 B3:.8 C4:.8 A3:.8 G3#:.8 B3:.8 E4:.8 C4:.8 D4:.8 B3:.8 C4:.4 E4:.4 A4:.4 A4:.4 G4#:1.6 E5:.4 B4:.2 C5:.2 D5:.4 C5:.2 B4:.2 A4:.4 A4:.2 C5:.2 E5:.4 D5:.2 C5:.2 B4:.4 B4:.2 C5:.2 D5:.4 E5:.4 C5:.4 A4:.4 A4:.4 pause:.4 pause:.2 D5:.4 F5:.2 A5:.4 G5:.2 F5:.2 E5:.6 C5:.2 E5:.4 D5:.2 C5:.2 B4:.4 B4:.2 C5:.2 D5:.4 E5:.4 C5:.4 A4:.4 A4:.4 pause:.4"
mii_tune =  "F4#:.5 A4:.25 C5#:.25 pause:.25 A4:.25 pause:.25 F4#:.25  D4:.25 D4:.25 D4:.25 pause:1 C4#:.25 D4:.25 F4#:.25 A4:.25 C5#:.25 pause:.25 A4:.25 pause:.25 F4#:.25 E5:.75 E5b:.25 D5:.5 pause:.5 G4#:.5 C5#:.25 F4#:.25 pause:.25 C5#:.25 G4#:.25 pause:.25 C5#:.25 pause:.25 G4:.25 F4#:.25 pause:.25 E4:.25 pause:.25 E4:.25 E4:.25 E4:.25 pause:.75 E4:.25 E4:.25 E4:.25 pause:.75 D4#:.5 D4:.5 C4#:.5 A4:.25 C5#:.25 pause:.25 A4:.25 pause:.25 F4#:.25 E4:.25 E4:.25 E4:.25 pause:.25 E5:.25 E5:.25 E5:.25 pause:.5 F4#:.25 A4:.25 C5#:.25 pause:.25 A4:.25 pause:.25 F4#:.25 C5#:1 B4:.5 pause:.5 B4:.25 G4:.25 D4:.25 C4#:.5 B4:.25 G4:.25 C4#:.25 A4:.25 F4#:.25 C4:.25 B3:.5 F4:.25 D4:.25 B3:.25 E4:.25 E4:.25 E4:.25 pause:1 A4#:.25 B4:.25 C5#:.25 D5:.25 F5#:.25 A5:.25 pause:1.5 A3:.5 A3#:.5 B3:.75 A3#:.25 B3:1.5 A3:.25 A3#:.25 B3:.25 F4#:.5 C4#:.25 B3:.75 A3#:.25 B3:2 B3:.5 B3#:.5 C4#:.75 B3#:.25 C4#:1.5 C4#:.25 B3#:.25 C4#:.25 G4#:.5 D4#:.25 C4#:.75 D4#:.25 B3:.75 C4#:.25 D4:.25 F4#:.5 D4:.25 G4#:.25 G4#:.25 G4#:.25 pause:.25"

main(mary)