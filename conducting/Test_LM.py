import os, sys, inspect, thread, time, play_wav
# src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# lib_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.append("../lib")
sys.path.append("../lib/x64")

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
class conductor_listener_trainer(Leap.Listener):
	first_call = 0
	curr_song = None
	def set_song(self, new_song):
		self.curr_song = new_song

	def on_connect(self, controller):
		print "Connected"
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.frame().fps = 4

	def on_frame(self, controller):
		if not self.curr_song:
			return
		frame = controller.frame()
		frame.fps = 4
		play = False
		pause = False
		end = False
		if not frame.hands:
			print "pause"
			self.curr_song.play(0, 1, 0)
			pause = True
			return
		for gesture in frame.gestures():
			if gesture.type is Leap.Gesture.TYPE_SWIPE:
				play = True
			if gesture.type is Leap.Gesture.TYPE_CIRCLE:
				end = True
		if play:
			print "play"
			self.curr_song.play(self.first_call, 0, 0)
		elif end:
			print "stop"
			self.curr_song.play(0, 0, 1)
			self.first_call = 0
		self.first_call = 1

# class conductor_controller(Leap.Controller):
# 	def __init__(self, conductor_listener_trainer):
# 		super

def create_training_set_play():
	listener = conductor_listener_trainer()
	controller = Leap.Controller()
	print "Press Enter to stop training"
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		# Remove the sample listener when done
		controller.remove_listener(listener)


def main():
	# Create a sample listener and controller
	new_song = play_wav.song(sys.argv[1])
	listener = conductor_listener_trainer()
	listener.set_song(new_song)
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller
	controller.add_listener(listener)

	# Keep this process running until Enter is pressed
	print "Press Enter to quit..."
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		# Remove the sample listener when done
		controller.remove_listener(listener)

if __name__ == "__main__":
	main()