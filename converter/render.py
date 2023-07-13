import wave, struct

def play(notes, vol, sample_freq):
	for (duration, pitch) in notes:
		sample_count = duration * sample_freq / 50
		isample_count= int(sample_count)
		if pitch is None:
			for i in range(0, isample_count):
				yield 0
		else:
			note_freq = 261.63 * (2 ** (pitch / 12.0))
			note_period = sample_freq / note_freq

			for i in range(0, isample_count):
				if i % note_period < (note_period / 2.0):
					yield vol
				else:
					yield 0
	yield 0

def to_wave(note_data, out_filename, freq=44100):
	wav = wave.open(out_filename, 'w')
	wav.setparams((1, 1, freq, 0, 'NONE', 'not compressed'))

	generators = [
		play(notes, vol, freq)
		for (vol, notes) in note_data
	]

	while True:
		vol = 0
		for (i, gen) in enumerate(generators):
			if not gen:
				continue
			try:
				vol += next(gen)
			except StopIteration:
				generators[i] = None

		if any(generators):
			wav.writeframes(struct.pack('B', int(vol)))
		else:
			break

	wav.close()
