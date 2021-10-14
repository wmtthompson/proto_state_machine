'''
Created on Apr 23, 2021

@author: william
'''

import queue
from builtins import isinstance, TypeError

class State(object):
    def __init__(self, event_queue):
        if not isinstance(event_queue, queue.Queue):
            raise TypeError("Did not pass a queue type.")
        self.event_queue = event_queue
    
    def on_event(self, event):
        return self

class CountDownState(State):
    def __init__(self, event_queue):
        State.__init__(self, event_queue)
    
    def on_event(self, event):
        if event == "min reached":
            return CountUpState(self.event_queue)
        else:
            #if the event is not meant for this one, put it back
            self.event_queue.put(event)
            return self

class CountUpState(State):
    def __init__(self, event_queue):
        State.__init__(self, event_queue)
    
    def on_event(self, event):
        if event == "max reached":
            return CountDownState(self.event_queue)
        else:
            #if the event was not meant for this instance, put it back
            self.event_queue.put(event)
            return self

class DisconnectedState(State):
    def __init__(self, event_queue):
        
        State.__init__(self, event_queue)
    
    def on_event(self, event):
        if event == "connected":
            return DisconnectedState(self.event_queue)
        else:
            self.event_queue.put(event)
            return self

class ConnectedState(State):
    def __init__(self, event_queue):
        State.__init__(self, event_queue)
    
    def on_event(self, event):
        if event == "disconnected":
            return DisconnectedState(self.event_queue)
        else:
            self.event_queue.put(event)
            return self

class Device(object):
    def __init__(self):
        self.device_queue = queue.Queue()
        self.conn_state = DisconnectedState(self.device_queue)
        self.count_state = CountUpState(self.device_queue)
        self.count = 0
    
    def run(self):
        while (True):
            if not self.device_queue.empty():
                event1 = self.device_queue.get(block=False)
                self.count_state = self.count_state.on_event(event1)
            if isinstance(self.count_state, CountUpState):
                print("Counting Up")
                self.count += 1
                if self.count > 5:
                    self.device_queue.put("max reached")
            elif isinstance(self.count_state, CountDownState):
                print("Counting Down")
                self.count -= 1
                if self.count == 0:
                    self.device_queue.put("min reached")
            else:
                pass
                
                