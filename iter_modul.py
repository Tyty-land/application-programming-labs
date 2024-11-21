import csv
import os


class KeywordPhotoIter:
    """
    This iterator is designed to create a list of names of downloaded files
    works with a file (data.csv) containing absolute and relative paths to files,
    and also with the path to the folder where these files are located
    :param csv_or_dir_path: .csv file or root folder
    """

    def __init__(self, csv_or_dir_path: str, start_or_end: int):
        self.data_keyword = []
        if ".csv" in csv_or_dir_path and csv_or_dir_path != "":
            with open(csv_or_dir_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    self.data_keyword.append(row[1])
                self.data_keyword.pop(0)
        elif csv_or_dir_path != "":
            self.data_keyword = os.listdir((csv_or_dir_path + "/").replace("//", "/"))
            end = len(self.data_keyword)
            i = 0
            while i < end:
                if ".jpg" not in self.data_keyword[i] and ".png" not in self.data_keyword[i]:
                    self.data_keyword.pop(i)
                    end -= 1
                else:
                    i += 1
        if start_or_end == 1:
            self.index = len(self.data_keyword) - 1
        else:
            self.index = 0
        self.limit = len(self.data_keyword)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.limit:
            self.index += 1
            return self.data_keyword[self.index - 1]
        else:
            raise StopIteration

    def next(self):
        self.index += 1
        if self.index < self.limit:
            return self.data_keyword[self.index]
        else:
            raise StopIteration

    def back(self):
        self.index -= 1
        if self.index >= 0:
            return self.data_keyword[self.index]
        else:
            raise StopIteration

    def get_current_size(self):
        return self.limit

    def get_current_index(self):
        return self.index

    def get_elem(self, index: int):
        if 0 <= index < self.limit:
            return self.data_keyword[index]
