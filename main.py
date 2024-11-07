import argparse
from iter_modul import KeywordPhotoIter
from csv_modul import writer_csv
from csv_modul import create_absolut_dir

from icrawler.builtin import GoogleImageCrawler
from typing import Tuple


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
    iter_checker(file_annotation, f'{save_dir}image_{key_word}_dir')


def iter_checker(file_annotation: str, root_dir: str) -> None:
    """
    This function is designed to demonstrate the operation of the iterator in two parameters,
     namely, the annotation file .csv or the root folder where all images are saved
    :param file_annotation: The path or name of the annotation file .csv
    :param root_dir: The root folder with images
    :return None:
    """
    csv_data = []
    for i in KeywordPhotoIter(file_annotation):
        csv_data.append(i)
    dir_data = []
    for i in KeywordPhotoIter(root_dir):
        dir_data.append(i)
    print(csv_data)
    print(dir_data)


if __name__ == '__main__':
    main()
