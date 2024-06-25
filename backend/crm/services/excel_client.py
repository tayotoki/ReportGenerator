from typing import Literal

import pathlib
import pandas as pd
from abc import ABC
from typing import Generator, Optional, Sequence
from collections.abc import Sequence as SequenceNotStr
from typing import Hashable


class BaseExcelClient(ABC):
    """Базовый загрузчик xlsx файлов"""

    engine: Literal["xlrd", "openpyxl", "odf", "pyxlsb", "calamine"] = "openpyxl"

    def __init__(self, path: pathlib.Path, sheet_names: Optional[str] = None) -> None:
        self.path = path
        self.sheets = sheet_names

    @property
    def file(self) -> pd.ExcelFile:
        """Файл для парсинга в датафреймы pandas"""

        return pd.ExcelFile(self.path, engine=self.engine)

    @property
    def sheets_list(self) -> list[str]:
        """Список страниц документа"""

        with self.file:
            if isinstance(self.sheets, str):
                return [
                    sheet for sheet in self.file.sheet_names
                    if sheet in self.sheets
                ]
            return self.file.sheet_names

    def _get_header(self, sheet: str, header: int = 0) -> list:
        """Получение заголовков из первого ряда таблицы"""

        with self.file as xlsx:
            df: pd.DataFrame = xlsx.parse(sheet, engine=self.engine, header=header, nrows=1)
            return df.columns.tolist()

    def _get_columns_by_names(self, sheet: str, names: SequenceNotStr[Hashable]) -> list:
        """Получение ячеек `usecols` по именам заголовков"""

        headers = self._get_header(sheet)
        usecols = [i for i, col in enumerate(headers) if col in names]
        return usecols

    def get_tables(
        self,
        names: Optional[SequenceNotStr[Hashable]] = None,
        header: Optional[int] = 0,
    ) -> Generator[pd.DataFrame, None, None]:
        """Получение таблиц по каждому/переданному листу документа"""

        with self.file as xlsx:
            for sheet in self.sheets_list:
                usecols = None
                if names:
                    usecols = self._get_columns_by_names(sheet, names)

                table: pd.DataFrame = xlsx.parse(
                    sheet,
                    engine=self.engine,
                    header=header,
                    usecols=usecols,
                )
                yield table
