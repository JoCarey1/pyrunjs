import unittest
import pyrunjs


class TestRunnerMethods(unittest.TestCase):

    def test_hello_world(self):
        js_script = """function HelloWorld() { return 'Hello World!'; } """
        self.assertEqual(pyrunjs.run_js(js_script, "HelloWorld()"), "Hello World!")

    def test_add(self):
        self.assertEqual(pyrunjs.run_js('', "1 + 2"), "3")

    def test_run_error(self):
        with self.assertRaises(RuntimeError):
            pyrunjs.run_js('', "let let a = 1;")


if __name__ == '__main__':
    unittest.main()
