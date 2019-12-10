import asyncio

@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost:%s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    
    writer.close()

loop = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

# DeprecationWarning: "@coroutine" decorator is deprecated since Python 3.8, use "async def" instead
#   def wget(host):
# wget www.163.com...
# wget www.sina.com.cn...
# wget www.sohu.com...
# www.sina.com.cn header > HTTP/1.1 302 Moved Temporarily
# www.sina.com.cn header > Server: nginx
# www.sina.com.cn header > Date: Tue, 10 Dec 2019 09:44:54 GMT
# www.sina.com.cn header > Content-Type: text/html
# www.sina.com.cn header > Content-Length: 138
# www.sina.com.cn header > Connection: close
# www.sina.com.cn header > Location: https://www.sina.com.cn/
# www.sina.com.cn header > X-Via-CDN: f=edge,s=ctc.xian.ha2ts4.42.nb.sinaedge.com,c=223.11.128.21;
# www.sina.com.cn header > X-Via-Edge: 157597109456315800bdf433a8971283126cc
# An open stream object is being garbage collected; call "stream.close()" explicitly.
# www.sohu.com header > HTTP/1.1 200 OK
# www.sohu.com header > Content-Type: text/html;charset=UTF-8
# www.sohu.com header > Connection: close
# www.sohu.com header > Server: nginx
# www.sohu.com header > Date: Tue, 10 Dec 2019 09:43:44 GMT
# www.sohu.com header > Access-Control-Allow-Credentials: true
# www.sohu.com header > Vary: Origin,Access-Control-Request-Method,Access-Control-Request-Headers
# www.sohu.com header > Access-Control-Allow-Headers: Origin,Content-Type,authorization,Accept,token,X-Requested-With
# www.sohu.com header > Content-Encoding: gzip
# www.sohu.com header > Access-Control-Allow-Methods: POST,GET,OPTIONS,DELETE
# www.sohu.com header > Content-Language: zh-CN
# www.sohu.com header > Access-Control-Expose-Headers: Origin,Access-Control-Request-Method,Access-Control-Request-Headers,X-forwared-port,X-forwarded-host
# www.sohu.com header > Cache-Control: max-age=60
# www.sohu.com header > X-From-Sohu: X-SRC-Source
# www.sohu.com header > FSS-Cache: HIT from 4330546.6820924.5510744
# www.sohu.com header > FSS-Proxy: Powered by 4461620.7083070.5641820
# An open stream object is being garbage collected; call "stream.close()" explicitly.
# www.163.com header > HTTP/1.1 200 OK
# www.163.com header > Date: Tue, 10 Dec 2019 09:44:53 GMT
# www.163.com header > Content-Type: text/html; charset=GBK
# www.163.com header > Connection: close
# www.163.com header > Expires: Tue, 10 Dec 2019 09:45:57 GMT
# www.163.com header > Server: nginx
# www.163.com header > Cache-Control: no-cache,no-store,private
# www.163.com header > Age: 17
# www.163.com header > Vary: Accept-Encoding
# www.163.com header > X-Ser: BC51_dx-lt-yd-shandong-jinan-5-cache-6, BC40_dx-lt-yd-shandong-jinan-5-cache-6, BC24_dx-neimenggu-huhehaote-4-cache-3
# www.163.com header > cdn-user-ip: 223.11.128.21
# www.163.com header > cdn-ip: 110.76.156.22
# www.163.com header > X-Cache-Remote: HIT
# www.163.com header > cdn-source: baishan
# An open stream object is being garbage collected; call "stream.close()" explicitly.