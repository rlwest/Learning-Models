#################### ham cheese production model ###################


import ccm      
log=ccm.log(html=True)   

from ccm.lib.actr import *  

class Subway(ccm.Model):        # items in the environment look and act like chunks - but note the syntactic differences
    bread=ccm.Model(isa='bread',location='on_counter')
    cheese=ccm.Model(isa='cheese',location='on_counter')
    ham=ccm.Model(isa='ham',location='on_counter')
    bread_top=ccm.Model(isa='bread_top',location='on_counter')

class MotorModule(ccm.Model):     # create a motor module do the actions 
    def do_bread(self):           # note that technically the motor module is outside the agent
        yield 2                   # but it is controlled from within the agent, i.e., it bridges the cognitive and the environment
        print "do the bread"
        self.parent.parent.bread.location='on_plate'    # self=MotorModule, parent=MyAgent, parent of parent=Subway
    def do_cheese(self):     
        yield 2                   # yield refers to how long the action takes, but cognition can continue while waiting for an action to complete
        print "do the cheese"
        self.parent.parent.cheese.location='on_plate'   # in this case the motor actions make changes to the environment objects
    def do_ham(self):     
        yield 2
        print "do the ham"
        self.parent.parent.ham.location='on_plate'
    def do_bread_top(self):     
        yield 2
        print "do the bread on top"
        self.parent.parent.bread_top.location='on_plate'
        
class MyAgent(ACTR):    
    focus=Buffer()
    motor=MotorModule()

    def init():
        focus.set('sandwich bread')

    def bread_bottom(focus='sandwich bread'):
        print "I have a piece of bread"     
        focus.set('sandwich cheese')
        motor.do_bread()                  # direct the motor module to do an action

    def cheese(focus='sandwich cheese', bread='location:on_plate'):   # production fires off the environment directly
        print "I have cheese"                                         # this is legitimate if it is assumed that the agent is... 
        focus.set('sandwich ham')                                     # continuously and successfully monitoring the envionment
        motor.do_cheese()                                             # and time for monitoring is incorporated into the action time

    def ham(focus='sandwich ham', cheese='location:on_plate'):        # slot name required for objects
        print "I have ham"
        focus.set('sandwich bread_top')
        motor.do_ham()

    def bread_top(focus='sandwich bread_top', ham='location:on_plate'):
        print "I have bread"
        focus.set('stop')
        motor.do_bread_top()

    def stop_production(focus='stop', bread_top='location:on_plate'):  # wait for the action to complete before stopping
        print "I have made a ham and cheese sandwich"
        self.stop()


tim=MyAgent()
env=Subway()
env.agent=tim 
ccm.log_everything(env)

env.run()
ccm.finished()
