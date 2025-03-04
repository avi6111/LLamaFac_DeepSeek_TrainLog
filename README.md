# LLamaFac_DeepSeek_TrainLog

A project for small tools(mostly python files）of LLM Traning

**主要分两大块**

* 功能代码
* 学习文档

**细分就是各个功能段的代码：洗数据，微调工具，学习算法，打包，应用工具等**

（暂时前期只有洗数据部分，都卡了几天了）

## 过程0-“洗数据”

| name            | func                                         | desc                  |
| --------------- | -------------------------------------------- | --------------------- |
| pyArrayCheck.py | python分块处理内存测试                       | 美什么用              |
| pytorchVer      | 测试torch 版本                               | 功能同另外一个i额目录 |
| swithUTF8       | 改文件格式，批量，方便后续代码不需要重新读取 |                       |
| textToJson      | 改gb2321 中文编码文件 为utf-8文件，可批量    |                       |

## 过程x-应用工具

### 聊天
