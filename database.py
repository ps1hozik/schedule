import pymysql.cursors

from settings import DATABASE


connection = pymysql.connect(
    host=DATABASE["HOST"],
    user=DATABASE["USER"],
    password=DATABASE["PASSWORD"],
    database=DATABASE["NAME"],
    port=DATABASE["PORT"],
    cursorclass=pymysql.cursors.DictCursor,
)
