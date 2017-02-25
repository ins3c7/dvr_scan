#/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'ins3c7 - fev/2017'

import socket, threading, time, os, json, requests
from datetime import datetime

logo = '''
 _ __  _   __ __   ______ 
| |  \| |/' _/__`./ _/_  |
| | | ' |`._`.|_ | \__/ / 
|_|_|\__||___/__.'\__/_/  
              * portscan *
'''

class tcp_scanner:
  def __init__(self, addr=[], port=None, threads=None):
    self.addr = addr
    self.port = port
    self.threads = threads
    self.print_here = None

  def start(self):
    self.t1 = datetime.now()
    self.start_scanning()
    self.t2 = datetime.now()
    self.total_time = self.t2-self.t1
    time.sleep(4)
#    print '\n[+] Total time Consumed: {}\n'.format(str(self.total_time))

  def start_scanning(self):
    active_threads = 0
    threads = []
    
    addrs = []
    
    ad1 = '.'.join(self.addr.split('.')[0:2])
    in2, en2 = self.addr.split('.')[2].split('-')
    in3, en3 = self.addr.split('.')[3].split('-')

    for i in range(int(in2), int(en2)+1):
      for j in range(int(in3), int(en3)+1):
        addrs.append(str(ad1)+'.'+str(i)+'.'+str(j))

    for addr in addrs:
      if active_threads == 40:
        time.sleep(1)
      sobj = threading.Thread(target=self.main_engine, args={addr})
      sobj.start()
      active_threads = int(threading.activeCount())

    for i in threads:
      i.join()

  def main_engine(self, addr):
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(3)
      k = str(s.connect_ex((addr, int(self.port))))
      if k == '0':
        try:
          r = requests.get('http://ip-api.com/json/' + str(addr))
          resp = r.json()
          cidade = resp['city'].encode('utf-8')
          estado = resp['region'].encode('utf-8')
          print '[OPEN]', addr+':'+self.port+' / '+str(cidade)+'-'+str(estado)
        except Exception, e:
          pass
      else:
        pass
      s.close()
    except:
      pass

if __name__ == '__main__':
  os.system('clear')
  print logo
  print
  addr = str(raw_input('Addr: '))
  port = str(raw_input('Port: '))
  print
  print 'Scanning...'
  print

  scan = tcp_scanner(addr=addr, port=port)
  scan.start()
