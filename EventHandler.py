import pygame
import pygame_gui
import logging


class EventHandler(object):
    __soundboard = None
    __keyboard_map = dict()

    __multiply_modifier = False
    __profile_modifier = False
    __pressed_stop = False

    def __init__(self, soundboard, keyboard_map: dict):
        self.__keyboard_map = keyboard_map
        self.__soundboard = soundboard

    def handle(self, event_list: list):
        """
        Handles the event contained in the passed event list
        """
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                self.__handle_key_down_event(event)
            elif event.type == pygame.KEYUP:
                self.__handle_key_up_event(event)
            elif event.type == pygame.QUIT:
                self.__soundboard.close()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    self.__handle_button_click_event(event)

    def __handle_button_click_event(self, event):
        """
        Handles the events of type button click
        """
        logging.debug(f"Button clicked: {event.ui_element.text}")
        # Check if the clicked button is a profile button
        if event.ui_element in self.__soundboard.get_profile_buttons():
            # If it is, switch to the corresponding profile
            self.__soundboard.use_profile(
                self.__soundboard.get_profile_buttons()[event.ui_element]
            )
        else:
            # If it's not a profile button, play the corresponding sound
            self.__soundboard.play(event.ui_element.text, loop=False)

    def __handle_key_down_event(self, event):
        """
        Handles the events of type keydown
        """
        if event.key == pygame.K_ESCAPE:
            self.__soundboard.close()
        elif event.key == pygame.K_2:
            self.__profile_modifier = True
        elif event.key == pygame.K_3:
            self.__multiply_modifier = True
        elif event.key == pygame.K_SPACE:
            self.__pressed_stop = True

        if event.key in self.__keyboard_map and not self.__profile_modifier:
            sound_key = self.__keyboard_map[event.key]
            for button, key in self.__soundboard.get_buttons().items():
                if key == sound_key:
                    button.select()
            if self.__multiply_modifier:
                self.__soundboard.play(self.__keyboard_map[event.key], loop=True)
            else:
                self.__soundboard.play(self.__keyboard_map[event.key], loop=False)

        if self.__pressed_stop:
            self.__soundboard.stop_all_sounds()

    def __handle_key_up_event(self, event):
        """
        Handles the events of type keyup
        """
        if event.key in self.__keyboard_map:
            sound_key = self.__keyboard_map[event.key]
            for button, key in self.__soundboard.get_buttons().items():
                if key == sound_key:
                    button.unselect()

        if self.__profile_modifier and event.key in self.__keyboard_map:
            self.__soundboard.use_profile(self.__keyboard_map[event.key])

        if event.key == pygame.K_SPACE:
            self.__pressed_stop = False
        elif event.key == pygame.K_3:
            self.__multiply_modifier = False
        elif event.key == pygame.K_2:
            self.__profile_modifier = False
