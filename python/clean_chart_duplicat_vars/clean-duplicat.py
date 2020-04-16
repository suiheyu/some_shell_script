import shutil
import yaml
import os
import re
from functools import reduce

class MyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

var_pattern = re.compile(r'\{\{.*?\.Values\.([a-zA-Z.-]*).*?\}\}')
path_spliter = "."

# 列出目录下的文件列表（不递归）
def dir_file(file_dir):
    list_files = [];
    for file in os.listdir(file_dir):
        file_path = os.path.join(file_dir,file)
        if os.path.isdir(file_path):
            pass
        else:
            list_files.append(file_path)
    return list_files

#读取yaml文件
def readYamls(file_names):
    return dict( zip(
        file_names,
        list( map( lambda file_name: yaml.load(open(file_name,"r",encoding="utf-8")), file_names ) )
    ))

#文件中的变量
def readVariables(file_names):
    rList = list(
        map(
            lambda str: str.strip(),
            list(
                reduce(
                    lambda l1,l2 : l1 + l2,
                    list( map( lambda file_name: var_pattern.findall( open(file_name,"r",encoding="utf-8").read() ) , file_names ) )
                )
            )
        )
    )
    rList.sort()
    key = [ k for k in rList ]
    value = [ True for k in rList ]
    return dict(zip(key,value))

#删除没有用到的变量
def deleteNotUseVariables(obj, varMap, refPath = ""):
    if type(obj) == dict:
        if refPath in varMap:
            return None
        for key in list(obj.keys()):
            tRefPath = key if len(refPath) == 0 else path_spliter.join([refPath,key])
            tempPath = deleteNotUseVariables(obj[key],varMap, tRefPath)
            if (tempPath != None and tempPath == False) or (tempPath == None and len(obj[key].items()) == 0 ) :
                del obj[key]
                print( 'delete path:'+tRefPath)
        return None
    elif type(obj) == list:
        return refPath in varMap
    elif type(obj) == str or type(obj) == int or type(obj) == float or type(obj) == bool or type(obj) == complex or type(obj) == type(None):
        return refPath in varMap
    else:
        message = '###Exception Type'+ str(type(refPath))
        raise MyError(message)

# 备份values文件
def backValues(values_files,back_dir):
    if os.path.exists(back_dir):
        shutil.rmtree(back_dir)
    os.mkdir(back_dir);
    for values_file in values_files:
        shutil.move(values_file,back_dir)

#从指定目录中清楚value文件中重复的变量
def cleanDupliateYaml(base_dir,templates_dir = "templates",back_dir = "back"):
    templates_dir = os.path.join(base_dir,templates_dir);
    back_dir = os.path.join(base_dir,back_dir);
    file_names = dir_file(base_dir)
    values_files = list(filter( lambda str : re.match(".*values.*\.yaml",str),file_names))
    yamls = readYamls(values_files)
    backValues(values_files,back_dir)

    templates_file_name = dir_file(templates_dir)
    varMap = readVariables(templates_file_name)

    for (key,value) in yamls.items():
        print('-----------')
        print(key)
        deleteNotUseVariables(value,varMap)
        print('-----------')

    for (path,value) in yamls.items():
        with open(path,'w',encoding='utf-8') as f:
            print('***save file:'+path)
            yaml.dump(value, f)

def readProperties(file_name):
    resultDic = {};
    f = open(file_name,"r",encoding="utf-8");
    while True:
        tempStr = f.readline();
        noBlankStr = tempStr.strip();
        if len(noBlankStr) != 0:
            keyValue = list(map( lambda str:str.strip(), noBlankStr.split("=")))
            resultDic[keyValue[0]] = keyValue[1]
        if tempStr:
            break;
    return resultDic

valueMap = readProperties("clean-duplicat.properties")
base_dirs = list(filter( lambda str:str, valueMap.get('base_dirs').split(',')))
if not base_dirs:
    raise MyError("need properties: base_dirs")

templates_dir = valueMap.get('templates_dir') if valueMap.get('templates_dir') else 'templates';
back_dir = valueMap.get('back_dir') if valueMap.get('back_dir') else 'back';
for base_dir in base_dirs:
    print('#######################################')
    print('##################'+ base_dir + '###################')
    print('#######################################')
    cleanDupliateYaml(base_dir,templates_dir,back_dir)




