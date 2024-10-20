from kivy.core.window import Window
from kivy.uix.widget import Widget


class KeyboardManager:
    def __init__(self, app):
        self.app = app
        # Create a dummy widget to handle keyboard events
        self.dummy_widget = Widget()
        self._keyboard = Window.request_keyboard(
            self._on_keyboard_closed, self.dummy_widget, "text"
        )
        if self._keyboard:
            self._keyboard.bind(on_key_down=self._on_key_down)

    def _on_keyboard_closed(self):
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_key_down)
            self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == "down":
            self.app.move_selection_down()
            return True
        elif keycode[1] == "up":
            self.app.move_selection_up()
            return True
        elif keycode[1] == "enter":
            self.app.activate_current_selection()
            return True
        return False

    def release(self):
        """Release keyboard resources"""
        if self._keyboard:
            self._keyboard.release()
