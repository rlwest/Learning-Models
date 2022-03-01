from python_actr import *  

class Subway(Model):        
    coffee_machine = Model(isa='coffee_machine', button='up')
    cup = Model(isa='cup', state='empty', location='coffeemachine')

class ActionModule(Model):     

    def human_action(self, action, env_object, slot_name, slot_value):
        if action:='push':
            yield 1
        elif action:='grab':
            yield 2
        x = self.parent.parent[env_object]
        setattr(x, slot_name, slot_value)
        print('barista actions')
        print('   object=',env_object)
        print('   slot=',slot_name)
        print('   value=',slot_value)

    def coffeemachine_action(self, action, env_object, slot_name, slot_value):
        x = self.parent.parent[env_object]
        if action:='pour':
            setattr(x, slot_name, 'in_progress')
            yield 4
        setattr(x, slot_name, slot_value)
        print('coffee machine actions')
        print('   object=',env_object)
        print('   slot=',slot_name)
        print('   value=',slot_value)
        
class Human(ACTR):    
    focus=Buffer()
    focus.set('state:start')
    action=ActionModule()

    def START(focus='state:start',cup='state:empty'):
        print('pushing coffee machine button')
        action.human_action('push','coffee_machine', 'button', 'down')
        focus.set('state:wait')

    def Grab_coffee(focus='state:wait',cup='state:full'):
        print('grabbing the coffee')
        action.human_action('grab','cup', 'location', 'hand')
        focus.set('state:stop')


class Coffee_Machine(ACTR):
    production_time=0.0
    focus=Buffer()
    focus.set('state:off')
    action=ActionModule()

    def On(focus='state:off',coffee_machine='button:down'):
        print('pouring coffee')
        action.coffeemachine_action('pour','cup', 'state', 'full')
        focus.set('state:on')

    def Off(focus='state:on',cup='state:full'):
        print('finished pouring coffee')
        action.coffeemachine_action('reset','coffee_machine', 'button', 'up')
        focus.set('state:off')


tim=Human()
machine1=Coffee_Machine()
env=Subway()
env.agent=tim
env.agent=machine1 

log_everything(env)

env.run()

