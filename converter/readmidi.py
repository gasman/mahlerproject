from mido import MidiFile
import sys

import render
import basic

render_single_wave = False
render_mutiple_wave = False
render_basic_code = False

class Channel(object):
	def __init__(self, velocity, output_velocity):
		self.note = None
		self.current_time = 0
		self.quantized_current_time = 0
		self.history = []
		self.velocity = velocity
		self.output_velocity = output_velocity

	def note_on(self, note, time):
		self.stop_note(time)
		self.current_time = time
		self.note = note

	def stop_note(self, time):
		if time > self.current_time:
			quantized_time = int(time * 50)
			if self.note is None:
				pitch = None
			else:
				pitch = self.note[1] - 60

			quantized_length = quantized_time - self.quantized_current_time
			while quantized_length > 255:
				self.history.append((255, pitch))
				quantized_length -= 255
			if quantized_length > 0:
				self.history.append((quantized_length, pitch))

			self.quantized_current_time = quantized_time
			self.current_time = time
		self.note = None

	def note_off(self, note, time):
		if note == self.note:
			self.stop_note(time)

mid = MidiFile(sys.argv[1])

velocity_stats = {}

# rachmaninov3
#channel_velocities = [100, 100, 90, 90, 90, 80, 80, 80, 70, 70, 70, 60, 60, 50, 50, 40]

# mahler1
# channel_velocities = [112, 101, 67, 42, 35, 30, 110, 103, 90, 44]

# mahler3
channel_velocities = [20, 30, 40, 80, 100, 100, 110, 110, 115, 115, 120, 120]

# mahler4
channel_velocities = [20, 30, 40, 80, 100, 100, 110, 110, 115, 115, 120, 120]

# minute waltz
#channel_velocities = [30, 45, 60, 100]

# star wars
#channel_velocities = [127, 123, 119, 114, 110, 105, 95, 55, 43, 106, 99, 77]

# eine kleine nachtmusik
#channel_velocities = [80, 90, 100, 110, 120, 115, 80, 90, 80, 100, 110, 120]
#channel_velocities = [80, 90, 100, 110]

CHANNEL_COUNT = len(channel_velocities)
velocity_scale = 255.0 / sum(channel_velocities)

channels = [
	Channel(channel_velocities[i], velocity_scale * channel_velocities[i])
	for i in range(0, CHANNEL_COUNT)
]

note_assignments = {}

time = 0
for message in mid:
	time += message.time
	if message.type == 'note_off' or (message.type == 'note_on' and message.velocity == 0):
		note_ref = (message.channel, message.note)
		try:
			channel = note_assignments[note_ref].pop()
			channel.note_off(note_ref, time)
		except (KeyError, IndexError):
			pass

	elif message.type == 'note_on':
		note_ref = (message.channel, message.note)
		try:
			velocity_stats[message.velocity] += 1
		except KeyError:
			velocity_stats[message.velocity] = 1

		channel = sorted(channels, key=lambda c: -(
			# key function: highest score = most suitable for allocating the note here
			# score 100000 for not currently playing, 10000 for currently playing the desired note
			# otherwise, score 10 for each second it has been sounding
			(100000 if c.note is None else (10000 if c.note[1] == message.note else 10 * (c.current_time - time)))
			# subtract 1000 for each point difference in volume
			- 1000 * abs(c.velocity - message.velocity)
			# subtract 0.1 for each note in channel's history, to distribute notes more equally
			- 0.1 * len(c.history)
		))[0]

		channel.note_on(note_ref, time)
		try:
			note_assignments[note_ref].append(channel)
		except KeyError:
			note_assignments[note_ref] = [channel]

for i, c in enumerate(channels):
	print("channel %i: %i bytes" % (i, len(c.history)*2))
	f = open("%d.bip" % (i+100), 'wb')
	for (duration, pitch) in c.history:
		f.write(bytearray([duration, (pitch or -128) + 128]))
	f.write(bytearray([0, 0]))

print("velocity stats:")
for i in sorted(velocity_stats.keys()):
	print("%i: %i" % (i, velocity_stats[i]))

note_data = [
	(c.output_velocity, c.history)
	for c in channels
]


if (render_basic_code):
	basic.to_basic(channels)

if (render_single_wave):
	if (len(sys.argv) > 2):
		print("Rendering waveform")
		render.to_wave(note_data, sys.argv[2], freq=11025)
	else:
		print("Render single wave requested, but no filename given. Please supply one on the command line.")

if (render_mutiple_wave):
	if (len(sys.argv) > 2):
		for i, c in enumerate(channels):
			print("Rendering channel {}...".format(i))
			render.to_wave([(c.output_velocity, c.history)], str(i) + "_" + sys.argv[2], freq=11025)
	else:
		print("Render multiple wave requested, but no filename given. Please supply one on the command line.")
