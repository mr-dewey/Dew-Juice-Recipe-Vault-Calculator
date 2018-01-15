# Python 2.7
# Author: Will Rooney
# January 14th, 2018

class Recipe():

	def __init__(self, name=None, flavors=[], VG=70, PG=30, NIC=3, desc=None):
		self.name = name
		if flavors is not None:
			self.flavors = flavors
		else:
			self.flavors = []
		self.VG = VG
		self.PG = PG
		self.NIC = NIC
		if desc is not None:
			self.desc = desc
		else:
			self.desc = "No description."
		#print 'Name: ',self.name
		#print 'Flavors:\n',self.flavors

	def addFlavor(self, flavor, strength):
		"""
		Add a new flavor to the recipe
		Pre:
			strength is an integer between [0,100]
		Post:
			If flavor str is unique in recipe
			Flavor object added to recipe's flavors
		"""
		for item in self.flavors:
			if item['Name'].lower() == flavor.lower():
				item['Strength']= strength
				return
		self.flavors.append({'Name': flavor, 'Strength': strength})

	def modifyFlavorStrength(self, flavor, strength):
		for item in self.flavors:
			if flavor.lower() == item["Name"].lower():
				item["Strength"] = strength
				return True
		return False

	def modifyFlavorName(self, flavor, newFlavor):
		for item in self.flavors:
			if item["Name"].lower() == newFlavor.lower():
				return False

		for item in self.flavors:
			if flavor.lower() == item["Name"].lower():
				item["Name"] = newFlavor
				return True
		return False

	def getRecipe(self):
		recipe = {}
		recipe["Name"] = self.name
		recipe["Flavors"] = self.flavors
		recipe["VG"] = self.VG
		recipe["PG"] = self.PG
		recipe["NIC"] = self.NIC
		recipe["Description"] = self.desc
		return recipe

	def setName(self, name):
		if name is not None:
			self.name = name

	def setVG(self, VG=70):
		if VG >=0 and VG <= 100: 
			self.VG = VG
			self.PG = 100 - VG
		else:
			self.VG=70
			self.PG=30

	def setPG(self, PG=30):
		if PG >=0 and PG <= 100: 
			self.PG = PG
			self.VG = 100 - PG
		else:
			self.VG=70
			self.PG=30

	def setNIC(self, NIC=0):
		if NIC >= 0 and NIC <= 24:
			self.NIC = NIC
		else:
			self.NIC = 0

	def setDesc(self, desc):
		if desc is not None:
			self.desc = desc

	def setFlavors(self, flavors=[]):
		self.flavors = flavors

	def __str__(self):
		formattedFlavors = ""
		perc = '%'
		for flavor in self.flavors:
			formattedFlavors += "\t%s %s - %s\n" % (flavor["Strength"], perc, flavor["Name"])
		return "%s:\n\t%s\n\n%s" % (self.name, self.desc, formattedFlavors)


