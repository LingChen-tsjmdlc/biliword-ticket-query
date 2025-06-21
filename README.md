# BW 2025 余票查询

## 🛑备注
> 因制作紧急，**没有给_查询间隔_等配置**, 代码很简单，如需要请自行修改

## 🚀 快速启动

1. 克隆项目
``` bash
git clone https://github.com/LingChen-tsjmdlc/biliword-ticket-query.git
```

2. 推荐创建 conda 环境（需提前安装 anaconda/miniconda）
```bash
# 推荐使用 IDE 为 Pycharm
conda create --name bw-ticket-query python=3.8  # 创建一个叫 bw-ticket-query 的环境
conda activate bw-ticket-query  # 激活环境
```

3. 安装依赖
``` bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

4. 运行
``` bash
python run main.py
```
5. 打包
```bash
# 安装 pyinstaller 包
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
```
```bash
# 打包为 exe，exe文件在 `.\dist` 目录下
pyinstaller --onefile '.\bw2025 余票查询.py'
```