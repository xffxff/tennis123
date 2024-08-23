# [Tennis 123](https://www.tennis123.net/) 比赛数据分析

这是一个帮助你分析自己在 Tennis 123 网站上的比赛数据的工具，通过它你可以更深入地了解自己近期的比赛表现。

## 安装

你可以使用 Poetry 来安装这个工具：

```bash
poetry install
```

或者使用pip：

```bash
pip install .
```

## 使用方法

安装完成后，你可以通过以下命令来运行分析工具：

```bash
python tennis123/main.py username
```

例如，如果你想分析用户名为`xffxff`的比赛数据，你可以运行：

```bash
python tennis123/main.py xffxff
```

该工具支持一个可选参数`--last-n-matches`，用于指定分析最近的多少场比赛。例如，如果你只想分析最近的10场比赛，可以这样运行：

```bash
python tennis123/main.py xffxff --last-n-matches 10
```

请注意，运行后工具会输出分析结果，具体输出的内容取决于工具的实现。

## 示例输出

运行命令后，你可能会看到类似以下的输出：

```
Match win rate for xffxff is 50.88% over 57 matches.
Game win rate for xffxff is 50.96% over 314 games.
Match win rate for xffxff in the last 20 matches is 60.00%.
Game win rate for xffxff in the last 20 matches is 58.49% over 106 games.
```