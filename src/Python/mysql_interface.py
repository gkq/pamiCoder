#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.externals import joblib
import MySQLdb as mysql

def connect_database(ip='localhost',user='root', #'10.255.29.119'
    pwd='abc123',database='tianchi'):

    try:
        conn=mysql.connect(ip,user,pwd,database)
        cur=conn.cursor()
        print("MySQL Connection: Success")
        return conn,cur
    except mysql.Error as e:
        print("MySQL Error %d:%s"%(e.args[0],e.args[1]))
        return None,None

def fetch_data(cur,feature_table_name,table_schema='result'):
    '''
        fetch_data: Get the np.array type from database
        param:
            cur: cursor
            feature_table_name: table name of user-item feature
            table_schema: database name, default is 'tianchi'
            except_fields: Since we only need the feature values except user-id,item-id
                            record-id, we have to eliminate them from feature fields,
                            default is [('user_id',),('item_id',)]
    '''
    try:
        sql_select_data='''
            select user_id,item_id from %s
        '''%(feature_table_name)
        data_count=cur.execute(sql_select_data)
        data_tuples=cur.fetchall()
        return data_tuples
    except mysql.Error as e:
        print("MySQL Error %d:%s"%(e.args[0],e.args[1]))


def main(args):
    pass
def disconnect_database(conn,cur):
    try:
        cur.close()
        conn.close()
        print("MySQL Disconnection: Success")
    except mysql.Error as e:
        print("MySQL Error %d:%s"%(e.args[0],e.args[1]))

def converFormat(Array):
    Result=[]
    for Elem in Array:
        Result.append(int(Elem))
    return Result

# Result=joblib.load('rf.model_new_test')
# # print Result
# [conn,cur]=connect_database()
# testing_data=fetch_data(cur,'pre_ui_user_item_category')
# total=0
# csv=open('result.csv2','w')
# Temp='user_id,item_id\r\n'
#
# for i,item in enumerate(Result):
#     if item[1]>0.3:
#         total+=1
#         Temp=Temp+str(testing_data[i][0])+','+str(testing_data[i][1])+'\r\n'
# total=0;
# SQL="drop table if exists result.prediction;"
# cur.execute(SQL)
# SQL="create table result.prediction(user_id int,item_id int);"
# cur.execute(SQL)
# for i,item in enumerate(Result):
# 	# print item
# 	if item[1]>0.3:
# 		total=total+1
# 		# cur.execute('insert into result.prediction values (%s,%s)',testing_data[i])
# cur.close()
# conn.commit()
# conn.close
# print(total)
# # print Temp
# csv.write(Temp)
# csv.close()

[conn,cur]=connect_database()
SQL = 'select * from mars_tianchi_user_actions where user_id=\'7063b3d0c075a4d276c5f06f4327cf4a\''
cur.execute(SQL)
res = cur.fetchall()
print(res)