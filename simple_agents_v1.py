#################### ham cheese production model ###################


import ccm      
log=ccm.log(html=True)   

from ccm.lib.actr import *  

class Subway(ccm.Model):        # items in the environment look and act like chunks - but note the syntactic differences
    bread=ccm.Model(isa='bread',location='on_counter')
    cheese=ccm.Model(isa='cheese',location='on_counter')
    ham=ccm.Model(isa='ham',location='on_counter')
    bread_top=ccm.Model(isa='bread_top',location='on_counter')

    sue_voice=ccm.Model(isa='voice',message='none')      # sounds are part of the environment

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

    def sue_speaks(self):       # create a sound object
        yield 2
        print "sue is speaking"
        self.parent.parent.sue_voice.message='finished'
        
class MyAgent(ACTR):    
    focus=Buffer()
    motor=MotorModule()

    def init():
        focus.set('sandwich bread')

    def bread_bottom(focus='sandwich bread'):
        print "tim - I have a piece of bread"     
        focus.set('sandwich cheese')
        motor.do_bread()                  # direct the motor module to do an action

    def cheese(focus='sandwich cheese', bread='location:on_plate'):   # production fires off the environment directly
        print "tim - I have cheese"                                         # this is legitimate if it is assumed that the agent is... 
        focus.set('sandwich ham')                                     # continuously and successfully monitoring the envionment
        motor.do_cheese()                                             # and time for monitoring is incorporated into the action time

    def stop_production(sue_voice='message:finished'):                # wait for sue to say she is finished
        print "tim - we are done"
        self.stop()                        # stops the whole thing, not just the agent

class MyAgent2(ACTR):    
    focus=Buffer()
    motor=MotorModule()

    def init():
        focus.set('sandwich ham')

    def ham(focus='sandwich ham', cheese='location:on_plate'):        # slot name required for objects
        print "sue - I have ham"
        focus.set('sandwich bread_top')
        motor.do_ham()

    def bread_top(focus='sandwich bread_top', ham='location:on_plate'):
        print "sue - I have bread"
        focus.set('finished')
        motor.do_bread_top()

    def finished(focus='finished', bread_top='location:on_plate'):  # wait for the action to complete before stopping
        print "sue - we have made a ham and cheese sandwich"
        print "sue - finished"
        focus.set('stop')
        motor.sue_speaks()                   # says she is finished

tim=MyAgent()
sue=MyAgent2()
env=Subway()
env.agent=tim
env.agent=sue

ccm.log_everything(env)

env.run()
ccm.finished()
