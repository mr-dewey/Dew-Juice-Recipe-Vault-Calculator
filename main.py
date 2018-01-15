# Python 2.7
# Author: Will Rooney
# January 14th, 2018

from Recipes import Recipe
from time import sleep
import json
import Tkinter
import tkMessageBox
import os

class ejuice_app_tk(Tkinter.Tk):
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.recipeVault = []
		self.initialize()

	def initialize(self):
		self.grid()

		# Search Entry
		self.entrySearchVariable = Tkinter.StringVar()
		self.entrySearch = Tkinter.Entry(self,textvariable=self.entrySearchVariable)
		self.entrySearch.grid(column=0,row=0,columnspan=9,sticky='EW')
		self.entrySearch.bind("<Button-1>", self.OnEntrySearchClick)
		self.entrySearch.bind("<KeyRelease>", self.OnSearch)
		self.entrySearchVariable.set(u"Search for a recipe.")

		# *** Recipe Data *** #

		# Name Entry
		self.recipeNameLabelVariable = Tkinter.StringVar()
		recipeLabel = Tkinter.Label(self,textvariable=self.recipeNameLabelVariable,anchor="w")
		recipeLabel.grid(column=2,row=1,columnspan=6,sticky='EW')
		self.recipeNameLabelVariable.set(u"Recipe Name:")

		self.entryRecipeNameVariable = Tkinter.StringVar()
		self.entryRecipeName = Tkinter.Entry(self,textvariable=self.entryRecipeNameVariable)
		self.entryRecipeName.grid(column=2,row=2,columnspan=6,sticky='EW')
		self.entryRecipeNameVariable.set(u"Recipe Name")

		# Batch ml Entry
		self.batchLabelVariable = Tkinter.StringVar()
		batchLabel = Tkinter.Label(self,textvariable=self.batchLabelVariable,anchor="w")
		batchLabel.grid(column=8,row=1,sticky='EW')
		self.batchLabelVariable.set(u"Batch ml:")

		self.entryBatchVariable = Tkinter.StringVar()
		self.entryBatch = Tkinter.Entry(self,textvariable=self.entryBatchVariable)
		self.entryBatch.grid(column=8,row=2,sticky='EW')
		self.entryBatch.bind("<KeyRelease>", self.calculateBatch)
		self.entryBatchVariable.set(u"30")

		# Description Entry
		self.DescriptionLabelVariable = Tkinter.StringVar()
		DescriptionLabel = Tkinter.Label(self,textvariable=self.DescriptionLabelVariable,anchor="w")
		DescriptionLabel.grid(column=2,row=3,columnspan=7,sticky='EW')
		self.DescriptionLabelVariable.set(u"Description:")

		self.entryDescriptionVariable = Tkinter.StringVar()
		self.entryDescription = Tkinter.Entry(self,textvariable=self.entryDescriptionVariable)
		self.entryDescription.grid(column=2,row=4,columnspan=7,sticky='EW')
		self.entryDescriptionVariable.set(u"Recipe Description")

		# PG Entry
		self.PGLabelVariable = Tkinter.StringVar()
		PGLabel = Tkinter.Label(self,textvariable=self.PGLabelVariable,anchor="w")
		PGLabel.grid(column=2,row=5,sticky='EW')
		self.PGLabelVariable.set(u"PG %:")

		self.entryPGVariable = Tkinter.StringVar()
		self.entryPG = Tkinter.Entry(self,textvariable=self.entryPGVariable)
		self.entryPG.grid(column=2,row=6,sticky='EW')
		self.entryPG.bind("<KeyRelease>", self.onPGModified)
		self.entryPGVariable.set(u"30")

		# PG ml
		self.PG_ml_LabelVariable = Tkinter.StringVar()
		PG_ml_Label = Tkinter.Label(self,textvariable=self.PG_ml_LabelVariable,anchor="w")
		PG_ml_Label.grid(column=3,row=5,sticky='EW')
		self.PG_ml_LabelVariable.set(u"PG ml:")

		self.PG_ml_Variable = Tkinter.StringVar()
		PG_ml = Tkinter.Label(self,textvariable=self.PG_ml_Variable,anchor="w",fg="white",bg="blue")
		PG_ml.grid(column=3,row=6,sticky='EW')
		self.PG_ml_Variable.set(u"0.0")


		# VG Entry
		self.VGLabelVariable = Tkinter.StringVar()
		VGLabel = Tkinter.Label(self,textvariable=self.VGLabelVariable,anchor="w")
		VGLabel.grid(column=4,row=5,sticky='EW')
		self.VGLabelVariable.set(u"VG %:")

		self.entryVGVariable = Tkinter.StringVar()
		self.entryVG = Tkinter.Entry(self,textvariable=self.entryVGVariable)
		self.entryVG.grid(column=4,row=6,sticky='EW')
		self.entryVG.bind("<KeyRelease>", self.onVGModified)
		self.entryVGVariable.set(u"70")

		# VG ml
		self.VG_ml_LabelVariable = Tkinter.StringVar()
		VG_ml_Label = Tkinter.Label(self,textvariable=self.VG_ml_LabelVariable,anchor="w")
		VG_ml_Label.grid(column=5,row=5,sticky='EW')
		self.VG_ml_LabelVariable.set(u"VG ml:")

		self.VG_ml_Variable = Tkinter.StringVar()
		VG_ml = Tkinter.Label(self,textvariable=self.VG_ml_Variable,anchor="w",fg="white",bg="blue")
		VG_ml.grid(column=5,row=6,sticky='EW')
		self.VG_ml_Variable.set(u"0.0")

		# NIC Entry
		self.NICLabelVariable = Tkinter.StringVar()
		NICLabel = Tkinter.Label(self,textvariable=self.NICLabelVariable,anchor="w")
		NICLabel.grid(column=6,row=5,sticky='EW')
		self.NICLabelVariable.set(u"NIC (mg):")

		self.entryNICVariable = Tkinter.StringVar()
		self.entryNIC = Tkinter.Entry(self,textvariable=self.entryNICVariable)
		self.entryNIC.grid(column=6,row=6,sticky='EW')
		self.entryNIC.bind("<KeyRelease>", self.calculateBatch)
		self.entryNICVariable.set(u"0")

		# NIC Concentration - Assume PG base
		self.NICConcLabelVariable = Tkinter.StringVar()
		NICConcLabel = Tkinter.Label(self, textvariable=self.NICConcLabelVariable,anchor="w")
		NICConcLabel.grid(column=7,row=5,sticky='EW')
		self.NICConcLabelVariable.set(u"NIC Src (mg/ml)")

		self.entryNICConcVariable = Tkinter.StringVar()
		self.entryNICConc = Tkinter.Entry(self,textvariable=self.entryNICConcVariable)
		self.entryNICConc.grid(column=7,row=6,sticky='EW')
		self.entryNICConc.bind("<KeyRelease>", self.calculateBatch)
		self.entryNICConcVariable.set(u"36")

		# NIC ml
		self.NIC_ml_LabelVariable = Tkinter.StringVar()
		NIC_ml_Label = Tkinter.Label(self,textvariable=self.NIC_ml_LabelVariable,anchor="w")
		NIC_ml_Label.grid(column=8,row=5,sticky='EW')
		self.NIC_ml_LabelVariable.set(u"NIC ml:")

		self.NIC_ml_Variable = Tkinter.StringVar()
		NIC_ml = Tkinter.Label(self,textvariable=self.NIC_ml_Variable,anchor="w",fg="white",bg="blue")
		NIC_ml.grid(column=8,row=6,sticky='EW')
		self.NIC_ml_Variable.set(u"0.0")


		# Recipe List
		self.listbox_row_span=10
		self.yScroll = Tkinter.Scrollbar(self, orient=Tkinter.VERTICAL)
		self.yScroll.grid(row=1, column=1,rowspan=self.listbox_row_span, sticky=Tkinter.N+Tkinter.S)
		self.xScroll = Tkinter.Scrollbar(self, orient=Tkinter.HORIZONTAL)
		self.xScroll.grid(row=10, column=0, stick=Tkinter.E+Tkinter.W)
		self.listbox = Tkinter.Listbox(self,
			xscrollcommand=self.xScroll.set,
			yscrollcommand=self.yScroll.set)
		self.listbox.grid(row=1, column=0, rowspan=self.listbox_row_span-1, sticky=Tkinter.N+Tkinter.S+Tkinter.E+Tkinter.W)
		self.xScroll['command'] = self.listbox.xview
		self.yScroll['command'] = self.listbox.yview
		self.listbox.bind('<<ListboxSelect>>', self.onRecipeSelect)

		# Dynamic Flavor Data
		self.workingFlavors = []

		self.flavorRow = self.listbox_row_span

		flavorNameVariable = Tkinter.StringVar()
		flavorNameLabel = Tkinter.Label(self,textvariable=flavorNameVariable,anchor="w")
		flavorNameLabel.grid(column=2,row=7, columnspan=5, sticky='EW')
		flavorNameVariable.set(u"Flavor Name:")

		flavorStrengthVariable = Tkinter.StringVar()
		flavorStrengthLabel = Tkinter.Label(self,textvariable=flavorStrengthVariable,anchor="w")
		flavorStrengthLabel.grid(column=7,row=7,sticky='EW')
		flavorStrengthVariable.set(u"Flavor Srength %:")

		# Flavor ml
		self.flavor_ml_LabelVariable = Tkinter.StringVar()
		flavor_ml_Label = Tkinter.Label(self,textvariable=self.flavor_ml_LabelVariable,anchor="w")
		flavor_ml_Label.grid(column=8,row=7,sticky='EW')
		self.flavor_ml_LabelVariable.set(u"Flavor ml:")

		# Add Flavor Button
		self.addFlavorButton = Tkinter.Button(self, text=u"Add Flavor", command=self.OnAddFlavorButtonClick)
		self.addFlavorButton.grid(column=2,row=8,columnspan=6,sticky='EW')

		# Delete Flavor Button
		self.deleteFlavorButton = Tkinter.Button(self, text=u"Delete Flavor", command=self.OnDeleteFlavorButtonClick)
		self.deleteFlavorButton.grid(column=8,row=8,sticky='EW')

		# Seperator 1
		blankLabel_1_Variable = Tkinter.StringVar()
		self.blankLabel_1 = Tkinter.Label(self,textvariable=blankLabel_1_Variable,anchor="w",bg="grey")
		self.blankLabel_1.grid(column=2,row=9, columnspan=7, sticky='EW')

		# Save or Add Flavor
		self.saveButton = Tkinter.Button(self, text=u"Update or Add Recipe", command=self.OnsaveButtonClick)
		self.saveButton.grid(column=2,row=10,columnspan=6,sticky='EW')

		# Delete Selected Flavor
		self.deleteButton = Tkinter.Button(self, text=u"Delete Recipe", command= self.OnDeleteButtonClick)
		self.deleteButton.grid(column=8,row=10,sticky='EW')

		# Seperator 2
		blankLabel_2_Variable = Tkinter.StringVar()
		self.blankLabel_2 = Tkinter.Label(self,textvariable=blankLabel_2_Variable,anchor="w",bg="grey")
		self.blankLabel_2.grid(column=0,row=11, columnspan=9, sticky='EW')

		self.loadRecipes()

		self.grid_columnconfigure(0,weight=1)
		self.resizable(True,True)
		self.update()
		self.minsize(600,400)
		self.geometry(self.geometry())
		self.entrySearch.focus_set()
		self.entrySearch.selection_range(0, Tkinter.END)

	def onRecipeSelect(self, event):
		self.resetFlavors()
		w = event.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		for recipe in self.recipeVault:
			if recipe.name.lower() == value.lower():
				self.entryRecipeNameVariable.set(recipe.name)
				self.entryDescriptionVariable.set(recipe.desc)
				self.entryPGVariable.set(recipe.PG)
				self.entryVGVariable.set(recipe.VG)
				self.entryNICVariable.set(recipe.NIC)
				self.flavorRow = self.listbox_row_span
				for flavor in recipe.flavors:
					self.addFlavor(flavor['Name'],flavor['Strength'])
				self.calculateBatch(None)
				break

	def OnAddFlavorButtonClick(self):		
		# add new flavor entry
		self.addFlavor(name='Flavor ' + str(self.flavorRow-self.listbox_row_span), strength = '0')

	def OnDeleteFlavorButtonClick(self):		
		# add new flavor entry
		if len(self.workingFlavors) > 0:
			self.workingFlavors[-1][1].destroy()
			self.workingFlavors[-1][3].destroy()
			self.workingFlavors[-1][5].destroy()
			self.workingFlavors.pop()
			self.flavorRow -= 1
			# TO-DO: repetitive - need to wrap into function and add flexibility for futur additions
			self.addFlavorButton.grid(column=2,row=self.flavorRow-1,columnspan=6,sticky='EW')
			self.deleteFlavorButton.grid(column=8,row=self.flavorRow-1,sticky='EW')
			self.blankLabel_1.grid(column=2,row=self.flavorRow, columnspan=7, sticky='EW')
			self.saveButton.grid(column=2,row=self.flavorRow+1,columnspan=6,sticky='EW')
			self.deleteButton.grid(column=8,row=self.flavorRow+1,sticky='EW')
			self.blankLabel_2.grid(column=0,row=self.flavorRow+2, columnspan=9, sticky='EW')
			self.listbox.grid(row=1, column=0, rowspan=self.flavorRow, sticky=Tkinter.N+Tkinter.S+Tkinter.E+Tkinter.W)
			self.yScroll.grid(row=1, column=1,rowspan=self.flavorRow+1, sticky=Tkinter.N+Tkinter.S)
			self.xScroll.grid(row=self.flavorRow+1, column=0, stick=Tkinter.E+Tkinter.W)

	def addFlavor(self, name, strength):
		self.flavorRow += 1

		# TO-DO: repetitive - need to wrap into function and add flexibility for futur additions
		self.addFlavorButton.grid(column=2,row=self.flavorRow-1,columnspan=6,sticky='EW')
		self.deleteFlavorButton.grid(column=8,row=self.flavorRow-1,sticky='EW')
		self.blankLabel_1.grid(column=2,row=self.flavorRow, columnspan=7, sticky='EW')
		self.saveButton.grid(column=2,row=self.flavorRow+1,columnspan=6,sticky='EW')
		self.deleteButton.grid(column=8,row=self.flavorRow+1,sticky='EW')
		self.blankLabel_2.grid(column=0,row=self.flavorRow+2, columnspan=9, sticky='EW')
		self.listbox.grid(row=1, column=0, rowspan=self.flavorRow, sticky=Tkinter.N+Tkinter.S+Tkinter.E+Tkinter.W)
		self.yScroll.grid(row=1, column=1,rowspan=self.flavorRow+1, sticky=Tkinter.N+Tkinter.S)
		self.xScroll.grid(row=self.flavorRow+1, column=0, stick=Tkinter.E+Tkinter.W)

		# New flavor elements
		entryFlavorNameVariable = Tkinter.StringVar()
		entryFlavorName = Tkinter.Entry(self,textvariable=entryFlavorNameVariable)
		entryFlavorName.grid(column=2,row=self.flavorRow-2, columnspan=5, sticky='EW')
		entryFlavorNameVariable.set(name)

		entryFlavorStrengthVariable = Tkinter.StringVar()
		entryFlavorStrength = Tkinter.Entry(self,textvariable=entryFlavorStrengthVariable)
		entryFlavorStrength.grid(column=7,row=self.flavorRow-2,sticky='EW')
		entryFlavorStrength.bind("<KeyRelease>", self.calculateBatch)
		entryFlavorStrengthVariable.set(strength)

		# calculated ml
		ml_Variable = Tkinter.StringVar()
		ml = Tkinter.Label(self,textvariable=ml_Variable,anchor="w",fg="white",bg="blue")
		ml.grid(column=8,row=self.flavorRow-2,sticky='EW')
		ml_Variable.set(u"0.0")

		self.workingFlavors.append([entryFlavorNameVariable, entryFlavorName,  entryFlavorStrengthVariable, entryFlavorStrength, ml_Variable, ml])

	def resetFlavors(self):
		for item in self.workingFlavors:
			item[1].destroy()
			item[3].destroy()
			item[5].destroy()
		self.workingFlavors = []

	def OnsaveButtonClick(self):
		recipeName = self.entryRecipeNameVariable.get()
		temp_list = list(self.listbox.get(0, Tkinter.END))
		for recipe in self.recipeVault:
			if recipeName.lower() == recipe.name.lower():
				# update recipe
				recipe.VG = self.entryVGVariable.get()
				recipe.PG = self.entryPGVariable.get()
				recipe.NIC = self.entryNICVariable.get()
				recipe.desc = self.entryDescriptionVariable.get()
				recipe.flavors = []
				for flavor in self.workingFlavors:
					recipe.addFlavor(flavor[0].get(), flavor[2].get())
				self.saveVault()
				return
		# New recipe
		self.recipeVault.append(Recipe(
			recipeName,
			None, # TO-DO - Flavors
			self.entryVGVariable.get(),
			self.entryPGVariable.get(),
			self.entryNICVariable.get(),
			self.entryDescriptionVariable.get()))
		for flavor in self.workingFlavors:
			self.recipeVault[-1].addFlavor(flavor[0].get(), flavor[2].get())
		self.update_list()
		self.saveVault()

	def OnDeleteButtonClick(self):
		recipeName = self.entryRecipeNameVariable.get()
		result = tkMessageBox.askquestion("Delete Recipe '" + recipeName + "'", "Are You Sure?", icon='warning')
		if result == 'yes':
			to_remove = [i for i, recipe in enumerate(self.recipeVault) if recipeName.lower() == recipe.name.lower() ]
			for index in reversed(to_remove):
				del self.recipeVault[index]
				self.update_list()
				self.saveVault()
				print recipeName,'successfully deleted'
		else:
			print 'Delete Recipe - Canceled'

	def OnSearch(self, event):
		term = self.entrySearchVariable.get().lower()
		#print 'Term:',term
		self.listbox.delete(0, Tkinter.END)
		temp_list = []
		for recipe in self.recipeVault:
			if term in recipe.name.lower():
				temp_list.append(recipe.name)
		temp_list.sort()
		for item in temp_list:
			self.listbox.insert(Tkinter.END, item)

	def OnEntrySearchClick(self, event):
		print 'Search Clicked'
		self.entrySearch.focus_set()
		self.entrySearch.select_range(0, Tkinter.END)
		return 'break'

	def onPGModified(self, event):
		if (self.entryPGVariable.get()):
			pg_perc = int(float(self.entryPGVariable.get()))
		else: pg_perc = 0
		vg_perc = 100 - pg_perc
		self.entryPGVariable.set(str(pg_perc))
		self.entryVGVariable.set(str(vg_perc))
		self.calculateBatch(None)

	def onVGModified(self, event):
		if (self.entryVGVariable.get()):
			vg_perc = int(float(self.entryVGVariable.get()))
		else: vg_perc = 0
		pg_perc = 100 - vg_perc
		self.entryPGVariable.set(str(pg_perc))
		self.entryVGVariable.set(str(vg_perc))
		self.calculateBatch(None)

	def calculateBatch(self, event):
		if self.entryBatchVariable.get():
			target_ml = float(self.entryBatchVariable.get())
		else:
			target_ml = 0.0
		if self.entryNICVariable.get():
			target_nic = float(self.entryNICVariable.get())
		else:
			target_nic = 0.0
		if self.entryNICConcVariable.get():
			nic_src = float(self.entryNICConcVariable.get())
		else:
			nic_src = 36.0
		if self.entryVGVariable.get():
			vg_perc = float(self.entryVGVariable.get())
		else:
			vg_perc=0.0
		if self.entryPGVariable.get():
			pg_perc = float(self.entryPGVariable.get())
		else:
			pg_perc = 0.0

		nic_ml = (target_nic * target_ml) / nic_src
		vg_ml = vg_perc/100.0 * target_ml
		pg_ml = target_ml - vg_ml
		pg_used = nic_ml

		for flavor in self.workingFlavors:
			if flavor[2].get():
				flavor_perc = float(flavor[2].get())
			else:
				flavor_perc = 0.0
			flavor_ml = target_ml * flavor_perc/100.0
			flavor[4].set(str(flavor_ml))
			pg_used += flavor_ml
		pg_ml = pg_ml - pg_used

		self.NIC_ml_Variable.set(str(nic_ml))
		self.VG_ml_Variable.set(str(vg_ml))
		self.PG_ml_Variable.set(str(pg_ml))

	def loadRecipes(self):
		if os.path.isfile('recipeData') and os.access('recipeData', os.R_OK):
			# Load recipes
			json_data = open('recipeData').read()
			recipeData = json.loads(json_data)
			for data in recipeData:
				self.listbox.insert(Tkinter.END,data["Name"])
				self.recipeVault.append(Recipe(data["Name"],
					data["Flavors"],
					data["VG"],
					data["PG"],
					data["NIC"],
					data["Description"]))
			self.sort_list()
		else:
			# No recipes exist or file is inaccessible
			print 'Could not find file: recipeData'

	def saveVault(self):
		data = []
		for recipe in self.recipeVault:
			data.append(recipe.getRecipe())
		with open('recipeData', 'w') as fp:
			json.dump(data, fp, indent=4, sort_keys=True)
		print 'saved'

	def sort_list(self):
		temp_list = list(self.listbox.get(0, Tkinter.END))
		temp_list.sort()
		# delete contents in listbox
		self.listbox.delete(0, Tkinter.END)
		# load sorted data into listbox
		for item in temp_list:
			self.listbox.insert(Tkinter.END, item)

	def update_list(self):
		self.listbox.delete(0, Tkinter.END)
		temp_list = []
		for recipe in self.recipeVault:
			temp_list.append(recipe.name)
		temp_list.sort()
		for item in temp_list:
			self.listbox.insert(Tkinter.END, item)


if __name__ == "__main__":
	app = ejuice_app_tk(None)
	app.title('Dew-Recipe Vault')
	app.mainloop()


