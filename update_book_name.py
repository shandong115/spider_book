import MySQLdb
import os
from os.path import getsize
import time
import io

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
    
def get_book_size():

    dir_path = "/home/zhaodan/tmp/book/"
    books=os.listdir(dir_path)
    i=0
    with io.open('filesize.txt', mode='wb') as ff:
        for book in books:
            try:
                filesize = getsize(dir_path+book)
                msg = book+'|'+str(filesize)+'\n'
                ff.write(msg)
                i=i+1
                if(i%100 == 0):                    
                    print('have dealed:'+str(i))
            except Exception as e:
                print(e)
                print(book + ' getsize fail.................\r\n')
            #break;

    
    
def update_book_size():

    sql = "SELECT book_id, name FROM book_meta where book_id>6199"
    print(sql)

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=database, charset = 'utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    books = cursor.fetchall()

    dir_path = "/usr/share/nginx/html/epub3/"
    i=0
    print(str(len(books)))
    for book in books:
        book_id = book[0]
        book_name = book[1]

        file_name = dir_path + str(book_id) + '.epub'
        try:
            fielsize = getsize(file_name)
            sql2 = "UPDATE book_meta SET size = %d WHERE book_id = %d" % (fielsize,book_id)
            print(sql2)
            cursor.execute(sql2)
            i=i+1
            if(i%10 == 0):
                db.commit()
                print('commit ok:'+str(i))
                time.sleep(2)
        except Exception as e:
            print(e)
            print(file_name + ' getsize fail.................\r\n')
            db.commit()
        #else:
            #print(file_name + 'update size success: ' + str(fielsize) + '\r\n')    
        #break
    db.commit()
    db.close()
    
def update_book_name():

    sql = "SELECT book_id, name FROM book_meta where book_id<6200"
    print(sql)

    db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=database, charset = 'utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    books = cursor.fetchall()
    db.close()

    for book in books:
        print('book id: ' + str(book[0]))
        print('book name: ' + book[1])
        try:
            os.rename(book[1]+'.epub', str(book[0])+'.epub')
        except Exception as e:
            print e
            print(str(book[0]) + ' rename fail.................\r\n')
        else:
            print(str(book[0]) + 'rename success\r\n')
        break

    print("books num: "+str(len(books)))


if __name__ == '__main__':
    printVersion()
    #get_book_size()
    #update_book_size()
    update_book_name()