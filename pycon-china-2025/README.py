# TODO 请注意，该文件是从 README.ipynb 转换而来，仅用于不想安装 Jupyter Notebook 的用户阅读。建议直接阅读 README.ipynb 来获取更好的阅读体验。
# %% [markdown]
# # README
# 
# 请注意这里只提供关键代码，具体的描述请参考演讲稿原文。

# %%
# 安装依赖
%pip install sudachipy sudachidict_full

# %% [markdown]
# ## 基本操作
# 
# 这里对应演讲稿中的「基本操作」章节。
# 
# ### 基础测试

# %%
from typing import List

from sudachipy import Dictionary

def analyze_text(text: str) -> List[List[str]]:
    tokenizer = Dictionary(dict="full").create()
    result_list = []
    for token in tokenizer.tokenize(text):
        result = [token.surface(), token.normalized_form()]
        result_list.append(result)
    return result_list

print(analyze_text("晩ご飯を食べましたか。"))

# %% [markdown]
# ## 有挑战性的测试

# %%
from typing import List

from sudachipy import Dictionary

def analyze_text(text: str) -> List[List[str]]:
    tokenizer = Dictionary(dict="full").create()
    result_list = []
    for token in tokenizer.tokenize(text):
        result = [token.surface(), token.normalized_form()]
        result_list.append(result)
    return result_list


print(analyze_text("なんで『春日影』やったの！？"))

# %% [markdown]
# ## 如何添加未登录词
# 
# 这里对应演讲稿的「如何添加未登录词」章节。

# %%

import shutil
from pathlib import Path
import sudachidict_full

# 找到 sudachidict 的安装位置
sudachi_dir = Path(sudachidict_full.__file__).parent

# 搜索 system.dic
found = False
# 注意， 虽然我们安装的是「sudachidict_full」，但词典名是「system.dic」
for file in sudachi_dir.rglob("system.dic"):
    print(f"找到: {file}")
    shutil.copy(file, "system.dic")
    print("✓ system.dic 已复制到当前目录")
    found = True
    break

if not found:
    print("❌ 未找到 system.dic")
    print(f"sudachidict 路径: {sudachi_dir}")

# %%
# 你可以将下面的代码复制到终端然后执行
# sudachipy ubuild -s system_full.dic -o user.dic user.csv

import os
# 删除之前的编译结果
output_file = "user.dic"
if os.path.exists(output_file):
    os.remove(output_file)
    print(f"已删除旧的 {output_file}")

import subprocess
result = subprocess.run(["which", "sudachipy"], capture_output=True, text=True)
sudachipy_path = result.stdout.strip()
print(sudachipy_path)
subprocess.run([sudachipy_path, "ubuild", "-s", "system.dic", "-o", "user.dic", "user.csv"])

# %% [markdown]
# ## 测试已添加登录词的编译文件

# %%
from typing import List

from sudachipy import Dictionary


def analyze_text(text: str) -> List[List[str]]:
	# 就是用 config='{"userDict": ["user.dic"]}'指定
    tokenizer = Dictionary(dict="full", config='{"userDict": ["user.dic"]}').create()
    result_list = []
    for token in tokenizer.tokenize(text):
        result = [token.surface(), token.normalized_form()]
        result_list.append(result)
    return result_list


print(analyze_text("なんで『春日影』やったの！？"))

# %% [markdown]
# ## 通过词性确定左右连接ID
# 
# ### 「なんで」

# %%
# 你可以将下面的代码复制到终端然后执行
# sudachipy ubuild -s system_full.dic -o user-with-nannde.dic user.csv

import os
# 删除之前的编译结果
output_file = "user.dic"
if os.path.exists(output_file):
    os.remove(output_file)
    print(f"已删除旧的 {output_file}")

import subprocess
result = subprocess.run(["which", "sudachipy"], capture_output=True, text=True)
sudachipy_path = result.stdout.strip()
print(sudachipy_path)
subprocess.run([sudachipy_path, "ubuild", "-s", "system.dic", "-o", "user-with-nannde.dic", "user-with-nannde.csv"])

# %%
from typing import List

from sudachipy import Dictionary


def analyze_text(text: str) -> List[List[str]]:
	# 就是用 config='{"userDict": ["user.dic"]}'指定
    tokenizer = Dictionary(dict="full", config='{"userDict": ["user-with-nannde.dic"]}').create()
    result_list = []
    for token in tokenizer.tokenize(text):
        result = [token.surface(), token.normalized_form()]
        result_list.append(result)
    return result_list


print(analyze_text("なんで『春日影』やったの！？"))

# %% [markdown]
# ### 将「やった」当做名词

# %%
# 你可以将下面的代码复制到终端然后执行
# sudachipy ubuild -s system_full.dic -o user-with-yatta-as-noun.dic user-with-yatta-as-noun.csv

import os
# 删除之前的编译结果
output_file = "user.dic"
if os.path.exists(output_file):
    os.remove(output_file)
    print(f"已删除旧的 {output_file}")

import subprocess
result = subprocess.run(["which", "sudachipy"], capture_output=True, text=True)
sudachipy_path = result.stdout.strip()
print(sudachipy_path)
subprocess.run([sudachipy_path, "ubuild", "-s", "system.dic", "-o", "user-with-yatta-as-noun.dic", "user-with-yatta-as-noun.csv"])

# %%
from typing import List

from sudachipy import Dictionary


def analyze_text(text: str) -> List[List[str]]:
	# 就是用 config='{"userDict": ["user.dic"]}'指定
    tokenizer = Dictionary(dict="full", config='{"userDict": ["user-with-yatta-as-noun.dic"]}').create()
    result_list = []
    for token in tokenizer.tokenize(text):
        result = [token.surface(), token.normalized_form()]
        result_list.append(result)
    return result_list

print(analyze_text("やった"))
print(analyze_text("なんで『春日影』やったの！？"))

# %% [markdown]
# ### ### 将「やった」当做「感動詞」

# %%
# 你可以将下面的代码复制到终端然后执行
# sudachipy ubuild -s system_full.dic -o user-with-yatta-as-kanndou.dic user-with-yatta-as-kanndou.csv

import os
# 删除之前的编译结果
output_file = "user.dic"
if os.path.exists(output_file):
    os.remove(output_file)
    print(f"已删除旧的 {output_file}")

import subprocess
result = subprocess.run(["which", "sudachipy"], capture_output=True, text=True)
sudachipy_path = result.stdout.strip()
print(sudachipy_path)
subprocess.run([sudachipy_path, "ubuild", "-s", "system.dic", "-o", "user-with-yatta-as-kanndou.dic", "user-with-yatta-as-kanndou.csv"])

# %%
from typing import List

from sudachipy import Dictionary


def analyze_text(text: str) -> List[List[str]]:
    # 注意是user-with-yatta-as-「kanndou」.dic
    tokenizer = Dictionary(dict="full", config='{"userDict": ["user-with-yatta-as-kanndou.dic"]}').create()
    result_list = []
    for token in tokenizer.tokenize(text):
        result = [token.surface(), token.normalized_form()]
        result_list.append(result)
    return result_list

print(analyze_text("やった"))
print(analyze_text("なんで『春日影』やったの！？"))


