
# coding: utf-8

# In[1]:

import Tkinter
from Tkinter import END
import tkFileDialog
import sqlite3
import datetime
import pandas
import pickle
from pandas import DataFrame, Series
from pandastable import Table

class StoneManagement(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent=parent
        self.initialize()
        
    def initialize(self):
        self.grid()
        
        directory="C:\Users\jqiao\Desktop\Stone Management.db"
        
        try:
            Directory = open('DB_Directory.obj', 'r')  
            directory = pickle.load(Directory_File)
        except:
            pass
        
        #Directory Select
        def askdirectory():
            global directory
            directory=str(tkFileDialog.askopenfilename(defaultextension=".db",filetypes=[('DataBase','.db')],parent=self))
            Directory_File=open('DB_Directory.obj','w')
            pickle.dump(directory,Directory_File)
        
        Directory=Tkinter.Button(self,anchor="w",fg="black",bg="white",text="ReSet\nDirectory",command=askdirectory)
        Directory.grid(row=0,column=0)
        

        #Image
        Idata="""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"""
        img=Tkinter.PhotoImage(data=Idata)        
        img=img.subsample(3,3)
        label_Image=Tkinter.Label(self,image=img,height=50, width=200)
        label_Image.image=img
        label_Image.grid(column=2, row=0, columnspan=2)        
        
        #Label
        label_MM= Tkinter.Label(self,
                              anchor="w",fg="black",bg="grey",text="MM Size")
        label_MM.grid(column=0,row=1,sticky='EW')
             
        label_Clarity = Tkinter.Label(self,
                              anchor="w",fg="black",bg="grey",text="Clarity")
        label_Clarity.grid(column=0,row=2,sticky='EW')
        
        label_Color = Tkinter.Label(self,
                              anchor="w",fg="black",bg="grey",text="Color")
        label_Color.grid(column=0,row=3,sticky='EW')
        
        label_Quantity = Tkinter.Label(self,
                              anchor="w",fg="black",bg="grey",text="Quantity")
        label_Quantity.grid(column=0,row=4,sticky='EW')
        
        label_Carat = Tkinter.Label(self,
                              anchor="w",fg="black",bg="grey",text="Total Carat Weight")
        label_Carat.grid(column=0,row=5,sticky='EW')
        
        label_Cost = Tkinter.Label(self,
                              anchor="w",fg="black",bg="grey",text="Average Cost")
        label_Cost.grid(column=0,row=6,sticky='EW')
        
        self.Conversation=Tkinter.StringVar()
        self.Conversation.set("Welcome!")
        label_Conversation = Tkinter.Label(self,
                              anchor="center",fg="black",bg="grey",textvariable=self.Conversation,font=18,wraplength=85)
        label_Conversation.grid(column=3,row=4,rowspan=3,sticky='EW')
        
        #Drop Dwon Box    
        MM_L = Tkinter.StringVar(self)
        MM_L.set("")
        Drop_MM=Tkinter.OptionMenu(self,MM_L,"1.7 mm","1.8 mm","1.9 mm","2.0 mm","2.1 mm","2.2 mm","2.3 mm","2.4 mm","2.5 mm","2.6 mm","2.7 mm","2.8 mm","2.9 mm","3.0 mm","3.1 mm","3.2 mm","3.3 mm","3.4 mm","3.5 mm","3.6 mm","3.7 mm","3.8 mm","3.9 mm","4.0 mm")
        Drop_MM.grid(column=2,row=1)
        Drop_MM.config(width=10)
        
        Clarity_L = Tkinter.StringVar(self)
        Clarity_L.set("")
        Drop_Clarity=Tkinter.OptionMenu(self,Clarity_L,"IF","VVS","VS","SI","I")
        Drop_Clarity.grid(column=2,row=2)
        Drop_Clarity.config(width=10)
        
        Color_L = Tkinter.StringVar(self)
        Color_L.set("")
        Drop_Color =Tkinter.OptionMenu(self,Color_L,"DEF","GHI","JKL","MNO","PQR","STU","VWX","YZ","TLB","LB","FLB","FB","FDB","FDOB")
        Drop_Color.grid(column=2,row=3)
        Drop_Color.config(width=10)
        
        
        #Input Box
        Quantity_Input = Tkinter.Entry(self,width=15,justify='center',bd=5)
        Quantity_Input.grid(column=2,row=4)
        
        Carat_Input = Tkinter.Entry(self,width=15,justify='center',bd=5)
        Carat_Input.grid(column=2,row=5)       

        Cost_Input = Tkinter.Entry(self,width=15,justify='center',bd=5)
        Cost_Input.grid(column=2,row=6)  
        
        #In-Out Formula
        def StoneIn():
            conn=sqlite3.connect(directory)
            StoneDB=conn.cursor()
            Clarity=Clarity_L.get()
            StoneDB.execute('SELECT id FROM Clarity_List WHERE Clarity= ?', (Clarity,))
            Clarity_id=StoneDB.fetchone()[0]
            Color=Color_L.get()
            StoneDB.execute('SELECT id FROM Color_List WHERE Color= ?', (Color,))
            Color_id=StoneDB.fetchone()[0]
            MM=MM_L.get()
            StoneDB.execute('SELECT id FROM MM_Size_List WHERE MM_Size= ?', (MM,))
            MM_id=StoneDB.fetchone()[0]
            StoneDB.execute('SELECT Quantity,Total_Carat,Total_Cost FROM Stones WHERE Color_id=? AND Clarity_id=? AND MM_Size_id=?',(Color_id,Clarity_id,MM_id))
            try:
                Result=StoneDB.fetchone()
                Quantity_Old=Result[0]
                Carat_Old=Result[1]
                Cost_Old=Result[2]
            except:
                Quantity_Old=0
                Carat_Old=0
                Cost_Old=0
            Quantity=int(Quantity_Input.get())+Quantity_Old
            Carat=float(Carat_Input.get())+Carat_Old
            Cost=float(Cost_Input.get())*float(Carat_Input.get())+Cost_Old
            if Quantity<0:
                self.Conversation.set("Negative Quantity Will Be Incurred")
            elif Carat<0:
                self.Conversation.set("Negative Carat Will Be Incurred")
            elif Cost<0:
                self.Conversation.set("Negative Cost Will Be Incurred")
            else:
                StoneDB.execute('''INSERT OR REPLACE INTO Stones (Color_id,Clarity_id,MM_Size_id,Quantity,Total_Carat,Total_Cost,Last_Update) VALUES (?,?,?,?,?,?,DATETIME())''',(Color_id,Clarity_id,MM_id,Quantity,Carat,Cost))
                conn.commit()
                self.Conversation.set("Stones Added "+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
                MM_L.set("")
                Clarity_L.set("")
                Color_L.set("")
                Quantity_Input.delete(0,END)
                Carat_Input.delete(0,END)
                Cost_Input.delete(0,END)

        
        def StoneOut():
            conn=sqlite3.connect(directory)
            StoneDB=conn.cursor()
            Clarity=Clarity_L.get()
            StoneDB.execute('SELECT id FROM Clarity_List WHERE Clarity= ?', (Clarity,))
            Clarity_id=StoneDB.fetchone()[0]
            Color=Color_L.get()
            StoneDB.execute('SELECT id FROM Color_List WHERE Color= ?', (Color,))
            Color_id=StoneDB.fetchone()[0]
            MM=MM_L.get()
            StoneDB.execute('SELECT id FROM MM_Size_List WHERE MM_Size= ?', (MM,))
            MM_id=StoneDB.fetchone()[0]
            StoneDB.execute('SELECT Quantity,Total_Carat,Total_Cost FROM Stones WHERE Color_id=? AND Clarity_id=? AND MM_Size_id=?',(Color_id,Clarity_id,MM_id))
            try:
                Result=StoneDB.fetchone()
                Quantity_Old=Result[0]
                Carat_Old=Result[1]
                Cost_Old=Result[2]
            except:
                Quantity_Old=0
                Carat_Old=0
                Cost_Old=0
            Quantity=Quantity_Old-int(Quantity_Input.get())
            Carat=Carat_Old-float(Carat_Input.get())
            Cost=Cost_Old-float(Cost_Input.get())*float(Carat_Input.get())
            if Quantity<0:
                self.Conversation.set("Negative Quantity Will Be Incurred")
            elif Carat<0:
                self.Conversation.set("Negative Carat Will Be Incurred")
            elif Cost<0:
                self.Conversation.set("Negative Cost Will Be Incurred")
            else:
                StoneDB.execute('''INSERT OR REPLACE INTO Stones (Color_id,Clarity_id,MM_Size_id,Quantity,Total_Carat,Total_Cost,Last_Update) VALUES (?,?,?,?,?,?,DATETIME())''',(Color_id,Clarity_id,MM_id,Quantity,Carat,Cost))
                conn.commit()
                self.Conversation.set("Stones Taken "+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'))
                MM_L.set("")
                Clarity_L.set("")
                Color_L.set("")
                Quantity_Input.delete(0,END)
                Carat_Input.delete(0,END)
                Cost_Input.delete(0,END)

            
        #In-Out View Button
        InButton = Tkinter.Button(self,text="In",bd=3,width=5,command=StoneIn)
        InButton.grid(column=3,row=1)

        OutButton = Tkinter.Button(self,text="Out",bd=3,width=5,command=StoneOut)
        OutButton.grid(column=3,row=2)
        
        #Second Window
        def View():
            ViewStone=Tkinter.Toplevel()
            ViewStone.title("View Stone Inventory")
            
            label_MM2= Tkinter.Label(ViewStone,
                              fg="black",bg="grey",text="MM Size",anchor='center')
            label_MM2.grid(column=0,row=0,columnspan=2,sticky='EW')

            label_Clarity2 = Tkinter.Label(ViewStone,
                                  fg="black",bg="grey",text="Clarity",anchor='center')
            label_Clarity2.grid(column=2,row=0,columnspan=2,sticky='EW')

            label_Color2 = Tkinter.Label(ViewStone,
                                  fg="black",bg="grey",text="Color",anchor='center')
            label_Color2.grid(column=4,row=0,columnspan=2,sticky='EW')
            
            

            
            
            MM_L2 = Tkinter.StringVar(ViewStone)
            MM_L2.set("")
            Drop_MM2=Tkinter.OptionMenu(ViewStone,MM_L2,"1.7 mm","1.8 mm","1.9 mm","2.0 mm","2.1 mm","2.2 mm","2.3 mm","2.4 mm","2.5 mm","2.6 mm","2.7 mm","2.8 mm","2.9 mm","3.0 mm","3.1 mm","3.2 mm","3.3 mm","3.4 mm","3.5 mm","3.6 mm","3.7 mm","3.8 mm","3.9 mm","4.0 mm")
            Drop_MM2.grid(column=0,row=1,columnspan=2)
            Drop_MM2.config(width=10)

            Clarity_L2 = Tkinter.StringVar(ViewStone)
            Clarity_L2.set("")
            Drop_Clarity2=Tkinter.OptionMenu(ViewStone,Clarity_L2,"IF","VVS","VS","SI","I")
            Drop_Clarity2.grid(column=2,row=1,columnspan=2)
            Drop_Clarity2.config(width=10)
            
            Color_L2 = Tkinter.StringVar(ViewStone)
            Color_L2.set("")
            Drop_Color2 =Tkinter.OptionMenu(ViewStone,Color_L2,"DEF","GHI","JKL","MNO","PQR","STU","VWX","YZ","TLB","LB","FLB","FB","FDB","FDOB")
            Drop_Color2.grid(column=4,row=1,columnspan=2)
            Drop_Color2.config(width=10)
            
            global List
            
            def MM_change(*args):
                if MM_L2.get()!="":
                    Clarity_L2.set("")
                    Color_L2.set("")
                    global List
                    try:
                        for labels in List:
                            labels.grid_forget()
                    except:
                        pass    
                    conn=sqlite3.connect(directory)
                    StoneDB=conn.cursor()
                    MM2=MM_L2.get()
                    StoneDB.execute('SELECT id FROM MM_Size_List WHERE MM_Size= ?', (MM2,)) 
                    MM_id2=StoneDB.fetchone()[0]
                    StoneDB.execute('SELECT Clarity_List.Clarity,Color_List.Color,MM_Size_List.MM_Size,Stones.Total_Cost,Stones.Quantity,Stones.Last_Update FROM Stones JOIN Clarity_List ON Stones.Clarity_id=Clarity_List.id JOIN Color_List ON Stones.Color_id=Color_List.id JOIN MM_Size_List ON Stones.MM_Size_id=MM_Size_List.id WHERE MM_Size_id=?',(MM_id2,))  
                    Result2=DataFrame(StoneDB.fetchall())
                    Result2.columns=['Clarity','Color','MM_Size','Total_Cost','Total_Carat','Last_Update']
                    Result2['Average Cost']=Result2['Total_Cost']/Result2['Total_Carat']
                    Result2.drop(['Last_Update','MM_Size'],axis=1,inplace =True)
                    Result2['Clarity']=pandas.Categorical(Result2['Clarity'],categories=['IF','VVS','VS','SI','I'],ordered=True)
                    Result2.sort_values('Clarity')
                    Result3=Result2.pivot('Color','Clarity')
                    Clarity_3=Result2.Clarity.unique()
                    Color_L3=Result2.Color.unique()
                    Color_L3.sort()
                    n=3
                    List=[]
                    for table in range(3):
                        Table_label = Tkinter.Label(ViewStone, text=list(Result2.columns.values)[table+2],height=1)
                        Table_label.grid(row=n,column=0,columnspan=6)
                        List.append(Table_label)
                        n=n+2
                        for column in range(len(Clarity_3)):
                            label = Tkinter.Label(ViewStone, text=str(Clarity_3[column]),height=1, 
                                             borderwidth=0)
                            label.grid(row=n-1, column=column+1, sticky="nsew", padx=1, pady=1)
                            List.append(label)

                        for row in range(len(Color_L3)):
                            label = Tkinter.Label(ViewStone, text=str(Color_L3[row]),height=1, 
                                             borderwidth=0)
                            label.grid(row=n, column=0, sticky="nsew", padx=1, pady=1)
                            List.append(label)
                            for column in range(len(Clarity_3)):
                                label = Tkinter.Label(ViewStone, text='{:.2f}'.format(Result3.iloc[row][column+table*len(Clarity_3)]), 
                                                 borderwidth=0,height=1)
                                label.grid(row=n, column=column+1, sticky="nsew", padx=1, pady=1)
                                List.append(label)
                            n=n+1

                        n=n+1
                    conn.commit()
                    
            MM_L2.trace("w",MM_change)

            def Clarity_change(*args):
                if Clarity_L2.get()!="":
                    Color_L2.set("")
                    MM_L2.set("")
                    global List
                    try:
                        for labels in List:
                            labels.grid_forget()
                    except:
                        pass
                    conn=sqlite3.connect(directory)
                    StoneDB=conn.cursor()
                    Clarity2=Clarity_L2.get()
                    StoneDB.execute('SELECT id FROM Clarity_List WHERE Clarity= ?', (Clarity2,))
                    Clarity_id2=StoneDB.fetchone()[0]
                    StoneDB.execute('SELECT Clarity_List.Clarity,Color_List.Color,MM_Size_List.MM_Size,Stones.Total_Cost,Stones.Quantity,Stones.Last_Update FROM Stones JOIN Clarity_List ON Stones.Clarity_id=Clarity_List.id JOIN Color_List ON Stones.Color_id=Color_List.id JOIN MM_Size_List ON Stones.MM_Size_id=MM_Size_List.id WHERE Clarity_id=?',(Clarity_id2,)) 
                    Result2=DataFrame(StoneDB.fetchall())
                    Result2.columns=['Clarity','Color','MM_Size','Total_Cost','Total_Carat','Last_Update']
                    Result2['Average Cost']=Result2['Total_Cost']/Result2['Total_Carat']
                    Result2.drop(['Last_Update','Clarity'],axis=1,inplace =True)
                    Result2.sort_values('Color')
                    Result3=Result2.pivot('MM_Size','Color')
                    Color_3=Result2.Color.unique()
                    MM_L3=Result2.MM_Size.unique()
                    MM_L3.sort()
                    n=3
                    List=[]
                    for table in range(3):
                        Table_label = Tkinter.Label(ViewStone, text=list(Result2.columns.values)[table+2],height=1)
                        Table_label.grid(row=n,column=0,columnspan=6)
                        List.append(Table_label)
                        n=n+2
                        for column in range(len(Color_3)):
                            label = Tkinter.Label(ViewStone, text=str(Color_3[column]),height=1, 
                                             borderwidth=0)
                            label.grid(row=n-1, column=column+1, sticky="nsew", padx=1, pady=1)
                            List.append(label)
                            

                        for row in range(len(MM_L3)):
                            label = Tkinter.Label(ViewStone, text=str(MM_L3[row]),height=1, 
                                             borderwidth=0)
                            label.grid(row=n, column=0, sticky="nsew", padx=1, pady=1)
                            List.append(label)
                            for column in range(len(Color_3)):
                                label = Tkinter.Label(ViewStone, text='{:.2f}'.format(Result3.iloc[row][column+table*len(Color_3)]), 
                                                 borderwidth=0,height=1)
                                label.grid(row=n, column=column+1, sticky="nsew", padx=1, pady=1)
                                List.append(label)
                            n=n+1

                        n=n+1
                    conn.commit() 
            Clarity_L2.trace("w",Clarity_change)

            def Color_change(*args):
                if Color_L2.get()!="":
                    Clarity_L2.set("")
                    MM_L2.set("")
                    global List
                    try:
                        for labels in List:
                            labels.grid_forget()
                    except:
                        pass
                    conn=sqlite3.connect(directory)
                    StoneDB=conn.cursor()
                    Color2=Color_L2.get()
                    StoneDB.execute('SELECT id FROM Color_List WHERE Color= ?', (Color2,))
                    Color_id2=StoneDB.fetchone()[0]
                    StoneDB.execute('SELECT Clarity_List.Clarity,Color_List.Color,MM_Size_List.MM_Size,Stones.Total_Cost,Stones.Quantity,Stones.Last_Update FROM Stones JOIN Clarity_List ON Stones.Clarity_id=Clarity_List.id JOIN Color_List ON Stones.Color_id=Color_List.id JOIN MM_Size_List ON Stones.MM_Size_id=MM_Size_List.id WHERE Color_id=?',(Color_id2,)) 
                    Result2=DataFrame(StoneDB.fetchall())
                    Result2.columns=['Clarity','Color','MM_Size','Total_Cost','Total_Carat','Last_Update']
                    Result2['Average Cost']=Result2['Total_Cost']/Result2['Total_Carat']
                    Result2.drop(['Last_Update','Color'],axis=1,inplace =True)
                    Result2['Clarity']=pandas.Categorical(Result2['Clarity'],categories=['IF','VVS','VS','SI','I'],ordered=True)
                    Result2.sort_values('Clarity')
                    Result3=Result2.pivot('MM_Size','Clarity')
                    Clarity_3=Result2.Clarity.unique()
                    MM_L3=Result2.MM_Size.unique()
                    MM_L3.sort()
                    n=3
                    List=[]
                    for table in range(3):
                        Table_label = Tkinter.Label(ViewStone, text=list(Result2.columns.values)[table+2],height=1)
                        Table_label.grid(row=n,column=0,columnspan=6)
                        List.append(Table_label)
                        n=n+2
                        for column in range(len(Clarity_3)):
                            label = Tkinter.Label(ViewStone, text=str(Clarity_3[column]),height=1, 
                                             borderwidth=0)
                            label.grid(row=n-1, column=column+1, sticky="nsew", padx=1, pady=1)
                            List.append(label)

                        for row in range(len(MM_L3)):
                            label = Tkinter.Label(ViewStone, text=str(MM_L3[row]),height=1, 
                                             borderwidth=0)
                            label.grid(row=n, column=0, sticky="nsew", padx=1, pady=1)
                            List.append(label)
                            for column in range(len(Clarity_3)):
                                label = Tkinter.Label(ViewStone, text='{:.2f}'.format(Result3.iloc[row][column+table*len(Clarity_3)]), 
                                                 borderwidth=0,height=1)
                                label.grid(row=n, column=column+1, sticky="nsew", padx=1, pady=1)
                                List.append(label)
                            n=n+1

                        n=n+1
                    conn.commit()

            Color_L2.trace("w",Color_change)
            

            

        ViewButton =Tkinter.Button(self,text="View inventory",bd=3,width=12,command=View)
        ViewButton.grid(column=3,row=3)

    

if __name__=="__main__":
    app=StoneManagement(None)
    app.title('Stone Inventory Management')
    app.mainloop()  


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



