from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.core.window import Window

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            speedup = 1.1
            offset  = 0.02 * Vector(0, ball.center_y-self.center_)
            ball.velocity = speedup * (offset - ball.velocity)


class PongGame(Widget):
    ball=ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[0] == 273:
            self.player1Dir = 0
        elif keycode[0] == 274:
            self.player1Dir = 0;

        if keycode[0] == 114:
            self.player2Dir = 0
        elif keycode[0] == 102:
            self.player2Dir = 0;


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # 273 up
        # 274 down
        # 275 right
        # 276 left
        # 308 ALT
        # 306 CTRL

        # 114 r
        # 102 f
        # 103 g
        # 100 d
        #  97 a
        # 115 s

        if keycode[0] == 273:
            self.player1Dir = 1
        elif keycode[0] == 274:
            self.player1Dir = -1;

        if keycode[0] == 114:
            self.player2Dir = 1
        elif keycode[0] == 102:
            self.player2Dir = -1


        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None


    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0,360))

    def update(self, dt):
       self.ball.move()
       if(self.ball.y < 0) or (self.ball.top > self.height):
           self.ball.velocity_y *= -1

       if(self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1

            
class PongApp(App):
    def build(self):
       game = PongGame()
       game.serve_ball()
       Clock.schedule_interval(game.update, 1.0/60.0)
       return game

class PongBall(Widget):

    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    
    velocity = ReferenceListProperty(velocity_x,velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

if __name__ == '__main__':
    PongApp().run()



    