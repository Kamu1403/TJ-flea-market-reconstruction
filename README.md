## Introduction

- This is a software refactoring project for the TJ-flea-market project.
  The project builds corresponding http service web pages based on the 
  **Python Flask** framework, and uses **MySql** as the database back-end.
- Developed in collaboration with the gitlab group, the original project is at 
  [Gitlab project](https://gitlab.com/tj-cs-swe/cs10102302-2022/tluafed/tj-flea-market-reconstruction)
- More information in the [Documents](/doc) 

<img src="/doc/1.jpg" width="400"/><img src="/doc/2.jpg" width="400"/>
## Dependencies

### Python
- We use python=3.10.0 and **Python Flask** framework in our project.
- See [requirements.txt](requirements.txt) or [environment.yml](environment.yml) 
  for the dependency library
- You are advised to use anaconda to manage the python environment and install the required 
  dependent libraries

### MySql

- Version 8.0.29
- We changed the database name, user name, and password in the config file in the original project
- Here is how to configure user privileges in the database:
```
mysql> CREATE USER 'root'@'%' IDENTIFIED BY 'PASSWORD';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
mysql> FLUSH PRIVILEGES;
```

## Installation

Use anaconda to configure the environment as follows:
```
conda create -n tj_market python==3.10.0
conda activate tj_market
pip install -r requirements.txt
```
OR
```
conda env create --file environment.yml
```


## Getting Started

1. Before formal operation, clear the following contents:
   - the user avatar ```user/resource/user-pic/*``` (except ```80000000/```and
     ```default_avatar.jpg```)
   - the commodity information ```item/static/resource/item_pic/*```, 
     ```item/static/resource/temp/*``` 
   - user chats ```chat/static/resource/temp/*``` 

2. In ```config.py```, set ```drop_database``` to ```False```
3. In ```app/init_database.py```, the bottom of ```init_database() ```function, 
   comment ```fake_data()``` to disable auto mocked data
4. In ```api/routes.py```, comment the "test backdoor" for the verification code registering: 
```python
if code == "IEW32DGCBCDZI2B3ELJ7KIAS4HQZMU0M":  # 测试用后门
    return [0, "验证通过"]
```

5. In the python or anaconda environment, to run the program:
```
python main.py
```
OR you can follow the instructions of [Python Flask](https://palletsprojects.com/p/flask/)
to modify the run params


## Thanks to the Third Party Libs

[Python Flask](https://flask.palletsprojects.com/en/2.2.x/#)
