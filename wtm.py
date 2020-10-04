from pygame import mixer
import time

mixer.init(48000)

soundNum = {
	'C': 1, 'c': 1,
	'D': 2, 'd': 2,
	'E': 3, 'e': 3,
	'F': 4, 'f': 4,
	'G': 5, 'g': 5,
	'A': 6, 'a': 6,
	'B': 7, 'b': 7
}

noteNum = {
	"whole": 4,
	"half": 2,
	"quarter": 1,
	"eighth": 0.5,
	"sixteenth": 0.25
}

f = open("test.wtm", "r")

lines = f.readlines()
speed = 0
try: speed = int(lines[0])
except: print("wtm: fatal: speed is not an integer.", end='\r')

for i in range(1, len(lines)):
	temp = lines[i].split()
	note = 0
	pitch = 0
	duration = 0
	try: note = soundNum[temp[0]]
	except: print("wtm: fatal: unexpected note.", end='\r')
	try: pitch = int(temp[1])
	except: print("wtm: fatal: pitch is not an integer.", end='\r')
	try: duration = float(temp[2]) * speed
	except:
		try: duration = noteNum[temp[2]] * speed
		except: print("wtm: fatal: unexpected duration for a note." % i, end='\r')
	print(pitch, note, duration)
	mixer.Sound("media/%d_%d.wav" % (pitch, note)).play(maxtime=int(duration))
	time.sleep(duration / 1000)

f.close()