#!/usr/bin/env python3
import yaml
import os
import logging
import sys
import pygame
import pygame_gui
from EventHandler import EventHandler

"""
TODO keys need to be more flexible
in terms of assignment
"""


class Soundboard(object):
    __AUTO_KEYS = tuple("qweasdzxcv")
    __buttons = dict()
    __current_profile = None
    __labels = dict()
    __manager = None
    __profiles = list()
    __sounds = dict()

    def __init__(self, profiles_folder: str):
        self.__load_profiles(profiles_folder)
        self.__load_soundboard(self.__profiles)
        self.__manager = pygame_gui.UIManager(
            (800, 600)
        )  # assuming a window size of 800x600

        y = 0
        for key in self.__AUTO_KEYS:
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((0, y), (100, 50)),
                text=key,
                manager=self.__manager,
            )
            self.__buttons[button] = key
            label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((110, y), (300, 50)),
                text="filler text",
                manager=self.__manager,
            )
            self.__labels[key] = label
            y += 60  # move the next button down by 60 pixels

        if self.__current_profile is None:
            raise FileNotFoundError("The soundboard cannot work without profiles")

    def __load_profiles(self, profiles_folder: str):
        """
        Loads the profile paths into memory.
        """
        self.__profiles = [
            os.path.join(profiles_folder, x) for x in next(os.walk(profiles_folder))[1]
        ]
        if len(self.__profiles) == 0:
            logging.debug("No profiles available")

    def __load_soundboard(self, profile_list: list):
        """
        Loads all the sounds inside a 2D list:

        - C:/path/profiles/1
          - Loaded sound number 1
          - Loaded sound number 2
        - C:/path/profiles/2
          - Loaded sound number 5

        The number of the sound is the key that has to be pressed to play it.
        """
        self.__sounds = dict()
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
        pygame.init()
        pygame.display.set_mode((100, 100))

        trigger_keys = list(self.__AUTO_KEYS)

        for folder in profile_list:
            profile_key = os.path.split(folder)[1]
            directory_tree = next(os.walk(folder))
            sound_list = dict()
            key_count = 0
            for sound_file in directory_tree[2]:
                sound_key = trigger_keys[key_count]
                sound_list[sound_key] = {
                    "sound": pygame.mixer.Sound(os.path.join(folder, sound_file)),
                    "name": sound_file,
                }
                key_count += 1

            self.__sounds[profile_key] = sound_list

        # Just get the "first" element of the dict
        for key, value in self.__sounds.items():
            logging.debug("current profile key %s" % key)
            self.__current_profile = key
            break

    def update_labels(self):
        """
        Updates the labels with the names of the sounds in the current profile.
        """
        sound_names = self.get_current_profile_sounds()
        count = 0
        for key, label in self.__labels.items():
            if count < len(sound_names):
                label.set_text(sound_names[count])
                count += 1
            else:
                label.set_text("")

    def use_profile(self, profile_key: int):
        """
        Starts using the profile number passed.
        """
        if profile_key not in self.__sounds.keys():
            logging.debug("The profile number %s is not available" % profile_key)
            return

        self.__current_profile = profile_key
        self.update_labels()

        logging.debug("Using profile number %s" % profile_key)

    def play(self, sound_key: int, loop: bool):
        """
        Plays the given sound key located in the given profile.
        """
        profile = self.__current_profile
        if sound_key in self.__sounds[profile]:
            sound = self.__sounds[profile][sound_key]
            sound["sound"].stop()
            should_loop = -1 if loop else 0
            sound["sound"].play(loops=should_loop)
            logging.debug(
                "Playing sound %s in profile %s with loop = %d"
                % (sound_key, profile, should_loop)
            )
        else:
            logging.debug(
                "Either the profile number %s key or the sound key %s do not exist"
                % (profile, sound_key)
            )

    def get_manager(self):
        """
        Returns the pygame_gui manager
        """
        return self.__manager

    def get_current_profile_sounds(self):
        """
        Returns the names of the sounds in the current profile.
        """
        return [
            sound["name"] for sound in self.__sounds[self.__current_profile].values()
        ]

    def stop_all_sounds(self):
        """
        Stops all sounds
        """
        pygame.mixer.stop()

    def close(self):
        """
        Close the soundboard application
        """
        logging.debug("Closing application")
        pygame.quit()
        sys.exit(0)


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    current_dir = os.path.dirname(__file__)
    config = dict()
    config_path = os.path.join(current_dir, "config.yml")

    with open(config_path, "r") as stream:
        config = yaml.safe_load(stream)

    profiles_dir = os.path.join(current_dir, config["profiles_folder"])

    keyboard_map = {
        pygame.K_q: "q",
        pygame.K_w: "w",
        pygame.K_e: "e",
        pygame.K_a: "a",
        pygame.K_s: "s",
        pygame.K_d: "d",
        pygame.K_z: "z",
        pygame.K_x: "x",
        pygame.K_c: "c",
        pygame.K_v: "v",
    }

    soundboard = Soundboard(profiles_dir)
    event_handler = EventHandler(soundboard, keyboard_map)

    clock = pygame.time.Clock()
    is_running = True
    screen = pygame.display.set_mode((800, 600))

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            event_handler.handle([event])  # pass the event to your event handler

            # This line is needed to process pygame_gui events
            soundboard.get_manager().process_events(event)

        # This line is needed to update the pygame_gui manager
        soundboard.get_manager().update(time_delta)

        soundboard.update_labels()

        # Clear the screen before drawing
        screen.fill((0, 0, 0))

        # Draw your user interface
        soundboard.get_manager().draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

    # while True:
    #    event_handler.handle(pygame.event.get())


if __name__ == "__main__":
    main()
