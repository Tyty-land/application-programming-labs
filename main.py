import argparse
import re
from typing import Tuple, List


def main() -> None:
    """
    This function is the main one. The find() function is called in it.
    Exception handling is also present
    :return: None:
    """
    try:
        file_name, gender, letter = get_p()
        profiles = split(file_reader(file_name))
        print(find(profiles, gender, letter))
    except Exception as exc:
        print(exc)


def get_p() -> Tuple[str, str, str]:
    """
    get_p() is designed for parsing command-line parameters and then grouping them into a tuple(res_tuple),
     which is subsequently output as the result of this function
    :return: res_tuple:
    """
    p_cmd = argparse.ArgumentParser()
    p_cmd.add_argument("-f", "--file", type=str, help="file name")
    p_cmd.add_argument("-g", "--gender", type=str, help="Male/Female")
    p_cmd.add_argument("-l", "--letter", type=str, help="One Letter")
    args = p_cmd.parse_args()
    res_tuple = (args.file, args.gender, args.letter)
    return res_tuple


def file_reader(file_name: str) -> str:
    """
    This function opens a file by its path
    or name(file_name)
    and enters the contents into a string(result_string).
    If it is impossible to find the file, it displays an error
    :param file_name: path or name
    :return: result_string: file content
    """
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            result_string = file.read()
        return result_string
    except FileNotFoundError:
        raise FileNotFoundError("Звуки сирены: Файла с таким именем не существует")
    except PermissionError:
        raise PermissionError("Звуки сирены: Нет прав доступа к данному файлу")


def split(string: str) -> List[str]:
    """
    This function divides the string
    into separate questionnaire lines and enters them
    into an array (list), assigning the corresponding number
    :param string: any str
    :return: list:
    """
    profiles = re.split(r"\d+\)\n", string)
    del profiles[0]
    for i in range(len(list)):
        profiles[i] = str(i + 1) + ")\n" + profiles[i]
    return profiles


def find(profiles: list, gender: str, letter: str) -> List[str]:
    """
    The search function by parameters. Finds
    suitable questionnaires from the profiles list by the corresponding gender
    and letter/combination at the beginning of the name(letter)
    and outputs an array with the names found in these questionnaires (name_list)
    :param profiles:
    :param gender:
    :param letter:
    :return: None:
    """
    name_list = []
    for profile in profiles:
        if (re.search(r"Пол:\s+" + gender, profile) is not None
                and re.search(r"Имя:\s+" + letter, profile) is not None):
            tmp_1 = re.findall(r"Имя:\s+\w+\n", profile)
            tmp_2 = re.split(r":\s+", tmp_1[0])
            if tmp_2[1][:-1] not in name_list:
                name_list.append(tmp_2[1][:-1])
    return name_list


if __name__ == '__main__':
    main()
    print()
