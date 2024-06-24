from abc import abstractmethod, ABC
from collections.abc import Mapping, AsyncIterator
from typing import Coroutine, Optional


class BaseConverter(Mapping):
    """
    Базовый конвертер данных
    """

    FIELDS_MAPPER: dict[str, str]
    UPDATE_FIELDS: list[str]

    def __init__(self, api_data, action="create", **kwargs):
        self._data = api_data
        self._action = action
        self._extra = kwargs
        self._clean_data = self.get_clean_data()

    @abstractmethod
    def cleanup_create_data(self):
        """
        Очистка данных перед созданием объекта
        """

    @abstractmethod
    def cleanup_update_data(self):
        """
        Очистка данных перед обновлением объекта
        """

    def get_cleanup_method(self):
        """
        Получение метода очистки данных
        """

        cleanup_methods = {
            "create": self.cleanup_create_data,
            "update": self.cleanup_update_data,
        }

        return cleanup_methods.get(self._action)

    def get_clean_data(self):
        cleanup_method = self.get_cleanup_method()
        if cleanup_method is None or not callable(cleanup_method):
            raise NotImplementedError("action не реализован")
        return cleanup_method()

    @property
    def data(self):
        """
        Сырые данные
        """

        return self._data

    @property
    def clean_data(self):
        """
        Очищенные данные
        """

        return self._clean_data

    def __iter__(self):
        return iter(self.clean_data)

    def __getitem__(self, item):
        return self.clean_data[item]

    def __len__(self):
        return len(self.clean_data)

    def __repr__(self):
        return repr(self.clean_data)
