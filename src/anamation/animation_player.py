import pygame
import random

from src.utils import util
from src.anamation.particle_effect import ParticleEffect

class AnimationPlayer:
	"""_summary_
	"""
	def __init__(self) -> None:
		self.frames = {
			# magic
			'flame': util.import_folder('assets/graphics/particles/flame/frames'),
			'aura': util.import_folder('assets/graphics/particles/aura'),
			'heal': util.import_folder('assets/graphics/particles/heal/frames'),

			# attacks 
			'claw': util.import_folder('assets/graphics/particles/claw'),
			'slash': util.import_folder('assets/graphics/particles/slash'),
			'sparkle': util.import_folder('assets/graphics/particles/sparkle'),
			'leaf_attack': util.import_folder('assets/graphics/particles/leaf_attack'),
			'thunder': util.import_folder('assets/graphics/particles/thunder'),

			# monster deaths
			'squid': util.import_folder('assets/graphics/particles/smoke_orange'),
			'raccoon': util.import_folder('assets/graphics/particles/raccoon'),
			'spirit': util.import_folder('assets/graphics/particles/nova'),
			'bamboo': util.import_folder('assets/graphics/particles/bamboo'),

			# leafs 
			'leaf': (
				util.import_folder('assets/graphics/particles/leaf1'),
				util.import_folder('assets/graphics/particles/leaf2'),
				util.import_folder('assets/graphics/particles/leaf3'),
				util.import_folder('assets/graphics/particles/leaf4'),
				util.import_folder('assets/graphics/particles/leaf5'),
				util.import_folder('assets/graphics/particles/leaf6'),
				self.__reflect_images(util.import_folder('assets/graphics/particles/leaf1')),
				self.__reflect_images(util.import_folder('assets/graphics/particles/leaf2')),
				self.__reflect_images(util.import_folder('assets/graphics/particles/leaf3')),
				self.__reflect_images(util.import_folder('assets/graphics/particles/leaf4')),
				self.__reflect_images(util.import_folder('assets/graphics/particles/leaf5')),
				self.__reflect_images(util.import_folder('assets/graphics/particles/leaf6')),
				)
		}

	def __reflect_images(self, frames):
		"""_summary_

		Args:
			frames (_type_): _description_

		Returns:
			_type_: _description_
		"""
		return [pygame.transform.flip(frame, True, False) for frame in frames]
	
	def create_grass_particles(self, pos, groups):
		"""_summary_

		Args:
			pos (_type_): _description_
			groups (_type_): _description_
		"""
		animation_frames = random.choice(self.frames['leaf'])
		ParticleEffect(pos, animation_frames, groups)

	def generate_particles(self,animation_type:str, pos, groups):
		"""_summary_

		Args:
			animation_type (str): _description_
			pos (_type_): _description_
			groups (_type_): _description_
		"""
		animation_frames = self.frames[animation_type]
		ParticleEffect(pos, animation_frames, groups)
		
