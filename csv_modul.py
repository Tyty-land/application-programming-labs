import csv
import os
import re


CONST_activ_dir = os.getcwd().replace("\\", "/").lower() + "/"


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

