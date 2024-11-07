import csv
import os
import pandas as pd

from typing import List

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
