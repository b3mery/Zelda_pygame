""" Support Functions for handling files
"""
from csv import reader
import os
import pygame


def import_csv_layout(path):
    """Read CSV File to a List, returning list of lists

    Args:
        path (str): Directory file path

    Returns:
        List: List of rows as lists
    """
    with open(path, mode="r", encoding='utf-8') as level_map:
        layout = reader(level_map, delimiter=',')
        terrain_map = [list(row) for row in layout]
    return terrain_map

def import_folder_images(path):
    """Import all items 

    Args:
        path (str): directory path

    Returns:
        list: list of pygame images
    """
    surface_list = []
    for _, __,img_files in os.walk(path):
        for img in img_files:
            file_path = f"{path}/{img}"
            img_surf = pygame.image.load(file_path).convert_alpha()
            surface_list.append(img_surf)
    return surface_list
