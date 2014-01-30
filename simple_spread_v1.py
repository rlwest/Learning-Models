#################### ham cheese forgetting DM model ###################

# this model turns on the subsymbolic processing for DM, which causes forgetting


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
    DM=Memory(DMbuffer,latency=0.05,threshold=1)     # latency controls the relationship between activation and recall
                                                     # activation must be above threshold - can be set to none
            
    dm_n=DMNoise(DM,noise=0.0,baseNoise=0.0)         # turn on for DM subsymbolic processing
    dm_bl=DMBaseLevel(DM,decay=0.5,limit=None)       # turn on for DM subsymbolic processing


    dm_spread=DMSpreading(DM,focus)                  # turn on spreading activation for DM from focus
    dm_spread.strength=2                             # set strength of activation for buffers
    dm_spread.weight[focus]=.5                       # set weight to adjust for how many slots in the buffer
                                                     # usually this is strength divided by number of slots

    def init():
        DM.add('customer:customer condiment:mustard')
        focus.set('sandwich bread')
        
    def bread_bottom(focus='sandwich bread'):   
        print "I have a piece of bread"
        focus.set('sandwich cheese')    

    def cheese(focus='sandwich cheese'):        
        print "I have put cheese on the bread"  
        focus.set('sandwich ham')

    def ham(focus='sandwich ham'):
        print "I have put  ham on the cheese"
        focus.set('customer condiment')         
                                        
    def condiment(focus='customer condiment'):  # customer will spread activation to 'customer mustard'
        print "recalling the order"
        DM.request('customer:customer condiment:?condiment')                # request gets boost from spreading activation 
        focus.set('sandwich condiment') 

    def order(focus='sandwich condiment', DMbuffer='customer:customer condiment:?condiment'):  
        print "I recall they wanted......."         
        print condiment             
        print "i have put the condiment on the sandwich"
        focus.set('sandwich bread_top')

    def forgot(focus='sandwich condiment', DMbuffer=None, DM='error:True'):
        print "I recall they wanted......."
        print "I forgot"
        focus.set('stop')

    def bread_top(focus='sandwich bread_top'):
        print "I have put bread on the ham"
        print "I have made a ham and cheese sandwich"
        focus.set('stop')               

    def stop_production(focus='stop'):
        self.stop()

tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment
