# pyrunjs

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