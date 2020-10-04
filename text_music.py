from pygame import mixer as m
from time import sleep

m.init(48000)

def play_txt(txt: str):
	src = txt.split('\n')
	spe = src.pop(0)
	try:
		spe = int(spe)
	except:
		print("wtm: fatal: The speed is not an integer.")
		return

	for line in src:
		sound, pitch, duration = line.split()
		try:
			sound_num = {
				'c': 1,
				'd': 2,
				'e': 3,
				'f': 4,
				'g': 5,
				'a': 6,
				'b': 7
			}[sound]
			pitch = int(pitch)
			if duration[-1] == '.':
				duration_ms = 1.5
				duration = duration[:-1]
			else:
				duration_ms = 1
			duration_ms *= {
				'whole': 4,
				'half': 2,
				'quarter': 1,
				'eighth': .5,
				'sixteenth': .25
			}[duration] * spe
		except:
			print("wtm: fatal: Your note %s does not work." % line)
			return
		m.Sound("media/%d_%d.wav" % (pitch, sound_num)).play(maxtime=int(duration_ms))
		sleep(duration_ms / 1000)
