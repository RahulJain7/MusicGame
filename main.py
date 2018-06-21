from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.lang import Builder
from random import randrange
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup
import time
new_level_texts = {1: "Level 1:\n\nTouch the key\nthat matches the falling card.",
                   2: "Level 2:\n\nTouch the wagon\nthat matches the selected key.",
                   3: "Level 3:\n\nTouch the wagon\nthat matches the selected key.",
                   4: "Level 4:\n\nTouch the wagon\nthat matches the selected key.",
                   5: "Level 5:\n\nTouch the wagon\nthat matches the selected key.",
                   6: "Level 6:\n\nTouch the key\nthat matches the falling card.",
                   7: "Please purchase additional levels\n\n to continue playing."}

card_sources = {0: 'card_c.jpg', 1: 'card_d.jpg', 2: 'card_e.jpg', 3: 'card_f.jpg', 4: 'card_g.jpg', 5: 'card_a.jpg',
                6: 'card_b.jpg'}
score = 0
level = 0
lives = 3
best_score=0
NO_OF_LEVELS = 7
new_number = 3
frame_number = 0
score_sound = SoundLoader.load("score_sound.wav")
score_sound.volume = 0.5
wrong_note = SoundLoader.load("wrong_note.wav")

class pop(Popup):
	
	pass

def show_popup(result):		
	respop = pop(content = Label(text=result))
	respop.open()
	Clock.schedule_once(respop.dismiss,2.5)

def pick_new_number(starting, ending, step=1):
    global new_number

    previous = new_number
    new_number = randrange(starting, ending, step)
    if new_number == previous:
        pick_new_number(starting, ending, step)
    return new_number		


def check_for_new_level(instance):
    print 'in check'
    global score
    score = score+1	
    Clock.unschedule(instance.move_objects)
    if score % 1 == 0:  # Use 20 for the game; use 1 for testing. (starting level is 0)
	print 'yes'        
	if instance.level_no + 1 < NO_OF_LEVELS:
           instance.parent.transition =SlideTransition(direction='left')
	   instance.parent.current='Level'+str(instance.level_no + 1)
	else:
	   instance.parent.transition = SlideTransition(direction='left')
           instance.parent.current='welcomescreen'
    else:
	instance.load_level()


def won():
    global score 
    score += 1
    

def deduct_life(instance):
    global lives
    global level
    global best_score

    Clock.unschedule(instance.move_objects)
    lives -= 1

    if lives > 0:
        instance.load_level()
    elif lives == 0:
        if score > int(best_score):
            with open('best_score.txt', 'w') as new_best_score:
                new_best_score.write(str(score))
            best_score = score
        #Popup game over
	lives = 3
	level = 0
        instance.parent.transition = SlideTransition(direction='left')
        instance.parent.current='welcomescreen'


class status(BoxLayout):
	def __init__(self,**kwargs):
		super(status, self).__init__(**kwargs)
		#self.ids.label_score.text = str(score)
		#self.ids.label_level.text = str(level)
		#self.ids.label_lives.text = str(lives)
		#self.ids.label_best_score.text = str(best_score)
	
class TouchResponsiveImage(Image):
    selection_number = None
    is_touch_responsive = True

    initial_touch_x = None
    initial_touch_y = None

    relative_touch_x = None
    relative_touch_y = None

    #velocity_x = 0
    #velocity_y = 0

    def run_logic(self):
        pass

    def on_touch_down(self, touch):
        self.initial_touch_x = touch.x  # Defining the touch's x position
        self.initial_touch_y = touch.y  # Defining the touch's y position

        self.relative_touch_x = self.initial_touch_x - self.x  # Defining the touch's x position relative to the image
        self.relative_touch_y = self.initial_touch_y - self.y  # Defining the touch's y position relative to the image

        self.run_logic()


class Keyboard(Image):
    def __init__(self,**kwargs):
	super(Keyboard,self).__init__(**kwargs)
	
	self.selection_number = None
	self.is_touch_responsive = True

	self.initial_touch_x = None
	self.initial_touch_y = None

	self.relative_touch_x = None
	self.relative_touch_y = None
	self.kh1 = self.height
	self.kw1 = self.width

    def on_touch_down(self, touch):
        self.initial_touch_x = touch.x  # Defining the touch's x position
        self.initial_touch_y = touch.y  # Defining the touch's y position

        self.relative_touch_x = self.initial_touch_x - self.x  # Defining the touch's x position relative to the image
        self.relative_touch_y = self.initial_touch_y - self.y  # Defining the touch's y position relative to the image
        if self.is_touch_responsive is True and self.relative_touch_x is not None and self.relative_touch_y is not None:
          
            if 0 <= self.relative_touch_y < 3*self.kh1/8:  # If touch is below the height where the black keys end
                if 0 <= self.relative_touch_x < self.kw1/7:
                    self.selection_number = 0
                elif self.kw1/7 <= self.relative_touch_x < 2 * self.kw1/7:
                    self.selection_number = 1
                elif 2*self.kw1/7 <= self.relative_touch_x < 3*self.kw1/7:
                    self.selection_number = 2
                elif 3*self.kw1/7 <= self.relative_touch_x < 4*self.kw1/7:
                    self.selection_number = 3
                elif 4* self.kw1/7 <= self.relative_touch_x < 5 * self.kw1/7:
                    self.selection_number = 4
                elif 5* self.kw1/7 <= self.relative_touch_x < 6* self.kw1/7:
                    self.selection_number = 5
                elif 6 *self.kw1/7 <= self.relative_touch_x < self.kw1:
                    self.selection_number = 6
	    	    
            elif 3 / 8 * self.kh1 <= self.relative_touch_y < self.kh1:  # If touch is above the height where the black keys end

                if 0 <= self.relative_touch_x < 3 / 28 * self.kw1:
                    self.selection_number = 0
                elif 3 / 28 * self.kw1 <= self.relative_touch_x < 5 / 28 * self.kw1:
                    self.selection_number = 7  # 7 stands for "black key"
                elif 5 / 28 * self.kw1 <= self.relative_touch_x < 7 / 28 * self.kw1:
                    self.selection_number = 1
                elif 7 / 28 * self.kw1 <= self.relative_touch_x < 9 / 28 * self.kw1:
                    self.selection_number = 7
                elif 9 / 28 * self.kw1 <= self.relative_touch_x < 12 / 28 * self.kw1:
                    self.selection_number = 2
                elif 12 / 28 * self.kw1 <= self.relative_touch_x < 15 / 28 * self.kw1:
                    self.selection_number = 3
                elif 15 / 28 * self.kw1 <= self.relative_touch_x < 17 / 28 * self.kw1:
                    self.selection_number = 7
                elif 17 / 28 * self.kw1 <= self.relative_touch_x < 19 / 28 * self.kw1:
                    self.selection_number = 4
                elif 19 / 28 * self.kw1 <= self.relative_touch_x < 21 / 28 * self.kw1:
                    self.selection_number = 7
                elif 21 / 28 * self.kw1 <= self.relative_touch_x < 23 / 28 * self.kw1:
                    self.selection_number = 5
                elif 23 / 28 * self.kw1 <= self.relative_touch_x < 25 / 28 * self.kw1:
                    self.selection_number = 7
                elif 25 / 28 * self.kw1 <= self.relative_touch_x < self.kw1:
                    self.selection_number = 6
	

class Train(TouchResponsiveImage):
	def __init__(self,**kwargs):
	    super(Train,self).__init__(**kwargs)
	    selection_number = None
	    is_touch_responsive = True

	    initial_touch_x = None
	    initial_touch_y = None

	    relative_touch_x = None
	    relative_touch_y = None

	    #velocity_x = 0
	    #velocity_y = 0


    	def on_touch_down(self, touch):
		self.initial_touch_x = touch.x  # Defining the touch's x position
		self.initial_touch_y = touch.y  # Defining the touch's y position

		self.relative_touch_x = self.initial_touch_x - self.x  # Defining the touch's x position relative to the image
		self.relative_touch_y = self.initial_touch_y - self.y  # Defining the touch's y position relative to the image


		wheels_height = self.parent.width/62
		wagon_space = self.parent.width/62
		wagon_width = wagon_space*8
		wagon_height = wagon_space*4
		print wheels_height + wagon_height
		print wheels_height
		print self.y
		print self.relative_touch_y
		if self.is_touch_responsive is True and self.relative_touch_x is not None and self.relative_touch_y is not None:
		    print 'yes'
		    if wheels_height <= self.relative_touch_y < wheels_height + wagon_height:
			print 'yes'
		        if 0 <= self.relative_touch_x < wagon_width:
		            self.selection_number = 0
		        elif wagon_width + wagon_space <= self.relative_touch_x < wagon_width*2 + wagon_space:
		            self.selection_number = 1
		        elif (wagon_width + wagon_space)*2 <= self.relative_touch_x < wagon_width*3 + wagon_space*2:
		            self.selection_number = 2
		        elif (wagon_width + wagon_space)*3 <= self.relative_touch_x < wagon_width*4 + wagon_space*3:
		            self.selection_number = 3
		        elif (wagon_width + wagon_space)*4 <= self.relative_touch_x < wagon_width*5 + wagon_space*4:
		            self.selection_number = 4
		        elif (wagon_width + wagon_space)*5 <= self.relative_touch_x < wagon_width*6 + wagon_space*5:
		            self.selection_number = 5
		        elif (wagon_width + wagon_space)*6 <= self.relative_touch_x <= self.width:
		            self.selection_number = 6
		print self.selection_number
class Level3_cards(Image):
	def __init__(self,**kwargs):
	    super(Level3_cards,self).__init__(**kwargs)
	    self.i = 0

class Level4_cards(Image):
	def __init__(self,**kwargs):
	    super(Level4_cards,self).__init__(**kwargs)
	    self.i = 0

class WelcomeScreen(Screen):
	global score
	global level
	global lives
	score = 0
	level = 0
	lives = 3
	def load_level(self):
		print 'loaded the level'
	
	def next_level(self):
		self.parent.transition =SlideTransition(direction='left')
		self.parent.current='Level1'
	
	def EXIT(self):
		exit(0)
		
		


class Level1(Screen):
	def __init__(self,**kwargs):
		super(Level1,self).__init__(**kwargs)

	def load_level(self):
		global score
		global lives
		global level
		global frame_number
		self.kw1 = self.ids.keyboard.width
		cw = self.ids.card.width
		wh = self.height
		frame_number = 0
		self.ids.sts.ids.label_level.text = str(level)
		self.ids.sts.ids.label_score.text = str(score)
		self.ids.sts.ids.label_lives.text = str(lives)
		self.ids.keyboard.selection_number = None
		self.ids.keyboard.is_touch_responsive = True
		self.ids.card.random_number = pick_new_number(0,7)
		self.ids.card.source = card_sources[self.ids.card.random_number]
		self.ids.card.x = [self.ids.keyboard.x/2 - cw/2, (self.width + self.ids.keyboard.right)/2 - cw/2][randrange(0, 2)]
		self.ids.card.initial_y = wh
		self.ids.card.initial_velocity_y = -1.5
		self.ids.card.acceleration_y = self.ids.card.initial_velocity_y/15

		Clock.schedule_interval(self.move_objects,0)

	
	def move_objects(self,dt):
		global score
		global level
		global lives
		global best_score
		global frame_number

		self.ids.card.y = 1/2*self.ids.card.acceleration_y*frame_number**2 + self.ids.card.initial_velocity_y*frame_number + self.ids.card.initial_y
		frame_number += 1

		if self.ids.keyboard.is_touch_responsive is True and self.ids.keyboard.relative_touch_x is not None \
		    and self.ids.keyboard.relative_touch_y is not None:  # If the keyboard is touch-responsive

			if self.ids.keyboard.selection_number == self.ids.card.random_number:  # If the right key was touched
			    score_sound.play()
			    self.ids.keyboard.is_touch_responsive = False
			    show_popup('Congratulations..Right Key')
			    check_for_new_level(self)

			elif self.ids.keyboard.selection_number is not None and self.ids.keyboard.selection_number != self.ids.card.random_number:  # If the wrong key was touched
			    wrong_note.play()
			    print self.ids.keyboard.width
			    print self.ids.keyboard.relative_touch_x
		     	    print self.ids.keyboard.kw1
			    print self.ids.keyboard.selection_number
			    self.ids.keyboard.is_touch_responsive = False
			    show_popup('Wrong Key Pressed..')
			    deduct_life(self)

		if self.ids.card.top <= 0:  # If the card goes off the bottom of the screen

			frame_number = 0

			if self.ids.keyboard.selection_number is None:  # If no key has been touched
			    wrong_note.play()
			    self.ids.keyboard.is_touch_responsive = False
			    show_popup('No Key Pressed')
			    deduct_life(self)


		
class Level2(Screen):
	def __init__(self,**kwargs):
		super(Level2,self).__init__(**kwargs)
	def load_level(self):
		self.ids.sts.ids.label_level.text = str(level)
	    	self.ids.sts.ids.label_score.text = str(score)
	    	self.ids.sts.ids.label_lives.text = str(lives)

		
		#self.ids.keyboard.remove_widget(self.ids.question_mask)
		self.ids.question_mark.random_number = pick_new_number(0, 7)
		self.ids.question_mark.note_number = self.ids.question_mark.random_number

		self.ids.train.selection_number = None
		self.ids.train.is_touch_responsive = True
		self.ids.train.velocity_x = -5
		self.ids.train.x = self.width

    		Clock.schedule_interval(self.move_objects, 0)

	def move_objects(self,dt):
	    global score
	    global level
	    global lives
	    global best_score
	    self.ids.train.x += self.ids.train.velocity_x  # Move the self.ids.train according to its horizontal velocity

	    if self.ids.train.is_touch_responsive is True and self.ids.train.relative_touch_x is not None \
		    and self.ids.train.relative_touch_y is not None:  # If the self.ids.train is touch-responsive and has been touched

		if self.ids.train.selection_number == self.ids.question_mark.note_number:  # If the right wagon was touched
		    score_sound.play()
		    self.ids.train.is_touch_responsive = False
		    self.ids.train.velocity_x *= 2
		    show_popup('Congratulatons..right wagon selected..!!')
		    check_for_new_level(self)

		elif self.ids.train.selection_number is not None \
		        and self.ids.train.selection_number != self.ids.question_mark.note_number:  # If the wrong wagon was touched
		    wrong_note.play()
		    self.ids.train.is_touch_responsive = False
		    show_popup('Wrong Wagon')
		    deduct_life(self)

	    if self.ids.train.right <= 0:  # If the self.ids.train goes off the left edge of the screen

		#self.ids.keyboard.remove_widget(self.ids.question_mask)
		self.ids.train.velocity_x = -5

		if self.ids.train.selection_number is None:  # If no wagon has been touched
		    wrong_note.play()
		    self.ids.train.is_touch_responsive = False
		    show_popup('Time Out..No wagon selected')
		    self.load_level()
		    deduct_life(self)

		elif self.ids.train.selection_number == self.ids.question_mark.note_number:  # If the right wagon was touched
		    check_for_new_level()
		    self.ids.train.selection_number = None
		    self.ids.train.is_touch_responsive = True
		    self.ids.train.x = self.width
		     

	
class Level3(Screen):
    def __init__(self,**kwargs):
	    super(Level3,self).__init__(**kwargs)
	  
    # global note  # This is needed because the object "note" will be recreated from a different class
    # global card  # This is needed because the object "card" will be recreated from a different class
    def load_level(self):
	    self.ids.sts.ids.label_level.text = str(level)
	    self.ids.sts.ids.label_score.text = str(score)
	    self.ids.sts.ids.label_lives.text = str(lives)
	    self.ids.question_mark.random_number = pick_new_number(0, 14)
	    self.ids.question_mark.note_number = self.ids.question_mark.random_number % 7
	    self.ids.train.selection_number = None
	    self.ids.train.is_touch_responsive = True
	    self.ids.train.x = 0 - self.ids.train.width
	    self.ids.train.velocity_x = 5
            for i in range(0,14):
		self.ids['smallcard'+str(i+1)].source = card_sources[i%7]
	    Clock.schedule_interval(self.move_objects, 1 / 60)



    def move_objects(self,dt):
	    global score
	    global level
	    global lives
	    global best_score

	    self.ids.train.x += self.ids.train.velocity_x  # Move the self.ids.train according to its horizontal velocity

	    if self.ids.train.is_touch_responsive is True and self.ids.train.relative_touch_x is not None \
		    and self.ids.train.relative_touch_y is not None:  # If the self.ids.train is touch-responsive

		if self.ids.train.selection_number == self.ids.question_mark.note_number:  # If the right wagon was touched
		    score_sound.play()
		    self.ids.train.is_touch_responsive = False
		    self.ids.train.velocity_x *= 2
		    show_popup('Congratulations..right wagon selected')
		    check_for_new_level(self)

		elif self.ids.train.selection_number is not None \
		        and self.ids.train.selection_number != self.ids.question_mark.note_number:  # If the wrong wagon was touched
		    wrong_note.play()
		    self.ids.train.is_touch_responsive = False
		    show_popup('Wrong wagon selected')
		    self.load_level()
		    deduct_life(self)

	    if self.ids.train.x >= self.width:  # If the self.ids.train goes off the right edge of the screen

		self.ids.train.velocity_x = 5

		if self.ids.train.selection_number is None:  # If no wagon has been touched
		    self.load_level()
		    self.ids.train.is_touch_responsive = False
		    show_popup('No wagon Selected')
		    self.load_level()
		    deduct_life(self)

		elif self.ids.train.selection_number == self.ids.question_mark.note_number:  # If the right wagon was touched
		    check_for_new_level(self)
		    self.ids.train.selection_number = None
		    self.ids.train.is_touch_responsive = True
		    
		 

		    self.ids.question_mark.random_number = pick_new_number(0, 14)
		    question_mark.x = self.ids.keyboard.x + self.ids.question_mark.random_number / 14 * self.width + self.width / 14 / 4
		    self.ids.question_mark.y = self.ids.keyboard.y + self.width / 14 / 4
		    self.ids.question_mark.size = (self.width / 14 / 2, self.width / 14)
		    self.ids.question_mark.note_number = self.ids.question_mark.random_number % 7	
		

class Level4(Screen):
	def __init__(self,**kwargs):
	    super(Level4,self).__init__(**kwargs)

	def load_level(self):
	 

	    self.ids.question_mark.random_number = pick_new_number(0, 21)
	    self.ids.sts.ids.label_level.text = str(level)
	    self.ids.sts.ids.label_score.text = str(score)
	    self.ids.sts.ids.label_lives.text = str(lives)
	    self.ids.question_mark.note_number = self.ids.question_mark.random_number % 7

	    self.ids.train.selection_number = None
	    self.ids.train.is_touch_responsive = True
	    self.ids.train.x = self.width
	    self.ids.train.velocity_x = -5
	    for i in range(21):
		if i%7%2 == 0:
			self.ids['smallcard'+str(i)].source = card_sources[i%7]



	    Clock.schedule_interval(self.move_objects, 1 / 60)
	def move_objects(self,dt):
	    global score
	    global level
	    global lives
	    global best_score
	

	    self.ids.train.x += self.ids.train.velocity_x  # Move train according to its horizontal velocity

	    if self.ids.train.is_touch_responsive is True and self.ids.train.relative_touch_x is not None \
		    and self.ids.train.relative_touch_y is not None:  # If the train is touch-responsive

		if self.ids.train.selection_number == self.ids.question_mark.note_number:  # If the right wagon was touched
		    score_sound.play()
		    self.ids.train.is_touch_responsive = False
		    self.ids.train.velocity_x *= 2
		    check_for_new_level(self)

		elif self.ids.train.selection_number is not None and self.ids.train.selection_number != self.ids.question_mark.note_number: \
		        # If the wrong wagon was touched
		    wrong_note.play()
		    self.ids.train.is_touch_responsive = False
		    deduct_life(self)

	    if self.ids.train.right <= 0:  # If the train goes off the left edge of the screen



		if self.ids.train.selection_number is None:  # If no wagon has been touched
		    wrong_note.play()
		    self.ids.train.is_touch_responsive = False
		    show_popup('No wagon selected')
		    deduct_life(self)

		elif self.ids.train.selection_number == self.ids.question_mark.note_number:  # If the right wagon was touched
		    check_for_new_level()
		    train.selection_number = None
		    train.is_touch_responsive = True
		    train.x = ww
		    background.remove_widget(label_good_job)

		    question_mark.random_number = pick_new_number(0, 21)
		    question_mark.x = self.ids.keyboard.x + question_mark.random_number / 21 * kw2 + kw2 / 21 / 4
		    question_mark.y = self.ids.keyboard.y + kw3 / 21 / 4
		    question_mark.size = (kw3 / 21 / 2, kw3 / 21)
		    question_mark.note_number = question_mark.random_number % 7


class Level5(Screen):
	def __init__(self,**kwargs):
	    super(Level5,self).__init__(**kwargs)

	def load_level(self):
	    self.ids.sts.ids.label_level.text = str(level)
	    self.ids.sts.ids.label_score.text = str(score)
	    self.ids.sts.ids.label_lives.text = str(lives)
	    self.ids.question_mark.random_number = pick_new_number(0, 21)
	    
	    self.ids.question_mark.note_number = self.ids.question_mark.random_number % 7

	    self.ids.train.selection_number = None
	    self.ids.train.is_touch_responsive = True
	    self.ids.train.x = 0 - self.ids.train.width
	    self.ids.train.velocity_x = 5

	    for i in range(21):
		if i % 7 % 4 == 0:
		    self.ids.keyboard.add_widget(Image(source=card_sources[i % 7],
		                                pos=(self.ids.keyboard.x + i * self.width/21+ self.width / 21 / 4, self.ids.keyboard.y + self.width / 21 / 4),
		                                size=(self.width / 21 / 2, self.width / 21)))

	    Clock.schedule_interval(self.move_objects, 1 / 60)

	def move_objects(self,dt):
	    global score
	    global level
	    global lives
	    global best_score

	    self.ids.train.x += self.ids.train.velocity_x  # Move self.ids.train according to its horizontal velocity

	    if self.ids.train.is_touch_responsive is True and self.ids.train.relative_touch_x is not None \
		    and self.ids.train.relative_touch_y is not None:  # If the self.ids.train is touch-responsive

		if self.ids.train.selection_number == self.ids.question_mark.note_number:  # If the right wagon was touched
		    score_sound.play()
		    self.ids.train.is_touch_responsive = False
		    self.ids.train.velocity_x *= 2
		    check_for_new_level(self)

		elif self.ids.train.selection_number is not None and self.ids.train.selection_number != self.ids.question_mark.note_number: \
		        # If the wrong wagon was touched
		    wrong_note.play()
		    self.ids.train.is_touch_responsive = False
		    self.load_level()
		    deduct_life(self)

	    if self.ids.train.x >= self.width:  # If the self.ids.train goes off the right edge of the screen

		self.ids.train.velocity_x = 5

		if self.ids.train.selection_number is None:  # If no wagon has been touched
		    wrong_note.play()
		    self.ids.train.is_touch_responsive = False
		    self.load_level()
		    deduct_life(self)

		elif self.ids.train.selection_number == question_mark.note_number:  # If the right wagon was touched
		    check_for_new_level()
		    self.ids.train.selection_number = None
		    self.ids.train.is_touch_responsive = True
		    self.ids.train.x = 0 - self.ids.train.width
		  

		    question_mark.random_number = pick_new_number(0, 21)
		    question_mark.x = keyboard_3.x + question_mark.random_number / 21 * kw2 + kw2 / 21 / 4
		    question_mark.y = keyboard_3.y + kw3 / 21 / 4
		    question_mark.size = (kw3 / 21 / 2, kw3 / 21)
		    question_mark.note_number = question_mark.random_number % 7

class Level6(Screen):
	def __init__(self,**kwargs):
	    super(Level6,self).__init__(**kwargs)
	def load_level(self):
	    # global note  # This is needed because the object "note" will be recreated from a different class
	    # global card  # This is needed because the object "card" will be recreated from a different class

            self.ids.sts.ids.label_level.text = str(level)
	    self.ids.sts.ids.label_score.text = str(score)
  	    self.ids.sts.ids.label_lives.text = str(lives)
	    self.ids.keyboard.selection_number = None
	    self.ids.keyboard.is_touch_responsive = True
	    self.ids.card.flipcardpos = randrange(0,2)
	    self.ids.card.random_number = pick_new_number(0, 7)
	    self.ids.card.source = card_sources[self.ids.card.random_number]
	    
	    self.ids.card.initial_y = self.height
	    self.ids.card.initial_velocity_y = -self.width / 3000
	    self.ids.card.acceleration_y = self.ids.card.initial_velocity_y / 20 


	    Clock.schedule_interval(self.move_objects, 1 / 60)

	def move_objects(self,dt):
	    global score
	    global level
	    global lives
	    global best_score
	    global frame_number

	    self.ids.card.y = 1 / 2 * self.ids.card.acceleration_y * frame_number ** 2 + self.ids.card.initial_velocity_y * frame_number + self.ids.card.initial_y
	    frame_number += 1

	    if self.ids.keyboard.is_touch_responsive is True and self.ids.keyboard.relative_touch_x is not None \
		    and self.ids.keyboard.relative_touch_y is not None:  # If the keyboard is touch-responsive

		if self.ids.keyboard.selection_number == self.ids.card.random_number:  # If the right key was touched
		    score_sound.play()
		    self.ids.keyboard.is_touch_responsive = False
		    check_for_new_level(self)

		elif self.ids.keyboard.selection_number is not None \
		        and self.ids.keyboard.selection_number != self.ids.card.random_number:  # If the wrong key was touched
		    wrong_note.play()
		    self.ids.keyboard.is_touch_responsive = False
		    show_popup('Wrong Key')
		    self.load_level()
		    deduct_life(self)

	    if self.ids.card.top <= 0:  # If the card goes off the bottom of the screen

		frame_number = 0

		if self.ids.keyboard.selection_number is None:  # If no key has been touched
		    wrong_note.play()
		    self.ids.keyboard.is_touch_responsive = False
		    show_popup('Time Out..No Key Pressed')
		    self.load_level()
		    deduct_life(self)

		elif self.ids.keyboard.selection_number == self.ids.card.random_number:  # If the right key was touched
		    show_popup('Congratulations..right key pressed')
		    check_for_new_level()
		    self.ids.keyboard.selection_number = None
		    self.ids.keyboard.is_touch_responsive = True

		    self.ids.card.random_number = pick_new_number(0, 7)
		    self.ids.card.source = self.ids.card_sources[card.random_number]

		    if card.x == keyboard.x / 2 - cw / 2:
		        card.x = (ww + keyboard.right) / 2 - cw / 2
		    elif card.x == (ww + keyboard.right) / 2 - cw / 2:
		        card.x = keyboard.x / 2 - cw / 2


class ScreenManagement(ScreenManager):
	pass




class MusicApp(App):
	def build(self):
		return Builder.load_file('musiclayout.kv')

if __name__ == '__main__':
	MusicApp().run()


