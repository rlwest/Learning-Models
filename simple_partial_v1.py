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
    DM=Memory(DMbuffer,latency=0.05,threshold=1)     
                                                    
            
    dm_n=DMNoise(DM,noise=0.6,baseNoise=0.0)         # turn on some noise to allow errors
    dm_bl=DMBaseLevel(DM,decay=0.5,limit=None)    


    dm_spread=DMSpreading(DM,focus)                  
    dm_spread.strength=2                             
    dm_spread.weight[focus]=.5                       
                                                     

    partial=Partial(DM,strength=1.0,limit=-1.0)        # turn on partial matching
    partial.similarity('customer1','customer2',-0.1)   # set the similarity between customer1 and customer2 - they are very similar
    partial.similarity('customer1','customer3',-0.9)   # set the similarity between customer1 and customer3 - not so similar


    def init():
        DM.add('customer:customer1 condiment:mustard')         # customer1's order
        DM.add('customer:customer2 condiment:ketchup')         # customer2's order
        DM.add('customer:customer3 condiment:mayonnaise')      # customer3's order
        focus.set('sandwich bread')
        
    def bread_bottom(focus='sandwich bread'):   
        print "I have a piece of bread"
        focus.set('sandwich cheese')    

    def cheese(focus='sandwich cheese'):        
        print "I have put cheese on the bread"  
        focus.set('sandwich ham')

    def ham(focus='sandwich ham'):
        print "I have put  ham on the cheese"
        focus.set('customer1 condiment')         
                                        
    def condiment(focus='customer1 condiment'):  # customer1 will spread activation to 'customer1 mustard'
        print "recalling the order"              # but also some to 'customer2 ketchup' and less to 'customer3 mayonaise'
        DM.request('customer:customer1 condiment:?condiment')               
        focus.set('sandwich condiment') 

    def order(focus='sandwich condiment', DMbuffer='customer:? condiment:?condiment'):  
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
