 # -*- coding: utf-8 -*-
import time

import logging
import sys

from pymongo import MongoClient



ANTIGATEKEY = "bd9b2d2502d523555354b2dcd136df82"


def serveJSONResponse(response):
    import json
    # print response

    data = json.loads(response)
    links = []
    for x in data.get('rows', []):
        links.append(x['T'])
    return links

def storeFile(fname, **kwargs):
    from gridfs import GridFS
    logger = logging.getLogger('storeFile')
    try:
        logger.info('try to store %s in GridFS' % fname)
        mongo = MongoClient(kwargs.get('host', 'localhost'),
                            port=kwargs.get('port', 6060))

        name = kwargs.get('db','test')
        db = mongo[name]

        fs = GridFS(db)
        oid = None
        with open(fname) as f:
            oid = fs.put(f, filename=fname)
        return oid
    except Exception, err:
        print err
        logger.error(err)

def getFile(oid, fname, **kwargs):
    from gridfs import GridFS
    logger = logging.getLogger('storeFile')
    try:
        logger.info('try to get %s from GridFS', oid)
        mongo = MongoClient(kwargs.get('host', 'localhost'),
                            port=kwargs.get('port', 6060))

        name = kwargs.get('db','test')
        db = mongo[name]

        fs = GridFS(db)
        fh = fs.get(oid)
        if fh:
            with open(fname, 'wb') as fp:
                for chunk in iter(lambda: fh.read(), ''):
                    fp.write(chunk)
    except Exception, err:
        print err
        logger.error(err)

def antigate(fcaptcha, numeric=1):
    """ Input: fcaptcha = path/to/image/with/captcha
        Output: captcha or None
    """
    import urllib2
    from poster.encode import multipart_encode
    from poster.streaminghttp import register_openers


    register_openers()

    #numeric=1 means only numeric on captcha (0 for )
    #see antigate docs for more information about params
    #http://antigate.com/panel.php?action=api
    antigate_data = {"key" : ANTIGATEKEY,
                     "file": open(fcaptcha, "rb"),
                     "numeric" : str(numeric)}
    #there are two ways to send request image: post with multipart and base64
    #because of ... , we use oldstyle multipart.
    datagen, headers = multipart_encode(antigate_data)

    request = urllib2.Request("http://antigate.com/in.php", datagen, headers)
    response = urllib2.urlopen(request).read()
    # print response
    if response[:2] == 'OK':
        #yes, hardcode ID style.
        ID = response[3:]
        #print "Let's wait for captureee"
        timeouts=[10, 5, 5, 5, 10]
        for i, delay in enumerate(timeouts):
            print '%d try, sleep for %dsec' % (i, delay)
            time.sleep(delay)
            url_response = "http://antigate.com/res.php?key=%s&action=get&id=%s" % (ANTIGATEKEY, ID)
            response = urllib2.urlopen(url_response).read()
            # print response
            if response[:3] == 'OK|':
                return response[3:]
            if response == 'CAPCHA_NOT_READY':
                continue
            else:
                #There are 3 possible errors.
                #Nothing to do, print and return None.
                print response
                return None
    else:
        #There are 9 possible errors.
        #It should be fixed on web-interface of antigate I think.
        #So just None return
        print response
        return None


def fetch(link, ext=None, path=None, csize=16 * 1024):
    import urllib2
    from uuid import uuid4
    logger = logging.getLogger('fetch')
    logger.info('try to fetch %s to %s' % (link, path))
    if ext is None:
        ext = ''
    if path is None:
        path = 'tmp/%s.%s' % (str(uuid4()), ext)
    try:
        request = urllib2.urlopen(link)
        with open(path, 'wb') as fp:
            for chunk in iter(lambda: request.read(csize), ''):
                fp.write(chunk)
        return path
    except Exception, err:
        print 'Fetch error, ', err
        logger.error(err)
        return None


def newDocument(data, **kwargs):
    mongo = MongoClient(kwargs.get('host', 'localhost'),
                        port=kwargs.get('port', 6060))
    db, name = kwargs.get('db', 'test'), kwargs.get('collection', 'test')
    collection = mongo[db][name]
    oid = collection.insert(data)
    return oid


def egrul(**kwargs):
    """input: {'ogrninnul':'s'}, output: oid in mongo"""
    import mechanize
    from bs4 import BeautifulSoup
    import cookielib

    logger = logging.getLogger()

    url = "http://egrul.nalog.ru"

    result = {k : v for (k, v) in kwargs.iteritems() if k in ['ogrninnul']}
    if len(result) == 0:
        logger.warning('Wrong argument')
        return None

    result['url'] = url
    for tr in xrange(0, 3):
        try:
            logger.info('%d try' % tr)
            br = mechanize.Browser()
            br.set_handle_robots(False)
            response = br.open(url)
            br.select_form(nr=0)
            #here it is! if you want to use another method, you should be careful about HiddenControl(kind=ul)
            if result.has_key('ogrninnul'):
                br['ogrninnul'] = kwargs['ogrninnul']
            else:
                raise NotImplementedError
            #let's find captcha image! The first img with right signature of src
            soup = BeautifulSoup(response.get_data())
            for x in soup.find_all('img'):
                link = x.get('src')
                pattern = '/static/captcha.html?'
                if link[:len(pattern)] == pattern:
                    clink = url + link
                    break
            image = fetch(clink, ext='gif')
            if not image:
                raise Exception('No image')

            #the most time consumption fragment
            captcha = antigate(image)
            if not captcha:
                raise Exception('No captcha')

            br['captcha'] = captcha
            response = br.submit().read().decode('utf-8')

            links = serveJSONResponse(response)
            logger.info('%d links', len(links))
            if len(links) > 0:
                result['files'] = [storeFile(fetch(url + '/download/' + t, ext='pdf'), **kwargs) for t in links]


            return newDocument(result, **kwargs)

        except Exception, err:
            # print response.read().decode('utf-8')
            logger.error(err)

    logger.warning('possible no result')
    return newDocument(result, **kwargs)

def nalogruuwsfind(**kwargs):
    import mechanize
    import bs4
    from bs4 import BeautifulSoup
    import cookielib

    logger = logging.getLogger()

    url = "https://service.nalog.ru/uwsfind.do"

    result = {k : v for (k, v) in kwargs.iteritems() if k in ['ogrn']}
    if len(result) == 0:
        logger.warning('Wrong argument')
        return None

    result['url'] = url

    try:

        br = mechanize.Browser()
        br.set_handle_robots(False)

        response = br.open(url)

        br.select_form(nr=0)
        if result.has_key('ogrn'):
            br['ogrn'] = result['ogrn']
        else:
            raise NotImplementedError

        response = br.submit()
        soup = BeautifulSoup(response.get_data())
        if soup.find(id='notfound'):
            logger.warning('notfound')
            return newDocument(result, **kwargs)
        else:
            data = soup.find(id='uwsdata')
            if data:
                trs = data.find('tbody').find_all('tr')
                tmp = []
                for x in trs:
                    tmp.append(str(x))
                result['data'] = tmp
                return newDocument(result, **kwargs)

    except Exception, err:
        logger.warning(err)

    logger.warning('possible no data')
    return newDocument(result, **kwargs)



def nalogrubaddrdo(**kwargs):
    import mechanize
    import bs4
    from bs4 import BeautifulSoup
    import cookielib
    import json

    logger = logging.getLogger()

    url_root = "https://service.nalog.ru"
    url = "https://service.nalog.ru/baddr.do"

    result = {k : v for (k, v) in kwargs.iteritems() if k in ['ogrn']}
    if len(result) == 0:
        logger.warning('Wrong argument')
        return None

    result['url'] = url

    try:
        br = mechanize.Browser()
        br.set_handle_robots(False)

        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
                         ('Accept', 'application/json, text/javascript, */*')]

        response = br.open(url)
        br.select_form(nr=0)
        soup = BeautifulSoup(response.get_data())
        for x in soup.find_all('img'):
            link = x.get('src')
            pattern = '/static/captcha.html?'
            if link[:len(pattern)] == pattern:
                clink = url_root + link
                break
        #may be we can use BytesIO.. but not today.
        image = fetch(clink, ext='gif')
        if not image:
            raise Exception('No image')
        captcha = antigate(image)
        if not captcha:
            raise Exception('No captcha')
        br['captcha'] = captcha

        if result.has_key('ogrn'):
            br['ogrn'] = result['ogrn']
        else:
            raise NotImplementedError
        response = br.submit().read().decode('utf-8')
        # soup = BeautifulSoup(response.get_data())
        data = json.loads(response)
        if data.has_key('rows'):
            result.update({'data' : data['rows']})
        return newDocument(result, **kwargs)
    except Exception, err:
        logging.warning(err)

    return newDocument(result, **kwargs)


def vestnikvgr(s):
    raise NotImplementedError
    url = 'http://www.vestnik-gosreg.ru/publ/vgr/'

def vestnikfz83(**kwargs):
    import mechanize
    import bs4
    from bs4 import BeautifulSoup
    import cookielib

    logger = logging.getLogger()

    url = "http://www.vestnik-gosreg.ru/publ/fz83/"

    result = {k : v for (k, v) in kwargs.iteritems() if k in ['query']}
    if len(result) == 0:
        logger.warning('Wrong argument')
        return None
    result['url'] = url

    try:
        br = mechanize.Browser()

        br.set_handle_robots(False)

        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'),
                         ('Accept', 'application/json, text/javascript, */*')]

        response = br.open(url)

        br.select_form(nr=0)
        if result.has_key('query'):
            br['query'] = result['query']
        else:
            raise NotImplementedError

        response = br.submit()

        soup = BeautifulSoup(response.get_data())
        div = soup.find(id='SearchReport')
        tmp = div.string
        if tmp:
            result.update({'data' : tmp})

        return newDocument(result, **kwargs)

    except Exception, err:
        logger.warning(err)

    logger.warning('possible no data')
    return newDocument(result, **kwargs)

if __name__ == "__main__":
    print 'Please, use run.py'
