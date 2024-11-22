import re

class TextPreprocesser:
  def __init__(self, text: str) -> None:
    self.__text = text.lower()
    self.__regex_for_ukrainian_words = r"\b[А-Яа-яїЇєЄЮюґҐіІ'`’-]+"
    self.__regex_for_abriviantions = r"[А-ЯЇЄЮҐІ'`’-]{2,}"
    self.__regex_for_wordes_removed_to_another_line = r'-\s+'
    self.abriviation_list = self.__get_abriviations()

  def __get_abriviations(self) -> list:
    abriviation_list = re.findall(self.__regex_for_abriviantions, self.__text)
    return abriviation_list

  def get_normalised_text(self) -> str:
    text_without_abriviations = re.sub(self.__regex_for_abriviantions, '', self.__text)
    ukrainian_words = re.findall(self.__regex_for_ukrainian_words, text_without_abriviations)
    tetx_with_ukrainian_words = ' '.join(ukrainian_words)
    normalised_text = re.sub(self.__regex_for_wordes_removed_to_another_line, '', tetx_with_ukrainian_words)
    return normalised_text