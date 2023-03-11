import matplotlib.pyplot as plt
from src.preprocessed_image import PreprocessedImage


def show_preprocessed_image(pi: PreprocessedImage):
    plt.figure()
    plt.imshow(pi.load_image_as_array())  # imshow expect BGR [..., ::-1]
    plt.title("Raw image of {}".format(pi.get_base_file_name()))
