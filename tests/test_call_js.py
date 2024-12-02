import json
import unittest
import pyrunjs


class TestCallJs(unittest.TestCase):

    def test_hello_world(self):
        js_script = """function HelloWorld() { return 'Hello World!'; } """
        self.assertEqual("Hello World!", pyrunjs.call_js(js_script, "HelloWorld"))

    def test_string_param(self):
        js_script = """function add(a) { return a; } """
        self.assertEqual("my msg.", pyrunjs.call_js(js_script, "add", "my msg."))

    def test_int_param(self):
        js_script = """function add(a) { return 1 + a; } """
        self.assertEqual("10", pyrunjs.call_js(js_script, "add", 9))

    def test_list_and_tuple_params(self):
        js_script = """function add(a, b, c) { return a + b - c; } """
        list_params = [1, 2, 3]
        self.assertEqual("0", pyrunjs.call_js(js_script, "add", list_params))
        tuple_params = (1, 2, 3)
        self.assertEqual("0", pyrunjs.call_js(js_script, "add", tuple_params))

    def test_dict_param(self):
        js_script = """function get_msg(a) { return a.msg; } """
        dict_params = {
            "key1": "value1",
            "key2": "value2",
            "msg": "hi"
        }
        self.assertEqual("hi", pyrunjs.call_js(js_script, "get_msg", dict_params), "msg should be hi")

    def test_tuple_param_with_dict(self):
        js_script = """function makeJsObj(a, b, c, d) { 
            a.key1 = a.key1 + b; 
            a.key2 = a.key2 + c;
            a.msg = d;
            return a; 
         } """
        dict_params = {
            "key1": "value1",
            "key2": 1,
            "msg": "hi"
        }
        params = (dict_params, 23, 1, "hello")
        result = pyrunjs.call_js(js_script, "makeJsObj", params)
        expected_dict = {
            "key1": "value123",
            "key2": 2,
            "msg": "hello"
        }
        self.assertEqual(json.loads(result), expected_dict)


if __name__ == '__main__':
    unittest.main()
