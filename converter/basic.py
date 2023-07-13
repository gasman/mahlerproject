
def to_basic(channels):
	for i, c in enumerate(channels):
		print("channel %i: %i bytes" % (i, len(c.history)*2))
		f = open("%d.bas" % (i+100), 'w')
		f.write("10 RESTORE\n")
		f.write("20 READ d, p\n")
		f.write("30 IF p=0 THEN PAUSE d : GOTO 20\n")
		f.write("40 BEEP d * 0.02,p-128\n")
		f.write("50 GOTO 20\n")

		line_number = 100
		line_code = ""
		line_concat = ""
		data_pairs = 0
		for (duration, pitch) in c.history:
			if (data_pairs == 0):
				line_code = "{} DATA ".format(line_number)
				line_concat = ""
				line_number = line_number + 10

			line_code += "{}{},{}".format(line_concat, duration, (pitch or -128) + 128)
			line_concat = ", "

			data_pairs = data_pairs + 1
			if (data_pairs > 10):
				data_pairs = 0
				f.write(line_code + "\n")

		# Any lines left?
		f.write(line_code + "\n")
