from time import sleep
from pynput import keyboard

class Ticker:
    def __init__(self, fps: int = 30, keypress_control: bool = False):
        self._fps = fps
        self._delay = 0
        self._playing = False
        self._keypress_control = keypress_control
        self._observer_functions = []

        self.__update_delay()

    def start(self):
        if not self._keypress_control:
            self.__start()
            return

        #  def on_press(key):
        #     # try:
        #     #     print('alphanumeric key {0} pressed'.format(
        #     #         key.char))
        #     # except AttributeError:
        #     #     print('special key {0} pressed'.format(
        #     #         key))
        #     pass
    
        def on_release(key):
            # print('{0} released'.format(
            #     key))
            if key == keyboard.Key.space:
                # Stop listener
                if self.playing:
                    self.stop()
                else:
                    self.start()
            
            if key == keyboard.Key.esc:
                # Stop listener
                self.stop()
                return False
            
        with keyboard.Listener(
                    # on_press=on_press,
                    on_release=on_release
                    ) as listener:
        
                self.__start()
                listener.join()

    def __start(self):
        if self._playing:
            return

        self._playing = True
        while True:
            for observer_func in self._observer_functions:
                observer_func()
            sleep(self._delay)

            if not self._playing:
                break

    def stop(self):
        if not self._playing:
            return

        self._playing = False

    def register_observer_func(self, observer_func):
        if callable(observer_func) and not observer_func in self._observer_functions:
            
            self._observer_functions.append(observer_func)

    def unregister_observer_func(self, observer_func):
        if callable(observer_func) and observer_func in self._observer_functions:
            self._observer_functions.remove(observer_func)

    def clear_observers(self):
        self._observer_functions.clear()

    @property
    def playing(self) -> int:
        return self._playing

    @property
    def fps(self) -> int:
        return self._fps
    
    @fps.setter
    def fps(self, value: int):
        self._fps = value
        self.__update_delay()

    def __update_delay(self):
        self._delay = 1 / self._fps


