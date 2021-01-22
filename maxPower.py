#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import pandas as pd
import sys, getopt
from sqlalchemy import create_engine
import cx_Oracle
from pandas import Series, DataFrame, merge


def main(argv):
    year = "2021"
    device = "L"
    outputfile = "max.csv"
    try:
        opts, args = getopt.getopt(argv, "hy:d:o:", ["year=", "device=", "ofile="])
    except getopt.GetoptError:
        print("test.py -y <year> -d <device> -o <outputfile>")
        print(
            "            2020 \n                     TR:变压器 \n                     lN:线路 \n\
                                 LD:负荷\n                                 max.csv"
        )
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("test.py -y <year> -d <device> -o <outputfile>")
            print(
                "            2020 \n                     TR:变压器 \n                     lN:线路\
                 \n                     LD:负荷\n                                 max.csv"
            )
            sys.exit()
        elif opt in ("-y", "--year"):
            year = arg
        elif opt in ("-d", "--device"):
            device = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print("输入的年份为：%s" % (year))
    print("输入的设备为：%s" % (device))
    print("输出的文件为：%s" % (outputfile))
    return year, device, outputfile


# import pandas as pd
# from sqlalchemy import create_engine
# import cx_Oracle
def sql(year, DF, suffix):
    db = cx_Oracle.connect("userid", "password", "10.10.1.10:1521/dbinstance")
    print(db.version)
    cr = db.cursor()
    # sql='select * from sys_user'
    with open(outputfile, "wt") as f:
        print("PATHNAME_y,BRK_NAME,BRK_ID,max,occur_time", file=f)
    for i in range(len(DF)):
        ycid = "0" + str(DF.iloc[i, 0]) + suffix  # yc_ID
        sqlsel = "select * from ems.SVR_YC_SAMPLE_DEFINE where YC_ID in (%s) ;" % (ycid)
        cr.execute(sqlsel)
        rs = cr.fetchall()
        ycsd = pd.DataFrame(rs)
        his = ycsd.iloc[0, 2]
        cur = ycsd.iloc[0, 3]
        sql = (
            "select %s,occur_time from(select %s,occur_time from %s  \
            where occur_time >= to_date(%s,'yyyy')  order by %s desc ) where rownum =1 ;"
            % (cur, cur, his, year, cur)
        )
        cr.execute(sql)
        rs = cr.fetchall()
        maxpqi = pd.DataFrame(rs)
        maxp = maxpqi.iloc[0, 0]  # 最大值
        octime = maxpqi.iloc[0, 1]  # 最大值时刻
        with open(outputfile, "wt") as f:
            print(
                "%s,%s,%s,%s,%s,"
                % (DF.iloc[i, 9], DF.iloc[i, 2], DF.iloc[i, 0], maxp, octime),
                file=f,
            )
    db.close()


def mergedb():
    ln = pd.read_csv(
        "C:\\Users\\liujg\\Downloads\\ACLN_DOT.csv",
        usecols=[
            "ACLN_DOT_ID",
            "FAC_ID",
            "ACLN_DOT_NAME",
            "ACLN_ID",
            "BAY_ID",
            "PATHNAME",
        ],
    )  # sql  取值
    brk = pd.read_csv(
        "C:\\Users\\liujg\\Downloads\\BRK_DEVICE.csv",
        usecols=["BRK_ID", "FAC_ID", "BRK_NAME", "BRK_TYPE", "BAY_ID", "PATHNAME"],
    )
    brk["BAY_ID"] = brk["BAY_ID"].fillna("null")  # 标记无bay
    brk = brk[~brk["BAY_ID"].isin(["null"])]  # 反选无bay
    ln["BAY_ID"] = ln["BAY_ID"].fillna("null")  # 标记无bay
    ln = ln[~ln["BAY_ID"].isin(["null"])]  # 反选无bay
    sqldb = merge(brk, ln, on=("BAY_ID", "FAC_ID"), how="inner")  # 取交集
    return sqldb


def pqi(device):
    suffix = "0030"  # 负荷p
    suffix = "0040"  # 负荷q
    suffix = "0050"  # 负荷I
    suffix = "0050"  # 主变P
    suffix = "0060"  # 主变q
    suffix = "0070"  # 主变I
    suffix = "0040"  # 线路p
    suffix = "0050"  # 线路q
    suffix = "0060"  # 线路I

    return suffix


if __name__ == "__main__":
    year, device, outputfile = main(sys.argv[1:])
    sqldb = mergedb()
    suffix = pqi(device)
    sql(year, sqldb, suffix)

