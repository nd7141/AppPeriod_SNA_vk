import logging
import os
import sys
from pymongo import MongoClient
from gridfs import GridFS

import crawler


def testMongo(**kwargs):
    logger = logging.getLogger()
    try:
        mongo = MongoClient(kwargs.get('host', 'localhost'), port=kwargs.get('port', 6060))
        ctest = mongo.test_database.test.count()
        cfiles = mongo.test_database.fs.files.count()
        logger.info('We have connection')
        logger.info('We have %d documents in test and %d files in fs.files' % (ctest, cfiles))
    except Exception, err:
        logger.error(err)


def testGridFS(**kwargs):
    logger = logging.getLogger()
    try:
        fname = [f for f in os.listdir('.') if f[-3:] == '.py'][0]
        logger.info('Try to store file into GridFS')
        oid = crawler.storeFile(fname, **kwargs)
        logger.info('Should be on test_database.fs.files %s',oid)
        fout = 'tmp/tested.py_'
        crawler.getFile(oid, fout, **kwargs)
        if os.path.isfile(fout):
            logger.info('File retrieved')
        else:
            logger.warning('Not retrieved')
    except Exception, err:
        logger.error(err)


def sampleAll():
    params = {'host' : 'localhost', 'port' : 6060}

    positive = '1145658008033'
    negative = '0020202020003'

    params['ogrninnul'] = positive
    print crawler.egrul(**params)
    params['ogrninnul'] = negative
    print crawler.egrul(**params)

    params['ogrn'] = positive
    print crawler.nalogruuwsfind(**params)
    params['ogrn'] = negative
    print crawler.nalogruuwsfind(**params)

    params['ogrn'] = '1020800568040'
    print crawler.nalogrubaddrdo(**params)

    params['ogrn'] = ''
    print crawler.nalogrubaddrdo(**params)

    params['ogrn'] = '1145658008033'
    print crawler.nalogrubaddrdo(**params)

    params['query'] = '1145658008033'
    print crawler.vestnikfz83(**params)




def testAll():
    settings = {'host' : 'localhost', 'port' : 6060}

    testMongo(**settings)
    testGridFS(**settings)

if __name__ == "__main__":

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    testAll()
    sampleAll()