import musicalbeeps
import threading


player = musicalbeeps.Player(volume=0.2, mute_output=True)


def play(melody=''):
    """
    Plays a given tune and allows for skipping playback
    :param melody: String of notes to be played
    :return: Nothing
    """

    if len(melody) < 1:
        print('No melody entered, aborting...')

        return 1

    # Function enabling multithreading
    def parallel_play(e, melody):

        # Melody is a list of notes
        if type(melody) == list:
            for note_with_duration in melody:
                if e.is_set():
                    break

                note, duration = decouple_representation(note_with_duration)

                player.play_note(note, duration)

        # Melody is a string
        else:
            notes_to_play = string_to_notes(melody)

            for note in notes_to_play:
                if e.is_set():
                    break

                player.play_note(note[0], note[1])

        print('Playback finished.')

    # Start a new thread for audio playback and give it an event
    event = threading.Event()
    main_thread = threading.Thread(name='audio playback',
                                   target=parallel_play, args=(event, melody))
    main_thread.start()

    print('To skip playback press ENTER')

    # Keep checking if user wants to skip
    while not event.is_set():
        if input() == '':
            print('Skipping playback.')
            event.set()

            break


def decouple_representation(single_note: str) -> tuple:
    """
    Splits sound representation from duration
    :param single_note: A string containing sound notation (eg. C4#:.4)
    :return: Tuple first element of which is sound and second is the duration (eg. (C4#, 0.4))
    """

    # If the duration is not noted, the player will use default value of 0.5 s
    duration_noted = len(single_note.split(':')) > 1

    note = single_note.split(':')[0]
    if duration_noted:
        duration = float(single_note.split(':')[1])

        return note, duration

    return note, 0.5


def string_to_notes(melody: str) -> list[tuple[str, float]]:
    """
    Splits a string of notes into a list of tuples containing notes
    :param melody: String containing all the notes
    :return: List of tuples, first tuple element represents a note,
        second element in a tuple is duration of the note in seconds
    """

    notes_with_duration = melody.split()

    # List of tuples (note, duration)
    parsed_notes = []

    for note_with_duration in notes_with_duration:
        parsed_notes.append(decouple_representation(note_with_duration))

    return parsed_notes
