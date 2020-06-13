#python2.6.6 192.168.31.42环境
import MySQLdb
import os

host = "127.0.0.1"
user = "dayou"
passwd = "asdasd321321"
database = "bookdb"

def printVersion():
    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=database, charset = 'utf8')

    cursor = db.cursor()

    cursor.execute("SELECT VERSION()")

    data = cursor.fetchone()

    print("database version : %s" %data)

    db.close()


def update_book_name():

    sql = "SELECT book_id, name FROM book_meta where book_id>6199 and book_id<6399"
    print(sql)

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=database, charset = 'utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    books = cursor.fetchall()
    db.close()

    for book in books:
     #   print('book id: ' + str(book[0]))
     #   print('book name: ' + book[1])
        try:
            os.rename(book[1]+'.epub', str(book[0])+'.epub')
        except Exception as e:
            print e
            print(str(book[0]) + ' rename fail.................\r\n')
        else:
            print(str(book[0]) + 'rename success\r\n') 

    print("books num: "+str(len(books)))


if __name__ == '__main__':
    printVersion()
    update_book_name()