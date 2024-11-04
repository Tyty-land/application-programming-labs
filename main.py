import argparse
import csv
import cv2
import matplotlib.pyplot as plt
import os
import pandas as pd
import re
import math

from icrawler.builtin import GoogleImageCrawler
from typing import List, Tuple


CONST_activ_dir = os.getcwd().replace("\\", "/").lower() + "/"


def reader_csv(data_frame: str) -> List[list]:
    """
    The function is designed to read data from a
    DataFrame into a new list line by line,
    applying the necessary data transformations for the program
    :param data_frame: The path or name to the DataFrame (.csv)
    :return data_list: List of image data
    """
    with open(data_frame, 'r', encoding='utf-8') as data:
        data_list = data.read().split("\n")
        for i in range(len(data_list)):
            if data_list[i] == "":
                data_list.pop(i)
            else:
                data_list[i] = data_list[i].split(";")
    return data_list


def get_data_imgs(absolut_save_dir: str) -> List[list]:
    """
    The function prepares information about the pictures contained in the corresponding folder,
    according to the task. Creates a list of strings and returns it
    :param absolut_save_dir: The path to the folder with pictures
    :return data_imgs: List of data about images
    """
    images = os.listdir(absolut_save_dir)
    data_imgs = [["Absolute Path:", "Relative path:", "Height:", "Width:", "Color_depth:"]]
    for image in images:
        relative_save_dir = absolut_save_dir
        if CONST_activ_dir in relative_save_dir:
            relative_save_dir = relative_save_dir.replace(CONST_activ_dir, "/")
        img = cv2.imread(f"{absolut_save_dir}/{image}")
        height, width = img.shape[:-1]
        depth_color = math.ceil((os.path.getsize(f"{absolut_save_dir}/{image}")*8)/(height*width))
        row = [f"{absolut_save_dir}/{image}", f"{relative_save_dir}/{image}", height, width, depth_color]
        data_imgs.append(row)
    return data_imgs


def pandas_statistical_calculation(data_frame: str) -> List[list]:
    """
    Pandas statistics on images from the corresponding DataFrame.
    The data is arranged in a certain order
    :param data_frame: The path or name to the DataFrame (.csv)
    :return statistical_list: List of statistical data
    """
    data_imgs = reader_csv(data_frame)
    writer_csv(data_imgs, 'data_frame_pandas.csv', 1)
    df = pd.read_csv('data_frame_pandas.csv', delimiter=';', names=data_imgs[0])
    statistical_list = [[df['Height:'].count(),
                         df['Height:'].sum(),
                         df['Height:'].mean(),
                         df['Height:'].median(),
                         df['Height:'].min(),
                         df['Height:'].max(),
                         df['Height:'].mode(),
                         df['Height:'].abs(),
                         df['Height:'].prod(),
                         df['Height:'].std(),
                         df['Height:'].var(),
                         df['Height:'].sem(),
                         df['Height:'].skew(),
                         df['Height:'].kurt(),
                         df['Height:'].quantile(),
                         df['Height:'].cumsum(),
                         df['Height:'].cumprod(),
                         df['Height:'].cummax(),
                         df['Height:'].cummin()
                         ],
                        [df['Width:'].count(),
                         df['Width:'].sum(),
                         df['Width:'].mean(),
                         df['Width:'].median(),
                         df['Width:'].min(),
                         df['Width:'].max(),
                         df['Width:'].mode(),
                         df['Width:'].abs(),
                         df['Width:'].prod(),
                         df['Width:'].std(),
                         df['Width:'].var(),
                         df['Width:'].sem(),
                         df['Width:'].skew(),
                         df['Width:'].kurt(),
                         df['Width:'].quantile(),
                         df['Width:'].cumsum(),
                         df['Width:'].cumprod(),
                         df['Width:'].cummax(),
                         df['Width:'].cummin()
                         ],
                        [df['Color_depth:'].count(),
                         df['Color_depth:'].sum(),
                         df['Color_depth:'].mean(),
                         df['Color_depth:'].median(),
                         df['Color_depth:'].min(),
                         df['Color_depth:'].max(),
                         df['Color_depth:'].mode(),
                         df['Color_depth:'].abs(),
                         df['Color_depth:'].prod(),
                         df['Color_depth:'].std(),
                         df['Color_depth:'].var(),
                         df['Color_depth:'].sem(),
                         df['Color_depth:'].skew(),
                         df['Color_depth:'].kurt(),
                         df['Color_depth:'].quantile(),
                         df['Color_depth:'].cumsum(),
                         df['Color_depth:'].cumprod(),
                         df['Color_depth:'].cummax(),
                         df['Color_depth:'].cummin()
                         ]]
    os.remove('data_frame_pandas.csv')
    return statistical_list


def create_absolut_dir(save_dir: str) -> str:
    """
    The function checks whether a folder with photos is being created in the new directory of the current directory
    or this folder is located on another disk or in another branch that is not adjacent to this one.
    If the folder should still be located in this directory from where the program is launched, then
    the path to the current directory where the program was launched is appended
    to the path
    :param save_dir: the path to the photo saving folder obtained by the command line parameter
    :return absolut_dir: The absolute path to the corresponding file or folder
    """
    if re.search(r"\w:/+", save_dir) is None and re.search(r"\w:\\+", save_dir) is None:
        save_dir = CONST_activ_dir + save_dir
    if re.search(r"\.\w+", save_dir) is None:
        absolut_dir = (save_dir + "/").replace("\\", "/").replace("//", "/")
        return absolut_dir
    else:
        absolut_dir = save_dir.replace("\\", "/").replace("//", "/")
        return absolut_dir


def writer_csv(data_imgs: List[list], data_frame: str, index_start: int) -> None:
    """
    This function creates a DataFrame of images in the format (.csv)
    according to the appropriate parameters,
    namely the list of image data, the path and name to the future
    DataFrame and the index number in the list of image data
    from which you will need to start entering data
    :param data_imgs: List of image data
    :param data_frame: The path or name to the DataFrame (.csv)
    :param index_start: Starting index
    :return None:
    """
    if index_start < len(data_imgs):
        with open(data_frame, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            for i_row in range(index_start, len(data_imgs)):
                writer.writerow(data_imgs[i_row])


def get_p() -> Tuple[str, str, str]:
    """
     A function that accepts command-line parameters, namely:
        -k = keyword to search for a photo (default = "None")
        -sd = path to the future folder with photos (default = "")
        -D = path and name to the .csv DataFrame (default = "DataFrame.csv")
    then collects these parameters into a tuple and returns this tuple
    :return res_tuple: a tuple containing all three cmd parameters
    """
    p_cmd = argparse.ArgumentParser()
    p_cmd.add_argument("-k", "--keyword", type=str, help="keyword", default="None")
    p_cmd.add_argument("-sd", "--save_dir", type=str, help="save dir", default="")
    p_cmd.add_argument("-D", "--data_frame", type=str, help="data frame file", default="DataFrame.csv")
    args = p_cmd.parse_args()
    res_tuple = (args.keyword, create_absolut_dir(args.save_dir), create_absolut_dir(args.data_frame))
    return res_tuple


def main() -> None:
    """
    The main function that performs the main logic of the program.
    The commented part is needed to verify the data obtained
    using Pandas
    :return None:
    """
    key_word, save_dir, data_frame = get_p()
    google_crawl = GoogleImageCrawler(storage={'root_dir': f'{save_dir}image_{key_word}_dir'})
    google_crawl.crawl(keyword=key_word, max_num=50)
    writer_csv(get_data_imgs(f'{save_dir}image_{key_word}_dir'), data_frame, 0)
    pd_st = pandas_statistical_calculation(data_frame)
    # for i in range(len(pd_st)):
    #     for j in range(len(pd_st[i])):
    #         print(pd_st[i][j], "\n")
    data_frame_filter(data_frame, int(pd_st[0][5]), int(pd_st[1][5]))
    sort_square_images(data_frame)
    display_histogram(data_frame, 5)


def data_frame_filter(data_frame: str, height_max: int, width_max: int) -> None:
    """
    A function from the task that filters the data in the DataFrame by
    the width and height of the images. Overwrite the entire file with the DataFrame,
    that is, creates a new DataFrame that will already be filtered
    :param data_frame: The path or name to the DataFrame (.csv)
    :param height_max: Information from Pandas about the maximum height
    :param width_max: Information from Pandas about the maximum width
    :return None:
    """
    data_imgs = reader_csv(data_frame)
    os.remove(data_frame)
    i = 1
    end = len(data_imgs)
    while i < end:
        if int(data_imgs[i][2]) > height_max or int(data_imgs[i][3]) > width_max:
            data_imgs.pop(i)
            end -= 1
        else:
            i += 1
    writer_csv(data_imgs, data_frame, 0)


def sort_square_images(data_frame: str) -> None:
    """
    The function adds a new column of information about each image - the area of the image.
    At the same time, it sorts from a smaller area to a larger one. The DataFrame is being overwritten
    :param data_frame: The path or name to the DataFrame (.csv)
    :return None:
    """
    data_imgs = reader_csv(data_frame)
    os.remove(data_frame)
    data_imgs[0].append("Square:")
    for i_row in range(1, len(data_imgs)):
        data_imgs[i_row].append(str(int(data_imgs[i_row][2]) * int(data_imgs[i_row][3])))
    writer_csv(sort_data(data_imgs, 5), data_frame, 0)


def sort_data(data_imgs: List[list], i_sort_param: int) -> List[list]:
    """
    A function for sorting a two-dimensional array by parameter.
    Taking the second index of the parameter,
    it is fully sorted from the smallest to the largest,
    counting from the beginning of the list
    :param data_imgs: List of image data
    :param i_sort_param: The second index of the list item
    :return data_imgs: List of image data (SORT)
    """
    x = 2
    while x < len(data_imgs):
        if int(data_imgs[x][i_sort_param]) < int(data_imgs[x - 1][i_sort_param]):
            y = x
            while int(data_imgs[y][i_sort_param]) < int(data_imgs[y - 1][i_sort_param]):
                tmp = data_imgs[y]
                data_imgs[y] = data_imgs[y - 1]
                data_imgs[y - 1] = tmp
                y -= 1
                if y == 1:
                    x = 2
                    break
                x = y
        x += 1
    return data_imgs


def display_histogram(data_frame: str, i_sort_param: int) -> None:
    """
    The function is needed to display a histogram for a specific parameter.
    The parameter is selected the same as when sorting (sort_data)
    :param data_frame: The path or name to the DataFrame (.csv)
    :param i_sort_param: The second index of the list item
    :return None:
    """
    data_imgs = reader_csv(data_frame)
    x = []
    for i in range(1, len(data_imgs)):
        x.append(int(data_imgs[i][i_sort_param]))
    plt.figure(figsize=(10, 5))
    plt.hist(x)
    plt.title(f"Гистограмма площадей картинок")
    plt.xlabel('Площадь')
    plt.ylabel('Кол-во картинок')
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.show()


if __name__ == '__main__':
    main()
