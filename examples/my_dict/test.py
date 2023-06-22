import pytest
from my_dict import ProtectedError, ViaDotDict, dict_factory

test_dict = {
    "name": "dict",
    "number": 1,
    "info": {
        "data": "no data",
        "len": 3,
    },
}


@pytest.fixture
def normal_dict():
    """Usually dict fixture."""
    return dict_factory(test_dict)


@pytest.fixture
def forbidden_read_dict():
    """Fixture dict with forbidden on reading."""
    return dict_factory(test_dict, read=False)


@pytest.fixture
def readonly_dict():
    """Readonly dict fixture."""
    return dict_factory(
        test_dict,
        read=True,
        change=False,
        add=False,
        delete=False,
    )


@pytest.fixture
def protected_dict():
    """Protected dict fixture."""
    return dict_factory(test_dict, protected=["name", "info.data"])


def test_read_attribute_from_my_dict(
    normal_dict: ViaDotDict,
    forbidden_read_dict: ViaDotDict,
    protected_dict: ViaDotDict,
) -> None:
    """Test read attributes from ViaDotDict class."""
    # Test read usually dict attribute.
    assert normal_dict.name == "dict"
    assert normal_dict.number == 1
    assert normal_dict.info.data == "no data"

    with pytest.raises(KeyError):
        normal_dict.not_exist

    # Test read dict with forbidden on reading attribute.
    with pytest.raises(ProtectedError):
        forbidden_read_dict.name

    with pytest.raises(ProtectedError):
        forbidden_read_dict.number

    # Test read protected dict attribute.
    with pytest.raises(ProtectedError):
        protected_dict.name


def test_change_attribute_in_my_dict(
    normal_dict: ViaDotDict,
    readonly_dict: ViaDotDict,
    protected_dict: ViaDotDict,
) -> None:
    """Test change attributes in ViaDotDict class."""
    # Test change usually dict attribute.
    assert normal_dict.name == "dict"
    normal_dict.name = "other name"
    assert normal_dict.name == "other name"

    # Test change readonly dict attribute.
    assert readonly_dict.name == "dict"
    with pytest.raises(ProtectedError):
        readonly_dict.name = "other name"
    assert readonly_dict.name == "dict"

    # Test change protected dict attribute.
    protected_dict.number = 33
    assert protected_dict.number == 33
    with pytest.raises(ProtectedError):
        protected_dict.name = "other name"


def test_add_attribute_to_my_dict(
    normal_dict: ViaDotDict,
    readonly_dict: ViaDotDict,
    protected_dict: ViaDotDict,
) -> None:
    """Test add attributes to ViaDotDict class."""
    # Test add usually dict attribute.
    with pytest.raises(KeyError):
        normal_dict.new_attribute

    normal_dict.new_attribute = "done!"
    assert normal_dict.new_attribute == "done!"

    # Test add readonly dict attribute.
    with pytest.raises(ProtectedError):
        readonly_dict.new_attribute = "error"

    # Test add protected dict attribute.
    protected_dict.new_attribute = 33
    assert protected_dict.new_attribute == 33


def test_delete_attribute_from_my_dict(
    normal_dict: ViaDotDict,
    readonly_dict: ViaDotDict,
    protected_dict: ViaDotDict,
) -> None:
    """Test delete attributes from ViaDotDict class."""
    # Test delete usually dict attribute.
    del normal_dict.name
    with pytest.raises(KeyError):
        normal_dict.name

    # Test delete readonly dict attribute.
    with pytest.raises(ProtectedError):
        del readonly_dict.info.data

    # Test delete protected dict attribute.
    del protected_dict.number
    with pytest.raises(KeyError):
        protected_dict.number

    with pytest.raises(ProtectedError):
        del protected_dict.name
