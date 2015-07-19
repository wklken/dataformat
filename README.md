# dataformat
A tool to generate data or reformat source data to csv/xml, useful for test data

### help msg

```
usage: dataformat.py [-h] -i INPUT [-o OUTPUT] -t TOTAL -a ARRAY [-F '\t']
                     [-P '\t'] [-f ''] [-s] [-e]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file path
  -o OUTPUT, --output OUTPUT
                        output file path, default input_file_path.dist
  -t TOTAL, --total TOTAL
                        output file total columns
  -a ARRAY, --array ARRAY
                        column index array, e.g '1,3,4' or '3,5=abc,6:2'
  -F '\t', --FS '\t'    input file field separator, default '\t', support
                        multi FS, e.g. '\t|^A|\'
  -P '\t', --OFS '\t'   output file field separator, default '\t', support
                        multi OFS, e.g. '0=\t,1=' means all use '\t' as OFS,
                        column 1 use ^A
  -f '', --fill ''      output file column default fill str, default ''
  -s, --serialnumber    use column number to fill output file column
  -e, --error           the wrong line of input file will oupt directly
```


### how to use?

input file `data`
```
A1,A2,A3,A4
B1,B2,B3,B4
```

#### 1. change separator to /

```
./dataformat.py -i data -t 4 -F ',' -P '/' -a "1,2,3,4"

# cat data.dist
A1/A2/A3/A4
B1/B2/B3/B4
```

#### 2. gen 10 columns

```
./dataformat.py -i data -t 10 -F ',' -P '/' -a "1,2,3,4"

# cat data.dist
A1/A2/A3/A4//////
B1/B2/B3/B4//////
```

#### 4. other columns filled with '-'

```
./dataformat.py -i data -t 10 -F ',' -P '/' -a "1,2,3,4" -f '-'

# cat data.dist
A1/A2/A3/A4/-/-/-/-/-/-
B1/B2/B3/B4/-/-/-/-/-/-
```

#### 5. column 10 with default value 'D10'

```
./dataformat.py -i data -t 10 -F ',' -P '/' -a "1,2,3,4,10=D10" -f '-'

# cat data.dist
A1/A2/A3/A4/-/-/-/-/-/D10
B1/B2/B3/B4/-/-/-/-/-/D10
```

#### 6. switch column 1 and column 2

use map
```
./dataformat.py -i data -t 10 -F ',' -P '/' -a "1:2,2:1,3,4,10=D10" -f '-'

# cat data.dist
A2/A1/A3/A4/-/-/-/-/-/D10
B2/B1/B3/B4/-/-/-/-/-/D10
```

equals:
```
./dataformat.py -i data -t 10 -F ',' -P '/' -a "1:2,2:1,3:3,4:4,10=D10" -f '-'
```

#### 7. to be continue





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

# DONE
1. 使用argparse, 重构命令行
2. 重构help message
3. 重构文件读取及处理, 大文件的处理方法
11. add readme

# TODO:
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
12. 实现这个
./dataformat.py -i data -t 10 -F ',' -P '/' -a "1:2,2:1,3,4,9:1,10=D10" -f '-'
13. 处理异常, 莫名其妙没结果的
