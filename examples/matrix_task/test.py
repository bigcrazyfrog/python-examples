import pytest
from matrix import DifferentSizeException, Matrix, Size
from pytest_lazyfixture import lazy_fixture


@pytest.fixture
def first_square_matrix() -> Matrix:
    """Fixture for square matrix."""
    return Matrix([
        [1, 2],
        [3, 4],
    ])


@pytest.fixture
def second_square_matrix() -> Matrix:
    """Fixture for square matrix."""
    return Matrix([
        [1, 1],
        [0, 1],
    ])


@pytest.fixture
def two_four_matrix() -> Matrix:
    """Fixture for matrix with two rows and four columns."""
    return Matrix([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
    ])


@pytest.fixture
def four_two_matrix() -> Matrix:
    """Fixture for matrix with four rows and two columns."""
    return Matrix([
        [1, 2],
        [3, 4],
        [5, 6],
        [7, 8],
    ])


@pytest.mark.parametrize(
    ["first_matrix", "second_matrix", "expected"],
    [
        [
            lazy_fixture("first_square_matrix"),
            lazy_fixture("second_square_matrix"),
            [
                [2, 3],
                [3, 5],
            ],
        ],
        [
            lazy_fixture("second_square_matrix"),
            lazy_fixture("second_square_matrix"),
            [
                [2, 2],
                [0, 2],
            ],
        ],
    ],
)
def test_matrix_sum(
    first_matrix: Matrix,
    second_matrix: Matrix,
    expected: list[list[int]],
):
    """Test sum of matrix."""
    matrix_sum = first_matrix + second_matrix
    assert matrix_sum.data == expected


def test_sum_matrix_with_different_size(
    first_square_matrix: Matrix,
    two_four_matrix: Matrix,
):
    """Test sum of matrix with different size."""
    with pytest.raises(DifferentSizeException):
        first_square_matrix + two_four_matrix


@pytest.mark.parametrize(
    ["matrix", "size"],
    [
        [
            lazy_fixture("first_square_matrix"),
            (2, 2),
        ],
        [
            lazy_fixture("two_four_matrix"),
            (2, 4),
        ],
    ],
)
def test_matrix_size(
    matrix: Matrix,
    size: Size,
):
    """Test get size of matrix."""
    assert matrix.size == size


@pytest.mark.parametrize(
    ["matrix", "number", "expected"],
    [
        [
            lazy_fixture("two_four_matrix"),
            2,
            [
                [2, 4, 6, 8],
                [10, 12, 14, 16],
            ],
        ],
        [
            lazy_fixture("first_square_matrix"),
            4,
            [
                [4, 8],
                [12, 16],
            ],
        ],
        [
            lazy_fixture("first_square_matrix"),
            1,
            [
                [1, 2],
                [3, 4],
            ],
        ],
        [
            lazy_fixture("first_square_matrix"),
            0,
            [
                [0, 0],
                [0, 0],
            ],
        ],
    ],
)
def test_matrix_by_number_mul(
    matrix: Matrix,
    number: int,
    expected: list[list[int]],
):
    """Test multiplication matrix by number."""
    result = matrix * number
    assert result.data == expected

    result = number * matrix
    assert result.data == expected


@pytest.mark.parametrize(
    ["first_matrix", "second_matrix", "expected"],
    [
        [
            lazy_fixture("first_square_matrix"),
            lazy_fixture("second_square_matrix"),
            [
                [1, 3],
                [3, 7],
            ],
        ],
        [
            lazy_fixture("two_four_matrix"),
            lazy_fixture("four_two_matrix"),
            [
                [50, 60],
                [114, 140],
            ],
        ],
        [
            lazy_fixture("four_two_matrix"),
            lazy_fixture("two_four_matrix"),
            [
                [11, 14, 17, 20],
                [23, 30, 37, 44],
                [35, 46, 57, 68],
                [47, 62, 77, 92],
            ],
        ],
    ],
)
def test_matrix_by_matrix_mul(
    first_matrix,
    second_matrix,
    expected: list[list[int]],
):
    """Test multiplication matrix by matrix."""
    result = first_matrix @ second_matrix
    assert result.data == expected


@pytest.mark.parametrize(
    ["matrix", "expected"],
    [
        [
            lazy_fixture("first_square_matrix"),
            [
                [1, 3],
                [2, 4],
            ],
        ],
        [
            lazy_fixture("second_square_matrix"),
            [
                [1, 0],
                [1, 1],
            ],
        ],
    ],
)
def test_matrix_transposing(
    matrix: Matrix,
    expected: list[list[int]],
):
    """Test transposing of matrix."""
    assert matrix.T().data == expected


@pytest.mark.parametrize(
    ["matrix", "power", "expected"],
    [
        [
            lazy_fixture("first_square_matrix"),
            4,
            [
                [199, 290],
                [435, 634],
            ],
        ],
        [
            lazy_fixture("second_square_matrix"),
            8,
            [
                [1, 8],
                [0, 1],
            ],
        ],
        [
            lazy_fixture("first_square_matrix"),
            1,
            [
                [1, 2],
                [3, 4],
            ],
        ],
    ],
)
def test_matrix_power(
    matrix: Matrix,
    power: int,
    expected: list[list[int]],
):
    """Test power of matrix."""
    result = matrix ** power
    assert result.data == expected


def test_incorrect_power_matrix(
    first_square_matrix: Matrix,
):
    """Test incorrect power of matrix."""
    with pytest.raises(ValueError):  # noqa: PT011
        first_square_matrix ** -2


@pytest.mark.parametrize(
    ["matrix", "expected"],
    [
        [
            lazy_fixture("first_square_matrix"),
            [
                [-1, -2],
                [-3, -4],
            ],
        ],
        [
            lazy_fixture("second_square_matrix"),
            [
                [-1, -1],
                [0, -1],
            ],
        ],
    ],
)
def test_unary_minus_of_matrix(
    matrix: Matrix,
    expected: list[list[int]],
):
    """Test unary minus of matrix."""
    result = -matrix
    assert result.data == expected
