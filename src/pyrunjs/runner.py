import subprocess
import re

_RETURN_MSG_PATTERN = re.compile(r"##(.*)##(.*)##$")


class RunResult:
    def __init__(self, status: bool, js_type=None, output=None, error=None):
        self.status = status
        self.js_type = js_type
        self.output = output
        self.error = error


def run_js(js_script: str, expression: str):
    """
        在 js_script 脚本基础上运行 js 表达式，并获得表达式返回值
    """
    result = run_js_with_result(js_script, expression)
    if result.status:
        return result.output
    else:
        msg = "run js error: " + result.error
        raise RuntimeError(msg)


def run_js_with_result(js_script: str, expression: str):
    if js_script is None or expression is None:
        raise ValueError('js_script and expression are required')
    js_code = f'''
        (function() {{
            {js_script}
            ;
            (function(){{
                let result = {expression};
                let result_type = typeof result;
                if (result_type !== 'string') {{
                    result = JSON.stringify(result);
                }}
                process.stdout.write(`##${{result_type}}##${{result}}##`);
            }})()
        }})()
    '''
    p = subprocess.Popen(['node'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate(js_code.encode('utf-8'))
    ok = p.wait() == 0
    result = RunResult(ok)
    if ok:
        g = _RETURN_MSG_PATTERN.search(out.decode('utf-8'))
        result.js_type = g.group(1)
        result.output = g.group(2)
    else:
        result.error = err.decode('utf-8')
    return result
