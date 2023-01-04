'''
ATANDA ABDULLAHI ADEWALE - QIAN ZHILING
UNIVERSITE DE BOURGOGNE,
MSC. COMPUTER VISION, VIBOT 2022/23    
'''
import random
import numpy as np
import time
import tkinter as tk
from tkinter import ttk
class Passenger(object):
    '''
    
    '''
    def __init__(self,enter_floor,target_floor,name):
        '''
        Args:
        enter_floor: The floor where passenger shows up and sends elevator request
        state: 'up' or 'down', intended moving direction of the passenger  
        waiting_time: Time tracker of the accumulated waiting time, default to 0
        '''
        self.enter_floor=enter_floor
        self.target_floor=target_floor
        self.name=name
        if enter_floor<target_floor:
            self.state='up'
        elif enter_floor>target_floor:
            self.state='down'
        else:
            raise ValueError('Passenger {} does not need elevatpr.'.format(name) )
        self.waiting_time=0
    
    def getName(self):
        return self.name

    def getState(self):
        return self.state
    
    def getEnterFloor(self):
        return self.enter_floor
    
    def getTargetFloor(self):
        return self.target_floor
    
    def getWaitingTime(self):
        return self.waiting_time
    
    def updateWaitingTime(self):
        self.waiting_time=self.getWaitingTime()+1
class ElevatorTarget(object):
    def __init__(self,floor,state):
        self.floor=floor
        self.state=state
        
    def __str__(self):
        return '- ({},{})'.format(self.floor,self.state)
        
    def getFloor(self):
        return self.floor
    
    def getState(self):
        return self.state
    
    def getDistance(self,end,tall):
        '''
        end: another ElevatorTarget object
        tall: int, the height of building, max_floor-min_floor
        '''
    
    def distance(self,end,min_floor,max_floor):
        if self.getState()=='up':
            if end.getState()=='up':
                if self.getFloor()<=end.getFloor():
                    return  end.getFloor()-self.getFloor()
                else:
                    return (max_floor-min_floor)*2-self.getFloor()+end.getFloor()
                
            elif end.getState()=='down':
                return max_floor*2-self.getFloor()-end.getFloor()

            elif end.getState()==None:
                if self.getFloor()<=end.getFloor():
                    return  end.getFloor()-self.getFloor()
                else:
                    return max_floor*2-self.getFloor()-end.getFloor()

        elif self.getState()=='down':
            if end.getState()=='up':
                return self.getFloor()+end.getFloor()-min_floor*2
            
            elif end.getState()=='down':
                if self.getFloor()>=end.getFloor():
                    return self.getFloor()-end.getFloor()
                else:
                    return (max_floor-min_floor)*2+self.getFloor()-end.getFloor()
                
            elif end.getState()==None:
                if self.getFloor()>=end.getFloor():
                    return  self.getFloor()-end.getFloor()
                else:
                    return self.getFloor()+end.getFloor()-min_floor*2
        
        elif self.getState()==None:
            return abs(end.getFloor()-self.getFloor())        
class BasicElevator(object):
    
    '''
    
    '''
    def __init__(self,min_floor,max_floor):
        '''
        '''
        self.max_floor=max_floor
        self.min_floor=min_floor
        self.current_floor=min_floor
        self.state=None
        self.target_list=[]
        self.travel_distance=0
    
    def getMaxFloor(self):
        return self.max_floor
    
    def getMinFloor(self):
        return self.min_floor
    
    def getState(self):
        return self.state
    
    def setState(self,new_state):
        '''
        Args:
        new_state: string 'up','down' or None when standby
        '''
        self.state=new_state
    
    def getCurrentFloor(self):
        return self.current_floor
    
    def updateCurrentFloor(self):
        if self.getState()=='up':
            if self.getCurrentFloor()==self.getMaxFloor():
                raise ValueError('Exceed max floor')    
            else: self.current_floor=self.getCurrentFloor()+1
                
        if self.getState()=='down':
            if self.getCurrentFloor()==self.getMinFloor():
                raise ValueError('Exceed min floor')    
            else: self.current_floor=self.getCurrentFloor()-1
    
    def getTargetList(self):
        return self.target_list
    
    def setTargetList(self,new_list):
        self.target_list=new_list
    
    def checkTargetList(self):
        '''
        eliminate reached target from top of the target list
        '''
        old_list=self.getTargetList()
        current_floor=self.getCurrentFloor()
        current_state=self.getState()
        
        if old_list==[]:
            pass
        
        elif old_list[0].getFloor()==current_floor:
            self.setTargetList(old_list.copy()[1:])
            if old_list[0].getState()!=None:
                self.setState(old_list[0].getState())
        
        if self.getTargetList()==[]:
            self.setState(None)
                
    def addTargetList(self,new_target):
        '''
        Args:
        new_target: a ElevatorTarget object
        '''
        old_list=self.getTargetList()
        current_state=ElevatorTarget(self.getCurrentFloor(),self.getState())
        min_floor=self.getMinFloor()
        max_floor=self.getMaxFloor()
            
        if new_target.getFloor() not in [target.getFloor() for target in old_list]:
            old_list.append(new_target)
            new_list=[old_list[i] for i in np.argsort([current_state.distance(i,min_floor,max_floor) for i in old_list])]
            self.setTargetList(new_list)
            
        else:
            new_list=[]
            for target in old_list:
                if target.getFloor()==new_target.getFloor():
                    if target.getState()==None:
                        new_list.append(new_target)
                    elif new_target.getState()==None:
                        new_list.append(target)
                    elif new_target.getState()==target.getState():
                        new_list.append(target)
                    else:
                        new_list.append(target)
                        new_list.append(new_target)
                else:
                    new_list.append(target)
                    
            ordered_list=[new_list[i] for i in np.argsort([current_state.distance(i,min_floor,max_floor) for i in new_list])]
            self.setTargetList(ordered_list)
                            
    def passengerTakeOff(self,current_passenger):
        '''
        Args:
        current_passenger: a list of passengers in this elevator'''
        new_passenger=[]
        tookoff_passenger=[]
        for passenger in current_passenger:
            if passenger.getTargetFloor()==self.getCurrentFloor():
                #print('- Passenger took off:',passenger.getName())
                #print('- Total waiting time:',passenger.getWaitingTime())
                #print(passenger.getName(),passenger.getWaitingTime())
                tookoff_passenger.append(passenger)
            else:
                new_passenger.append(passenger)
        return (new_passenger,tookoff_passenger)
    
    def passengerTakeOn(self,waiting_passenger):
        '''
        Args:
        waiting_passenger: a dictionary with floor as keys and list of passengers as values
        
        Returns:
        a tuple (list of new passenger,dictionary of new waiting passenger)
        '''
        new_waiting_passenger=[]
        new_takeon_passenger=[]
        floor=self.getCurrentFloor()
        
        if self.getTargetList()==[]:
            return ([],waiting_passenger)
            
        elif floor!=self.getTargetList()[0].getFloor():
            return ([],waiting_passenger)
        
        elif waiting_passenger[floor]==[]:
            return ([],waiting_passenger)
        
        else:
            for passenger in waiting_passenger[floor]:
                if passenger.getState()==self.getTargetList()[0].getState():
                    new_takeon_passenger.append(passenger)
                    #print('- Passenger took on:',passenger.getName())
                    #print('- Target:',passenger.getTargetFloor())
                else:
                    new_waiting_passenger.append(passenger)              
            waiting_passenger[floor]=new_waiting_passenger
            return (new_takeon_passenger,waiting_passenger)
        
    def updateState(self):
        if self.getTargetList()==[]:
            pass
        else:
            next_target=self.getTargetList()[0]
            current_floor=self.getCurrentFloor()
            if current_floor>next_target.getFloor():
                self.setState('down')
            elif current_floor<next_target.getFloor():
                self.setState('up')
            else:
                self.setState(next_target.getState())
    
    def getDistance(self):
        return self.travel_distance
    
    def updateDistance(self):
        if self.getState()!=None:
            self.travel_distance=self.getDistance()+1    
def panelpress(i):
    global n1,n2,n3,n4,n5,n6,n7,n8,n9,n10
    n1,n2,n3,n4,n5,n6,n7,n8,n9,n10=i,i,i,i,i,i,i,i,i,i   
def press(instructions):
    #print('hello')
    global counter
    if instructions=='1st floor up':       
        enter_floor=1#modify
        target_floor=n1

        if enter_floor!=target_floor:
            name='p'+str(counter)
            counter+=1
            person=Passenger(enter_floor,target_floor,name)
            elevator.addTargetList(ElevatorTarget(person.getEnterFloor(),person.getState()))
            waiting_passenger[enter_floor]=waiting_passenger[enter_floor]+[person]
            #print('New passenger waiting, name: {},floor: {},directon: {}'.format(person.name,person.getEnterFloor(),person.getState()))
        
    elif instructions=='2nd floor up'or instructions=='2nd floor down':
        enter_floor=2
        target_floor=n2
        
        if enter_floor!=target_floor:
            name='p'+str(counter)
            counter+=1
            person=Passenger(enter_floor,target_floor,name)
            elevator.addTargetList(ElevatorTarget(person.getEnterFloor(),person.getState()))
            waiting_passenger[enter_floor]=waiting_passenger[enter_floor]+[person]
            #print('New passenger waiting, name: {},floor: {},directon: {}'.format(person.name,person.getEnterFloor(),person.getState()))
    elif instructions=='3rd floor up'or instructions=='3rd floor down':
        enter_floor=3
        target_floor=n3
        if enter_floor!=target_floor:
            name='p'+str(counter)
            counter+=1
            person=Passenger(enter_floor,target_floor,name)
            elevator.addTargetList(ElevatorTarget(person.getEnterFloor(),person.getState()))
            waiting_passenger[enter_floor]=waiting_passenger[enter_floor]+[person]
            #print('New passenger waiting, name: {},floor: {},directon: {}'.format(person.name,person.getEnterFloor(),person.getState()))   
    elif instructions=='4th floor up'or instructions=='4th floor down':
        enter_floor=4
        target_floor=n4
        if enter_floor!=target_floor:
            name='p'+str(counter)
            counter+=1
            person=Passenger(enter_floor,target_floor,name)
            elevator.addTargetList(ElevatorTarget(person.getEnterFloor(),person.getState()))
            waiting_passenger[enter_floor]=waiting_passenger[enter_floor]+[person]            
            #print('New passenger waiting, name: {},floor: {},directon: {}'.format(person.name,person.getEnterFloor(),person.getState()))    
    elif instructions=='5th floor up'or instructions=='5th floor down':
        enter_floor=5
        target_floor=n5
        if enter_floor!=target_floor:
            name='p'+str(counter)
            counter+=1
            person=Passenger(enter_floor,target_floor,name)
            elevator.addTargetList(ElevatorTarget(person.getEnterFloor(),person.getState()))
            waiting_passenger[enter_floor]=waiting_passenger[enter_floor]+[person]            
            #print('New passenger waiting, name: {},floor: {},directon: {}'.format(person.name,person.getEnterFloor(),person.getState()))    
    elif instructions=='6th floor up' or instructions=='6th floor down':
        enter_floor=6
        target_floor=n6
        if enter_floor!=target_floor:
            name='p'+str(counter)
            counter+=1
            person=Passenger(enter_floor,target_floor,name)
            elevator.addTargetList(ElevatorTarget(person.getEnterFloor(),person.getState()))
            waiting_passenger[enter_floor]=waiting_passenger[enter_floor]+[person]            
            #print('New passenger waiting, name: {},floor: {},directon: {}'.format(person.name,person.getEnterFloor(),person.getState()))    
    elif instructions=='7th floor up'or instructions=='7th floor down':
        enter_floor=7
        target_floor=n7
        if enter_floor!=target_floor:
            name='p'+str(counter)
            counter+=1
            person=Passenger(enter_floor,target_floor,name)
            elevator.addTargetList(ElevatorTarget(person.getEnterFloor(),person.getState()))
            waiting_passenger[enter_floor]=waiting_passenger[enter_floor]+[person]            
            #print('New passenger waiting, name: {},floor: {},directon: {}'.format(person.name,person.getEnterFloor(),person.getState()))    
    elif instructions=='8th floor up'or instructions=='8th floor down':    
        enter_floor=8
        target_floor=n8
        if enter_floor!=target_floor:
            name='p'+str(counter)
            counter+=1
            person=Passenger(enter_floor,target_floor,name)
            elevator.addTargetList(ElevatorTarget(person.getEnterFloor(),person.getState()))
            waiting_passenger[enter_floor]=waiting_passenger[enter_floor]+[person]            
            #print('New passenger waiting, name: {},floor: {},directon: {}'.format(person.name,person.getEnterFloor(),person.getState())) 
    elif instructions=='9th floor up'or instructions=='9th floor down':    
        enter_floor=9
        target_floor=n9
        if enter_floor!=target_floor:
            name='p'+str(counter)
            counter+=1
            person=Passenger(enter_floor,target_floor,name)
            elevator.addTargetList(ElevatorTarget(person.getEnterFloor(),person.getState()))
            waiting_passenger[enter_floor]=waiting_passenger[enter_floor]+[person]            
            #print('New passenger waiting, name: {},floor: {},directon: {}'.format(person.name,person.getEnterFloor(),person.getState()))    
    elif instructions=='10th floor down':
        enter_floor=10
        target_floor=n10
        if enter_floor!=target_floor:
            name='p'+str(counter)
            counter+=1
            person=Passenger(enter_floor,target_floor,name)
            elevator.addTargetList(ElevatorTarget(person.getEnterFloor(),person.getState()))
            waiting_passenger[enter_floor]=waiting_passenger[enter_floor]+[person]            
            #print('New passenger waiting, name: {},floor: {},directon: {}'.format(person.name,person.getEnterFloor(),person.getState()))    
#%%
master=tk.Tk()
master.geometry('700x525')
#%%
frame1 = tk.Frame(master)
frame1.pack(side=tk.LEFT)   

button18 = tk.Button(frame1, text='10 down', fg='black', bg='cyan',
                command=lambda: press('10th floor down')).pack()

#%%
button16 = tk.Button(frame1, text='9 up',fg='white', bg='grey',
                command=lambda: press('9th floor down')).pack(padx= (0, 0), pady= (5, 0))
button17 = tk.Button(frame1, text='9 down', fg='black', bg='cyan',
                command=lambda: press('9th floor down')).pack()

#%%
button14 = tk.Button(frame1, text='8 up', fg='white', bg='grey',
                command=lambda: press('8th floor down')).pack(padx= (0, 0), pady= (5, 0))
button15 = tk.Button(frame1, text='8 down', fg='black', bg='cyan',
                command=lambda: press('8th floor down')).pack()

#%%floor7
button12 = tk.Button(frame1, text='7 up', fg='white', bg='grey',
                command=lambda: press('7th floor down')).pack(padx= (0, 0), pady= (5, 0))
button13 = tk.Button(frame1, text='7 down', fg='black', bg='cyan',
                command=lambda: press('7th floor down')).pack()

#%%floor6
button10 = tk.Button(frame1, text='6 up', fg='white', bg='grey',
                command=lambda: press('6th floor down')).pack(padx= (0, 0), pady= (5, 0))
button11 = tk.Button(frame1, text='6 down', fg='black', bg='cyan',
                command=lambda: press('6th floor down')).pack()

#%%floor5
button8 = tk.Button(frame1, text='5 up', fg='white', bg='grey',
                command=lambda: press('5th floor up')).pack(padx= (0, 0), pady= (5, 0))
button9 = tk.Button(frame1, text='5 down', fg='black', bg='cyan',
                command=lambda: press('5th floor down')).pack()

#%%floor4
button6 = tk.Button(frame1, text='4 up', fg='white', bg='grey',
                command=lambda: press('4th floor up')).pack(padx= (0, 0), pady= (5, 0))
button7 = tk.Button(frame1, text='4 down', fg='black', bg='cyan',
                command=lambda: press('4th floor down')).pack()

#%%floor3
button4 = tk.Button(frame1, text='3 up', fg='white', bg='grey',
                command=lambda: press('3rd floor up')).pack(padx= (0, 0), pady= (5, 0))
button5 = tk.Button(frame1, text='3 down', fg='black', bg='cyan',
                command=lambda: press('3rd floor down')).pack()

#%%floor2
button2 = tk.Button(frame1, text='2 up', fg='white', bg='grey',
                command=lambda: press('2nd floor up')).pack(padx= (0, 0), pady= (5, 0))
button3 = tk.Button(frame1, text='2 down', fg='black', bg='cyan',
                command=lambda: press('2nd floor down')).pack()

#%%floor1
button1 = tk.Button(frame1, text='1 up', fg='white', bg='grey',
                command=lambda: press('1st floor up')).pack(padx= (0, 0), pady= (5, 0))

#%%

################################################################################!!!###############        
#%%       
n=50
elevator_1=BasicElevator(1,10)#set the minist floor is 1,the maxest floor 2
elevator=elevator_1
min_floor=elevator.getMinFloor()
max_floor=elevator.getMaxFloor()
counter=0
waiting_passenger={}
for i in range(min_floor,max_floor+1):
    waiting_passenger[i]=[]#创建字典保存每层楼的等待乘客
passenger_1=[]
# Set up canvas constants
#%%create the elevator structure
# Add Image

bg = tk.PhotoImage(file='b.png')


canvas_area = tk.Frame(master)
w = tk.Canvas(master, width=1000, height=1000)
w.create_image(0,0, image = bg)
w.pack()
w.create_rectangle(70, 10, 170, 510, fill = "white")    
for i in range(1,10):
    w.create_line(70, 50*i+10, 170, 50*i+10)
   
for i in range(10):
    w.create_text(20, 50*i+18,anchor=tk.NW,text=str(10-i)+'F',font = ('TimesNewRoman',15))
w.create_text(375, 30, anchor=tk.NW,text='Passengers take off: ')
w.create_text(375, 150, anchor=tk.NW,text='Passengers take on: ')
w.create_text(375, 270, anchor=tk.NW,text='Passengers in the elevator: ')
master.update()

frame2=tk.Frame(w, width= 100, height= 100)
frame2.place(x=200, y=100) 
panellabel=tk.Label(frame2,text='panel buttons').grid(columnspan=2, ipadx=10)
panelbutton1 = tk.Button(frame2, text='1', fg='black', pady=10, padx=10, bg='yellow',
                command=lambda: panelpress(1)).grid(row=2, column=0)
panelbutton2 = tk.Button(frame2, text='2', fg='black', pady=10, padx=10, bg='yellow',
                command=lambda: panelpress(2)).grid(row=2, column=1)
panelbutton3 = tk.Button(frame2, text='3', fg='black', pady=10, padx=10, bg='yellow',
                command=lambda: panelpress(3)).grid(row=3, column=0)
panelbutton4 = tk.Button(frame2, text='4', fg='black', pady=10, padx=10, bg='yellow',
                command=lambda: panelpress(4)).grid(row=3, column=1, pady=5)
panelbutton5 = tk.Button(frame2, text='5', fg='black', pady=10, padx=10, bg='yellow',
                command=lambda: panelpress(5)).grid(row=4, column=0)
panelbutton6 = tk.Button(frame2, text='6', fg='black', pady=10, padx=10, bg='yellow',
                command=lambda: panelpress(6)).grid(row=4, column=1)
panelbutton7 = tk.Button(frame2, text='7', fg='black', pady=10, padx=10, bg='yellow',
                command=lambda: panelpress(7)).grid(row=5, column=0)
panelbutton8 = tk.Button(frame2, text='8', fg='black', pady=10, padx=10, bg='yellow',
                command=lambda: panelpress(8)).grid(row=5, column=1, pady=5)
panelbutton9 = tk.Button(frame2, text='9', fg='black', pady=10, padx=10, bg='yellow',
                command=lambda: panelpress(9)).grid(row=6, column=0)
panelbutton10 = tk.Button(frame2, text='10', fg='black', pady=10, padx=10, bg='yellow',
                command=lambda: panelpress(10)).grid(row=6, column=1)
#%%main
#for i in range(n):
while(True):
    print('Timestep -',i)
    timestep_label=w.create_text(480, 10, anchor=tk.NW,text='Timestep '+str(i))
    
    # update floor
    elevator.updateCurrentFloor()
    print('Current Floor:',elevator.getCurrentFloor())

    
    # Draw empty elevator
    floor=elevator.getCurrentFloor()
    elevator_sqr=w.create_rectangle(72, (10-floor)*50+12, 168, (10-floor)*50+58, fill = "grey")#create the elevator box
    
    
    # update travel distance for KPI
    elevator.updateDistance()

    # Draw waiting passengers - 1:
    draw_passenger_wait=[]
    text_passenger_wait=[]
    for f in waiting_passenger:
        for i,p in enumerate(waiting_passenger[f]):
            row=i//3
            col=i%3
            draw_passenger_wait.append(w.create_rectangle(172+col*100, 
                                                          (10-f)*50+12+row*25, 
                                                          192+col*100,
                                                          (10-f)*50+32+row*25, 
                                                          fill = "red"))
            text_passenger_wait.append(w.create_text(200+col*100,
                                                     (10-f)*50+12+row*25,
                                                     anchor=tk.NW,
                                                     text=p.getName()+'-'+p.getState()))
            # if elevator.current_floor==p.target_floor:####################!!!!!!!#############
            #     #w.delete(elevator_sqr)
            #     print(p.target_floor)
            #     w.create_rectangle(72, (10-elevator.current_floor)*50+12, 100, (10-elevator.current_floor)*50+58, fill = "red")
            #     time.sleep(9)
    # Draw passenger in the elevator - 1:
    draw_passenger_on=[]
    text_passenger_on=[]
    # if elevator.current_floor==elevator.target_list[0]:####################!!!!!!!#############
    #     #w.delete(elevator_sqr)
    #     w.create_rectangle(72, (10-elevator.current_floor)*50+12, 100, (10-elevator.current_floor)*50+58, fill = "red")
    #     time.sleep(9)
    
    
    
    for i,p in enumerate(passenger_1):
        row=i//4
        col=i%4
        draw_passenger_on.append(w.create_rectangle(75+col*10,
                                                    (10-floor)*50+15+row*10,
                                                    85+col*10,
                                                    (10-floor)*50+25+row*10,
                                                    fill = 'red'))
        text_passenger_on.append(w.create_text(480, 
                                       290+20*i, 
                                       anchor=tk.NW,
                                       text=p.getName()+' heading to '+str(p.getTargetFloor())+'F'))
    master.update()
    time.sleep(1)
    
    # Let passengers who reach the target take off
    passenger_1, tookoff_passenger = elevator.passengerTakeOff(passenger_1)

    # Draw off passenger
    for p in draw_passenger_on:
        w.delete(p)
    for p in text_passenger_on:
        w.delete(p)
        
    draw_passenger_off=[]
    
    for i,p in enumerate(tookoff_passenger):
        draw_passenger_off.append(w.create_text(480, 
                                                50+20*i, 
                                                anchor=tk.NW,
                                                text=p.getName()+' waited for '+str(p.getWaitingTime())+' s'))
    
    # Draw passenger in the elevator - 2
    draw_passenger_on=[]
    text_passenger_on=[]
    for i,p in enumerate(passenger_1):
        row=i//4
        col=i%4
        draw_passenger_on.append(w.create_rectangle(75+col*10,
                                                    (10-floor)*50+15+row*10,
                                                    85+col*10,
                                                    (10-floor)*50+25+row*10,fill = 'red'))
        text_passenger_on.append(w.create_text(480, 
                                               290+20*i, 
                                               anchor=tk.NW,
                                               text=p.getName()+' heading to '+str(p.getTargetFloor())+'F'))
        
    master.update()
    time.sleep(1)
    
    # Take new passengers
    new_takeon,waiting_passenger=elevator.passengerTakeOn(waiting_passenger)
            
    # Draw passenger in the elevator - 3
    new_target_text=[]
    for i,p in enumerate(new_takeon):
        row=(i+len(passenger_1))//4
        col=(i+len(passenger_1))%4
        draw_passenger_on.append(w.create_rectangle(75+col*10,
                                                    (10-floor)*50+15+row*10,
                                                    85+col*10,
                                                    (10-floor)*50+25+row*10,
                                                    fill = 'red'))
        new_target_text.append(w.create_text(480, 
                                             170+20*i, 
                                             anchor=tk.NW,
                                             text=p.getName()+' heading to '+str(p.getTargetFloor())+'F'))
        text_passenger_on.append(w.create_text(480, 
                                               290+20*(i+len(passenger_1)), 
                                               anchor=tk.NW,
                                               text=p.getName()+' heading to '+str(p.getTargetFloor())+'F'))
    passenger_1=passenger_1+new_takeon
    
    # Checked current target
    elevator.checkTargetList()
    
    # Receive new target orders
    for new_passenger in new_takeon:
        elevator.addTargetList(ElevatorTarget(new_passenger.getTargetFloor(),None))   

    # Draw waiting passengers - 2
    for p in draw_passenger_wait:
        w.delete(p)    
    for p in text_passenger_wait:
        w.delete(p)
        
    draw_passenger_wait=[]
    text_passenger_wait=[]
    for f in waiting_passenger:
        for i,p in enumerate(waiting_passenger[f]):
            row=i//3
            col=i%3
            draw_passenger_wait.append(w.create_rectangle(172+col*100, 
                                                          (10-f)*50+12+row*25, 
                                                          192+col*100,
                                                          (10-f)*50+32+row*25, 
                                                          fill = "red"))
            text_passenger_wait.append(w.create_text(200+col*100,
                                                     (10-f)*50+12+row*25,
                                                     anchor=tk.NW,
                                                     text=p.getName()+'-'+p.getState()))
            
     #######
    # for f in waiting_passenger:
    #     for i,p in enumerate(waiting_passenger[f]):      
    #         if elevator.current_floor==p.target_floor:####################!!!!!!!#############
    #             #w.delete(elevator_sqr)
    #             print(p.target_floor)
    #             w.create_rectangle(72, (10-elevator.current_floor)*50+12, 100, (10-elevator.current_floor)*50+58, fill = "red")
    #             time.sleep(9)
######       
    master.update()
    time.sleep(1)
    #print('Current targets:')
    #for i in elevator.getTargetList():
        #print(i)

    # Update elevator moving direction
    elevator.updateState()
    #print('Current state:',elevator.getState())
    
    # Update passenger waiting time
    for f in waiting_passenger:
        temp=[]
        for passenger in waiting_passenger[f]:
            passenger.updateWaitingTime()
            temp.append(passenger)
        waiting_passenger[f]=temp
    #print('Waiting list:',[[j.getName()+'-'+j.getState() for j in waiting_passenger[i]] for i in waiting_passenger])        
    
    #print('------')   
    # Clear Canvas:
    w.delete(timestep_label)
    w.delete(elevator_sqr)
    for p in draw_passenger_on:
        w.delete(p)
    
    for p in draw_passenger_off:
        w.delete(p)
    
    for p in new_target_text:
        w.delete(p)
    
    for p in draw_passenger_wait:
        w.delete(p)
        
    for p in text_passenger_wait:
        w.delete(p)
    
    for p in text_passenger_on:
        w.delete(p)
        
                                     
master.mainloop()
    

    

