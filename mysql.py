'''
Created on Dec 1, 2013

MySQL API

@author: surfer
'''
import json

class db:

    def __init__(self, conn):
        self.conn = conn
        
    def Insert(self, table, data):
    # insert data (pairs of column and value) into table
        strCol = ''
        strVal = ''
        
        for k in data.keys():
            strCol += ',`' + k + '`'
            if isinstance(data[k], list):
                dataValue = '|'.join(data[k])
            elif isinstance(data[k], dict):
                dataValue = json.dumps(data[k], ensure_ascii=False)
            elif not isinstance(data[k], str):
                dataValue = str(data[k])
            else:
                dataValue = data[k]
            
            strVal += ",'" + self.conn.escape_string(dataValue) + "'"

        qs = "INSERT INTO `%s` (%s) VALUES (%s)" % (table, strCol[1:], strVal[1:])
        self.conn.query(qs)
            
        return self.conn.insert_id()
    
    def Update(self, dbname, updatedata, wheredict):
        
        where = '1'
        for k in wheredict.keys():
            where += " AND `"+k+"`='"+self.conn.escape_string(str(wheredict[k]))+"'"
        updatestr = ''
        for k in updatedata.keys():
            if updatedata[k]:
                updatestr += ",`"+k+"`='"+self.conn.escape_string(str(updatedata[k]))+"'"
        
        qs = "UPDATE `"+dbname+"` SET "+updatestr[1:]+" WHERE "+where
        self.conn.query(qs)
    
    def runQueryReturnOne(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()
         
    def getCount(self, dbname, wheredict):
        
        where = '1'
        for k in wheredict.keys():
            where += " AND `"+k+"`='"+self.conn.escape_string(str(wheredict[k]))+"'"
            
        qs = "SELECT COUNT(*) FROM `"+dbname+"` WHERE "+where
        self.conn.query(qs)
        r=self.conn.store_result()
        tup = r.fetch_row()
        return int(tup[0][0])
        
    def getAll(self, qs):
        self.conn.query(qs)
        r=self.conn.store_result()
        tup = r.fetch_row(maxrows=0, how=1)
        return tup
    
    def getOne(self, qs):
        self.conn.query(qs)
        r=self.conn.store_result()
        tup = r.fetch_row(maxrows=1, how=1)
        return tup[0]

    def check_crawled_url(self, url_table, url_filter):
        
        cur = self.conn.cursor()
        cur.execute("select 'dummy value' from %s where %s limit 1" % (url_table, url_filter))
        rows = cur.fetchall()
        
        if rows:
            is_url_found = True
        else:
            is_url_found = False
        
        return is_url_found