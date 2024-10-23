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
        use_interval=False,
        interval_duration=7,
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

        self.use_interval = use_interval
        self.interval_duration = interval_duration
        self.is_animating = True
        self.animation_event = None
        self.interval_event = None

        self.start_animation()

        if on_click:
            self.bind(on_press=on_click)

    def start_animation(self):
        if self.use_interval:
            self.start_interval_animation(0)  # Pass initial dt=0
        else:
            self.animation_event = Clock.schedule_interval(
                self.update_image, 1 / self.fps
            )

    def start_interval_animation(self, dt):
        self.is_animating = True
        self.current_image = 0  # Reset to first frame
        self.direction = 1  # Reset direction if using loop_reverse
        self.animation_event = Clock.schedule_interval(self.update_image, 1 / self.fps)

    def pause_animation(self, dt):
        if self.animation_event:
            self.animation_event.cancel()
        self.is_animating = False
        self.current_image = 31
        self.img.source = self.images[self.current_image]
        self.img.reload()
        # Schedule next animation cycle
        Clock.schedule_once(self.start_interval_animation, self.interval_duration)

    def update_image(self, dt):
        if not self.is_animating:
            return

        if self.loop_reverse:
            self.current_image += self.direction
            if self.current_image >= self.frame_count - 1 or self.current_image <= 0:
                self.direction *= -1
                if self.use_interval and self.current_image <= 0:
                    self.pause_animation(0)
                    return
        else:
            self.current_image = (self.current_image + 1) % len(self.images)
            if self.use_interval and self.current_image == 0:
                self.pause_animation(0)
                return

        self.img.source = self.images[self.current_image]
        self.img.reload()

    def update_animation(self, new_base_path, new_frame_count):
        self.base_path = new_base_path
        self.frame_count = new_frame_count
        self.images = [f"{self.base_path}{i}.png" for i in range(self.frame_count)]
        self.current_image = 0
        self.img.source = self.images[self.current_image]

    def on_remove(self):
        if self.animation_event:
            self.animation_event.cancel()
        if self.interval_event:
            self.interval_event.cancel()
