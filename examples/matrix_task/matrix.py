from __future__ import annotations

from collections import namedtuple
from collections.abc import Sequence
from typing import TypeAlias

Number: TypeAlias = int | float
Size = namedtuple("Size", ["rows_num", "columns_num"])


class DifferentSizeException(Exception):
    """Raise if matrices have different size."""


class Matrix:
    """Class for matrix computations.

    Provide the following matrix operations:
     - addition or subtraction
     - multiplication of two matrices
     - multiplication of matrix and a number
     - matrix transposing
     - dimensions check

    Attributes:
        rows_num: Get number of rows.
        columns_num: Get number of columns.
        size: Get size of matrix.
        T: Get matrix transposition.

    """

    def __init__(self, data: Sequence[Sequence[Number]]):
        """Constructor for Matrix class.

        Args:
            data: Matrix in the form of nested number sequences.

        """
        if len(set(map(len, data))) != 1:
            # Rows should have the same length because
            # the matrix is rectangle.
            raise DifferentSizeException(
                "Rows should have the same length.",
            )

        self.data = data

    @property
    def rows_num(self) -> int:
        return len(self.data)

    @property
    def columns_num(self) -> int:
        return len(self.data[0])

    @property
    def size(self) -> Size:
        """Get size of matrix."""
        return Size(self.rows_num, self.columns_num)

    def T(self) -> Matrix:
        """Get matrix transposition."""
        if self.rows_num != self.columns_num:
            raise DifferentSizeException(
                "Matrix should be square.",
            )

        return Matrix(
            [
                [
                    self[row_idx][col_idx] for row_idx in range(self.rows_num)
                ] for col_idx in range(self.columns_num)
            ],
        )

    def __matmul__(self, other_matrix: Matrix) -> Matrix:
        """Get multiplication matrix by matrix.

        Raises:
            DifferentSizeException: If the number of columns in the first
            matrix is not equal to the number of rows in the second matrix.

        """
        if other_matrix.rows_num != self.columns_num:
            raise DifferentSizeException(
                "the first matrix must have the same number "
                "of columns as the second matrix has rows",
            )

        result = [
            [
                sum(
                    row_elem * column_elem
                    for row_elem, column_elem in zip(row, column)
                )
                for column in zip(*other_matrix.data)
            ]
            for row in self.data
        ]

        return Matrix(result)

    def __mul__(self, number: Number) -> Matrix:
        """Get multiplication matrix by number."""
        return Matrix(
            [
                [elem * number for elem in rows]
                for rows in self.data
            ],
        )

    def __rmul__(self, number: Number) -> Matrix:
        """Get reflected multiplication."""
        return self.__mul__(number)

    def __getitem__(self, index: int) -> Sequence[Number]:
        """Get row by index.

        It is needed for getting elements by two indexes without call
        data attribute.

        """
        return self.data[index]

    def __add__(self, matrix: Matrix) -> Matrix:
        if self.size != matrix.size:
            # One matrix can be added to another matrix only if they have
            # the same dimensions.
            raise DifferentSizeException(
                "Matrices should have the same size.",
            )

        return Matrix(
            [
                [
                    self[row_idx][col_idx] + matrix[row_idx][col_idx]
                    for col_idx in range(self.columns_num)
                ] for row_idx in range(self.rows_num)
            ],
        )

    def __repr__(self) -> str:
        """Convert matrix to string."""
        return f"{self.__class__.__name__}({self.data})"

    def __str__(self) -> str:
        """Convert matrix to string."""
        return "\n".join(map(str, self.data))

    def __neg__(self) -> Matrix:
        """Unary minus operator."""
        return -1 * self

    def __sub__(self, matrix: Matrix) -> Matrix:
        """Binary minus operator."""
        return -matrix + self

    def __pow__(self, power: int) -> Matrix:
        """Positive pow of matrix use fast exponentiation algorithm.

        Raises:
            ValueError: Raise if power isn't positive.

        """
        if power <= 0:
            raise ValueError("Power must be positive.")

        result = Matrix(self.data)
        last_matrix = Matrix(self.data)

        power -= 1

        while power > 0:
            if power % 2:
                result @= last_matrix
            last_matrix @= last_matrix
            power //= 2

        return result
