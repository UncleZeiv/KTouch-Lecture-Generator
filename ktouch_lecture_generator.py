# coding=utf-8
# ktouch_lecture_generator
# author: unclezeiv@kerid.org
# generate a programmer-friendly ktouch lecture

import random
from xml.sax.saxutils import escape
from textwrap import dedent

class KTouchTemplates(object):
	lecture = dedent('''<KTouchLecture>
		<Title>Tricky Chars</Title>
		<FontSuggestions>Monospace</FontSuggestions>
		<Levels>
		%s
		</Levels>
	</KTouchLecture>''')
	line_tag = '\t<Line>%s</Line>\n'
	level_header = '\t<Level>\n\t\t<NewCharacters>%s</NewCharacters>\n'
	level_footer = '\t</Level>\n'


class KTouchGenLecture(object):

	def __init__(self):
		self.lecture_file = 'programmer_lecture.ktouch.xml'
		self.min_word_length = 1
		self.max_word_length = 9
		self.min_line_length = 45
		self.lines_of_new_chars = 10
		self.lines_of_review = 10
		self.accented_chars = 1

		# make "easy" characters more frequent
		self.extra_weight = 6

		self.normalset = 'qwertyuiopsadfghjk;;zxcvbnm,./'
		self.chargroups = [
			# mix_chargroups, chargroup
			(0, 'weiosdklxc,.' * self.extra_weight),
			(0, 'qrupafj;zvm/' * self.extra_weight),
			(0, 'qpa;z/10'),
			(0, 'woslx.29'),
			(0, 'eidkc,38'),
			(0, '47rufjvm'),
			(0, '56tyghbn'),
			(0, 'rtyufghjvbnm' * self.extra_weight),
			(0, '4567rtyufghjvbnm'),
			(1, 'WEIOSDKLXCQRUPAFJ:ZVM?<>'),
			(1, '\'#[]-=\\'),
			(1, '@~{}_+|'),
			(1, '0123456789'),
			(0, '0123456789'),
			(1, u'!"£$%^&*()'),
			]

		if self.accented_chars:
			self.chargroups += [
				(1, u'àèìòùé'),
				(1, u'ÀÈÌÒÙÉ'),
			]

	def generate_line(self, allowed_chars):
		cur_line_len = 0
		line = ''
		while 1:
			cur_word_length = random.randint(self.min_word_length, self.max_word_length)
			for character in xrange(cur_word_length):
				line += random.choice(allowed_chars)
			cur_line_len += cur_word_length + 1
			if cur_line_len < self.min_line_length:
				line += ' '
			else:
				break
		return line

	def generate_lecture(self):
		lecture = ''
		for index in xrange(len(self.chargroups)):
			mix_chargroups, chargroup = self.chargroups[index]

			# new characters
			lecture += KTouchTemplates.level_header % escape(''.join(set(chargroup)))
			for line in xrange(self.lines_of_new_chars):
				if mix_chargroups:
					lecture += KTouchTemplates.line_tag % escape(self.generate_line(chargroup + self.normalset * (index > 2)))
				else:
					lecture += KTouchTemplates.line_tag % escape(self.generate_line(chargroup))
			lecture += KTouchTemplates.level_footer

			# review
			lecture += KTouchTemplates.level_header % 'Review'
			for line in xrange(self.lines_of_review):
				allowed_chars = ''.join(elem[1] for elem in self.chargroups[:index + 1]) + self.normalset * index
				lecture += KTouchTemplates.line_tag % escape(self.generate_line(allowed_chars))
			lecture += KTouchTemplates.level_footer
		return lecture

	def write_file(self):
		lecture = self.generate_lecture()
		f = open(self.lecture_file, 'w')
		f.write(KTouchTemplates.lecture % lecture.encode('utf-8'))
		f.close()


if __name__ == '__main__':
	gen_lecture = KTouchGenLecture()
	gen_lecture.write_file()
