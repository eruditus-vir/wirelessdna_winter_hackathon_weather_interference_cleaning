# not used, no time to implement localization
# import geopy
# from src.preprocessed_image import PreprocessedImage
# from src.radar import Radar
# import networkx as nx
# import numpy as np
# import enum
# import geopy.distance
# from typing import Set
# from collections import deque
# from enum import Enum
#
# GENERAL_DISTANCE_OBJECT_1KM = d = geopy.distance.VincentyDistance(kilometers=1)
#
#
# class Bearing(Enum):
#     top = 0
#     left = 270
#     right = 90
#     down = 180
#
#     @staticmethod
#     def bearing_to_xy_change(bearing: 'Bearing'):
#         if bearing == Bearing.top:
#             return 0, -1
#         elif bearing == Bearing.right:
#             return 1, 0
#         elif bearing == Bearing.left:
#             return -1, 0
#         return 0, 1
#
#     @staticmethod
#     def get_all_bearings():
#         return [Bearing.top, Bearing.right, Bearing.left, Bearing.down]
#
#
# class PixelPosition:
#     def __init__(self,
#                  pixel_val,
#                  location_point: geopy.Point,
#                  image_x: int,
#                  image_y: int):
#         self.pixel_val = pixel_val
#         self.location_point = location_point
#         self.image_x = image_x
#         self.image_y = image_y
#
#     def distance_from_pixel_in_km(self, pixel_position: 'PixelPosition') -> float:
#         return geopy.distance.geodesic(self.location_point, pixel_position.location_point).km
#
#     def __str__(self):
#         return "{},{}".format(self.image_x, self.image_y)
#
#     def __hex__(self):
#         return "{},{}".format(self.image_x, self.image_y)
#
#     @classmethod
#     def from_previous_pixel(cls,
#                             image,
#                             previous_pixel: 'PixelPosition',
#                             direction: Bearing):
#         nx, ny = Bearing.bearing_to_xy_change(direction)
#         nx, ny = nx + previous_pixel.image_x, ny + previous_pixel.image_y
#         new_point = d.destination(point=previous_pixel.location_point, bearing=direction)
#         return PixelPosition(
#             pixel_val=image[nx, ny, :],
#             location_point=new_point,
#             image_x=nx,
#             image_y=ny
#         )
#
#
# class ImageGraph:
#     def __init__(self):
#         pass
#
#     @classmethod
#     def from_preprocessed_image_create_initial_mask_graph(cls,
#                                                           pi: PreprocessedImage) -> 'ImageGraph':
#         return cls.from_preprocessed_image(radar=pi.radar,
#                                            mask=pi.initial_mask)
#
#     @classmethod
#     def from_preprocessed_image(cls,
#                                 radar: Radar,
#                                 mask: np.numpy) -> 'ImageGraph':
#         """
#         Create Image Graph of the radar detection
#         get radar
#         get the required mask
#         create center point
#         from center point run bfs for depth of 240 to create Image Graph
#         :param pi:
#         :return:
#         """
#         # def bfs(graph: nx.Graph,
#         #         pixel_set: Set[PixelPosition]): # BFS should be running about 240, or 239 depth
#
#         center_point = geopy.Point(latitude=radar.latitude, longitude=radar.longitude)
#         center_mask_x = mask.shape[1] // 2
#         center_mask_y = mask.shape[0] // 2
#         center_pp = PixelPosition(pixel_val=mask[center_mask_y, center_mask_x, :],
#                                   location_point=center_point,
#                                   image_x=center_mask_x,
#                                   image_y=center_mask_y)
#         pixel_graph = nx.Graph()
#         # since we start at 240, 240 then  up and left need to be 240 while bottom and right need to be 239, 239
#         # what is the base case for bfs recursion?
#         visited_or_found_set = {center_pp}
#         waiting_list = deque([(center_pp, 240)])
#         pixel_graph.add_node(center_pp.__str__(), data=center_pp)
#         while len(waiting_list) != 0:
#             current, step = waiting_list.popleft()
#             if step == 0:
#                 continue
#             for direction in Bearing.get_all_bearings():
#                 npp = PixelPosition.from_previous_pixel(image=mask,
#                                                         previous_pixel=current,
#                                                         direction=direction)
#                 if npp in visited_or_found_set:
#                     pixel_graph.add_edge(current, npp)
#                     continue
#                 pixel_graph.add_node(, data=center_pp)
#                 pixel_graph.add_edge(current, npp)
#                 visited_or_found_set.add(npp)
#                 waiting_list.append((npp, step - 1))
#         return ImageGraph()
