#Complex fan retrieval productions, v.2
# Kam Kwok, 2014

import sys
sys.path.append('/Users/robertwest/CCMSuite')

import ccm
from ccm.lib.actr import *
log=ccm.log(html=True)

class CFanModel(ACTR):
    goal=Buffer()
    retrieval=Buffer()
    img=Buffer()
##    memory=Memory(retrieval,latency=0.63)
    memory=Memory(retrieval,latency=0.05,threshold=-25,maximum_time=20,finst_size=10,finst_time=0.0)
    spread=DMSpreading(memory,goal)
    spread.strength=1
    spread.weight[goal]=0.33
#***
# with slots 
    def init():
        memory.add('objs:ring cont:bucket')
        memory.add('objs:ring cont:box')
        memory.add('cont:box loc:pool')

### slotted *** *** by obj
    def start_obj(goal='cmd:test objs:?obj loc:?location'):
        memory.request('objs:?obj cont:?') #get contianer in retrieval
        goal.set('cmd:usecontainer objs:?obj loc:?location')
    
    def useContGetlocation(goal='cmd:usecontainer objs:?obj loc:?location',
                   retrieval='objs:?obj cont:?container', memory='error:False'):
        retrieval.clear()
        memory.request('cont:?container loc:?')
        goal.set('cmd:respond objs:?obj loc:?location')

    def respond_yes(goal='cmd:respond objs:?obj loc:?location',
                  retrieval='cont:?container loc:?location', memory='error:False'):
        print 'Yes'
        retrieval.clear()
        goal.clear()
    #wrong location
    def respond_wloc_retryC (goal='cmd:respond objs:?obj loc:?location',
                      retrieval='cont:?container loc:!?location'):
        img.set('cont:?container')
        print "Wrong location, re-try with container", container
        memory.request('cont:?container loc:?')
        goal.set('cmd:respond objs:?obj loc:?location')

    #Retry - no location retry with object   
    def respond_noloc_retryO (goal='cmd:respond objs:?obj loc:?location',
                      retrieval='cont:?container'):
        img.set('cont:?container')
        print "No location, re-try for another container"
        retrieval.clear()
        goal.set('cmd:test objs:?obj loc:?location')
    #retrieved the same container and retrieved no location
    # Retry O to get another C
    def respond_retryC_RetryOL(goal='cmd:respond objs:?obj loc:?location',
                      img='cont:?container',
                      retrieval='cont:?container'):
        print 'Get another container'
        retrieval.clear()
        goal.set('cmd:test objs:?obj loc:?location')
    # Say No:after retry, got a wrong location with the repeated container    
    def respond_No_wloc_img(goal='cmd:respond objs:?obj loc:?location',
                      img='cont:?container',
                      retrieval='cont:?container loc:!?location'):
        print 'No'
        retrieval.clear()
        goal.clear()

    def mem_error(goal='cmd:respond objs:?obj loc:?location',
                  img='cont:?container',
                  memory='error:True'):
        print "Cannot recall any fact...so no!"
        retrieval.clear()
        goal.clear()

#### slotted *** *** by location
#********************
    def start_loc(goal='cmd:testl objs:?obj loc:?location'):
        memory.request('cont:? loc:?location') #get contianer in retrieval
        goal.set('cmd:getobj objs:?obj loc:?location')
    
    def useContGetObj(goal='cmd:getobj objs:?obj loc:?location',
                   retrieval='cont:?container loc:?location', memory='busy:False'):
        retrieval.clear()
        memory.request('objs:? cont:?container')
        goal.set('cmd:respondl objs:?obj loc:?location')

    def respond_yes_loc(goal='cmd:respondl objs:?obj loc:?location',
                  retrieval='objs:?obj cont:?container', memory='error:False'):
        print 'Yes by location'
        retrieval.clear()
        goal.clear()
    #wrong object
    def respond_wobj_retryC (goal='cmd:respondl objs:?obj loc:?location',
                      retrieval='objs:!?obj cont:?container'):
        img.set('cont:?container')
        print "Wrong object, re-try with container", container
        memory.request('objs:? cont:?container')
        goal.set('cmd:respondl objs:?obj loc:?location')

    #Retry - no object retry with object   
    def respond_noobj_retryO (goal='cmd:respondl objs:?obj loc:?location',
                      retrieval='cont:?container'):
        img.set('cont:?container')
        print "No object, re-try for another container"
        retrieval.clear()
        goal.set('cmd:testl objs:?obj loc:?location')
    #retrieved the same container and retrieved no object
    # Retry O to get another C
    def respond_retryC_RetryOL(goal='cmd:respondl objs:?obj loc:?location',
                      img='cont:?container',
                      retrieval='cont:?container'):
        print 'Get another container'
        retrieval.clear()
        goal.set('cmd:testl objs:?obj loc:?location')
    # Say No:after retry, got a wrong object with the repeated container    
    def respond_No_wobj_img(goal='cmd:respondl objs:?obj loc:?location',
                      img='cont:?container',
                      retrieval='objs:!?obj cont:?container'):
        print 'No'
        retrieval.clear()
        goal.clear()

    def mem_error_l(goal='cmd:respondl objs:?obj loc:?location',
                  img='cont:?container',
                  memory='error:True'):
        print "Cannot recall any fact...so no!"
        retrieval.clear()
        goal.clear()

        
#*** *** by obj
        
### no slot ******
##    def init():
##        memory.add('ring in bucket')
##        memory.add('ring in box')
##        memory.add('box in pool')
##
### probe is ?obj in ?location
##    def start_obj(goal='test ?obj ?location'):
##        memory.request('?obj in ?') #get contianer in retrieval
##        goal.set('getcontainer ?obj ?location')
##    
##    def getcontainer(goal='getcontainer ?obj ?location',
##                   retrieval='?obj in ?container', memory='error:False'):
##        retrieval.clear()
##        memory.request('?container in ?')
##        goal.set('respond ?obj ?location')
##
##    def respond_yes(goal='respond ?obj ?location',
##                  retrieval='?container in ?location', memory='error:False'):
##        print 'Yes'
##        retrieval.clear()
##        goal.clear()
##
##    def respond_retry (goal='respond ?obj ?location',
##                      retrieval='?container in !?location',memory='error:False'):
##        img.set('?container')
##        print "re-try with container", container
##        memory.request('?container in ?')
##        goal.set('respond ?obj ?location')
####        retrieval.clear()
####        goal.set('test ?obj ?location')
##  
##    def respond_no(goal='respond ?obj ?location',
##                      img='?container',
##                      retrieval='?container in !?location'):
####    def respond_no(goal='respond ?obj ?location',
####                      retrieval='?container in !?location'):
##        print 'No'
##        retrieval.clear()
##        goal.clear()
##
##    def mem_error(goal='respond ?obj ?location', memory='error:True'):
##        print "Cannot recall any fact...so no!"
####        goal.set('test ?obj ?location')
##        retrieval.clear()
##        goal.clear()

##        # by location
##
##    def start_loc(goal='test byloc ?obj ?location'):
##        memory.request('? in ?location') #c
##        goal.set('getcontainerl ?obj ?location')#c
##    
##    def getcontainerl(goal='getcontainerl ?obj ?location',
##                   retrieval='?container in ?location', memory='busy:False'):
##        retrieval.clear()
##        memory.request('? in ?container')
##        goal.set('respondl ?obj ?location')
##
##    def respondl_yes(goal='respondl ?obj ?location',
##                  retrieval='?obj in ?container'):
##        print 'Yes'
##        retrieval.clear()
##        goal.clear()
##
##    def respondl_retry (goal='respondl ?obj ?location',
##                      retrieval='!?obj in ?container',memory='busy:False'):
##        img.set('?container')
##        print "re-try location", container
##        memory.request('? in ?container')
##        goal.set('respondl ?obj ?location')
####        retrieval.clear()
####        goal.set('test ?obj ?location')
##  
##    def respondl_no(goal='respondl ?obj ?location',
##                      img='?container',
##                      retrieval='!?obj in ?container'):
##        print 'No'
##        retrieval.clear()
##        goal.clear()
##
##    def mem_error(goal='? ? ?', memory='error:True'):
##        print "Cannot recall any fact, I'll say no."
##        retrieval.clear()
##        goal.clear()


model=CFanModel()
ccm.log_everything(model)
##for item in ['test ring pool','test hippie park']:
##    model.goal.set(item)
##    model.run()
##model.goal.set('test ring bank')
##model.run()
##model.goal.set('test ring pool')
##model.run()
model.goal.set('cmd:test objs:ring loc:pool')
model.run()
model.goal.set('cmd:test objs:ring loc:bank')
model.run()
##model.goal.set('cmd:testl objs:ring loc:pool')
##model.run()
##model.goal.set('cmd:testl objs:ring loc:bank')
##model.run()
