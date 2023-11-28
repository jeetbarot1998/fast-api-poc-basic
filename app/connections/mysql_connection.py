# import smtplib
# import pymysql
# import ssl
# import traceback
# import sys
# import os
#
# def connection():
#     try:
#         conn = pymysql.connect(host=os.getenv('HOST'),
#                                port = int(os.getenv('PORT')),
#                                user=os.getenv('USER'),
#                                passwd=os.getenv('PASSWD'),
#                                db=os.getenv('DATABASE_NAME'))
#         return conn
#     except Exception as err_msg:
#         for frame in traceback.extract_tb(sys.exc_info()[2]):
#             fname, lineno, fn, text = frame
#             print(f"Error in creating connection object for mysql {text} on line {lineno} with error as {err_msg} ")
#
#
# def test_connection():
#     try:
#         con = connection()
#         cursor = con.cursor()
#         cursor.execute("SELECT 1")  # Execute a simple query
#         result = cursor.fetchall()
#         if result:
#             print("Connection successful!", result)
#         else:
#             print("Connection failed.")
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         if con:
#             con.close()
#
# con = connection()
