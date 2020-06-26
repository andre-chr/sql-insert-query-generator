#!/usr/bin/env python3
import pandas as pd

import argparse


def format_col_names(arr):
    if len(arr) == 0:
        return '()'
    res = '('
    res += str(arr[0])
    for i in range(1, len(arr)):
        res += ', ' + str(arr[i])
    res += ')'
    return res


def format_col_values(arr):
    if len(arr) == 0:
        return '()'
    res = '('
    for i in range(len(arr)):
        if type(arr[i]) is int or type(arr[i]) is float:
            res += str(arr[i])
        else:
            res += "'{}'".format(arr[i])
        res += ', '
    res = res[:-2]
    res += ')'
    return res


"""
    :param: command line arguments
        input: the input file (csv/xlsx) to be converted into SQL insert statements 
        table_name: the table name in the query
    :output: prints the insert SQL statements based on the input file
"""
if __name__ == '__main__':
    ap = argparse.ArgumentParser()

    ap.add_argument('input', help='Input file')
    ap.add_argument('table_name', help='Table name')
    ap.add_argument('-e', '--extension', help='File extension', choices=['csv', 'xlsx'])
    ap.add_argument('-s', '--sheet', help='Sheet name')

    args = ap.parse_args()

    df = None
    if args.extension is None or args.extension == 'csv':
        # csv
        df = pd.read_csv(args.input)
    elif args.extension == 'xlsx' and args.sheet is not None:
        # excel
        df = pd.read_excel(args.input, sheet_name=args.sheet)
    elif args.extension == 'xlsx' and args.sheet is None:
        raise Exception('Invalid args: -s (--sheet) argument must be filled for xlsx file type')
    else:
        raise Exception('Invalid args: Please refer to --help')

    # remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    cols = format_col_names(df.columns)
    for row in df.values.tolist():
        # query = 'INSERT INTO {} {} VALUES {};'.format(args.table_name, cols, format_col_values(row))
        print('INSERT INTO {} {} VALUES {};'.format(args.table_name, cols, format_col_values(row)))

