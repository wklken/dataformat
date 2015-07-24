# dataformat

A tool to generate data or reformat source data to csv/xml, useful for test data

> target: 更方便地造数据, 最好的造数据工具(handy for test data generate)

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

default syntax
```
column_index=default_value
10=D10
```

e.g.

```
./dataformat.py -i data -t 10 -F ',' -P '/' -a "1,2,3,4,10=D10" -f '-'

# cat data.dist
A1/A2/A3/A4/-/-/-/-/-/D10
B1/B2/B3/B4/-/-/-/-/-/D10
```

#### 6. switch column 1 and column 2

map syntax
```
target_column_index:source_coulmn_index
1:2
means source file column 2 put into target file column 1 (2=>1)
```

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

#### 7. multi OFS(output field separator)

```
./dataformat.py -i data -t 10 -F ',' -P '0=/,1=-' -a "1:2,2:2,3:3,4:4,9:4,10=D10" -f '-'

# cat data.dist
A2-A2/A3/A4/-/-/-/-/A4/D10
B2-B2/B3/B4/-/-/-/-/B4/D10
```


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

### todo list

```
1. support field specific date generate: ts/YMD
2. support column process python function:  1:round(#2)+#3
3. output csv/xml/json?
4. support python2.6/2.7/3.x
5. processing infomation, and exception
6. add testcase

```

### Donation

You can Buy me a coffee:)  [link](http://www.wklken.me/pages/donation.html)

------------------------
------------------------

wklken

Email: wklken@yeah.net

Github: https://github.com/wklken

Blog: [http://www.wklken.me](http://www.wklken.me)

