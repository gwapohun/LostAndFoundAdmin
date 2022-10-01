#version.regex
#__version__='1.0'
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivymd.uix.filemanager import MDFileManager
from kivy.clock import Clock
from kivy.uix.button import Button
from kivymd.uix.snackbar import Snackbar

from kivy.core.window import Window
from kivy.utils import get_color_from_hex as ghex
from kivy.metrics import dp

from json import load , dump
from plyer import storagepath
from os.path import isfile , basename , exists , join
from network import send_files

# ==== My Button 
class SelectPicture(Button) :
	pass
class DeletePicture(Button) :
	pass
# ==== My Box Layout
class FileID(BoxLayout):
	pass
class ItemInformation(BoxLayout):
	pass
class ItemPicture(BoxLayout):
	pass
# ==== Pop Up
class MyPopUp(ModalView) :
	def configure(self , title : str , text : str ) :
		self.ids["title"].text = title
		self.ids["text"].text = text
		
# ==== Connect Ip
class ConnectToServer(ModalView) :
	pass

# ===== My Function
def errorMessage( msg : str ) :
	Snackbar(
		text = f"[color=ffffff]{msg}" ,
		snackbar_x = "10dp" ,
		snackbar_y = "10dp" ,
		bg_color = ghex("d10000"),
		size_hint_x = (Window.width - (dp(10) * 2)) / Window.width 
		).open()

def sendSuccess(msg : str) :
	Snackbar(
		text = f"[color=00000]{msg}" ,
		snackbar_x = "10dp" ,
		snackbar_y = "10dp" ,
		bg_color = ghex("98ff98"),
		size_hint_x = (Window.width - (dp(10) * 2)) / Window.width 
		).open()


# ===== Main Widget Of The App
class MainWidget(BoxLayout) :
	path : str = storagepath.get_external_storage_dir()
	pictures_ext : tuple = ("jpeg" , "png" , "jpg" )
	app_data : dict = { "data name" : "Lost And Found.json" , "user" : "new" }
	icon_clicked = [ "old" , "old" ]
	
	def __init__(self , **kwargs) :
		super(MainWidget , self).__init__(**kwargs)
		self.makeAppData()
		self.file_manager : MDFileManager = MDFileManager(
			exit_manager=self.exit_manager,  # function called when the user reaches directory tree root
			select_path=self.select_path,  # function called when selecting a file/directory
			preview = True ,
			selector = "file"
			)
		self.connectTo : ModalView = ConnectToServer()	
		
		Clock.schedule_interval(self.isOutFromRoot , 1 / 60)
		
	
	# --------- Introducing Widget
	def makeAppData(self ) :
		file = join(self.path , self.app_data["data name"])
		if not exists( file ) :
			with open( file , "w") as f :
				dump(self.app_data , f)
				self.icon_clicked = [ "new" , "new" ]
		else :
			with open( file , "r") as f :
				self.app_data = load(f)
				if self.app_data["user"] == "new" :
					self.icon_clicked = [ "new" , "new" ]
		
	def saveData(self) :
		file = join(self.path , self.app_data["data name"])
		with open(file , "w") as f :
			dump( self.app_data , f )
	
	# --------- Sending Data
	def sendTheData(self ) :
		if self.icon_clicked[0] == "new" :
			intro = MyPopUp()
			intro.configure(
				"Send Item Information " , 
				"\n[i]This button use to send the item information to the server \n\nThe requirement must be completed to successfully send the item information to the server [/i]"
				)
			intro.open()
			self.icon_clicked[0] = "old"
		else :
			self.readyToSendTheItem()
			
		if self.icon_clicked[0] == "old" and self.icon_clicked[1] == "old" :
			self.app_data["user"] = "old"
	
	def readyToSendTheItem(self) :
		ready2send : tuple =  (
			( self.ids["item_pic"].source != "" and len(self.ids["item_info"].text) != 0 ) , 
			len(self.ids["file_id"].text) != 0 ,
			len(self.connectTo.ids["ip"].text) != 0 ,
			len(self.connectTo.ids["port"].text) != 0 ,
			self.connectTo.ids["port"].text.isdigit()
		)
		if not ready2send[0] :
			errorMessage(" ! No Picture And Information About The Item")
		elif not ready2send[1] :
			errorMessage(" ! Empty File Name ")
		elif not ready2send[2] :
			errorMessage(" ! Empty IP Address ")
		elif not ready2send[3] :
			errorMessage(" ! Empty IP Port ")
		elif not ready2send[4] :
			errorMessage(" ! IP Port Is Not A Digit ")
		else :
			picData = b""
			picName = ""
			if self.ids["item_pic"].source != "" :
				picName = basename(self.ids["item_pic"].source)
				with open( self.ids["item_pic"].source , "rb" ) as f :
					picData = f.read()
					
			data : dict = {
				"admin" : True ,
				"file id" : self.ids["file_id"].text ,
				"item info" : self.ids["item_info"].text ,
				"item pic" : picData ,
				"item pic filename" : picName	# Added For Showwing Image
				}
			ip : str = self.connectTo.ids["ip"].text
			port : int = int(self.connectTo.ids["port"].text)
			if send_files( data , ip , port ) :
				sendSuccess("√ Send Success")
				self.restartData()
			else :
				errorMessage(f" ! Cannot Send In This IP ( {ip} , {port} ) ")
			
	def restartData(self):
		self.ids["item_pic"].source = ""
		self.ids["file_id"].text = ""
		self.ids["item_info"].text = ""
		
	# --------- Connect Server
	def connectToServer( self , *args  ) :
		if self.icon_clicked[1] == "new" :
			intro = MyPopUp()
			intro.configure(
				"SERVER IP address and port" , 
				"\n[i]This button use to specify the address and port of the server [/i]\n\n[b]Example :[/b] \n\n IP Addr : 0.tcp.ap.ngrok.io \n IP Port : 11201"
				)
			intro.open()
			self.icon_clicked[1] = "old"
		else :
			self.connectTo.open()
		if self.icon_clicked[0] == "old" and self.icon_clicked[1] == "old" :
			self.app_data["user"] = "old"
	
	# --------- Selecting Image
	def removeImage(self) :
		if self.ids["item_pic"].source :
		 	self.ids["item_pic"].source = ""
		
	def selectImage(self) :
		self.file_manager.show(self.path)
	
	def isOutFromRoot(self , *args ) :
		if not self.file_manager.current_path.startswith(self.path) :
			self.file_manager.close()
	
	def select_path(self , path) :
		print("Path : ", path)
		if isfile(path) :
			for ext in self.pictures_ext :
				if path.endswith(ext) :
					self.ids["item_pic"].source = path
					self.exit_manager()
	
	def exit_manager(self , *args) :
		print("Exit : ", *args)
		self.file_manager.close()
	
	

class LostAndFoundApp(MDApp) :
	
	def on_stop(self) :
		self.root.saveData()
	
LostAndFoundApp().run()
