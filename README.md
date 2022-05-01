# TJ-flea-market

同济跳蚤市场课程项目

## 成员须知

这里是develop分支，每次较小的迭代过程中请基于此分支创建临时分支进行开发，然后merge到此分支

## 运行环境说明

python版本3.10.0

依赖库见requirements.txt

安装方法：

```
conda create -n your_env python==3.10.0
conda activate your_env
pip install -r requirements.txt
或
conda env create -f environment.yml
```

## 使用说明

```
启动redis服务 命令行输入redis-server redis.windows.conf

python app.py
```
