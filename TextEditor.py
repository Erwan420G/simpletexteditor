from tkinter import *
from tkinter.messagebox import *
import tkinter.filedialog as tkfile

class App:
	def __init__(self, master):
		self.master = master
		master.title('Text Editor')
		self.menuBar = Menu(root, tearoff=0)
		master.config(menu=self.menuBar)

		self.filetype = [('All files', '.*'), ('Text files', '.txt')]
		self.filetype_save = [('Text files', '.txt'), ('All files', '.*')]
		self.info = ''
		self.fileOpenedOnce = False
		self.isSaved = False
		self.filePath, self.fileName = '', ''

		self._createWidgets()

	def _createWidgets(self):
		self.fileMenu = Menu(self.menuBar, tearoff=0)
		self.menuBar.add_cascade(label="Fichier", menu=self.fileMenu)

		self.fileMenu.add_command(label='Nouveau', command=self.askSave)
		self.fileMenu.add_command(label='Ouvrir...', command=self.open)
		self.fileMenu.add_command(label='Enregistrer', command=self.save)
		self.fileMenu.add_command(label='Enregistrer sous...', command=self.saveAs)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label='Quitter', command=quit)

		self.textBox = Text(self.master, bg='white', bd='2', width='100', height='25', relief='flat')
		self.textBox.pack()

	def quit(self):
		if self.textBox.get("1.0", "end-1c") != '':
			self.askSave()

		root.destroy()

	def askSave(self):
		choice = tkfile.messagebox.askyesnocancel("Enregistrer les modifications", "Souhaitez-vous enregistrer les modifications de ce fichier ?")
		if choice == True:
			self.save()

	def getFileInfo(self, info):
		split = info.count('/')

		if info != '':
			self.fileOpenedOnce = True
		else:
			self.fileOpenedOnce = False

		infos = info.split('/', split)

		for i in range(0, split+1):
			if i != split:
				self.filePath += infos[i] + '\\'
			else:
				self.filePath += infos[i]

		self.fileName = infos[split]

	def checkSaveState(self):
		file = open(self.filePath)
		if file.read() == self.textBox.get("1.0", "end-1c"):
			return True
		else:
			return False

	def new(self):
		if self.textBox.get("1.0", "end-1c") != '':
			self.askSave()

	def open(self):
		if self.textBox.get("1.0", "end-1c") != '':
			self.askSave()

		self.info = tkfile.askopenfilename(initialdir='/', title="Select file", filetypes=self.filetype)
		self.getFileInfo(self.info)

		with open(self.filePath, 'r') as file:
			try:
				data = file.read()
				self.textBox.insert(END, data)
				self.isSaved = False
			except FileNotFoundError:
				tkfile.messagebox.showerror("Erreur", "Fichier non spécifié")
			except UnicodeDecodeError:
				tkfile.messagebox.showerror("Erreur", "Ce format de fichier n'est pas pris en compte")


	def saveAs(self):
		if self.textBox.get("1.0", "end-1c") != '':
			self.savePath = tkfile.asksaveasfilename(initialdir='/', title="Select location to save", filetypes=self.filetype_save)
			try:
				file = open(self.savePath, 'w')
				file.write(self.textBox.get("1.0", END))
				file.close()
				self.isSaved = True
			except FileNotFoundError:
				tkfile.messagebox.showerror("Erreur", "Emplacement non spécifié")
		else:
			pass

	def save(self):
		if self.textBox.get("1.0", "end-1c") != '':
			if self.isSaved == True:
				file = open(self.filePath, 'w')
				file.write(self.textBox.get("1.0", END))
				file.close()
			else:
				self.saveAs()
		else:
			pass

root = Tk()
main = App(root)
root.protocol("WM_DELETE_WINDOW", main.quit)
if main.filePath != '':
	main.isSaved = main.checkSaveState()
root.mainloop()
