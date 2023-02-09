import datetime
from src.radar import Radar, RadarCollection
from src.utils import rgb2hex
from src.color_scheme import AemetColorScheme
import os
from typing import List, Tuple
from PIL import Image
from datetime import datetime
import glob
from pathlib import Path
import numpy as np


class PreprocessedImage:
    mask_color_hexes = {"#0000fc", "#0094fc", "#00fcfc", "#ffff00", "#ffbb00", "#fe7e01", "#ff0000", "#c8065a",
                        "#00e200"}

    def __init__(self,
                 file_path: str,
                 image_taken_at: datetime,
                 radar: Radar):
        self.file_path = file_path
        self.image_taken_at = image_taken_at
        self.radar = radar
        # we dont load these initially to save space
        self.initial_mask = None  # phase 1 input
        self.interference_removed_mask = None  # phase 1 output. phase 2 input?
        self.reconstruction_mask = None  # final output
        self.aemet_color_scheme = None  # we can auto detect this

    def get_base_file_name(self):
        return os.path.basename(self.file_path)

    def set_aemet_color_scheme(self,
                               aemet_color_scheme: AemetColorScheme):
        self.aemet_color_scheme = aemet_color_scheme

    def set_initial_mask(self,
                         initial_mask):
        self.initial_mask = initial_mask

    def set_interference_removed_mask(self,
                                      interference_removed_mask):
        self.interference_removed_mask = interference_removed_mask

    def set_reconstruction_mask(self,
                                reconstruction_mask):
        self.reconstruction_mask = reconstruction_mask

    def load_image(self) -> Image:
        return self._load_image()

    def load_image_as_array(self) -> np.array:
        img = self._load_image()
        img = img.convert('RGB')
        imgarray = np.array(img)
        img.close()
        return imgarray

    def show(self):
        img = self._load_image()
        img.show()
        img.close()

    def _load_image(self) -> Image:
        return Image.open(self.file_path)

    def _generate_circle_mask(self,
                              h,
                              w) -> np.array:
        # implementation based on
        # https://stackoverflow.com/questions/44865023/how-can-i-create-a-circular-mask-for-a-numpy-array
        # TODO: center and radius need to be checked
        center = (int(w / 2), int(h / 2))
        radius = self.radar.radius
        Y, X = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((X - center[0]) ** 2 + (Y - center[1]) ** 2)
        mask = dist_from_center <= radius
        return mask

    def _mask_out_of_circle(self,
                            img: Image) -> np.array:
        img = img.convert("RGB")
        imgarray = np.array(img)
        mask = self._generate_circle_mask(img.height, img.width)
        imgarray[~mask, :] = 255
        img.close()
        return imgarray

    def _mask_out_none_reflection_color(self,
                                        img: Image) -> np.array:
        # if self.aemet_color_scheme is None:
        #     self._generate_aemet_color_scheme()
        img = img.convert("RGB")
        imgarray = np.array(img)
        # there has to be a way better way to do this than a double loop with numpy
        for x in range(img.width):
            for y in range(img.height):
                r, g, b = imgarray[x, y]
                hex = rgb2hex(r, g, b)
                if hex not in PreprocessedImage.mask_color_hexes:
                    imgarray[x, y, :] = 255
        img.close()
        return imgarray

    def _generate_aemet_color_scheme(self):
        """
        TODO: auto detect aemet color scheme in image and assign
        :return:
        """
        img = self._load_image()
        img = img.convert("RGB")
        # 26, 371, 37, 478
        cropped_img = img.crop((26, 371, 37, 478))
        self.set_aemet_color_scheme(AemetColorScheme.from_cropped_image(cropped_img))
        cropped_img.close()

    def generate_initial_mask(self):
        """
        this assume that the image is in aemet format
        :return:
        """
        raw_img = self._load_image()
        cropped_img = raw_img.crop((0, 0, self.radar.radius * 2, self.radar.radius * 2))
        masked_non_reflective_array = self._mask_out_none_reflection_color(cropped_img)
        masked_non_reflective_img = Image.fromarray(masked_non_reflective_array, 'RGB')
        initial_mask_array = self._mask_out_of_circle(masked_non_reflective_img)
        initial_mask = Image.fromarray(initial_mask_array, 'RGB')
        raw_img.close()
        cropped_img.close()
        masked_non_reflective_img.close()
        return initial_mask

    def __str__(self):
        return self.file_path

    def __hash__(self):
        return hash(self.file_path)

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.file_path == other.file_path

    def __lt__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.file_path < other.file_path

    def __gt__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.file_path > other.file_path

    @staticmethod
    def parse_file(file_name: str) -> Tuple[str, str]:
        """
        parse base file name to get radar code name and datetime string  from file name
        maybe use regex instead
        :param file_name:
        :return:
        """
        file_name = os.path.basename(file_name)  # might not work for windows system
        path_obj = Path(file_name)
        extensions = "".join(path_obj.suffixes)
        just_file_name = str(path_obj).replace(extensions, "")
        splitted = just_file_name.split('_')
        if len(splitted) != 3:
            raise Exception('{} is not parsable'.format(just_file_name))
        return splitted[1], splitted[2]

    @classmethod
    def from_file_path_and_radar_collection(cls,
                                            file_path: str,
                                            radar_collection: RadarCollection):
        """
        Given Image and Radar, correctly process it in such a way that u can get a mask up
        :param file_path:
        :param radar_collection:
        :return:
        """
        radar_code, datetime_str = PreprocessedImage.parse_file(file_path)
        radar_dict = radar_collection.to_dict()
        if radar_code not in radar_dict.keys():
            raise Exception("{} radar code is not in radars.yaml".format(radar_code))
        radar = radar_dict[radar_code]
        image_taken_at = datetime.strptime(datetime_str, "%Y%m%d%H%M")
        return PreprocessedImage(
            file_path=file_path,
            image_taken_at=image_taken_at,
            radar=radar
        )


class PreprocessedImageCollection:
    """
    may need to contain the metadata information but i havent think about how yet or what variables to introduce
    """

    def __init__(self,
                 preprocessed_images: List[PreprocessedImage]):
        self.preprocessed_images = preprocessed_images

    def size(self):
        return len(self.preprocessed_images)

    def set_aemet_color_scheme_to_all_images(self,
                                             aemet_color_scheme: AemetColorScheme):
        for pi in self.preprocessed_images:
            pi.set_aemet_color_scheme(aemet_color_scheme)

    def generate_initial_mask_to_all_images(self):
        for pi in self.preprocessed_images:
            pi.generate_initial_mask()

    def get_image(self, index: int):
        return self.preprocessed_images[index]

    def add_another_collection(self,
                               collection: 'PreprocessedImageCollection') -> 'PreprocessedImageCollection':
        """
        add without overlap
        :param collection:
        :return:
        """
        return PreprocessedImageCollection(
            list(set(self.preprocessed_images).union(set(collection.preprocessed_images))))

    def filter_based_on_radar_code(self,
                                   radar_code: str) -> 'PreprocessedImageCollection':

        images = [pi for pi in self.preprocessed_images if pi.radar.rdr_code == radar_code]
        return PreprocessedImageCollection(images)

    def filter_based_on_before_and_after_datetime(self,
                                                  before_dt: datetime,
                                                  after_dt: datetime) -> 'PreprocessedImageCollection':
        images = [pi for pi in self.preprocessed_images if after_dt <= pi.image_taken_at <= before_dt]
        return PreprocessedImageCollection(images)

    def filter_based_on_radar_code_and_time(self,
                                            radar_code: str,
                                            before_dt: datetime,
                                            after_dt: datetime) -> 'PreprocessedImageCollection':
        pic = self.filter_based_on_radar_code(radar_code)
        pic = pic.filter_based_on_before_and_after_datetime(before_dt=before_dt,
                                                            after_dt=after_dt)
        return pic

    @classmethod
    def from_radar_collection_and_aemet_folders_path(cls,
                                                     radar_collection: RadarCollection,
                                                     aemet_folders_path: str) -> 'PreprocessedImageCollection':
        """
        simply get all files --> file name should be in format {aemet}_{location}_{date_time_taken}.gif
        :param radar_collection:
        :param aemet_folders_path:
        :return:
        """
        all_gif_files = glob.glob(aemet_folders_path + '/**/*.gif', recursive=True)
        preprocessed_images = []
        for fname in all_gif_files:
            try:
                preprocessed_images.append(PreprocessedImage.from_file_path_and_radar_collection(file_path=fname,
                                                                                                 radar_collection=radar_collection))
            except Exception as e:
                # TODO: figure out if we need to solve this or print as a check is enough
                print(e)
        return PreprocessedImageCollection(sorted(preprocessed_images))


# not needed because u can just use file name
def get_subdirectory_name_in_directory(d_name: str) -> List[str]:
    return sorted([name for name in os.listdir(d_name) if os.path.isdir(os.path.join(*[d_name, name]))])
