## this model looks for an item in a location based on a search feature
## then it checks the object for a second feature
## the salience setting on the item searched for determines how fast it is found

import ccm      
log=ccm.log(html=True)   

from ccm.lib.actr import *  

class Sock_drawer(ccm.Model):
  sock1=ccm.Model(isa='sock',location='in_drawer',feature1='red_stripe',salience=0.5)
  sock2=ccm.Model(isa='sock',location='in_drawer',feature1='blue_stripe',salience=0.5)

class MyAgent(ACTR): 
  focus_buffer=Buffer()
  code_buffer=Buffer()
  visual_buffer=Buffer()
  vision_module=SOSVision(visual_buffer,delay=0) # delay=0 means the results of the visual search are
                                                 # placed in the visual buffer right after the request
                                                 # but the request takes 50 msec and the retieval takes 50 msec
                                                 # so actually it takes 100 msec to get the results at minimum
  
 ################ procedural production system ######################
  
  def init():
    focus_buffer.set('look')

  def find(focus_buffer='look'):
    vision_module.request('isa:sock location:in_drawer')
    focus_buffer.set('get_sock')
    print "I am looking for a sock"

  def found(focus_buffer='get_sock',visual_buffer='isa:sock location:in_drawer feature1:?feature1'):
    print('I found a sock')
    focus_buffer.set('check ?feature1')
    visual_buffer.clear
    
  def check_yes(focus_buffer='check red_stripe'):
    focus_buffer.set('stop')
    visual_buffer.clear
    print('it has a red stripe')

  def check_no(focus_buffer='check blue_stripe'):
    focus_buffer.set('look')
    visual_buffer.clear
    print('it has a blue stripe')
    
  def not_found(focus_buffer='get_sock',visual_buffer=None):
    focus_buffer.set('look')
    visual_buffer.clear
    print('where is that sock?')

    
tim=MyAgent()
env=Sock_drawer()
env.agent=tim 
ccm.log_everything(env)

env.run()
ccm.finished()
   













