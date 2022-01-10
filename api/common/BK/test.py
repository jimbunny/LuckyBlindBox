#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:jingtongyu
# datetime:2021/6/10 上午8:52
# software: PyCharm
import pandas as pd

df = pd.read_excel('address.xls', sheet_name='Sheet 1')
data=df.loc[:,['乡镇名称','县名称', '府名称', '邮编']].values#读所有行的title以及data列的值，这里需要嵌套列表
print("读取指定行的数据：\n{0}".format(data))