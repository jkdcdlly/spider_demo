# coding=utf-8
#
# Create Author: 陈志磊
#
# Create Date:  2018/5/26 下午10:33
#
# Author Email: chenzl@bbtree.com
#
# desc :
#
# 引入所需模块
import os
import sys

# # 项目目录
WORK_SPACE = os.path.split(os.path.realpath(__file__))[0].split("dw")[0]
# 加载自定义模块
sys.path.append(WORK_SPACE)
from dw.utils import dateutils
from dw.conf.init_conf import commonUtils

# 脚本名
FILE_NAME = os.path.split(os.path.realpath(__file__))[1].split(".")[0]
utils = commonUtils(FILE_NAME)

utils.logger.info("参数准备")
if len(sys.argv) > 1 and sys.argv[1]:
    SHORT_DATE = sys.argv[1]  # string类型
else:
    SHORT_DATE = dateutils.format_date(pattern="%Y%m%d")  # string类型
DATE = dateutils.to_datetime(SHORT_DATE)  # data类型
LONG_DATE = dateutils.format_date(DATE, pattern="%Y-%m-%d")  # string类型

START = dateutils.current_time()
utils.logger.info("开始时间:" + str(START))
utils.logger.info("业务日期:" + SHORT_DATE)
# ======================process_start========================================

utils.logger.info("模块一：")

sql = """

"""
utils.impala_run(sql, [SHORT_DATE])

utils.logger.info("模块二：增加compute stats")
utils.impala_run("compute incremental stats %s partition (dt='%s')" % ("table_name", "partitions"))
END = dateutils.current_time()
utils.logger.info("结束时间:" + str(END))
utils.logger.info("共耗时...." + str(END - START))