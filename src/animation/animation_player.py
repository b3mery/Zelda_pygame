import pygame
import random

from utils import util
from animation.particle_effect import ParticleEffect

class AnimationPlayer:
	"""Animation Particle Player.
	Responsible for creating particle anamaitons on the game screen.
	"""
	def __init__(self) -> None:
		self.frames = {
			# magic
			'flame': util.import_folder_images('assets/graphics/particles/flame/frames'),
			'aura': util.import_folder_images('assets/graphics/particles/aura'),
			'heal': util.import_folder_images('assets/graphics/particles/heal/frames'),

			# attacks 
			'claw': util.import_folder_images('assets/graphics/particles/claw'),
			'slash': util.import_folder_images('assets/graphics/particles/slash'),
			'sparkle': util.import_folder_images('assets/graphics/particles/sparkle'),
			'leaf_attack': util.import_folder_images('assets/graphics/particles/leaf_attack'),
			'thunder': util.import_folder_images('assets/graphics/particles/thunder'),

			# monster deaths
			'squid': util.import_folder_images('assets/graphics/particles/smoke_orange'),
			'raccoon': util.import_folder_images('assets/graphics/particles/raccoon'),
			'spirit': util.import_folder_images('assets/graphics/particles/nova'),
			'bamboo': util.import_folder_images('assets/graphics/particles/bamboo'),

			# leafs 
			'leaf': (
				util.import_folder_images('assets/graphics/particles/leaf1'),
				util.import_folder_images('assets/graphics/particles/leaf2'),
				util.import_folder_images('assets/graphics/particles/leaf3'),
				util.import_folder_images('assets/graphics/particles/leaf4'),
				util.import_folder_images('assets/graphics/particles/leaf5'),
				util.import_folder_images('assets/graphics/particles/leaf6'),
				self.__reflect_images(util.import_folder_images('assets/graphics/particles/leaf1')),
				self.__reflect_images(util.import_folder_images('assets/graphics/particles/leaf2')),
				self.__reflect_images(util.import_folder_images('assets/graphics/particles/leaf3')),
				self.__reflect_images(util.import_folder_images('assets/graphics/particles/leaf4')),
				self.__reflect_images(util.import_folder_images('assets/graphics/particles/leaf5')),
				self.__reflect_images(util.import_folder_images('assets/graphics/particles/leaf6')),
				)
		}

	def __reflect_images(self, frames):
		"""Flip(reflect) the images

		Args:
			frames (list): list of pygame.image files

		Returns:
			list: flippsed list of pygame.image files
		"""
		return [pygame.transform.flip(frame, True, False) for frame in frames]
	
	def create_grass_particles(self, pos:tuple, groups):
		"""Creates the grass particle animation

		Args:
			pos (tuple): x and y pos
			groups (list or string): sprite groups
		"""
		animation_frames = random.choice(self.frames['leaf'])
		ParticleEffect(pos, animation_frames, groups)

	def create_particles(self,animation_type:str, pos:tuple, groups):
		"""_summary_

		Args:
			animation_type (str): name of the anamation matchign key in self.frames
			pos (tuple): x and y pos
			groups (list or string): sprite groups
		"""
		animation_frames = self.frames[animation_type]
		ParticleEffect(pos, animation_frames, groups)
		
