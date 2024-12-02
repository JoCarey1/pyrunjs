# pyrunjs

使用python简单地调用js，获取js表达式返回值

# 安装

pdm

```bash
pdm add pyrunjs
```

pip

```bash
pip install pyrunjs
```

# 使用示例

```python
import pyrunjs

js_script = """function HelloWorld() { return 'Hello World!'; } """
result = pyrunjs.run_js(js_script, "HelloWorld()")
print(result)  # output: Hello World!
```

```python
import pyrunjs

result = pyrunjs.run_js('', "1 + 2")
print(result)  # output: 3
```

# 版本更新概要信息

* 0.1.2 `run_js`函数可用
* 0.1.3  
  * 新增`call_js`函数，可自动编写调用function的表达式。
  * 解决不同系统默认编码不同导致的乱码问题。(例：windows系统默认编码为GBK时，现在可能正常返回结果了)
* 0.1.4 添加对异步函数Promise的支持。run_js表达式返回异步函数时，可以获取resolve中的结果了。
