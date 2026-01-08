"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table. each table is made of:
        {name: [type, kind, index]}"""
        self.class_t: typing.Dict[str, typing.List] = {}
        self.subroutine_t: typing.Dict[str, typing.List] = {}
        self.idx_counts = {
            'STATIC': 0,
            'FIELD': 0,
            'ARG': 0,
            'VAR': 0,
        }

    def start_subroutine(self, is_method: bool = False) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table). is_method flag mean the first pushed argument to the
        table in Argument 0 is THIS implicitly, then we need to start the index
        of ARG from 1 instead of 0
        """
        self.subroutine_t.clear()
        if is_method:
            self.idx_counts['ARG'] = 1  # in methods arg 0 is THIS
        else:
            self.idx_counts['ARG'] = 0
        self.idx_counts['VAR'] = 0

    def define(self, name: str, var_type: str, var_kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        kind = var_kind.upper()
        if kind not in self.idx_counts:
            raise ValueError(f"Unknown kind: {kind}")

        idx = self.idx_counts[kind]
        self.idx_counts[kind] += 1
        entry = [var_type, kind, idx]
        if kind in ('STATIC', 'FIELD'):  # class arguments
            self.class_t[name] = entry
        else:  # ARG or VAR - subroutine arguments
            self.subroutine_t[name] = entry

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        counter: int = 0
        if kind in ["STATIC", "FIELD"]:
            for name, lst in self.class_t.items():
                if kind in lst:
                    counter += 1
            return counter
        else:
            for name, lst in self.subroutine_t.items():
                if kind in lst:
                    counter += 1
            return counter

    def kind_of(self, name: str) -> typing.Union[str, None]:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        if name in self.subroutine_t:
            return self.subroutine_t[name][1]  # lst = [type, kind, idx]
        elif name in self.class_t:
            return self.class_t[name][1]
        else:
            return None

    def type_of(self, name: str) -> typing.Union[str, None]:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        if name in self.subroutine_t:
            return self.subroutine_t[name][0]  # lst = [type, kind, idx]
        elif name in self.class_t:
            return self.class_t[name][0]
        else:
            return None

    def index_of(self, name: str) -> typing.Union[int, None]:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        if name in self.subroutine_t:
            return self.subroutine_t[name][2]  # lst = [type, kind, idx]
        elif name in self.class_t:
            return self.class_t[name][2]
        else:
            return None
