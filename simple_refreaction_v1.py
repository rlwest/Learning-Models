#################### ham cheese forgetting DM model ###################
 
import ccm      
log=ccm.log()  
from ccm.lib.actr import *

#####
# Python ACT-R requires an environment
# but in this case we will not be using anything in the environment
# so we 'pass' on putting things in there

class MyEnvironment(ccm.Model):
    pass

#####
# create an act-r agent

class MyAgent(ACTR):
    focus=Buffer()
    DMbuffer=Buffer()                   
    DM=Memory(DMbuffer,latency=0.05,threshold=-25,maximum_time=20,finst_size=10,finst_time=30.0)     
                                                    # turn down threshold
                                                    # maximum time - how long it will wait for a memory retrieval
                                                    # finst_size - how many chunks can be kept track of
                                                    # finst_time - how long a chunk can be kept track of
            
    dm_n=DMNoise(DM,noise=0.0,baseNoise=0.0)        
    dm_bl=DMBaseLevel(DM,decay=0.5,limit=None)   

    dm_spread=DMSpreading(DM,focus)                  
    dm_spread.strength=2                             
    dm_spread.weight[focus]=.5                       
                                                    
    partial=Partial(DM,strength=1.0,limit=-1.0)     
    partial.similarity('customer1','customer2',-0.1)   
    partial.similarity('customer1','customer3',-0.9)  

                    # note that this model uses slot names - slotname:slotcontent
    def init(): 
        DM.add('isa:order customer:customer1 type:ham_cheese condiment:mustard')         # customer1's order
        DM.add('isa:order customer:customer2 type:ham_cheese condiment:ketchup')         # customer2's order
        DM.add('isa:order customer:customer3 type:ham_cheese condiment:mayonnaise')      # customer3's order
        DM.add('isa:order customer:customer4 type:ham_cheese condiment:hot_sauce')       # customer4's order
        focus.set('isa:ingrediant type:bread')
        
    def bread_bottom(focus='isa:ingrediant type:bread'):   
        print "I have a piece of bread"
        focus.set('isa:ingrediant type:cheese')
        
    def cheese(focus='isa:ingrediant type:cheese'):        
        print "I have put cheese on the bread"  
        focus.set('isa:ingrediant type:ham')
        
    def ham(focus='isa:ingrediant type:ham'):
        print "I have put  ham on the cheese"
        focus.set('isa:order customer:customer1 type:ham_cheese condiment:unknown')         
                                        
    def condiment(focus='isa:order customer:customer1 type:ham_cheese condiment:unknown'):
        print "recalling the order"     
        DM.request('isa:order type:ham_cheese',require_new=True) # retrieve something that has not recently been retrieved           
        focus.set('retrieve_condiment')
        
    def order(focus='retrieve_condiment', DMbuffer='isa:order type:ham_cheese condiment:?condiment_order'): 
        print "I recall they wanted......."         
        print condiment_order            
        print "i have put the condiment on the sandwich"
        focus.set('isa:ingrediant type:bread_top')
        
    def bread_top(focus='isa:ingrediant type:bread_top'):
        print "I have put bread on the ham"
        print "I have made a ham and cheese sandwich"
        focus.set('isa:ingrediant type:bread')
        DMbuffer.clear()                        # clear the buffer for the next cycle


tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment
subway.run(3)                              # run the environment
ccm.finished()                             # stop the environment
