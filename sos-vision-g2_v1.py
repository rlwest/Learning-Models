## this model looks for an item in a location
## the salience setting on the item searched for determines how fast it is found

## this model is generalized to look for whatever is in the focus buffer
## so it can just be dumped into any model

import ccm      
log=ccm.log(html=True)   

from ccm.lib.actr import *  


class Sock_drawer(ccm.Model):
  sock1=ccm.Model(isa='sock',location='in_drawer',feature1='red_stripe',salience=0.5)
  sock2=ccm.Model(isa='sock',location='in_drawer',feature1='blue_stripe',salience=0.5)

class MyAgent(ACTR): 
  focus_buffer=Buffer()
  visual_buffer=Buffer()
  vision_module=SOSVision(visual_buffer,delay=0)
  imaginalbuffer=Buffer()

  def init():                                             
    focus_buffer.set('isa:sock location:in_drawer action:look')
    imaginalbuffer.set('isa:sock location:in_drawer feature1:red_stripe')
     ## the image of the object is in the imaginal buffer
     ## the focus is on searching for the type of object in a location
     ## once found the features of the object are checked against the imaginal buffer

  def find(focus_buffer='isa:?object location:?loc action:look'):
    vision_module.request('isa:?object location:?loc')
    focus_buffer.set('isa:?object location:?loc action:get')
    print 'I am looking for * * *'
    print object
     ## when the action is 'look' get the object and location from focus buffer
     ## reqest that from the visual buffer

  def found(focus_buffer='isa:?object location:?loc action:get',visual_buffer='isa:?object location:?loc feature1:?feature1'):
    print 'I found - - - '
    print object
    focus_buffer.set('isa:?object location:?loc feature1:?feature1 action:check')
    visual_buffer.clear
     ## 1st, object and location are defined from the focus buffer,
     ## 2nd, they are used to see if the visual buffer matches
     ## also, if it matches then feature1 is defined by the visual buffer
     ## feature1 then gets added to the focus buffer
    
  def check_yes(focus_buffer='isa:?object location:?loc feature1:?feature1 action:check',imaginalbuffer='feature1:?feature1'):
    focus_buffer.set('stop')
    visual_buffer.clear
    print 'it has ^ ^ ^'
    print feature1
     ## same trick - used to compare feature1 in focus to a feature in imaginal
     ## fires with a match

  def check_no(focus_buffer='isa:?object location:?loc feature1:?feature1 action:check',imaginalbuffer='feature1:!?feature1'): 
    focus_buffer.set('isa:?object location:?loc action:look')
    visual_buffer.clear
    print 'it has a @ @ @'
    print feature1
     ## same trick - used to compare feature1 in focus to a feature in imaginal
     ## fires with a not match
    
  def not_found(focus_buffer='isa:?object location:?loc action:get',visual_buffer=None):
    focus_buffer.set('isa:?object location:?loc action:look')
    visual_buffer.clear
    print 'where is that % % %'
    print object

    
tim=MyAgent()
env=Sock_drawer()
env.agent=tim 
ccm.log_everything(env)

env.run()
ccm.finished()













