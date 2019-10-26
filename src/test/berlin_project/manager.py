import logging
import pandas as pd


_logger = logging.getLogger(__name__)

def getCleanDataframe(listcoins,dictdata):
    data=[]
    for key in dictdata:
        if(key in listcoins):
            auxrow = []
            auxrow.append(key)
            auxrow.append(str(dictdata[key].get('Price_cny')))
            auxrow.append(str(dictdata[key].get('Name')))
            auxrow.append(str(dictdata[key].get('Timestamp')))
            auxrow.append(str(dictdata[key].get('Price_gbp')))
            auxrow.append(str(dictdata[key].get('Label')))
            auxrow.append(str(dictdata[key].get('Price_rur')))
            auxrow.append(str(float(dictdata[key].get('Price_btc'))))
            auxrow.append(str(dictdata[key].get('Price_usd')))
            auxrow.append(str(dictdata[key].get('Volume_24h')))
            auxrow.append(str(dictdata[key].get('Price_eur')))
            data.append(auxrow)
    df = pd.DataFrame(data, columns=['ID', 'Price_cny','Name_nm','Timestamp_tm','Price_gbp','Label','Price_rur','Price_btc','Price_usd','Volume_24h','Price_eur'])
    return df