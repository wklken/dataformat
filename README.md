# dataformat
A tool to generate data or reformat source data to csv/xml, useful for test data


# DONE
"""
1. 使用argparse, 重构命令行
2. 重构help message
3. 重构文件读取及处理, 大文件的处理方法
"""

# TODO:
"""
target: 更方便地造数据, 最好的造数据工具
0. 复盘, 写重构要点
4. 修改日期生成方式, 要更友好, 支持多种方式timestamp or str
5. 支持json/csv/tab等任意字符分隔/xml
6. 整数/小数/随机数/限制精度
7. 支持python2.4/2.5/2.6/2.7/3.x
8. 乱序/默认/填充值等
9. 找到原来的博客 http://www.jiancool.com/article/72353002070/ => 思考功能, 提供README.md
   http://wklken.me/posts/2011/12/10/python-dataformat.html
10. add testcase
11. add readme
"""


### update log

```
2011-08-05 version 0.1 created
2011-10-29 version 0.2 add row-row mapping ,default row value .rebuild all functions.
2011-12-17 version 0.3 add new functions, add timestamp creator.
2012-03-08 version 0.4 rebuild functions.
2012-06-22             add function to support multi output separators
2012-07-11             fix bug
2012-09-03 version 0.5 rebuild functions,add help msg!
2012-11-08             last version edited
2015-07-19 version 1.0 do a lot of changes
```
