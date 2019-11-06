import logging


from sqlalchemy import create_engine


_logger = logging.getLogger(__name__)

class DBService:

    def __init__(self, host,port,user,passw,schema,tablename):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__pass = passw
        self.__sche = schema
        self.__table = tablename
        try:
            self.__conn = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + schema, echo=False)
        except:
            raise Exception('Unable to connect to MySQL connector')



    def createTable(self):
        self.__conn.execute("""
            create table if not exists {0}.{1} (
                extract_date integer, 
                ID varchar(20),
                Price_cny float,
                Name_nm varchar(20),
                Timestamp_tm bigint,
                Price_gbp float,
                Label varchar(20),
                Price_rur float,
                Price_btc float,
                Price_usd float,
                Volume_24h double,
                Price_eur float
                )""".format(self.__sche,self.__table)
                )
        _logger.info('create table executed')


    def getAvailableCurrencies(self):
        L=[]
        sql = """select ID from crypto.metadata_currencies where activate = 'Y'"""
        respons = self.__conn.execute(sql)
        dataframe = respons.fetchall()
        for a in dataframe:
            L.append(a[0])
        return L


    def createMetaTable(self):
        self.__conn.execute("""
            create table if not exists crypto.ExecutionMetaTable (
                exec_date date, 
                num_cryptos integer,
                num_lines_extracted integer
                )"""
                )
        _logger.info('create table executed')

    def GetDataframeDay(self,daystored):
        query = """select * from {0}.{1} where extract_date = {2}""".format(self.__sche,self.__table,daystored)
        response = self.__conn.execute(query)
        dataframe = response.fetchall()
        return dataframe



    def storeDataFrame(self,dataframecleandata):
        dataframecleandata.to_sql(name=self.__table, con=self.__conn, if_exists = 'append', index=False)
        _logger.info('data stored')



    def storeExecution(self,daystored,len_limitcoins,len_dataframestored):
        sql = """insert into crypto.ExecutionMetaTable values (
        {0},
        {1},
        {2}
        )""".format(daystored,len_limitcoins,len_dataframestored)
        self.__conn.execute(sql)





