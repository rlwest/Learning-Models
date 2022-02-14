from python_actr import *  


class MyEnvironment(Model):
    pass


class MyAgent(ACTR):
    
    focus=Buffer()
    DMbuffer=Buffer()

    DM=Memory(DMbuffer,latency=0.05,threshold=-0.6,maximum_time=3,finst_size=3,finst_time=3)
    #DM=Memory(DMbuffer)
    dm_bl=DMBaseLevel(DM,decay=0.5,limit=None)
    #DM_inhibit=DMInhibition(DM, decayScale=1.0, timeScale=5.0)
    
    focus.set('goal:recall')

    DM.add('animal:tiger')
    DM.add('animal:lion')
    #DM.add('animal:shark')
    #DM.add('animal:mouse')
    #DM.add('animal:duck')
    


    def request(focus='goal:recall'):
        print("requesting")
        DM.request('animal:?x')            
        focus.set('goal:retrieve')     

    def retrieve(DMbuffer='animal:?animal'): 
        print("+++++++++++++++++++++++++++++++++++++++++++")                       
        print (animal)
        DMbuffer.set('nil')
        focus.set('goal:recall')

   

tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
log_everything(subway)
subway.run()                               # run the environment

