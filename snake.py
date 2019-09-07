import time
import random
import pygame as pg

class c_snake:
	UP = 0
	DOWN = 1
	LEFT = 2
	RIGHT = 3

	E_NOP = 0
	E_DIE = 1
	E_GET_FEED = 2

	def __init__(self, \
				map_size=[80, 60], \
				color=[255, 255, 255], \
				pos=None, \
				speed=10):
		self._color = color
		self._dir = self.DOWN
		self._border = [map_size[0] - 1, map_size[1] - 1]
		self._speed = speed

		self._snake = []
		self._update_cnt = 0
		self._event_q = []
		self._feeds = []
		self._feed_cnt = 0

		# generate initial snake
		if not pos:
			pos = [map_size[0]/2, map_size[1]/2]

		for i in range(0, 5):
			self._snake.append([pos[0], pos[1]-i])

	def key_down(self, key):
		self._dir = key

	def add_feed(self, num=1):
		cnt = 0
		while cnt < num:
			feed = [random.randint(0, self._border[0]), random.randint(0, self._border[1])]
			if not feed in self._snake:
				self._feeds.append(feed)
				cnt += 1

	def update(self):
		if self._update_cnt < self._speed:
			self._update_cnt += 1
			return

		head = self._snake[0]
		if self._dir == self.UP:
			new_head = [head[0], head[1]-1]
		elif self._dir == self.DOWN:
			new_head = [head[0], head[1]+1]
		elif self._dir == self.LEFT:
			new_head = [head[0]-1, head[1]]
		elif self._dir == self.RIGHT:
			new_head = [head[0]+1, head[1]]

		if new_head[0] < 0 or \
		   new_head[0] > self._border[0] or \
		   new_head[1] < 0 or \
		   new_head[1] > self._border[1]:
			self._event_q.append(self.E_DIE)

		self._snake.insert(0, new_head)

		if not new_head in self._feeds:
			del self._snake[-1]
		else:
			self._feeds.remove(new_head)
			self._feed_cnt += 1
			self._event_q.append(self.E_GET_FEED)
			if self._feed_cnt % 5 == 0:
				self._speed -= 1

		self._update_cnt = 0

	def get_event(self):
		if not len(self._event_q):
			return self.E_NOP
		else:
			return self._event_q.pop()

	def draw(self, canvas):
		for pos in self._snake:
			pg.draw.rect(canvas, \
				self._color, \
				[pos[0] * 10, pos[1] * 10, 9, 9], \
				0)

		for pos in self._feeds:
			pg.draw.rect(canvas, \
				[255, 0, 0], \
				[pos[0] * 10, pos[1] * 10, 9, 9], \
				0)

def main():
	pg.init()

	width = 400
	height = 300
	screen = pg.display.set_mode([width, height])
	pg.display.set_caption("snake game")

	bg = pg.Surface(screen.get_size())
	bg = bg.convert()

	snake = c_snake(map_size=[width/10, height/10])
	snake.add_feed()

	running = True
	while running:

		# handle system event
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
				break
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_UP:
					snake.key_down(c_snake.UP)
				elif event.key == pg.K_DOWN:
					snake.key_down(c_snake.DOWN)
				elif event.key == pg.K_LEFT:
					snake.key_down(c_snake.LEFT)
				elif event.key == pg.K_RIGHT:
					snake.key_down(c_snake.RIGHT)

		bg.fill((0, 0, 0))
		snake.update()

		# handle snake event
		snake_event = snake.get_event()
		if snake_event == c_snake.E_DIE:
			pg.quit()
			return
		elif snake_event == c_snake.E_GET_FEED:
			snake.add_feed()

		snake.draw(bg)

		screen.blit(bg, (0,0))
		pg.display.update()

		time.sleep(0.01)

	pg.quit()

if __name__ == '__main__':
	main()