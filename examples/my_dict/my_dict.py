from collections import namedtuple
from collections.abc import Iterable
from enum import StrEnum
from typing import Any

Protected_fields = namedtuple("Protected_fields", ["current", "next"])


class Permission(StrEnum):
    """Enumeration of permission names."""
    READ = "read"
    CHANGE = "change"
    ADD = "add"
    DELETE = "delete"


class ProtectedError(Exception):
    """Error called where you try to get access to protected attribute."""


class ViaDotDict:
    """Representation dictionary as class with parametrize access policy.

    The class accept the dictionary as input and provides access to its
    elements via “.” (dot).

    """

    def __init__(
        self,
        dict_data: dict[str, Any],
        access_params: dict[Permission, bool],
        protected: Iterable[str] | None = None,
    ):
        """Constructor for ViaDotDict class.

        Args:
            dict_data: Dictionary based class.
            access_params: Params contains access permissions.
            protected: The list of protected fields.

        """
        current_protected, next_protected = ViaDotDict._split_protected(
            protected,
        )
        formed_dict_data = self._set_input_dict_data(
            dict_data,
            access_params,
            next_protected,
        )

        super().__setattr__("_access_params", access_params)
        super().__setattr__("_protected", current_protected)
        super().__setattr__("_dict_data", formed_dict_data)

    @staticmethod
    def _split_protected(
        protected: Iterable[str] | None,
    ) -> Protected_fields:
        """Split list of protected field."""
        next_protected = []
        current_protected = []

        protected = protected or []
        for field in protected:
            current_field, *inner_fields = field.split(".", maxsplit=1)
            next_protected.extend(inner_fields)
            current_protected.append(current_field)

        return Protected_fields(current_protected, next_protected)

    def _set_input_dict_data(
        self,
        data: dict[str, Any],
        access_params: dict[Permission, bool],
        protected: Iterable[str],
    ) -> dict[str, Any]:
        """Put input dict to class data."""
        dict_data = {}
        for attribute, value in data.items():
            if not isinstance(value, dict):
                dict_data[attribute] = value
            else:
                dict_data[attribute] = ViaDotDict(
                    value,
                    access_params,
                    protected,
                )

        return dict_data

    def _raise_for_protected(self, attr_name: str) -> None:
        """Raise ProtectedError if attribute is protected."""
        if attr_name in self._protected:
            raise ProtectedError(f"attribute {attr_name} is forbidden.")

    def _raise_for_access(self, action: str) -> None:
        """Raise unconfirmed access."""
        if not self._access_params.get(action):
            raise ProtectedError(
                f"{self.__class__.__name__} has no access for {action}.",
            )

    def __getattr__(self, name: str) -> Any:
        """Getter for class attributes."""
        self._raise_for_access(Permission.READ)
        self._raise_for_protected(name)

        return self._dict_data[name]

    def __setattr__(self, name: str, value: Any) -> None:
        """Setter for class attributes."""
        if name in self._dict_data:
            self._raise_for_access(Permission.CHANGE)
            self._raise_for_protected(name)
        else:
            self._raise_for_access(Permission.ADD)

        self._dict_data[name] = value

    def __delattr__(self, name: str) -> None:
        """Deleter for class attributes."""
        self._raise_for_access(Permission.DELETE)
        self._raise_for_protected(name)

        del self._dict_data[name]


def dict_factory(
    dict_data: dict[str, Any],
    read: bool = True,
    change: bool = True,
    add: bool = True,
    delete: bool = True,
    protected: Iterable[str] | None = None,
) -> ViaDotDict:
    """Factory for ViaDotDict class."""
    access_params = {
        Permission.READ: read,
        Permission.CHANGE: change,
        Permission.ADD: add,
        Permission.DELETE: delete,
    }
    return ViaDotDict(dict_data, access_params, protected)
