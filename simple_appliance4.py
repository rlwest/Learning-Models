from python_actr import *  

class Subway(Model):        
    coffee_machine = Model(isa='coffee_machine', button='up')
    cup = Model(isa='cup', state='empty', location='coffeemachine')

class ActionModule(Model):     

##    def human_action(self, action, env_object, slot_name, slot_value):
##        if action:='push':
##            print('PUSH',action)
##            yield 5
##        elif action:='grab':
##            print('GRAB',action)
##            yield 2
##        x = self.parent.parent[env_object]
##        setattr(x, slot_name, slot_value)
##        print('Human actions')
##        print('-object=',env_object)
##        print('-slot=',slot_name)
##        print('-value=',slot_value)

    def push(self, env_object, slot_name, slot_value):
        x = self.parent.parent[env_object]
        setattr(x, slot_name, 'in_progress')
        yield 2
        x = self.parent.parent[env_object]
        setattr(x, slot_name, slot_value)
        print('-object=',env_object)
        print('-slot=',slot_name)
        print('-value=',slot_value)
    def grab(self, env_object, slot_name, slot_value):
        x = self.parent.parent[env_object]
        setattr(x, slot_name, 'in_progress')
        yield 3
        x = self.parent.parent[env_object]
        setattr(x, slot_name, slot_value)
        print('-object=',env_object)
        print('-slot=',slot_name)
        print('-value=',slot_value)
    def pour(self, env_object, slot_name, slot_value):
        x = self.parent.parent[env_object]
        setattr(x, slot_name, 'in_progress')
        yield 5
        setattr(x, slot_name, slot_value)
        print('-object=',env_object)
        print('-slot=',slot_name)
        print('-value=',slot_value)
    def reset(self, env_object, slot_name, slot_value):
        x = self.parent.parent[env_object]
        # no yield
        setattr(x, slot_name, slot_value)
        print('-object=',env_object)
        print('-slot=',slot_name)
        print('-value=',slot_value)
        
class Human(ACTR):    
    focus=Buffer()
    focus.set('state:start')
    action=ActionModule()

    def START(focus='state:start',cup='state:empty'):
        print('HUMAN:pushing coffee machine button')
        action.push('coffee_machine', 'button', 'down')
        focus.set('state:wait')

    def Grab_coffee(focus='state:wait',cup='state:full'):
        print('HUMAN:grabbing the coffee')
        action.grab('cup', 'location', 'hand')
        focus.set('state:stop')


class Coffee_Machine(ACTR):
    production_time=0.0
    focus=Buffer()
    focus.set('state:off')
    action=ActionModule()

    def On(focus='state:off',coffee_machine='button:down'):
        print('COFFEE_MACHINE:pouring coffee')
        action.pour('cup', 'state', 'full')
        focus.set('state:on')

    def Off(focus='state:on',cup='state:full'):
        print('COFFEE_MACHINE:finished pouring coffee')
        action.reset('coffee_machine', 'button', 'up')
        focus.set('state:off')


tim=Human()
machine1=Coffee_Machine()
env=Subway()
env.agent=tim
env.agent=machine1 

log_everything(env)

env.run()

