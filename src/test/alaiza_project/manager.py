import logging
import pandas as pd
import subprocess
import csv


_logger = logging.getLogger(__name__)

def getCleanDataframe(listcoins,dictdata,daystored):
    data=[]
    for key in dictdata:
        if(key in listcoins):
            auxrow = []
            auxrow.append(daystored)
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
    df = pd.DataFrame(data, columns=['extract_date','ID', 'Price_cny','Name_nm','Timestamp_tm','Price_gbp','Label','Price_rur','Price_btc','Price_usd','Volume_24h','Price_eur'])
    return df

def storeinBucket(daystored,dataframestored):
    (ret, current_path, err) = run_cmd(['pwd'])
    current_path = current_path.replace('\n','/')
    namefile = 'crypto_data_'+daystored+'.csv'
    with open(current_path+'output/'+namefile, 'wb') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(dataframestored)
    _logger.info('Exporting into bucket')
    (ret, out, err) = run_cmd(['gsutil','cp',current_path+'output/'+namefile,'gs://crypto-alaiza-project/data/crypto-WorldCoinIndex/'])
    if(ret==1):
        _logger.error('Exporting into bucket FAILED, maintaining the file: '+current_path + 'output/' + namefile)
    else:
        _logger.info('cleaning file: '+current_path + 'output/' + namefile)
        (ret, out, err) = run_cmd(['rm', current_path + 'output/' + namefile])

def storelogsBucket():
    (ret, current_path, err) = run_cmd(['pwd'])
    current_path = current_path.replace('\n', '/')
    (ret, files, err) = run_cmd(['ls', current_path + '/logs/'])
    Lfiles = files.split('\n')
    Lauxfiles = []
    for a in Lfiles:
        if ('crypto_logfile.log.' in a):
            Lauxfiles.append(a)
    for a in Lauxfiles:
        (ret, out, err) = run_cmd(['gsutil', 'cp', current_path + '/logs/'+a,'gs://crypto-alaiza-project/logs/crypto-WorldCoinIndex/'])
        (ret, out, err) = run_cmd(['rm', current_path + '/logs/' + a])
    print('done')


def GetQueriesForMetadata(fulldict, lastpricesfataframe):
    fulldictkeys = fulldict.keys()
    dictaux = {}
    for a in lastpricesfataframe:
        dictaux[a[0]] = a[1:]

    newcurrencies = []
    newupdates = []
    for a in fulldictkeys:
        if (str(a) not in dictaux.keys()):
            newcurrencies.append(a)
        else:
            price = fulldict.get(a).get('Price_eur')
            if (price!=dictaux.get(a)):
                newupdates.append([a,price])

    Lqueries = []

    return Lqueries

def run_cmd(args_list):
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_output, s_err = proc.communicate()
    s_return =  proc.returncode
    return s_return, s_output, s_err


