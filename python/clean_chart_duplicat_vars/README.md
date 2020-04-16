**用于对指定目录下的满足.\*values\.\*\\\.yaml 的文件中的变量去重**

* clean-duplicat.exe
    *可执行文件*

* clean-duplicat.properties
    *执行配置文件*
    
    一下是三个配置变量
    
    * base_dirs
    
        ```properties
        #values文件所在的目录
        base_dirs=waf-service
        #指定多个values文件目录以","分隔
        base_dirs=waf-service,waf-schedule,waf-report,
        ```
    
    * templates_dir
    
        *模板文件在base_dirs下的目录（相对目录，会拼接到base_dirs下）*
    
    * back_dir
    
        *执行后，原来的values文件的备份目录（相对目录，会拼接到base_dirs下）*
    
* clean-duplicat.py
    *源码*