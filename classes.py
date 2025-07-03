import enum

class DnDAbilityName(enum.StrEnum):
	STR = "Strength"
	DEX = "Dexterity"
	CON = "Constitution"
	INT = "Intelligence"
	WIS = "Wisdom"
	CHR = "Charisma"

class DnDLevelExp(enum.IntEnum):
	L01 = 0
	L02 = 300
	L03 = 900
	L04 = 2700
	L05 = 6500
	L06 = 14000
	L07 = 23000
	L08 = 34000
	L09 = 48000
	L10 = 64000
	L11 = 85000
	L12 = 100000
	L13 = 120000
	L14 = 140000
	L15 = 165000
	L16 = 195000
	L17 = 225000
	L18 = 265000
	L19 = 305000
	L20 = 355000

class MonetaryValue:
	def __init__(self, copper : int, silver : int = 0, gold : int = 0):
		self.value : int = copper + 10 * silver + 100 * gold

	@classmethod
	def from_gold(class_, amount : float) -> "MonetaryValue":
		in_copper = round(amount * 100)
		in_silver = round(amount * 10)
		return class_(in_copper % 10, in_silver % 10, int(amount))

	def __str__(self) -> str:
		return f"\u20B2{self.value / 100:.2f}"

	def get(self):
		return self.value

class AbilityScore:
	def __init__(self, name : DnDAbilityName, value : int):
		self.name = name
		self.value = value
	
	def __str__(self) -> str:
		return f"{self.getNamePrefix()}: {self.getScore(): >2d} {self.getBonus(): >+2d}"

	def toStrNoName(self) -> str:
		return str(self).split(':')[1].strip()

	def getNamePrefix(self) -> str:
		return self.name[:3].upper()

	def getName(self) -> str:
		return self.name

	def getScore(self) -> int:
		return self.value

	def getBonus(self) -> int:
		return (self.value - 10) // 2
