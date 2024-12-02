import unittest

import pyrunjs


class TestRunJsPromise(unittest.TestCase):

    def test_resolve_promise(self):
        js_script = """
            function add(a, b) {
                return new Promise((resolve, reject) => {
                    let sum = a + b;
                    resolve(sum);
                });
            }
        """
        self.assertEqual("3", pyrunjs.run_js(js_script, "add(1, 2)"))
        self.assertEqual("3", pyrunjs.call_js(js_script, "add", (1, 2)))

    def test_reject_promise(self):
        js_script = """
            function add(a, b) {
                return new Promise((resolve, reject) => {
                    reject('this is reject error');
                });
            }
        """
        with self.assertRaises(RuntimeError):
            pyrunjs.run_js(js_script, "add(1, 2)")
        with self.assertRaises(RuntimeError):
            pyrunjs.call_js(js_script, "add", (1, 2))


if __name__ == '__main__':
    unittest.main()
