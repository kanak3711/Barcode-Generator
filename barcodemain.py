import re, os, sys, upcean, csv;
from configparser import ConfigParser
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox
from tkinter import filedialog as fdial
from PIL import Image, ImageTk,ImageGrab;
import datetime
import tkinter.scrolledtext as tkst
global h
global w
root = tk.Tk()
class MainWin1(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self)
        width, height = master.winfo_screenwidth(), master.winfo_screenheight()
        master.geometry(set_size(master, width, height))
        master.resizable(True, True)
        master.title("Barcode generator")
      
        self.cwidth=tk.IntVar()
        self.cheight=tk.IntVar()
   
        self.master = master
        master.rowconfigure(1, weight=1)
        self.frameMain = ttk.Frame(master)
        self.frameMain.grid(row=1, column=0, columnspan=2, sticky='nswe', padx=(10, 0), pady=(0,10))
        self.frameType = ttk.Frame(self.frameMain, padding=(5, 5))
        self.frameType.grid(row=0, column=0, sticky="nswe", padx=(0,0), pady=(2,2))
        ttk.Label(self.frameType, text="Welcome to barcode generator!", font=('Comic Sans MS', 42)).grid(row=3, column=2,sticky='w', padx=(5,5), pady=(5,5))
        ttk.Label(self.frameType, text="Select canvas Size:", font=('Arial', 24)).grid(row=5, column=1,sticky='w', padx=(5,5), pady=(5,5))
        ttk.Label(self.frameType, text='Height:').grid(row=11, column=1, sticky='w', padx=(5, 0), pady=(5,0))
        self.bfont_size = ttk.Spinbox(self.frameType, wrap=True, from_=1, to=1000, textvariable=self.cheight)
        self.bfont_size.grid(row=12, column=1, sticky='we', pady=(5,5), padx=(5,5))
        ttk.Label(self.frameType, text='Width:').grid(row=13, column=1, sticky='w', padx=(5, 0), pady=(5,0))
        self.bfont_size = ttk.Spinbox(self.frameType ,wrap=True, from_=1, to=1000, textvariable=self.cwidth)
        self.bfont_size.grid(row=14, column=1, sticky='we', pady=(5,5), padx=(5,5))
        global w
        w=self.cwidth
        global h
        h=self.cheight

        self.frameButton = ttk.Frame(self.frameMain)
        self.frameButton.grid(row=4, column=0, sticky="nswe", padx=(0,5), pady=(5,5))
        self.frameButton.grid_columnconfigure(0, weight=1)
        self.frameButton.grid_columnconfigure(1, weight=1)
        
        self.btnSave = ttk.Button(self.frameButton, text='Cancel', command=quit)
        self.btnSave.grid(row=3, column=3, pady=(0,0), padx=(2, 0), sticky="we")
        self.btnSave = ttk.Button(self.frameButton, text='Ok', command=self.new_window)
        self.btnSave.grid(row=3, column=2, pady=(0,0), padx=(2, 0), sticky="we")   

    def display(self):
        print('')

    def new_window(self):
        self.master.withdraw()
        self.newWindow = tk.Toplevel(self.master)
        bb = MainWin(self.newWindow)

#===================================================================================================================
class MainWin(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self)
        width, height = master.winfo_screenwidth(), master.winfo_screenheight()
        master.geometry(set_size(master, width, height))
        master.resizable(True, True)
        master.title("Barcode generator v1.0")

        self.barcode_bg_color = (255, 255, 255);
        self.barcode_bar_color = (0, 0, 0);
        self.barcode_text_color = (0, 0, 0);
        self.barcode_list = {"EAN-13": "ean13", "EAN-8": "ean8", "EAN-5": "ean5"};
        self.bcsize = tk.IntVar()
        self.cwidth=tk.IntVar()
        self.cheight=tk.IntVar()
        self.ctwidth=tk.IntVar()
        self.ctheight=tk.IntVar()
        self.bctype = tk.StringVar()
        self.bcvalue = tk.StringVar()
        self.ean13start = self.ean08start = self.ean05start = ''
        self.existcomment = ''
        self.filedir = ''
        self.filetype = 'PNG'
        self.edited = False
        self.selected = ''
        self.oldvalue = ''
        self.fosize = tk.IntVar()
        self.fotype = tk.StringVar()

        self.master = master
        master.rowconfigure(1, weight=1)
        self.frameTopLeft = tk.Frame(master)
        self.frameTopLeft.grid(row=0, column=0, sticky='nw', padx=(10, 0))
        self.frameTopRight = tk.Frame(master, width=master.winfo_screenwidth()/2+80,height =master.winfo_screenwidth() )
        self.frameTopRight.grid(row=0, column=1, sticky='nsw', padx=(10,0))
        self.frameTopRight.grid_propagate(False)
        self.frameTopRight.configure(background='#73C6B6')
        self.frameMain = ttk.Frame(master)
        self.frameMain.grid(row=1, column=0, columnspan=2, sticky='nswe', padx=(10, 0), pady=(0,10))

        # Menubar
        master.option_add('*tearOff', False)
        self.menubar = tk.Menu(master)
        master.config(menu = self.menubar)
        self.file = tk.Menu(self.menubar)
        help_ = tk.Menu(self.menubar)

        self.menubar.add_cascade(menu = self.file, label = 'File')

        self.file.add_command(label = 'Save as', command = self.saveasfile)
        self.file.add_command(label = 'Settings', command =self.settings)
        self.file.add_command(label = 'Info', command =self.helpwin)
        self.file.entryconfig('Save as', accelerator = 'Ctrl+S')

        #Entries
        self.frameType = ttk.Frame(self.frameTopLeft, padding=(5, 5))
        self.frameType.grid(row=0, column=0, sticky="nswe", padx=(0,0), pady=(2,2))

        ttk.Label(self.frameType, text='Barcode type:  ').grid(row=0, column=0, sticky='w', padx=(2,0))
        options = ['EAN-13', 'EAN-8', 'EAN-5']
        self.bcode_type = ttk.OptionMenu(self.frameType, self.bctype, options[0], *options, style = 'raised.TMenubutton')
        self.bcode_type.grid(row=0, column=1, sticky='we')

        ttk.Label(self.frameType, text="Barcode size:").grid(row=1, column=0, sticky='w', padx=(2, 0))
        self.bcode_size = ttk.Spinbox(self.frameType, wrap=True,from_=1, to=10, textvariable=self.bcsize)
        self.bcode_size.grid(row=2, column=1, sticky='we', pady=(0,0),padx=(0,0))
        
        ttk.Label(self.frameType, text='Barcode value:').grid(row=3, column=0, sticky='w', padx=(2, 0))
        self.bcode_val = ttk.Entry(self.frameType, textvariable=self.bcvalue, font=('Arial', 15))
        self.bcode_val.grid(row=4, column=1, pady=(0,0), padx=(0,0))

        ttk.Label(self.frameType, text='Comment:').grid(row=5, column=0, sticky='w', padx=(5, 0), pady=(5,0))
        self.textFrame = ttk.Frame(self.frameType)
        self.textFrame.grid(row=6, column=1, pady=(0,0))
        self.textFrame.columnconfigure(0, weight=1)
        self.bcode_comment = tkst.ScrolledText(self.textFrame, wrap=tk.WORD, width=30, height=3, font=('Arial', 10))
        self.bcode_comment.grid(row=0, column=0, pady=(0,0), sticky='we')

        ttk.Label(self.frameType, text='Font Size:').grid(row=7, column=0, sticky='w', padx=(5, 0), pady=(5,0))
        self.bfont_size = ttk.Spinbox(self.frameType, wrap=True, from_=1, to=50, textvariable=self.fosize)
        self.bfont_size.grid(row=8, column=1, sticky='we', pady=(5,5))
#====================================================================================================================================
        ttk.Label(self.frameType, text='Font Style:').grid(row=9, column=0, sticky='w', padx=(5, 0), pady=(5,0))
        optione = ['Times', 'Helvetica', 'Symbol', 'Vardana', 'Comic Sans MS']
        self.bfont_type = ttk.OptionMenu(self.frameType, self.fotype, optione[0], *optione, style = 'raised.TMenubutton')
        self.bfont_type.config(width=20)
        self.bfont_type.grid(row=10, column=1, sticky='we')
            
        ttk.Label(self.frameType, text='Canvas Size:').grid(row=11, column=0, sticky='w', padx=(5, 0), pady=(5,0))
        ttk.Label(self.frameType, text='Height:').grid(row=11, column=1, sticky='w', padx=(5, 0), pady=(5,0))
        self.bfont_size = ttk.Spinbox(self.frameType, wrap=True, from_=1, to=1000, textvariable=self.cheight)
        self.bfont_size.grid(row=12, column=1, sticky='we', pady=(5,5), padx=(5,5))
        ttk.Label(self.frameType, text='Width:').grid(row=13, column=1, sticky='w', padx=(5, 0), pady=(5,0))
        self.bfont_size = ttk.Spinbox(self.frameType ,wrap=True, from_=1, to=1000, textvariable=self.cwidth)
        self.bfont_size.grid(row=14, column=1, sticky='we', pady=(5,5), padx=(5,5))

        # Buttons
        self.frameButton0 = ttk.Frame(self.frameType)
        self.frameButton0.grid(row=0, column=2, sticky="nswe", padx=(0,5), pady=(5,5))
        self.frameButton0.grid_columnconfigure(0, weight=1)
        self.frameButton0.grid_columnconfigure(1, weight=1)

        self.frameButton1 = ttk.Frame(self.frameType)
        self.frameButton1.grid(row=1, column=2, sticky="nswe", padx=(0,5), pady=(5,5))
        self.frameButton1.grid_columnconfigure(0, weight=1)
        self.frameButton1.grid_columnconfigure(1, weight=1)
        self.frameButton2 = ttk.Frame(self.frameType)
        self.frameButton2.grid(row=2, column=2, sticky="nswe", padx=(0,5), pady=(5,5))
        self.frameButton2.grid_columnconfigure(0, weight=1)
        self.frameButton2.grid_columnconfigure(1, weight=1)
        self.frameButton3 = ttk.Frame(self.frameType)
        self.frameButton3.grid(row=3, column=2, sticky="nswe", padx=(0,5), pady=(5,5))
        self.frameButton3.grid_columnconfigure(0, weight=1)
        self.frameButton3.grid_columnconfigure(1, weight=1)

        self.btnSave = ttk.Button(self.frameButton0, text='Add Canvas', command=self.Somecanvas,width="35")
        self.btnSave.grid(row=0, column=1, pady=(0,0), padx=(2, 0), sticky="we")
        self.btnGenerat = ttk.Button(self.frameButton2, text='Add Text', command=self.someFunction,width="35")
        self.btnGenerat.grid(row=0, column=1, pady=(0,0), padx=(5, 0), sticky="we")
        self.btnGenerate = ttk.Button(self.frameButton1, text='Generate', command=self.generate,width="35")
        self.btnGenerate.grid(row=0, column=1, pady=(0,0), padx=(5, 0), sticky="we")
        self.btnSave = ttk.Button(self.frameButton3, text='Add Image', command=self.someimg,width="35")
        self.btnSave.grid(row=0, column=1, pady=(0,0), padx=(5, 0), sticky="we")
        
        global w
        self.ctwidth=w
        global h
        self.ctheight=h
        
        # Preview
        self.canvas = tk.Canvas(self.frameTopRight, width=self.ctwidth.get(), height=self.ctheight.get());
        self.canvas.configure(background='white')
        self.canvas.config(highlightbackground='#5f5f5f')
        self.vsb = ttk.Scrollbar(self.frameTopRight, orient="vertical", command=self.canvas.yview)
        self.hsb = ttk.Scrollbar(self.frameTopRight, orient="horizontal", command=self.canvas.xview)
        self.vsb.grid(row=1, column=1, sticky="nse")
        self.hsb.grid(row=2, column=0, sticky="sew")
        self.canvas.config(yscrollcommand=lambda f, l: self.autoscroll(self.vsb, f, l))
        self.canvas.config(xscrollcommand=lambda f, l:self.autoscroll(self.hsb, f, l))
        self.canvas.grid(row=1, column=0, sticky ="nswe", padx=(0,5), pady=(0,5))
        
        # Table
        self.frameTopLeft.rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(self.frameTopLeft, selectmode="extended",columns=("barcodes","type",
            "comment"),displaycolumns="barcodes type comment",height='7')
        self.tree.grid(row=8, column=0, sticky="ns", padx=(8,8), pady=(8,8))
        self.vsb1 = ttk.Scrollbar(self.frameTopLeft, orient="vertical", command=self.tree.yview)
        self.hsb1 = ttk.Scrollbar(self.frameTopLeft, orient="horizontal", command=self.tree.xview)
        self.vsb1.grid(row=8, column=1, sticky="nse")
        self.hsb1.grid(row=8, column=0, sticky="sew")
        self.tree.config(yscrollcommand=lambda f, l: self.autoscroll(self.vsb1, f, l))
        self.tree.config(xscrollcommand=lambda f, l:self.autoscroll(self.hsb1, f, l))
        self.tree.heading("#0", text="#")
        self.tree.heading("barcodes", text="Barcodes")
        self.tree.heading("type", text="Type")
        self.tree.heading("comment", text="Comment")

        self.tree.column("#0",minwidth=20, width=80, stretch=True, anchor="center")
        self.tree.column("barcodes",minwidth=50, width=100, stretch=True, anchor="center")
        self.tree.column("type",minwidth=40, width=100, stretch=True, anchor="center")
        self.tree.column("comment",minwidth=120, width=250, stretch=True, anchor="center")

        self.tree.tag_configure('even', background='#d9dde2')
        self.tree.bind('<Double-Button-1>', self.edit)
        master.bind("<Escape>", self.exit_ui);
        master.bind('<Control-s>', self.saveasfile)

        self.get_from_ini()
        self.read_file()
#############################################################-------IMAGE----################################################################################
   
    def Somecanvas(self):
        self.canvas = tk.Canvas(self.frameTopRight, width=self.cwidth.get(), height=self.cheight.get());
        self.canvas.configure(background='white')
        self.canvas.config(highlightbackground='grey')
        self.vsb = ttk.Scrollbar(self.frameTopRight, orient="vertical", command=self.canvas.yview)
        self.hsb = ttk.Scrollbar(self.frameTopRight, orient="horizontal", command=self.canvas.xview)
        self.vsb.grid(row=1, column=1, sticky="nse")
        self.hsb.grid(row=2, column=0, sticky="sew")
        self.canvas.config(yscrollcommand=lambda f, l: self.autoscroll(self.vsb, f, l))
        self.canvas.config(xscrollcommand=lambda f, l:self.autoscroll(self.hsb, f, l))
        self.canvas.grid(row=1, column=0, sticky ="nswe", padx=(0,5), pady=(0,5))

    def someimg(self):
        self.loc =self.dragged =0
        self.image=ImageTk.PhotoImage(self.select_image())
        #self.defaultcolor =self.canvas.itemcget (self.canvas.create_text (30, 25,font =("Helvetica", 14), text ="Item 1", tags ="DnD"), "fill")
        #self.canvas.create_text (175, 175,font =("Helvetica", 14), text ="Item 4", tags ="DnD")
        self.canvas.create_image(50, 50,image=self.image,anchor='nw',tags= "Dn")
        #self.canvas.pack (expand =1, fill =tk.BOTH)

        self.canvas.tag_bind ("DnD", "<ButtonPress-1>", self.down)
        self.canvas.tag_bind ("DnD", "<ButtonRelease-1>", self.chkup)
        self.canvas.tag_bind ("DnD", "<Enter>", self.enter)
        self.canvas.tag_bind ("DnD", "<Leave>", self.leave)
        self.canvas.tag_bind ("Dn", "<ButtonPress-1>", self.down1)
        self.canvas.tag_bind ("Dn", "<ButtonRelease-1>", self.chkup1)
        self.canvas.tag_bind ("Dn", "<Enter>", self.enter1)
        self.canvas.tag_bind ("Dn", "<Leave>", self.leave1)

    def select_image(self): 
        file_path = fdial.askopenfilename()
       
        return Image.open(file_path)
        

    def down (self, event):
    
        self.loc =1
        self.dragged =0
        event.widget.bind ("<Motion>", self.motion)

    def down1 (self, event):
        
        self.loc =1
        self.dragged =0
        event.widget.bind ("<Motion>", self.motion1)

    def motion (self, event):
        root.config (cursor ="exchange")
        cnv = event.widget
        cnv.itemconfigure (tk.CURRENT, fill ="blue")
        x,y = cnv.canvasx(event.x), cnv.canvasy(event.y)
        got = event.widget.coords (tk.CURRENT, x, y)

    def motion1 (self, event):
        root.config (cursor ="exchange")
        cnv = event.widget
        cnv.itemconfigure (tk.CURRENT)
        x,y = cnv.canvasx(event.x), cnv.canvasy(event.y)
        got = event.widget.coords (tk.CURRENT, x, y)
      
    def leave (self, event):
       self.loc =0
    def leave1(self, event):
      self.loc =0

    def enter (self, event):
        self.loc =1
        if self.dragged ==event.time:
          self.up (event)

    def enter1(self, event):
        self.loc =1
        if self.dragged ==event.time:
          self.up (event)

    def chkup (self, event):
        event.widget.unbind ("<Motion>")
        root.config (cursor ="")
        self.target =event.widget.find_withtag (tk.CURRENT)
        event.widget.itemconfigure (tk.CURRENT, fill =self.defaultcolor)
        if self.loc: # is button released in same widget as pressed?
          self.up (event)
        else:
         self.dragged =event.time
    def chkup1(self, event):
        event.widget.unbind ("<Motion>")
        root.config (cursor ="")
        self.target =event.widget.find_withtag (tk.CURRENT)
        event.widget.itemconfigure (tk.CURRENT)
        if self.loc: # is button released in same widget as pressed?
          self.up1(event)
        else:
          self.dragged =event.time

    def up (self, event):
      event.widget.unbind ("<Motion>")
      if (self.target !=event.widget.find_withtag (tk.CURRENT)):
      
        event.widget.itemconfigure (tk.CURRENT, fill ="blue")
        self.master.update()
        time.sleep (.1)
        print ("%s Drag-N-Dropped onto %s" \
        %(event.widget.itemcget (self.target, "text"),event.widget.itemcget (tk.CURRENT, "text")),event.widget.itemconfigure (tk.CURRENT, fill =self.defaultcolor))

    def up1(self, event):
        event.widget.unbind ("<Motion>")
        if (self.target !=event.widget.find_withtag (tk.CURRENT)):
         
          event.widget.itemconfigure (tk.CURRENT, fill ="blue")
          self.master.update()
          time.sleep (.1)
          print ("%s Drag-N-Dropped onto %s" \
            %(event.widget.itemcget (self.target, "image"),event.widget.itemcget (tk.CURRENT, "image")),event.widget.itemconfigure (tk.CURRENT,))

####################################################################################################################################################################
    def updatecomment(self, value=None):
        self.bcode_comment.delete(1.0, tk.END)
        if value:
            self.bcode_comment.insert(tk.END, value)

    def clearall(self):
        self.bcode_comment.delete(1.0, tk.END)
        self.bcode_val.delete(0, 'end')

    def edit(self, event):
        w = event.widget
        self.selected = w.focus()
        self.edited = True
        if self.selected:
            values = self.tree.set(self.selected)
            self.oldvalue = values['barcodes']
            self.bcvalue.set(values['barcodes'])
            self.updatecomment(values['comment'])
            self.bctype.set(values['type'])
            self.previewbarcode(values['barcodes'])
    def someFunction(self):
        #Example(root).pack(fill="both", expand=True)
        #my_gui = Example(self.master)
        self.loc =self.dragged =0
        # text items with the tag "editable" will inherit these bindings
        self.canvas.tag_bind("editable","<Double-Button-1>", self.set_focus)
        self.canvas.tag_bind("editable","<Button-1>", self.set_cursor)
        self.canvas.tag_bind("editable","<Key>", self.do_key)
        self.canvas.tag_bind("editable","<Home>", self.do_home)
        self.canvas.tag_bind("editable","<End>", self.do_end)
        
        self.canvas.tag_bind("editable","<BackSpace>", self.do_backspace)
        self.canvas.tag_bind("editable","<Return>", self.do_return)
        self.canvas.tag_bind ("editable", "<ButtonPress-1>", self.down)
        self.canvas.tag_bind ("editable", "<ButtonRelease-1>", self.chkup)
        self.canvas.tag_bind ("editable", "<Enter>", self.enter)
        self.canvas.tag_bind ("editable", "<Leave>", self.leave)
       
        # create some sample text
        self.defaultcolor =self.canvas.itemcget (self.canvas.create_text (80, 80,anchor="nw",font =(self.fotype.get(),self.fosize.get()),tags=("editable",) ,text="Textbox"), "fill")
        #self.canvas.create_text(80, 80, anchor="nw", tags=("editable",) ,text="Textbox")


        
    def mysaveasfile(self):
        #print (os.getcwd()) # REMINDER OF THE CURRENT SAVE LOCATION
        c = self.canvas
        box = (c.winfo_rootx(),c.winfo_rooty(),c.winfo_rootx()+c.winfo_width(),c.winfo_rooty() + c.winfo_height())
        
        #now = datetime.datetime.now()
        #k=(now.strftime("%d-%m-%Y %H:%M:%S"))
        

        self.update() # UPDATE THE CANVAS DISPLAY
        savename ='kanak'
        #'im_{0:0>6}'.format(20)
        
        ImageGrab.grab(bbox = box)
        img=ImageGrab.grab(bbox = box)
       
        f = fdial.asksaveasfile(filetypes=(("Portable Network Graphics (*.png)", "*.png"),("All Files (*.*)", "*.*")),mode='wb',defaultextension='.png')
        if f is None:
            return

        filename = f.name
        extension = filename.rsplit('.', 1)[-1]

        img.save(f, extension)
        f.close()
  
    def generate(self):
        if not self.bcvalue.get() or self.edited:
            self.clearall()
            if not self.GenerateCode():
                return False
        self.previewbarcode(self.bcode_val.get())
        self.edited = False


    def saveasfile(self, event=None):
        if self.bcode_val.get():
            if event:
                self.savebarcode(self.bcode_val.get())
            else:
                self.savebarcode(self.bcode_val.get(), True)
            self.updatetree()
        else:
            mbox.showwarning("Warning", "Generate any barcode first!");


    def generatebarcode(self, bcodevalue):
        tmpbarcode = upcean.oopfuncs.barcode(self.barcode_list[self.bctype.get()], self.bcode_val.get());
        tmpbarcode.size = self.bcode_size.get();
        tmpbarcode.barcolor = self.barcode_bar_color;
        tmpbarcode.textcolor = self.barcode_text_color;
        tmpbarcode.bgcolor = self.barcode_bg_color;
        tmpbarcode.filename = None;
        return tmpbarcode


    def previewbarcode(self, bcodevalue):
        tmpbarcode = self.generatebarcode(bcodevalue)
        validbc = tmpbarcode.validate_draw_barcode();
        if(validbc):
            image1 = ImageTk.PhotoImage(validbc);
            self.canvas.create_image(validbc.size[0]/2, validbc.size[1]/2, image=image1,anchor='nw',tags= "Dn");
            self.canvas.config(scrollregion=(0,0, validbc.size[0], validbc.size[1]));
            self.canvas.image = image1;
            self.already_exist(False, bcodevalue)

            self.loc =self.dragged =0
            self.canvas.tag_bind ("Dn", "<ButtonPress-1>", self.down1)
            self.canvas.tag_bind ("Dn", "<ButtonRelease-1>", self.chkup1)
            self.canvas.tag_bind ("Dn", "<Enter>", self.enter1)
            self.canvas.tag_bind ("Dn", "<Leave>", self.leave1)

        else:
            mbox.showerror("Error", "Barcode couldn't be generated!")


    def savebarcode(self, bcodevalue, autoname=False):
        savestate = False;
        fname = "";
        if autoname:
            fname = self.filedir+'/'+ bcodevalue + '.' + self.filetype.lower()
        else:
            fname = fdial.asksaveasfilename(defaultextension='png', parent=self.master, title='Saving barcode', filetypes=[('PNG','*.png'), ('JPEG','*.jpg *.jpeg'), ('GIF','*.gif'), ('Adobe PDF','*.pdf'), ('Barcha fayllar','*.*')]);
        if(fname):
            self.mysaveasfile()
            savestate = True;
            if(not savestate):
                mbox.showerror("Warning", "Barcode saving error");
            else:
                mbox.showinfo("Info", "Barcode saved as file successfully");


    def updatetree(self):
        bcitem = self.getvalues()
        if self.isunique(bcitem[0]):
            idd = self.last_id()+1
            self.tree.insert('', 'end', idd, text=idd, values = bcitem)
            self.tree.focus_set()
        else:
            if self.edited:
                if self.oldvalue == bcitem[0]:
                    self.tree.set(self.selected, 'comment', bcitem[2])
                    self.tree.selection_set(self.selected)
                else:
                    return self.already_exist()
            else:
                return self.already_exist()
        self.clearall()
        self.edited = False
        self.write_file()
        return True


    def already_exist(self, warn=True, bcode=None):
        if warn:
            mbox.showwarning("Warning", "Barcode is already in table!");
            return False
        else:
            if not self.isunique(bcode):
                self.updatecomment(self.existcomment)


    def last_id(self):
        if self.tree.get_children():
            idmax = max([int(i) for i in self.tree.get_children()])
        else:
            idmax = 0
        return idmax


    def getvalues(self):
        return self.bcvalue.get(), self.bctype.get(), self.bcode_comment.get(1.0, '1.end')


    def GenerateCode(self):
        if self.bctype.get() == 'EAN-13':
            if self.ean13start.isdigit() and len(self.ean13start)>12:
                newcode = int(self.ean13start[:12])
                nextcode = False
                while nextcode == False:
                    if self.validate_ean13(newcode):
                        if self.isunique(str(newcode) +str(self.validate_ean13(newcode))):
                            nextcode == True
                            break
                    newcode += 1
                self.bcvalue.set(str(newcode) +str(self.validate_ean13(newcode)))
                return True
            else:
                mbox.showwarning("Warning", "Enter initial value for EAN-13!");
                return False
        elif self.bctype.get() == 'EAN-8':
            if self.ean08start.isdigit() and len(self.ean08start)>7:
                newcode = int(self.ean08start[:7])
                nextcode = False
                while nextcode == False:
                    if self.validate_ean08(newcode):
                        if self.isunique(str(newcode) +str(self.validate_ean08(newcode))):
                            nextcode == True
                            break
                    newcode += 1
                self.bcvalue.set(str(newcode) +str(self.validate_ean08(newcode)))
                return True
            else:
                mbox.showwarning("Warning", "Enter initial value for EAN-08!");
                return False
        elif self.bctype.get() == 'EAN-5':
            if self.ean05start.isdigit() and len(self.ean05start)==5:
                newcode = int(self.ean05start)
                nextcode = False
                while nextcode == False:
                    if self.isunique(str(newcode)):
                        nextcode == True
                        break
                    newcode += 1
                self.bcvalue.set(str(newcode))
                return True
            else:
                mbox.showwarning("Warning", "Enter initial value for EAN-05!");
                return False


    ############################################################################
    ##                        GIU RELATED OPERATIONS                          ##
    ############################################################################

    def exit_ui(self, event):
        self.master.quit();

    def setscale(self, var):
        value = self.bcode_size.get()
        if int(value) != value:
            self.bcode_size.set(round(value))

    def settings(self):
        setwin = SettingWin(self.master)
        self.get_from_ini()

    def helpwin(self):
        setwin = HelpWin(self.master)

    def autoscroll(self, sbar, first, last):
        """Hide and show scrollbar as needed."""
        first, last = float(first), float(last)
        if first <= 0 and last >= 1:
            sbar.grid_remove()
        else:
            sbar.grid()
        sbar.set(first, last)

    def zebra(self):
        childs = self.tree.get_children()
        if childs:
            n=0
            for child in childs:
                n += 1
                if (n%2==0):
                    tag='even'
                else:
                    tag='odd'
                self.tree.item(child, tags=(tag,))

    ############################################################################
    ##                           FILE OPERATIONS                              ##
    ############################################################################

    # Initializing from config.ini file
    def get_from_ini(self):
        self.config = ConfigParser()
        if not os.path.isfile('config.ini'):
            self.check_inifile()
        self.config.read('config.ini')
        sect = 'DefaultValues'
        try:
            if self.config.get(sect, 'Type'):
                self.bctype.set(self.config.get(sect, 'Type'))
            if self.config.get(sect, 'Size'):
                self.bcsize.set(self.config.get(sect, 'Size'))
            if self.config.get(sect, 'EAN13start'):
                self.ean13start = self.config.get(sect, 'EAN13start')
            if self.config.get(sect, 'EAN08start'):
                self.ean08start = self.config.get(sect, 'EAN08start')
            if self.config.get(sect, 'EAN05start'):
                self.ean05start = self.config.get(sect, 'EAN05start')
            if self.config.get(sect, 'filedirectory'):
                self.filedir = self.config.get(sect, 'filedirectory')
            if self.config.get(sect, 'FileType'):
                self.filetype = self.config.get(sect, 'FileType')
        except:
            mbox.showerror("Warning", "Error occured while loading Config.ini!");


    # Checks and creates if ini file is not found
    def check_inifile(self):
        text = '[DefaultValues]\nType = EAN-13\nEAN13start = 4780000000010\nEAN08start = 47800010\nEAN05start = 00000\nSize = 2\nFileType = PDF\nFileDirectory ='
        file = open('config.ini', 'w')
        file.write(text)
        file.close()


    def write_file(self):
        if self.tree.get_children():
            with open('data.csv', 'w', encoding='utf-8') as file:
                fieldnames = ["id", "barcodes", "type","comment"]
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
                writer.writeheader()
                for item in self.tree.get_children():
                    mydata = self.tree.set(item)
                    mydata["id"] = item
                    writer.writerow(mydata)
            self.zebra()

    def read_file(self):
        if os.path.isfile('data.csv'):
            try:
                with open('data.csv', encoding="utf-8") as csvfile:
                    reader = csv.DictReader(csvfile, fieldnames = None, delimiter=";")
                    for row in reader:
                        self.tree.insert("", "end", row["id"], text=row["id"],
                            values=[row["barcodes"], row["type"], row["comment"]])
                self.zebra()
            except:
                mbox.showerror("Xatolik", "Error occured while loading Data.csv!");


    ############################################################################
    ##                          BARCODE VALIDATIONS                           ##
    ############################################################################

    def isunique(self, bcode):
        if os.path.isfile('data.csv'):
            with open('data.csv', encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile, fieldnames = None, delimiter=";")
                for row in reader:
                    if row["barcodes"] == bcode:
                        self.existcomment = row["comment"]
                        return False
                return True
        else:
            return True


    def validate_ean13(self, upc, return_check=False):
        upc = str(upc);
        if(len(upc)>13):
            fix_matches = re.findall("^(\d{13})", upc);
            upc = fix_matches[0];
        if(len(upc)>13 or len(upc)<12):
            return False;
        upc_matches = list(upc);
        upc_matches = [int(x) for x in upc_matches];
        upc_matches1 = upc_matches[0:][::2];
        upc_matches2 = upc_matches[1:][::2];
        EvenSum = (upc_matches2[0] + upc_matches2[1] + upc_matches2[2] + upc_matches2[3] + upc_matches2[4] + upc_matches2[5]) * 3;
        OddSum = upc_matches1[0] + upc_matches1[1] + upc_matches1[2] + upc_matches1[3] + upc_matches1[4] + upc_matches1[5];
        AllSum = OddSum + EvenSum;
        CheckSum = AllSum % 10;
        if(CheckSum>0):
            CheckSum = 10 - CheckSum;
        if(not return_check and len(upc)==13):
            if(CheckSum!=upc_matches1[6]):
                return False;
            if(CheckSum==upc_matches1[6]):
                return True;
        if(return_check):
            return str(CheckSum);
        if(len(upc)==12):
            return str(CheckSum);


    def validate_ean08(self, upc, return_check=False):
        upc = str(upc);
        if(len(upc)>8):
            fix_matches = re.findall("^(\d{8})", upc);
            upc = fix_matches[0];
        if(len(upc)>8 or len(upc)<7):
            return False;
        upc_matches = list(upc);
        upc_matches = [int(x) for x in upc_matches];
        upc_matches1 = upc_matches[0:][::2];
        upc_matches2 = upc_matches[1:][::2];
        EvenSum = (upc_matches1[0] + upc_matches1[1] + upc_matches1[2] + upc_matches1[3]) * 3;
        OddSum = upc_matches2[0] + upc_matches2[1] + upc_matches2[2];
        AllSum = OddSum + EvenSum;
        CheckSum = AllSum % 10;
        if(CheckSum>0):
            CheckSum = 10 - CheckSum;
        if(not return_check and len(upc)==8):
            if(CheckSum!=upc_matches2[3]):
                return False;
            if(CheckSum==upc_matches2[3]):
                return True;
        if(return_check):
            return str(CheckSum);
        if(len(upc)==7):
            return str(CheckSum);

##################################################################################################################################################################3
    def down (self, event):
        #print ("Click on %s" %event.widget.itemcget (tk.CURRENT, "text"))
        self.loc =1
        self.dragged =0
        event.widget.bind ("<Motion>", self.motion)

    def motion (self, event):
        root.config (cursor ="exchange")
        cnv = event.widget
        cnv.itemconfigure (tk.CURRENT, fill ="blue")
        x,y = cnv.canvasx(event.x), cnv.canvasy(event.y)
        got = event.widget.coords (tk.CURRENT, x, y)
  
    def leave (self, event):
     self.loc =0

    def enter (self, event):
        self.loc =1
        if self.dragged ==event.time:
          self.up (event)

    def chkup (self, event):
        event.widget.unbind ("<Motion>")
        root.config (cursor ="")
        self.target =event.widget.find_withtag (tk.CURRENT)
        event.widget.itemconfigure (tk.CURRENT, fill =self.defaultcolor)
        if self.loc: # is button released in same widget as pressed?
          self.up (event)
        else:
          self.dragged =event.time

    def up (self, event):
        event.widget.unbind ("<Motion>")
        if (self.target ==event.widget.find_withtag (tk.CURRENT)):
          print("")
          #print ("Select %s" %event.widget.itemcget (tk.CURRENT, "text"))
        else:
          event.widget.itemconfigure (tk.CURRENT, fill ="blue")
          self.master.update()
          time.sleep (.1)
          #print ("%s Drag-N-Dropped onto %s" \
          #%(event.widget.itemcget (self.target, "text"),event.widget.itemcget (tk.CURRENT, "text")),event.widget.itemconfigure (tk.CURRENT, fill =self.defaultcolor))

    #44444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444       
    def do_return(self,event):
        '''Handle the return key by turning off editing'''

        self.canvas.focus("")
        self.canvas.delete("highlight")
        self.canvas.select_clear()

    '''def do_left(self, event):
       

        item = self.canvas.focus()
        if item:
            new_index = self.canvas.index(item, "insert") - 1
            self.canvas.icursor(item, new_index)
            self.canvas.select_clear()

    def do_right(self, event):
       
        item = self.canvas.focus()
        if item:
            new_index = self.canvas.index(item, "insert") + 1
            self.canvas.icursor(item, new_index)
            self.canvas.select_clear()'''

    def do_backspace(self, event):
        '''Handle the backspace key'''

        item = self.canvas.focus()
        if item:
            selection = self.canvas.select_item()
            if selection:
                self.canvas.dchars(item, "sel.first", "sel.last")
                self.canvas.select_clear()
            else:
                insert = self.canvas.index(item, "insert")
                if insert > 0:
                    self.canvas.dchars(item, insert-1, insert)
            self.highlight(item)

    def do_home(self, event):
        '''Move text cursor to the start of the text item'''

        item = self.canvas.focus()
        if item:
            self.canvas.icursor(item, 0)
            self.canvas.select_clear()

    def do_end(self, event):
        '''Move text cursor to the end of the text item'''

        item = self.canvas.focus()
        if item:
            self.canvas.icursor(item, "end")
            self.canvas.select_clear()

    def do_key(self, event):
        '''Handle the insertion of characters'''

        item = self.canvas.focus()
        if item and event.char >= " ":
            insert = self.canvas.index(item, "insert")
            selection = self.canvas.select_item()
            if selection:
                self.canvas.dchars(item, "sel.first", "sel.last")
                self.canvas.select_clear()
            self.canvas.insert(item, "insert", event.char)
            self.highlight(item)

    def highlight(self, item):
        '''Highlight the given text item to show that it's editable'''

        items = self.canvas.find_withtag("highlight")
        if len(items) == 0:
            # no highlight box; create it
            id = self.canvas.create_rectangle((0,0,0,0), fill="white",outline="blue",
                                              dash=".", tag="highlight")
            self.canvas.lower(id, item)
        else:
            id = items[0]

        # resize the highlight
        bbox = self.canvas.bbox(item)
        rect_bbox = (bbox[0]-4, bbox[1]-4, bbox[2]+4, bbox[3]+4)
        self.canvas.coords(id, rect_bbox)

    def set_focus(self, event):
        '''Give focus to the text element under the cursor'''

        if self.canvas.type("current") == "text":
            self.canvas.focus_set()
            self.canvas.focus("current")
            self.canvas.select_from("current", 0)
            self.canvas.select_to("current", "end")
            self.highlight("current")

    def set_cursor(self, event):
        '''Move the insertion point'''

        item = self.canvas.focus()
        if item:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)

            self.canvas.icursor(item, "@%d,%d" % (x, y))
            self.canvas.select_clear()


########################################################################################################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
class SettingWin(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self)
        self.top = tk.Toplevel()
        self.top.resizable(False, False)
        self.top.geometry(set_size(self.top, 230, 330))
        self.top.title("Default settings")

        self.default_type = tk.StringVar()
        self.default_size = tk.IntVar()
        self.default_filetype = tk.StringVar()
        self.default_dir = tk.StringVar()
        self.ean13 = tk.StringVar()
        self.ean08 = tk.StringVar()
        self.ean05 = tk.StringVar()

        self.frameMain = ttk.Frame(self.top)
        self.frameMain.grid(row=0, column=0, sticky='nswe', padx=(10,0))
        self.bottom = ttk.Frame(self.top)
        self.bottom.grid(row=1, column=0, sticky='nswe', padx=(10,0))
        self.bottom.columnconfigure(0, weight=1)
        self.bottom.columnconfigure(1, weight=1)


        ttk.Label(self.frameMain, text='Barcode type: ').grid(row=0, column=0, sticky='w', pady=(5,0))
        options = ['EAN-13', 'EAN-8', 'EAN-5']
        self.dbctype = ttk.OptionMenu(self.frameMain, self.default_type, options[0], *options, style = 'raised.TMenubutton')
        self.dbctype.config(width=7)
        self.dbctype.grid(row=0, column=1, pady=(5,0), sticky='we')
        ttk.Label(self.frameMain, text="Barcode size: ").grid(row=1, column=0, sticky='w', pady=(5,0))
        self.dbcsize = tk.Spinbox(self.frameMain, wrap=True, width=5, from_=1, to=10, textvariable=self.default_size);
        self.dbcsize.grid(row=1, column=1, pady=(5,0), sticky='e')
        ttk.Label(self.frameMain, text="Default file type:").grid(row=2, column=0, sticky='w', pady=(5,0))
        filetypes = ['PDF', 'PNG', 'JPG', 'GIF']
        self.dcfiletype = ttk.OptionMenu(self.frameMain, self.default_filetype, filetypes[0], *filetypes)
        self.dcfiletype.config(width=7)
        self.dcfiletype.grid(row=2, column=1, sticky='we', pady=(5,0))
        ttk.Label(self.frameMain, text='EAN-13 initial value:').grid(row=3, column=0, columnspan=2, sticky='w', pady=(5,0))
        self.dean13 = ttk.Entry(self.frameMain, width=33, textvariable=self.ean13)
        self.dean13.grid(row=4, column=0, columnspan=2)
        ttk.Label(self.frameMain, text='EAN-08 initial value:').grid(row=5, column=0, columnspan=2, sticky='w', pady=(5,0))
        self.dean08 = ttk.Entry(self.frameMain, width=33, textvariable=self.ean08)
        self.dean08.grid(row=6, column=0, columnspan=2)
        ttk.Label(self.frameMain, text='EAN-05 initial value:').grid(row=7, column=0, columnspan=2, sticky='w', pady=(5,0))
        self.dean05 = ttk.Entry(self.frameMain, width=33, textvariable=self.ean05)
        self.dean05.grid(row=8, column=0, columnspan=2)

        self.framepdf = ttk.Frame(self.frameMain)
        self.framepdf.grid(row=9, column=0, columnspan=2)
        ttk.Label(self.framepdf, text='File saving directory:  ', font=("Arial", 9)).grid(row=0, column=0, sticky='w', pady=(5,0))
        self.dfiledir = ttk.Entry(self.framepdf, width=23, font=("Arial", 9), textvariable=self.default_dir)
        self.dfiledir.grid(row=1, column=0, padx=(3, 0), pady=(5,0))
        self.pdfbtn = ttk.Button(self.framepdf, text='...', width=3, command=self.folder)
        self.pdfbtn.grid(row=1, column=1, padx=(5, 0), pady=(5, 0))

        self.skpSave = ttk.Button(self.bottom, text='Save', command=self.save_list)
        self.skpSave.grid(row=0, column=0, sticky='we', padx=(0, 5), pady=(10, 3))
        self.btcancel = ttk.Button(self.bottom, text='Cancel', command=self.cancel)
        self.btcancel.grid(row=0, column=1, sticky='we', padx=(5, 0), pady=(10, 3))

        self.dbcsize.focus_set()

        self.top.bind('<Escape>', self.cancel)

        self.get_from_ini()

        self.top.grab_set()
        master.wait_window(self.top)

    def get_from_ini(self):
        self.partlist=[]
        self.config = ConfigParser()
        self.config.read('config.ini')
        sect = 'DefaultValues'
        self.default_type.set(self.config.get(sect, 'Type'))
        self.default_size.set(self.config.get(sect, 'Size'))
        self.default_filetype.set(self.config.get(sect, 'FileType'))
        self.default_dir.set(self.config.get(sect, 'FileDirectory'))
        self.ean13.set(self.config.get(sect, 'EAN13start'))
        self.ean08.set(self.config.get(sect, 'EAN08start'))
        self.ean05.set(self.config.get(sect, 'EAN05start'))

    def update_list(self):
        self.name.delete(0, 'end')
        self.code.delete(0, 'end')
        self.address.delete(0, 'end')
        self.dockname.delete(0, 'end')
        self.pdfaddress.delete(0, 'end')
        self.name.insert(0, self.compname.get())
        self.code.insert(0, self.compcode.get())
        self.address.insert(0, self.compaddress.get())
        self.dockname.insert(0, self.dock.get())
        self.pdfaddress.insert(0, self.pdfdir.get())

    def folder(self):
        dirpath = fdial.askdirectory(mustexist=False,
                                     parent=self.master, title='Choose the folder')
        if dirpath:
            self.default_dir.set(dirpath)


    def save_list(self):
        sect = 'DefaultValues'
        self.config.set(sect,'Type', self.default_type.get())
        self.config.set(sect, 'Size', self.dbcsize.get())
        self.config.set(sect, 'FileType', self.default_filetype.get())
        self.config.set(sect, 'FileDirectory', self.default_dir.get())
        self.config.set(sect, 'EAN13start', self.ean13.get())
        self.config.set(sect, 'EAN08start', self.ean08.get())
        self.config.set(sect, 'EAN05start', self.ean05.get())
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        self.top.destroy()

    def cancel(self, event=None):
        self.top.destroy()


class HelpWin(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self)
        self.top = tk.Toplevel()
        self.top.resizable(False, False)
        self.top.geometry(set_size(self.top, 200, 150))
        self.top.title("Info")


        self.top.grab_set()
        master.wait_window(self.top)



def set_size(win, w=0, h=0, absolute=True, win_ratio=None):
    winw = win.winfo_screenwidth()
    winh = win.winfo_screenheight()
    if not absolute:
        w = int(winw * win_ratio)
        h = int(winh * win_ratio)
        screen = "{0}x{1}+{2}+{3}".format(w, h, str(int(winw*0.1)), str(int(winh*0.05)))
    else:
        screen = "{0}x{1}+{2}+{3}".format(w, h, str(int((winw-w)/2)), str(int((winh-h)/2)))
    return screen


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path).replace("\\","/")


app = MainWin1(root)
try:
    root.iconbitmap(default=resource_path('app.ico'))
except:
    pass

root.mainloop()
