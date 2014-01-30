#################### ham cheese production model ###################

# this is the simplest type of act-r model
# it uses only the production system and one buffer
# the buffer represents the focus of thought
# we call it the focus buffer but it is often called the goal buffer
# productions fire if they match the focus buffer
# each production changes the contents of focus buffer so a different production will fire on the next cycle


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

    production_time=0.05         # production parameter settings
    production_sd=0.01
    production_threshold=-20

    pm_new=PMNew(alpha=0.2)      # The new TD-inspired utility learning system



    def init():
        focus.set('sandwich bread')

    def bread_bottom(focus='sandwich bread'):     
        print "I have a piece of bread"          
        focus.set('sandwich cheese')             

    def cheese(focus='sandwich cheese'):          
        print "I have put cheese on the bread"    
        focus.set('sandwich ham')

    def ham(focus='sandwich ham'):
        print "I have put  ham on the cheese"
        focus.set('sandwich bread_top')

    def parma_ham(focus='sandwich ham'):            # this production competes with the ham production
        print "I have put parma ham on the cheese"
        focus.set('sandwich bread_top')
        self.reward(0.1)                            # but using parma ham is intrinsically rewarding                          

    def bread_top(focus='sandwich bread_top'):
        print "I have put bread on the ham"
        print "I have made a ham and cheese sandwich"
        focus.set('sandwich bread')                      # make another sandwich

                   

tim=MyAgent()                              
subway=MyEnvironment()                    
subway.agent=tim                          
ccm.log_everything(subway)                 

subway.run(5)     # run for 5 seconds to learn that param ham is more rewarding to use                              
ccm.finished()                             
