# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 16:09:19 2023

@author: Sajan Dayal, Mohammad Almubaid, Blake Jefferson
UT Austin Mechanical Engineering Students for ME369P under Dr. Pryor
Dream Team U04
"""
from datetime import datetime
import numpy as np
import tkinter as tk
from tkinter import ttk

from nba_api.stats.endpoints import PlayerGameLog
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo

def on_button_click(player):
    playerchosen = players.find_players_by_full_name(player)
    pid=playerchosen[0]['id']
    
    
    # Nikola Jokić
    gamelog=PlayerGameLog(player_id=pid, season = '2022')
    
    # pandas data frames (optional: pip install pandas)
    gamelog.get_data_frames()[0]
    
    #get game log
    seasonlog=gamelog.player_game_log.data['data']
    
    alltotals=[]
    
    day=0
    while day<7:
        dailystats=[0,0,0,0,0,0,0,0,0,0,0] #pts,ast, reb,stl,blk,tov,fgm,fg3m,pf,plus/minus,number of games
        alltotals.append(dailystats) #monday to sunday monday =0, sunday = 6
        day+=1
        
    for i in seasonlog:
        inputdate=i[3]
        date = datetime.strptime(inputdate, "%b %d, %Y")
        day = date.weekday()
        alltotals[day][0]+=i[24]
        alltotals[day][1]+=i[19]
        alltotals[day][2]+=i[18]
        alltotals[day][3]+=i[20]
        alltotals[day][4]+=i[21]
        alltotals[day][5]+=i[22]
        alltotals[day][6]+=i[7]
        alltotals[day][7]+=i[10]
        alltotals[day][8]+=i[23]
        alltotals[day][9]+=i[25]
        alltotals[day][10]+=1
        
    #daily per game average from monday to sunday
    #arrays in order- pts,ast, reb,stl,blk,tov,fgm,fg3m,pf,plus/minus
    
    num=0
    averages=[]
    while num < 10:
        averages.append([0,0,0,0,0,0,0])
        num+=1
    
    row=0
    col=0
    while row < len(averages):
        while col < 7:
            if alltotals[col][10]==0:
                averages[row][col]=np.nan
            else:
                averages[row][col]=alltotals[col][row]/alltotals[col][10]
            col+=1
        row+=1
        col=0
        
    test=1
    
    if np.isnan(averages).all():
        no_gamesplayed_gui(player)
        return
        
    maxandmin=np.zeros((10,4)) #min, dayofweek, max, day of week
    i=0
    while i < 10:
        stat=np.array(averages[i])
        maximum=np.nanmax(stat)
        maxandmin[i][2]=maximum
        
        #maxlocation = np.where(stat == maximum)[0][0]
        
        maxandmin[i][3]=np.nanargmax(stat)
        #maxandmin[i][3]=maxlocation
        
        minimum=np.nanmin(stat)
        maxandmin[i][0]=minimum
        
        #minlocation = np.where(stat == minimum)[0][0]
        
        maxandmin[i][1]=np.nanargmin(stat)
        #maxandmin[i][1]=minlocation
        
        i+=1
    maxandmin[5][2], maxandmin[5][0] = maxandmin[5][0], maxandmin[5][2] 
    maxandmin[5][1], maxandmin[5][3] = maxandmin[5][3], maxandmin[5][1]
    maxandmin[8][2], maxandmin[8][0] = maxandmin[8][0], maxandmin[8][2] 
    maxandmin[8][1], maxandmin[8][3] = maxandmin[8][3], maxandmin[8][1]
    create_new_gui(maxandmin, player)

def no_gamesplayed_gui(player):
    new_window = tk.Toplevel()
    new_window.title(f"{player} No Games Played")
    new_window.geometry("1200x400")
    new_window.resizable(True, True)
    result_label = tk.Label(new_window, text=f"{player} did not play a game in the 2022-2023 season")
    result_label.pack(pady=10)
    
def create_new_gui(result, player):
    # Create a new window for the result
   new_window = tk.Toplevel()
   new_window.title(f"{player}'s Best and Worst Day of Week for Each Stat")
   new_window.geometry("1600x1200")
   new_window.resizable(True, True)
   
   #pts,ast, reb,stl,blk,tov,fgm,fg3m,pf,plus/minus
   da=0
   dayofweek=[]
   bestday=np.array([0,0,0,0,0,0,0])
   worstday=np.array([0,0,0,0,0,0,0])
   while da<10:
       dow=[result[da][1], result[da][3]]
       
       if dow[0]==0:
           dow[0]='Monday'
           worstday[0]+=1
       elif dow[0]==1:
           dow[0]='Tuesday'
           worstday[1]+=1
       elif dow[0]==2:
           dow[0]='Wednesday'
           worstday[2]+=1
       elif dow[0]==3:
           dow[0]='Thursday'
           worstday[3]+=1
       elif dow[0]==4:
           dow[0]='Friday'
           worstday[4]+=1
       elif dow[0]==5:
           dow[0]='Saturday'
           worstday[5]+=1
       elif dow[0]==6:
           dow[0]='Sunday'
           worstday[6]+=1
           
       if dow[1]==0:
           dow[1]='Monday'
           bestday[0]+=1
       elif dow[1]==1:
           dow[1]='Tuesday'
           bestday[1]+=1
       elif dow[1]==2:
           dow[1]='Wednesday'
           bestday[2]+=1
       elif dow[1]==3:
           dow[1]='Thursday'
           bestday[3]+=1
       elif dow[1]==4:
           dow[1]='Friday'
           bestday[4]+=1
       elif dow[1]==5:
           dow[1]='Saturday'
           bestday[5]+=1
       elif dow[1]==6:
           dow[1]='Sunday'
           bestday[6]+=1
           
       dayofweek.append(dow)
       da+=1
   # Create widgets in the new window
   bestdayofweek=np.nanargmax(bestday)
   if bestdayofweek == 0:
       bestdayofweek='Monday'
   elif bestdayofweek==1:
       bestdayofweek='Tuesday'
   elif bestdayofweek==2:
       bestdayofweek='Wednesday'
   elif bestdayofweek==3:
       bestdayofweek='Thursday'
   elif bestdayofweek==4:
       bestdayofweek='Friday'
   elif bestdayofweek==5:
       bestdayofweek='Saturday'
   elif bestdayofweek==6:
       bestdayofweek='Sunday'
       
   worstdayofweek=np.nanargmax(worstday)
   if worstdayofweek == 0:
       worstdayofweek='Monday'
   elif worstdayofweek==1:
       worstdayofweek='Tuesday'
   elif worstdayofweek==2:
       worstdayofweek='Wednesday'
   elif worstdayofweek==3:
       worstdayofweek='Thursday'
   elif worstdayofweek==4:
       worstdayofweek='Friday'
   elif worstdayofweek==5:
       worstdayofweek='Saturday'
   elif worstdayofweek==6:
       worstdayofweek='Sunday'
   
   result_label = tk.Label(new_window, text=f"{player}'s Best Day of Week for Each Stat")
   result_label.pack(pady=10)
   
   result_lpt = tk.Label(new_window, text=f"Points:    Best Day - {dayofweek[0][1]} with {round(result[0][2],1)} ppg      Worst Day - {dayofweek[0][0]} with {round(result[0][0],1)} ppg")
   result_lpt.pack(pady=10)
   
   result_last = tk.Label(new_window, text=f"Assists:    Best Day - {dayofweek[1][1]} with {round(result[1][2],1)} apg      Worst Day - {dayofweek[1][0]} with {round(result[1][0],1)} apg")
   result_last.pack(pady=10)
   
   result_lreb = tk.Label(new_window, text=f"Rebounds:    Best Day - {dayofweek[2][1]} with {round(result[2][2],1)} rpg      Worst Day - {dayofweek[2][0]} with {round(result[2][0],1)} rpg")
   result_lreb.pack(pady=10)
   
   result_lstl = tk.Label(new_window, text=f"Steals:    Best Day - {dayofweek[3][1]} with {round(result[3][2],1)} spg      Worst Day - {dayofweek[3][0]} with {round(result[3][0],1)} spg")
   result_lstl.pack(pady=10)
   
   result_lblk = tk.Label(new_window, text=f"Blocks:    Best Day - {dayofweek[4][1]} with {round(result[4][2],1)} bpg      Worst Day - {dayofweek[4][0]} with {round(result[4][0],1)} bpg")
   result_lblk.pack(pady=10)
   
   result_ltov = tk.Label(new_window, text=f"Turnovers:    Best Day - {dayofweek[5][1]} with {round(result[5][2],1)} topg      Worst Day - {dayofweek[5][0]} with {round(result[5][0],1)} topg")
   result_ltov.pack(pady=10)
   
   result_lfgm = tk.Label(new_window, text=f"Field Goals Made:    Best Day - {dayofweek[6][1]} with {round(result[6][2],1)} fgmpg      Worst Day - {dayofweek[6][0]} with {round(result[6][0],1)} fgmpg")
   result_lfgm.pack(pady=10)
   
   result_l3pm = tk.Label(new_window, text=f"Three Pointers Made:    Best Day - {dayofweek[7][1]} with {round(result[7][2],1)} 3pmpg      Worst Day - {dayofweek[7][0]} with {round(result[7][0],1)} 3pmpg")
   result_l3pm.pack(pady=10)
   
   result_lpf = tk.Label(new_window, text=f"Fouls:    Best Day - {dayofweek[8][1]} with {round(result[8][2],1)} fpg      Worst Day - {dayofweek[8][0]} with {round(result[8][0],1)} fpg")
   result_lpf.pack(pady=10)
   
   result_lpm = tk.Label(new_window, text=f"Plus Minus:    Best Day - {dayofweek[9][1]} with {round(result[9][2],1)} +/-pg      Worst Day - {dayofweek[9][0]} with {round(result[9][0],1)} +/-pg")
   result_lpm.pack(pady=10)
   
   result_lpm = tk.Label(new_window, text=f"When they Perform Best:  {bestdayofweek}      When they Perform Worst: {worstdayofweek} ")
   result_lpm.pack(pady=10)


def search(event):
    value=event.widget.get()
    
    if value == '':
        combo_box['values']=display_player
    else:
        data=[]
        for item in display_player:
            if value.lower() in item.lower():
                data.append(item)
                combo_box['values'] = data
    
    



allplayers=players.get_active_players()

window = tk.Tk()
window.title("What Day Does A NBA Player Perform Best")
window.geometry("800x400")
window.resizable(True, True)

# Create a label
label = tk.Label(window, text="Select an NBA Player:")
label.pack(pady=10)

display_player = [item["full_name"] for item in allplayers]



combo_box=ttk.Combobox(window, value=display_player)
combo_box.set('Search Nba Players')
combo_box.pack()
combo_box.bind('<KeyRelease>',search)

combo_box.bind("<<ComboboxSelected>>", on_button_click)





# Create a Tkinter variable to store the selected option
#selected_option = tk.StringVar(window)
#selected_option.set(display_player[0]) 

# Create the dropdown menu
#dropdown_menu = tk.OptionMenu(window, selected_option, *display_player)

# Create a Button widget and pass the selected option to on_button_click
button = tk.Button(window, text="Enter", command=lambda: on_button_click(combo_box.get()))

# Pack or place the widgets in the window
#dropdown_menu.pack(pady=10)
button.pack()

window.mainloop()



