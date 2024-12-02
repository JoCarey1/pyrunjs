import json
import subprocess
import re
import base64

_RETURN_MSG_PATTERN = re.compile(r"##(.*)##(.*)##$")


class RunResult:
    def __init__(self, status: bool, js_type=None, output=None, error=None):
        self.status = status
        self.js_type = js_type
        self.output = output
        self.error = error


def call_js(js_script: str, call_func_name: str, call_func_params=None):
    """
        Call js_script with call_func_name and call_func_params
    """
    expression = make_call_expression(call_func_name, call_func_params)
    return run_js(js_script, expression)


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
    js_script = base64.b64encode(js_script.encode('utf-8')).decode('utf-8')
    js_code = f'''
        (function() {{
            eval(Buffer.from("{js_script}", "base64").toString("UTF-8"));
            !(function(){{
                let _handle_result = function(result) {{
                    let result_type = typeof result;
                    if (result_type !== 'string') {{
                        result = JSON.stringify(result);
                    }}
                    let result_base64 = Buffer.from(result, "UTF-8").toString("base64");
                    let result_type_base64 = Buffer.from(result_type, "UTF-8").toString("base64");
                    process.stdout.write(`##${{result_type_base64}}##${{result_base64}}##`);
                }}
                let expression_result = {expression};
                if (expression_result && typeof expression_result.then === 'function') {{
                    expression_result.then(obj => {{_handle_result(obj)}});
                }} else {{
                    _handle_result(expression_result);
                }}
            }})()
        }})()
    '''
    p = subprocess.Popen(['node'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate(js_code.encode('ascii'))
    ok = p.wait() == 0
    result = RunResult(ok)
    if ok:
        g = _RETURN_MSG_PATTERN.search(out.decode('ascii'))
        result.js_type = base64.b64decode(g.group(1)).decode('utf-8')
        result.output = base64.b64decode(g.group(2)).decode('utf-8')
    else:
        result.error = err.decode()
    return result


def make_call_expression(call_func_name, call_func_params):
    """
        @param call_func_name: Call function name
        @param call_func_params: Call function parameters
    """
    if not isinstance(call_func_name, str):
        raise RuntimeError(f"call_func_name must be a string")
    _call_func_params_is_list_or_tuple = False
    if not isinstance(call_func_params, (str, int, dict)):
        if isinstance(call_func_params, (list, tuple)):
            _call_func_params_is_list_or_tuple = True
            for param in call_func_params:
                if not isinstance(param, (str, int, dict)) and param is not None:
                    raise RuntimeError(f"call_func_params every param must be (str, int, dict) or None")
        elif call_func_params is not None:
            raise RuntimeError(f"call_func_params must be (str, int, dict) or None")
    if _call_func_params_is_list_or_tuple:
        params = [json.dumps(param, ensure_ascii=False) for param in call_func_params]
        expression = '{}({})'.format(call_func_name, ','.join(params))
    else:
        expression = '{}({})'.format(call_func_name, json.dumps(call_func_params, ensure_ascii=False))
    return expression
