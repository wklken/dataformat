#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
dataformat.py
this script change data from your source to the dest data format, generally used for data generate or reformat

url: https://github.com/wklken/dataformat
author: wklken@yeah.net
update_log:
"""

import sys
import time
import re
import argparse


#处理一行，转为目标格式，返回目标行
def one_line_format(parts, total, ft_map, output_separators, empty_fill_str, is_fill_with_column_no):
    outline = []
    # step1.获取每一列的值
    for index in range(1, total + 1):
        if index in ft_map:
            fill_index = ft_map[index]
            #加入使用默认值列  若是以d开头，后面是默认，否则取文件对应列 done
            if fill_index.startswith("d"):
                #列默认值暂不开启时间戳处理
                outline.append(fill_index[1:])
            else:
                # outline.append(handler_specal_part(parts[int(fill_index) - 1]))
                outline.append(parts[int(fill_index) - 1])
        else:
            #-s 选项生效，则填充列号, 否则，填充默认填充值
            column = str(index) if is_fill_with_column_no else empty_fill_str
            outline.append(column)

    # step2.组装加入输出分隔符，支持多分隔符
    default_outsp = output_separators.get(0, "\t")
    result = []
    outsize = len(outline)
    for index in range(outsize):
        result.append(outline[index])
        if index < outsize - 1:
            result.append(output_separators.get(index + 1, default_outsp))

    # step3.拼成一行返回
    return ''.join(result)


#处理入口，读文件，循环处理每一行，写出
#输入数据分隔符默认\t,输出数据默认分隔符\t
def process(input_file, total, rules, outpath, input_separators, outsp, empty_fill_str, is_fill_with_column_no, is_error_line_out):
    ft_map = {}
    #有效输入字段数（去除默认值后的）
    in_count = 0
    used_row = []
    #step1-3相当于数据预处理，解析传入选项

    rules = rules.split(",")

    #step1 处理映射列 不能和第二步合并
    for to_row in rules:
        if r"\:" not in to_row and len(to_row.split(":")) == 2:
            used_row.append(int(to_row.split(":")[1]))

        if r"\=" not in str(to_row) and len(str(to_row).split("=")) == 2:
            pass
        else:
            in_count += 1

    #step2 处理默认值列
    for to_row in rules:
        # 处理默认值列 1=abc
        if r"\=" not in str(to_row) and len(str(to_row).split("=")) == 2:
            ft_map.update({int(to_row.split("=")[0]): "d" + to_row.split("=")[1]})
            continue
        #处理列列映射  1:5
        elif r"\:" not in to_row and len(to_row.split(":")) == 2:
            ft_map.update({int(to_row.split(":")[0]): to_row.split(":")[1]})
            continue
        #其他普通列
        else:
            to_index = 0
            for i in range(1, total + 1):
                if i not in used_row:
                    to_index = i
                    break
            ft_map.update({int(to_row): str(to_index)})
            used_row.append(to_index)

    #setp3 处理输出分隔符   outsp  0=\t,1=    0代表默认的，其他前面带列号的代表指定的
    # TODO: 检测错误
    if len(outsp) > 1 and '=' in outsp and len(outsp.split(",")) > 1:
        outsp_kvs = re.findall(r"\d=.+?", outsp)
        output_separators = {}
        for outsp_kv in outsp_kvs:
            k, v = outsp_kv.split("=")
            output_separators.update({int(k): v})
    else:
        output_separators = {0: outsp}

    #step4 开始处理每一行
    is_multi_input_separators = len(input_separators.split("|")) > 0
    with open(outpath, "w") as f:
        result = []

        for line in input_file:
            line = line.strip("\n")
            #多个输入分隔符情况，使用正则切分成列
            if is_multi_input_separators:
                parts = re.split(input_separators, line)
            #否则使用正常字符串切分成列
            else:
                parts = line.split(input_separators)

            #正常的，切分后字段数大于等于配置的选项个数
            if len(parts) >= in_count:
                outline = one_line_format(parts, total, ft_map, output_separators, empty_fill_str, is_fill_with_column_no)
                result.append("%s\n" % outline)
            #不正常的，列数少于配置
            else:
                #若配置了-e 输出，否则列数不符的记录过滤
                if is_error_line_out:
                    result.append("%s\n" % line)

        #step5 输出结果
        f.writelines(result)
    input_file.close()


# #特殊的处理入口，处理维度为每一行,目前只有时间处理
# def handler_specal_part(part_str):
    # #timestamp 时间处理
    # #时间列，默认必须 TS数字=时间
    # if part_str.startswith("TS") and "=" in part_str:
        # ts_format = {
            # 8: "%Y%m%d",
            # 10: "%Y-%m-%d",
            # 14: "%Y%m%d%H%M%S",
            # 19: "%Y-%m-%d %H:%M:%S"
        # }
        # to_l = 0
        # #step1 确认输出的格式 TS8 TS10 TS14 TS19
        # if part_str[2] != "=":
            # to_l = int(part_str[2:part_str.index("=")])

        # part_str = part_str.split("=")[1].strip()
        # interval = 0
        # #step2 存在时间+-的情况 确认加减区间
        # if "+" in part_str:
            # inputdate = part_str.split("+")[0].strip()
            # interval = int(part_str.split("+")[1].strip())
        # elif "-" in part_str:
            # parts = part_str.split("-")
            # #20101020 - XX
            # if len(parts) == 2:
                # inputdate = parts[0].strip()
                # interval = -int(parts[1].strip())
            # #2010-10-20
            # elif len(parts) == 3:
                # inputdate = part_str
            # #2010-10-20 - XX
            # elif len(parts) == 4:
                # inputdate = "-".join(parts[:-1])
                # interval = -int(parts[-1])
            # else:
                # inputdate = part_str
        # else:
            # inputdate = part_str.strip()
        # #step3 将原始时间转为目标时间
        # part_str = get_timestamp(inputdate, ts_format, interval)

        # #step4 如果定义了输出格式，转换成目标格式，返回
        # if to_l > 0:
            # part_str = time.strftime(ts_format.get(to_l),
                                     # time.localtime(int(part_str)))
    # return part_str


#将时间由秒转化为目标格式
def get_timestamp(inputdate, ts_format, interval=0):
    if "now()" in inputdate:
        inputdate = time.strftime("%Y%m%d%H%M%S")
    inputdate = inputdate.strip()
    try:
        size = len(inputdate)
        if size in ts_format:
            ts = time.strptime(inputdate, ts_format.get(size))
        else:
            print "the input date and time expression error,only allow 'YYYYmmdd[HHMMSS]' or 'YYYY-MM-DD HH:MM:SS'  "
            sys.exit(0)
    except:
        print "the input date and time expression error,only allow 'YYYYmmdd[HHMMSS]' or 'YYYY-MM-DD HH:MM:SS'  "
        sys.exit(0)
    return str(int(time.mktime(ts)) + interval)


class StringEscapeAction(argparse.Action):
    """
    Parse value to value.decode("string_escape")
    """
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(StringEscapeAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.decode("string_escape"))


def main():
    """
    程序入口，读入参数，执行
    """
    # handle args
    parser = argparse.ArgumentParser()

    # parser.add_argument('move', choices=['rock', 'paper', 'scissors'])
    parser.add_argument("-i", "--input", required=True, type=argparse.FileType('r'),
                        help="input file path")
    # parser.add_argument("-i", "--input", required=True,
                        # help="input file path")
    parser.add_argument("-o", "--output",
                        help="output file path, default  input_file_path.dist")
    parser.add_argument("-t", "--total", type=int, required=True,
                        help="output file total columns")
    parser.add_argument("-a", "--array", required=True,
                        help="column index array, e.g '1,3,4' or '3,5=abc,6:2'")
    parser.add_argument("-F", "--FS", default='\t', action=StringEscapeAction, metavar=r"'\t'",
                        help=r"input file field separator, default '\t', support multi FS, e.g. '\t|^A|\'")
    parser.add_argument("-P", "--OFS", default='\t', action=StringEscapeAction, metavar=r"'\t'",
                        help=r"output file field separator, default '\t', support multi OFS, e.g. '0=\t,1=' means all use '\t' as OFS, column 1 use ^A")
    parser.add_argument("-f", "--fill", default='', metavar="''",
                        help="output file column default fill str, default ''")
    parser.add_argument("-s", "--serialnumber", action='store_true',
                        help="use column number to fill output file column")
    parser.add_argument("-e", "--error", action='store_true',
                        help="the wrong line of input file will oupt directly")

    args = parser.parse_args()

    output_path = args.output if args.output else ('%s.dist' % args.input.name)

    process(input_file=args.input, total=args.total, rules=args.array, outpath=output_path,
            input_separators=args.FS, outsp=args.OFS, empty_fill_str=args.fill,
            is_fill_with_column_no=args.serialnumber, is_error_line_out=args.error)


if __name__ == "__main__":
    main()
