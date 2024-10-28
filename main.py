import csv
import re
import os
from icrawler.builtin import GoogleImageCrawler
from typing import Tuple
import argparse

CONST_activ_dir = os.getcwd().replace("\\", "/").lower() + "/"


class KeywordPhotoIter:
    """
    This iterator is designed to create a list of names of downloaded files
    works with a file (data.csv) containing absolute and relative paths to files,
    and also with the path to the folder where these files are located
    :param data: .csv file or root folder
    """
    def __init__(self, data):
        self.data_keyword = []
        if ".csv" in data:
            with open(data, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    self.data_keyword.append(row[1].split("/")[-1])
                self.data_keyword.pop(0)
        else:
            self.data_keyword = os.listdir(data)
        self.limit = len(self.data_keyword)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.limit:
            self.index += 1
            return self.data_keyword[self.index - 1]
        else:
            raise StopIteration


def create_absolut_dir(save_dir: str) -> str:
    """
    The function checks whether a folder with photos is being created in the new directory of the current directory
    or this folder is located on another disk or in another branch that is not adjacent to this one.
    If the folder should still be located in this directory from where the program is launched, then
    the path to the current directory where the program was launched is appended
    to the path
    :param save_dir: the path to the photo saving folder obtained by the command line parameter
    :return absolut_dir:
    """
    if re.search(r"\w:/", save_dir) is None:
        save_dir = CONST_activ_dir + save_dir
    absolut_dir = (save_dir + "/").replace("//", "/")
    return absolut_dir


def writer_csv(absolut_save_dir: str, file_annotation: str) -> None:
    """
    This function creates a file.csv with information about each downloaded file, namely
    the absolute path to the file and its relative path. There are three columns in a row:
    The Image number, the absolute path of the image, the relative path of the image.
    :param absolut_save_dir: the absolute path to the images
    :param file_annotation: the path and name of the new file .csv
    :return None:
    """
    images = os.listdir(absolut_save_dir)
    data_csv = [["Number image:", "Absolut dir image:", "Relative dir image:"]]
    for image in images:
        relative_save_dir = absolut_save_dir
        if CONST_activ_dir in relative_save_dir:
            relative_save_dir = relative_save_dir.replace(CONST_activ_dir, "/")
        row = [f"{images.index(image) + 1}", f"{absolut_save_dir}/{image}", f"{relative_save_dir}/{image}"]
        data_csv.append(row)
    with open(file_annotation, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        for row in data_csv:
            writer.writerow(row)


def get_p() -> Tuple[str, str, str]:
    """
    A function that accepts command-line parameters, namely:
        -k = keyword to search for a photo (default = "None")
        -sd = path to the future folder with photos (default = "")
        -fa = path and name to the .csv file (default = "data.csv")
    then collects these parameters into a tuple and returns this tuple
    :return res_tuple: a tuple containing all three cmd parameters
    """
    p_cmd = argparse.ArgumentParser()
    p_cmd.add_argument("-k", "--keyword", type=str, help="keyword", default="None")
    p_cmd.add_argument("-sd", "--save_dir", type=str, help="save dir", default="")
    p_cmd.add_argument("-fa", "--file_annotation", type=str, help="Annotation file", default="data.csv")
    args = p_cmd.parse_args()
    res_tuple = (args.keyword, create_absolut_dir(args.save_dir), args.file_annotation)
    return res_tuple


def main() -> None:
    """
    The main function that performs the main work, namely
    uploading 50 photos by keyword(key_word), by a specific path(save_dir)
    and creates an annotation file(file_annotation) with the .csv extension, adding there
    the necessary information(see the description of the write_csv() function).
    The entire photo search is carried out using the methods of the (icrawler) module.
    :return None:
    """
    key_word, save_dir, file_annotation = get_p()
    google_crawl = GoogleImageCrawler(storage={'root_dir': f'{save_dir}image_{key_word}_dir'})
    google_crawl.crawl(keyword=key_word, max_num=10)
    writer_csv(f'{save_dir}image_{key_word}_dir', file_annotation)
    """
    These two lists are needed to check the iterator for two different parameters
    the paths to the root folder with pictures or the path to the annotation file .csv
    should display exactly the same lists in content and size.
    """
    csv_data = []
    for i in KeywordPhotoIter(file_annotation):
        csv_data.append(i)
    dir_data = []
    for i in KeywordPhotoIter(f'{save_dir}image_{key_word}_dir'):
        dir_data.append(i)
    print(csv_data)
    print(dir_data)


if __name__ == '__main__':
    main()
