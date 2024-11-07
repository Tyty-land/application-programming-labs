import csv
import os


class KeywordPhotoIter:
    """
    This iterator is designed to create a list of names of downloaded files
    works with a file (data.csv) containing absolute and relative paths to files,
    and also with the path to the folder where these files are located
    :param csv_or_dir_path: .csv file or root folder
    """

    def __init__(self, csv_or_dir_path: str):
        self.data_keyword = []
        if ".csv" in csv_or_dir_path:
            with open(csv_or_dir_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    self.data_keyword.append(row[1].split("/")[-1])
                self.data_keyword.pop(0)
        else:
            self.data_keyword = os.listdir(csv_or_dir_path)
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
