from numpy import place
from tkinter import *
from  PIL import Image,ImageTk
import requests
import pickle
from tkinter import ttk
from requests.models import Request
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from functools import partial

root=Tk()
root.geometry("600x600")
root.title("Weather Report")
def back():
    for widget in root.winfo_children():
        widget.destroy()
    Label(root,text="WEATHER REPORT",font="comicsansms 20 bold",fg="red").pack()
    panel = Label(root, image=new_image)
    panel.place(x=490,y=0)
    Button(root,text="Current  weather report",font="comicsansms 12 bold",fg="black",padx=5,command=current).pack(pady=15)
    Button(root,text="Forcast next 48 hr. weather",font="comicsansms 12 bold",fg="black",padx=5,command=forcast).pack(pady=10)
    Button(root,text="Complete Weather Report",font="comicsansms 12 bold",fg="black",padx=5,command=report).pack(pady=10)
    Button(root,text="Exit",font="comicsansms 12 bold",fg="black",padx=5,command=exit).pack(pady=10)

def forcast():
      for widget in root.winfo_children():
            widget.destroy()
      main_frame = Frame(root)
      main_frame.pack(fill=BOTH, expand=1)
      my_canvas = Canvas(main_frame)
      my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
      y_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
      y_scrollbar.pack(side=RIGHT, fill=Y)
      my_canvas.configure(yscrollcommand=y_scrollbar.set)
      my_canvas.bind("<Configure>", lambda e: my_canvas.config(scrollregion=my_canvas.bbox(ALL)))
      second_frame = Frame(my_canvas)
      my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
      panel = Label(second_frame, image=new_image)
      panel.place(x=490,y=0)
      Button(root,text="<--",font="comicsansms 12 bold",fg="black",padx=5,command=back).place(x=0,y=0)
      city=StringVar()
      Label(second_frame,text=" FORECAST  WEATHER ",font="comicsansms 18 bold",fg="red").place(x=100,y=0)
      Label(second_frame,text="Select City",font="comicsansms 15 bold").place(x=80,y=50)
      mycombobox=ttk.Combobox(second_frame,textvariable=city,values=["delhi","kanpur","bangalore","mumbai","jaipur","hyderabad","nagpur","pune"],state="readonly").place(x=250,y=50) 
      def hours():
            Label(second_frame,text="                               ",font="comicsansms 16 bold",fg="red").place(x=150,y=130)
            if(city.get()==""):
                Label(second_frame,text="Please select city!",font="comicsansms 16 bold",fg="red").place(x=150,y=130)
            else:
                dict={'delhi':'forecast','kanpur':'forecast_knp','pune':'forecast_pune','bangalore':'forecast_bengaluru','hyderabad':'forecast_hyderabad','mumbai':'forecast_bombay','nagpur':'forecast_nagpur','jaipur':'forecast_jaipur'}
                with open(f"E:\\weather reporting system\\project\\{dict[city.get()]}", 'rb') as f:
                    model = pickle.load(f)
                cities=pd.read_csv("E:\\weather reporting system\\project\\cities_lat_lon.csv")
                cities['city']=cities['city'].str.lower()
                lat=list(cities.loc[cities['city']==city.get(),'lat'])
                long=list(cities.loc[cities['city']==city.get(),'lng'])
                df=pd.DataFrame(columns=['pressure','humidity','dew_point','wind_speed'])
                api="550e7b96678d45b05121fdf5f6afb8c3"
                url=f"https://api.openweathermap.org/data/2.5/onecall?lat={lat[0]}&lon={long[0]}&appid={api}&units=metric"        
                data=requests.get(url).json()
                for i in range(0,48):
                    df.loc[i,'date']=data['hourly'][i]['dt']
                    time=df.loc[i,'date']
                    df.loc[i,'date']=datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
                    df.loc[i,'pressure']=data['hourly'][i]['pressure']
                    df.loc[i,'humidity']=data['hourly'][i]['humidity']
                    df.loc[i,'dew_point']=data['hourly'][i]['dew_point']
                    df.loc[i,'wind_speed']=data['hourly'][i]['wind_speed']
                    df.loc[i,'wind_deg'] = data['hourly'][i]['wind_deg']
                pred=model.predict(df.drop(['date'],axis='columns').values)
                pred=pred.reshape(1,48)
                for i in range(0,48):
                    Label(second_frame,text=f"{df['date'][i]}",font="comicsansms 11 bold").place(x=60,y=140+i*30)
                    Label(second_frame,text=f"{pred[0][i].round(decimals=2)} °C    ",font="comicsansms 11 bold").place(x=300,y=140+i*30)
        
      Button(second_frame,text="Submit",font="comicsansms 10 bold",fg="black",padx=5,command=hours).place(x=200,y=90)

      for thing in range(100):
                Label(second_frame, text=f"").grid(row=30, column=thing, pady=10, padx=10)

      for thing in range(100):
                Label(second_frame, text=f"").grid(row=thing, column=30, pady=10, padx=10)    

def report():
    for widget in root.winfo_children():
            widget.destroy()
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=1)
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
    y_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    y_scrollbar.pack(side=RIGHT, fill=Y)
    x_scrollbar = ttk.Scrollbar(root, orient=HORIZONTAL, command=my_canvas.xview)
    x_scrollbar.pack(side=BOTTOM, fill=X)
    my_canvas.configure(xscrollcommand=x_scrollbar.set,yscrollcommand=y_scrollbar.set)
    my_canvas.bind("<Configure>", lambda e: my_canvas.config(scrollregion=my_canvas.bbox(ALL)))
    second_frame = Frame(my_canvas)
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
    panel = Label(second_frame, image=new_image)
    panel.place(x=490,y=0)

    city=StringVar()
    Label(second_frame,text="COMPLETE  WEATHER  REPORT",font="comicsansms 18 bold",fg="red").place(x=100,y=0)
    Label(second_frame,text="Select City",font="comicsansms 15 bold").place(x=140,y=50)
    mycombobox=ttk.Combobox(second_frame,textvariable=city,values=["delhi","kanpur","bangalore","mumbai","jaipur","hyderabad","nagpur","pune"],state="readonly").place(x=300,y=50)
    Button(root,text="<--",font="comicsansms 12 bold",fg="black",padx=5,command=back).place(x=0,y=0)

    def perform():
        Label(second_frame,text="                                          ",font="comicsansms 16 bold",fg="red").place(x=190,y=130)
        if(city.get()==""):
            Label(second_frame,text="Please select city!",font="comicsansms 16 bold",fg="red").place(x=190,y=130)
        else:
            dict={'delhi':'forecast','kanpur':'forecast_knp','pune':'forecast_pune','bangalore':'forecast_bengaluru','hyderabad':'forecast_hyderabad','mumbai':'forecast_bombay','nagpur':'forecast_nagpur','jaipur':'forecast_jaipur'}
            with open(f"E:\\weather reporting system\\project\\{dict[city.get()]}", 'rb') as f:
                model = pickle.load(f)
            cities = pd.read_csv("E:\\weather reporting system\\project\\cities_lat_lon.csv")
            cities['city'] = cities['city'].str.lower()
            lat = list(cities.loc[cities['city'] == city.get(), 'lat'])
            long = list(cities.loc[cities['city'] == city.get(), 'lng'])
            df = pd.DataFrame(columns=['pressure', 'humidity', 'dew_point', 'wind_speed'])
            api = "550e7b96678d45b05121fdf5f6afb8c3"
            url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat[0]}&lon={long[0]}&appid={api}&units=metric"
            data = requests.get(url).json()
            for i in range(0, 48):
                df.loc[i, 'date'] = data['hourly'][i]['dt']
                time = df.loc[i, 'date']
                df.loc[i, 'date'] = datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
                df.loc[i, 'pressure'] = data['hourly'][i]['pressure']
                df.loc[i, 'humidity'] = data['hourly'][i]['humidity']
                df.loc[i, 'dew_point'] = data['hourly'][i]['dew_point']
                df.loc[i, 'wind_speed'] = data['hourly'][i]['wind_speed']
                df.loc[i, 'uvi'] = data['hourly'][i]['uvi']
                df.loc[i, 'clouds'] = data['hourly'][i]['clouds']
                df.loc[i, 'visibility'] = data['hourly'][i]['visibility']
                df.loc[i, 'wind_deg'] = data['hourly'][i]['wind_deg']
                df.loc[i, 'wind_gust'] = data['hourly'][i]['wind_gust']

            final=pd.DataFrame(columns=['time','pred'])
            for i in range(0,48):
                final.loc[i,'time']=df['date'].str.split(" ")[i][1]
                final.loc[i,'time']=final['time'].str.split(":")[i][0]+":"+final['time'].str.split(":")[i][1]

            temp = data['current']['temp']
            humidity = data['current']['humidity']
            feels_like = data['current']['feels_like']
            description = data['current']['weather'][0]['description']
            pressure = data['current']['pressure']
            dew_point = data['current']['dew_point']
            visibility = data['current']['visibility']
            clouds = data['current']['clouds']
            wind_speed = round(data['current']['wind_speed']*3.6,2)
            feature=['Temperture','Humidity','Feels Like','Description','Pressure','Dew Point','Wind speed','Visibility','Clouds']
            i=0
            for item in feature:
                Label(second_frame, text=f"{item}",font="comicsansms 11 bold").place(x=80, y=130+i*30)
                i+=1
            for i in range(0, 9):
                Label(second_frame, text=f"                                ", font="comicsansms 11 bold").place(x=250, y=130+i*30)
            Label(second_frame, text=f"{temp} °C",font="comicsansms 11 bold").place(x=250, y=130)
            Label(second_frame, text=f"{humidity} %",font="comicsansms 11 bold").place(x=250, y=160)
            Label(second_frame, text=f"{feels_like} °C",font="comicsansms 11 bold").place(x=250, y=190)
            Label(second_frame, text=f"{description}",font="comicsansms 11 bold").place(x=250, y=220)
            Label(second_frame, text=f"{pressure} hPa",font="comicsansms 11 bold").place(x=250, y=250)
            Label(second_frame, text=f"{dew_point} °C",font="comicsansms 11 bold").place(x=250, y=280)
            Label(second_frame, text=f"{wind_speed} km/hrs",font="comicsansms 11 bold").place(x=250, y=310)
            Label(second_frame, text=f"{visibility} m",font="comicsansms 11 bold").place(x=250, y=340)
            Label(second_frame, text=f"{clouds} %",font="comicsansms 11 bold").place(x=250, y=370)

            for i in range(0, 48):
                Label(second_frame, text=f"                            ", font="comicsansms 11 bold").place(x=80, y=440+i*30)
                Label(second_frame, text=f"                            ",font="comicsansms 11 bold").place(x=250, y=440+i*30)
            
            pred = model.predict(df.drop(['date', 'clouds', 'visibility', 'wind_gust', 'uvi'], axis='columns').values)
            pred = pred.reshape(1, 48)
            Label(second_frame, text="Next 48 hr. Forcast",font="comicsansms 11 bold", fg="red").place(x=140, y=410)
            # final=pd.DataFrame(columns=['time','pred'])
            for i in range(0,48):
            #     final.loc[i,'time']=df['date'].values[i]
                final.loc[i,'pred']=pred[0][i]
            for i in range(0, 48):
                Label(second_frame, text=f"{df['date'][i]}", font="comicsansms 11 bold").place(x=80, y=440+i*30)
                Label(second_frame, text=f"{pred[0][i].round(decimals=2)} °C",font="comicsansms 11 bold").place(x=250, y=440+i*30)

            fig, ax = plt.subplots(2)
            fig.suptitle("Temp vs Time Graph",size=15)
            fig.set_figheight(7)
            fig.set_figwidth(14)
            ax[0].scatter(final['time'][0:24],final['pred'][0:24],marker="o",c='b')
            ax[0].plot(final['time'][0:24],final['pred'][0:24])
            ax[0].set_title("First 24 hours",size=13)
            ax[0].set_xlabel("Time",size=12)
            ax[0].set_ylabel("Temperature",size=12)
            ax[1].set_title("Next 24 hours",size=13)
            ax[0].set_xticklabels(final['time'][0:24], rotation=45, ha='right')
            ax[1].scatter(final['time'][24:48],final['pred'][24:48],marker="o",c='b')
            ax[1].set_xticklabels(final['time'][24:48], rotation=45, ha='right')
            ax[1].plot(final['time'][24:48],final['pred'][24:48])
            ax[1].set_xlabel("Time",size=12)
            ax[1].set_ylabel("Temperature",size=12)
            # plt.subplots_adjust(left=0.1,
            #         bottom=0.1, 
            #         right=0.1, 
            #         top=0.1, 
            #         wspace=0.3, 
            #         hspace=0.5)
            plt.subplots_adjust(wspace=0.3,hspace=0.7)
            canvas = FigureCanvasTkAgg(fig,master = second_frame)  
            canvas.draw()
            canvas.get_tk_widget().place(x=350,y=440)
            # plt.show()
    Button(second_frame,text="Submit",font="comicsansms 10 bold",fg="black",padx=5,command=perform).place(x=250,y=90)

    for thing in range(100):
        Label(second_frame, text=f"").grid(row=30, column=thing, pady=10, padx=10)

    for thing in range(100):
        Label(second_frame, text=f"").grid(row=thing, column=30, pady=10, padx=10) 

  
def req(frame,city):
    if(city.get()==""):
        Label(frame,text='''
        Please 
        select 
        city!''',font="comicsansms 16 bold",fg="red").place(x=280,y=160)
    else:
        cities = pd.read_csv("E:\\weather reporting system\\project\\cities_lat_lon.csv")
        cities['city'] = cities['city'].str.lower()
        lat = list(cities.loc[cities['city'] == city.get(), 'lat'])
        long = list(cities.loc[cities['city'] == city.get(), 'lng'])
        print(lat,long)
        api="550e7b96678d45b05121fdf5f6afb8c3"
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat[0]}&lon={long[0]}&appid={api}&units=metric"
        data=requests.get(url).json()
        temp = data['current']['temp']
        humidity = data['current']['humidity']
        feels_like = data['current']['feels_like']
        description = data['current']['weather'][0]['description']
        pressure = data['current']['pressure']
        dew_point = data['current']['dew_point']
        visibility = data['current']['visibility']
        clouds = data['current']['clouds']
        wind_speed=round(data['current']['wind_speed']*3.6,2)
        for i in range(0,9):
            Label(frame,text=f"                          ",font="comicsansms 15 bold").place(x=250,y=130+i*30)
        Label(frame,text=f"{temp} °C",font="comicsansms 15 bold").place(x=250,y=130)
        Label(frame,text=f"{humidity} %",font="comicsansms 15 bold").place(x=250,y=160)
        Label(frame,text=f"{feels_like} °C",font="comicsansms 15 bold").place(x=250,y=190)
        Label(frame,text=f"{description}",font="comicsansms 15 bold").place(x=250,y=220)
        Label(frame,text=f"{pressure} hPa",font="comicsansms 15 bold").place(x=250,y=250)
        Label(frame,text=f"{dew_point} °C",font="comicsansms 15 bold").place(x=250,y=280)
        Label(frame,text=f"{wind_speed} Km\hr",font="comicsansms 15 bold").place(x=250,y=310)               
        Label(frame,text=f"{visibility} m",font="comicsansms 15 bold").place(x=250,y=340)
        Label(frame,text=f"{clouds} %",font="comicsansms 15 bold").place(x=250,y=370)

def current():
    for widget in root.winfo_children():
            widget.destroy()
    city=StringVar()
    panel = Label(root, image=new_image)
    panel.place(x=490,y=0)
    Label(root,text=" CURRENT  WEATHER  REPORT",font="comicsansms 18 bold",fg="red").pack()
    Label(root,text="Select City",font="comicsansms 15 bold").place(x=80,y=50)
    mycombobox=ttk.Combobox(root,textvariable=city,values=["delhi","kanpur","lucknow","bangalore","mumbai","jaipur","hyderabad","nagpur","pune"],state="readonly").place(x=250,y=50)
    Label(root,text="Temperture",font="comicsansms 15 bold").place(x=80,y=130)
    Label(root,text="Humidity",font="comicsansms 15 bold").place(x=80,y=160)
    Label(root,text="Feels Like",font="comicsansms 15 bold").place(x=80,y=190)
    Label(root,text="Description",font="comicsansms 15 bold").place(x=80,y=220) 
    Label(root,text="Pressure",font="comicsansms 15 bold").place(x=80,y=250)
    Label(root,text="Dew point",font="comicsansms 15 bold").place(x=80,y=280)
    Label(root,text="Wind Speed",font="comicsansms 15 bold").place(x=80,y=310)
    Label(root,text="Visibility",font="comicsansms 15 bold").place(x=80,y=340)
    Label(root,text="Clouds",font="comicsansms 15 bold").place(x=80,y=370)

    Button(root,text="<--",font="comicsansms 12 bold",fg="black",padx=5,command=back).place(x=0,y=0)
    Button(root,text="Submit",font="comicsansms 10 bold",fg="black",padx=5,command=partial(req,root,city)).place(x=200,y=90)


canvas= Canvas(root, width= 100, height= 100)
canvas.place(x=490,y=0)
img= (Image.open("E:\\weather reporting system\\project\\logo.png"))
resized_image= img.resize((80,80), Image.ANTIALIAS)
new_image= ImageTk.PhotoImage(resized_image)
canvas.create_image(10,10, anchor=NW, image=new_image)

Label(root,text="WEATHER REPORT",font="comicsansms 20 bold underline",fg="red").pack()
Button(root,text="Current  weather report",font="comicsansms 12 bold",fg="black",padx=5,command=current).pack(pady=15)
Button(root,text="Forcast next 48 hr. weather",font="comicsansms 12 bold",fg="black",padx=5,command=forcast).pack(pady=10)
Button(root,text="Complete Weather Report",font="comicsansms 12 bold",fg="black",padx=5,command=report).pack(pady=10)
Button(root,text="Exit",font="comicsansms 12 bold",fg="black",padx=5,command=exit).pack(pady=10)
root.mainloop()