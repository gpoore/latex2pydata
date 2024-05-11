import pytest
import textwrap
import latex2pydata


def test_loads_scalar_schema():
    data_str = textwrap.dedent('''\
        # latex2pydata metadata: {"schema": {"key1": "int", "key2": "bool", "key3": "str", "key4": "None"}}
        {
        "key1": "123",
        "key2": "True",
        "key3": "'abc'",
        "key4": "None",
        }
        ''')
    assert latex2pydata.loads(data_str) == {"key1": 123, "key2": True, "key3": 'abc', "key4": None}


def test_loads_collection_schema():
    data_str = textwrap.dedent('''\
        # latex2pydata metadata: {"schema": {"key1": "list[set[int|float]]"}}
        {
        "key1": "[{1, 2.3}, {4, 5}, {6.0, 7.1}]"
        }
        ''')
    assert latex2pydata.loads(data_str) == {"key1": [{1, 2.3}, {4, 5}, {6.0, 7.1}]}

    # This also checks for space-insensitive schema definitions
    data_str = textwrap.dedent('''\
        # latex2pydata metadata: {"schema": {"key1": "dict[int, float]"}}
        {
        "key1": "{1: 1.0, 2: 2.0}"
        }
        ''')
    assert latex2pydata.loads(data_str) == {"key1": {1: 1.0, 2: 2.0}}


def test_loads_keypath():
    data_str = textwrap.dedent('''\
        # latex2pydata metadata: {"schema": {"main.sub.subsub": "float"}}
        {
        "main.sub.subsub": "1.23"
        }
        ''')
    assert latex2pydata.loads(data_str) == {'main': {'sub': {'subsub': 1.23}}}

    data_str = textwrap.dedent('''\
        # latex2pydata metadata: {"schema": {"main_1.sub2.__subsub": "float"}}
        {
        "main_1.sub2.__subsub": "1.23"
        }
        ''')
    assert latex2pydata.loads(data_str) == {'main_1': {'sub2': {'__subsub': 1.23}}}


def test_loads_invalid_schema():
    with pytest.raises(latex2pydata.err.Latex2PydataSchemaError):
        # dangling |
        data_str = textwrap.dedent('''\
            # latex2pydata metadata: {"schema": {"key1": "list[set[int|float|]]"}}
            ''')
        latex2pydata.loads(data_str)

    with pytest.raises(latex2pydata.err.Latex2PydataSchemaError):
        # missing [
        data_str = textwrap.dedent('''\
            # latex2pydata metadata: {"schema": {"key1": "list int]"}}
            ''')
        latex2pydata.loads(data_str)

    with pytest.raises(latex2pydata.err.Latex2PydataSchemaError):
        # missing ]
        data_str = textwrap.dedent('''\
            # latex2pydata metadata: {"schema": {"key1": "list[int"}}
            ''')
        latex2pydata.loads(data_str)

    with pytest.raises(latex2pydata.err.Latex2PydataSchemaError):
        # nested too deep
        data_str = textwrap.dedent('''\
            # latex2pydata metadata: {"schema": {"key1": "list[list[list[int]]]"}}
            ''')
        latex2pydata.loads(data_str)
