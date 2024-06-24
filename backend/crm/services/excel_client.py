import pathlib
from abc import ABC, abstractmethod
from collections.abc import Generator, Hashable
from typing import Literal, Optional

import pandas as pd
from pandas import DataFrame
from pandas._typing import SequenceNotStr


class BaseExcelClient(ABC):
    """Базовый загрузчик xlsx файлов"""

    engine: Literal["xlrd", "openpyxl", "odf", "pyxlsb", "calamine"] = "openpyxl"

    def __init__(self, path: pathlib.Path, sheet_names: Optional[str] = None) -> None:
        self.path = path
        self.sheets = sheet_names

    @property
    def file(self) -> pd.ExcelFile:
        """Файл для парсинга в датафреймы pandas"""

        return pd.ExcelFile(self.path)

    @property
    def sheets_list(self) -> list[str]:
        """Список страниц документа"""

        with self.file:
            match self.sheets:
                case str(self.sheets) as sheet_names:
                    return [
                        sheet for sheet in self.file.sheet_names
                        if sheet in sheet_names
                    ]
                case _:
                    return self.file.sheet_names

    def get_tables(
        self,
        names: Optional[SequenceNotStr[Hashable]] = None,
        header: Optional[bool] = None,
    ) -> Generator[DataFrame, None, None]:
        """Получение таблиц по каждому/переданному листу документа"""

        with self.file as xlsx:
            for sheet in self.sheets_list:
                names = names if names else None
                header = header if header else None
                yield xlsx.parse(
                    sheet,
                    engine=self.engine,
                    header=header,
                    names=names,
                )
