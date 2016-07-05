from json import load
from sqlite3 import connect

def main():
    db = connect('database/trojan-evaluation.db')
    cs = db.cursor()
    cs.execute('delete from trojan')

    data = load(file('data/trojan.json'))
    i = 1
    for trojan in data['trojan']:
        sql = 'insert into trojan values({id}, \'{name}\', \'{url}\', {grade}, \'{time}\')'.format(id=i, **trojan)
        cs.execute(sql)
        i += 1
        
    db.commit()
    db.close()

if __name__ == '__main__':
    main()
