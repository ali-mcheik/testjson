import json
import unittest

from json_utils import merge, parse, serialize, validate


class TestParse(unittest.TestCase):
    def test_object(self):
        self.assertEqual(parse('{"key": "value"}'), {"key": "value"})

    def test_array(self):
        self.assertEqual(parse("[1, 2, 3]"), [1, 2, 3])

    def test_number(self):
        self.assertEqual(parse("42"), 42)

    def test_null(self):
        self.assertIsNone(parse("null"))

    def test_invalid_raises(self):
        with self.assertRaises(json.JSONDecodeError):
            parse("not json")


class TestSerialize(unittest.TestCase):
    def test_dict(self):
        self.assertEqual(serialize({"a": 1}), '{"a": 1}')

    def test_list(self):
        self.assertEqual(serialize([1, 2, 3]), "[1, 2, 3]")

    def test_none(self):
        self.assertEqual(serialize(None), "null")

    def test_indent(self):
        result = serialize({"a": 1}, indent=2)
        self.assertIn("\n", result)


class TestValidate(unittest.TestCase):
    def test_valid_object(self):
        self.assertTrue(validate('{"x": 1}'))

    def test_valid_array(self):
        self.assertTrue(validate("[true, false, null]"))

    def test_invalid_string(self):
        self.assertFalse(validate("hello"))

    def test_invalid_none(self):
        self.assertFalse(validate(None))


class TestMerge(unittest.TestCase):
    def test_simple_merge(self):
        self.assertEqual(merge({"a": 1}, {"b": 2}), {"a": 1, "b": 2})

    def test_override(self):
        self.assertEqual(merge({"a": 1}, {"a": 99}), {"a": 99})

    def test_recursive_merge(self):
        base = {"a": {"x": 1, "y": 2}}
        override = {"a": {"y": 99, "z": 3}}
        self.assertEqual(merge(base, override), {"a": {"x": 1, "y": 99, "z": 3}})

    def test_does_not_mutate_base(self):
        base = {"a": 1}
        merge(base, {"b": 2})
        self.assertEqual(base, {"a": 1})

    def test_non_dict_raises(self):
        with self.assertRaises(TypeError):
            merge([1, 2], {"a": 1})


if __name__ == "__main__":
    unittest.main()
