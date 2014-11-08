

import sys
sys.path.append('/Users/robertwest/CCMSuite')
#sys.path.append('C:\Users\rlwes_000\Documents\GitHub\ccmsuite')

import ccm      
log=ccm.log()   

from ccm.lib.actr import *  

class MyEnvironment(ccm.Model):
    pass

class MyAgent(ACTR):
    focus=Buffer()
    Imagebuffer=Buffer
    Visionbuffer=Buffer()
    DMbuffer=Buffer()
    DM=Memory(DMbuffer)

    
    def init():
        DM.add('objectx:apple container:bowl')
        #DM.add('objectx:apple container:bucket')
        #DM.add('objectx:apple container:bin')
        DM.add('container:bowl location:house')
        #DM.add('container:bucket location:store')
        #DM.add('container:bin location:park')
        focus.set('status:start')
        Visionbuffer.set('objectx:apple location:house')


#start trial
    def start(focus='status:start', Visionbuffer='objectx:?objectx'):
        print "recalling based on objects"
        DM.request('objectx:?objectx container:?')
        focus.set('status:get_container') 


#recall a container for the target object
    def container(focus='status:get_container', DMbuffer='objectx:?objectx container:?container'):  
        print objectx
        print "is in ......."         
        print container
        DM.request('container:?container location:?')
        focus.set('status:get_location')
        

#recall a location for the container the object is in
    def location(focus='status:get_location', DMbuffer='container:?container location:?location'):  
        print container
        print "is in ......."         
        print location
        focus.set('status:check_location')


#success
    def yes_location(focus='status:check_location', DMbuffer='container:?container location:?location', Visionbuffer='location:?location'):  
        print 'YES'
        focus.set('status:stop')


#failure
    def no_location(focus='status:check_location', DMbuffer='container:?container location:?location', Visionbuffer='location:!?location'):  
        print 'NO'
        focus.set('status:stop')



tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment
