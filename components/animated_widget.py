from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior


class AnimatedImage(ButtonBehavior, BoxLayout):
    def __init__(
        self,
        base_path,
        frame_count,
        fps=30,
        loop_reverse=False,
        image_size=(1, 1),
        on_click=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.base_path = base_path
        self.frame_count = frame_count
        self.fps = fps
        self.loop_reverse = loop_reverse
        self.images = [f"{self.base_path}{i}.png" for i in range(frame_count)]
        self.current_image = 0
        self.direction = 1
        self.img = Image(source=self.images[self.current_image], size_hint=image_size)
        self.add_widget(self.img)
        Clock.schedule_interval(self.update_image, 1 / self.fps)

        if on_click:
            self.bind(on_press=on_click)

    def update_image(self, dt):
        if self.loop_reverse:
            self.current_image += self.direction
            if self.current_image >= self.frame_count - 1 or self.current_image <= 0:
                self.direction *= -1
        else:
            self.current_image = (self.current_image + 1) % len(self.images)
        self.img.source = self.images[self.current_image]
        self.img.reload()

    def update_animation(self, new_base_path, new_frame_count):
        self.base_path = new_base_path
        self.frame_count = new_frame_count
        self.images = [f"{self.base_path}{i}.png" for i in range(self.frame_count)]
        self.current_image = 0
        self.img.source = self.images[self.current_image]
