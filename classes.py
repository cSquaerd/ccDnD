import base64
import enum
import random

from typing import Optional

class DnDAbilityName(enum.StrEnum):
	"""
	Names of the Ability scores present in D&D
	"""
	STR = "Strength"
	DEX = "Dexterity"
	CON = "Constitution"
	INT = "Intelligence"
	WIS = "Wisdom"
	CHR = "Charisma"

class DnDLevelExp(enum.IntEnum):
	"""
	The amounts of cumulative experience points needed to reach a corresponding level in D&D
	"""
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
	"""
	Representation of a monetary value, broken down into copper, silver, and gold coins.
	(copper is akin to a US penny, silver to a US dime, and gold to a US dollar)
	"""
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

class AbilityScoreModifier:
	def __init__(self, ability : DnDAbilityName, value : int, descriptor : Optional[str] = None):
		self.ability : DnDAbilityName = ability
		self.value : int = value

		if descriptor is not None:
			self.descriptor : str = descriptor
		else:
			self.descriptor : str = base64.urlsafe_b64encode(random.randbytes(6)).decode()
	
class AbilityScore:
	"""
	Representation of a D&D Ability Score, with automatic bonus factoring
	"""
	def __init__(self, name : DnDAbilityName, value : int, modifyStrRep : bool = False):
		self.name : DnDAbilityName = name
		self.value : int = value
		self.modifiers : dict[str, AbilityScoreModifier] = {}
		self.modifyStrRep : bool = modifyStrRep
	
	def __str__(self) -> str:
		return (
			f"{self.getNamePrefix()}: "
			f"{self.getScore(self.modifyStrRep): >2d} {self.getBonus(self.modifyStrRep): >+2d}"
		)

	def toStrNoName(self) -> str:
		return str(self, ).split(':')[1].strip()

	def getNamePrefix(self) -> str:
		return self.name[:3].upper()

	def getName(self) -> str:
		return self.name

	def getScore(self, modified : bool = False) -> int:
		if modified:
			modifierSum = sum(map(lambda m : m.value, self.modifiers.values()))
			return self.value + modifierSum

		return self.value

	def getBonus(self, modified : bool = False) -> int:
		return (self.getScore(modified) - 10) // 2

	def registerModifier(self, modifier : AbilityScoreModifier):
		if modifier.ability != self.name:
			raise ValueError(f"Ability mismatch ({modifier.ability} != {self.name})")
		if modifier.descriptor not in self.modifiers:
			self.modifiers[modifier.descriptor] = modifier

	def deregisterModifier(self, descriptor : str):
		if descriptor in self.modifiers:
			del self.modifiers[descriptor]

	def setModifyStrRep(self):
		self.modifyStrRep = True
	
	def unsetModifyStrRep(self):
		self.modifyStrRep = False

class Dice:
	"""
	Representation of a single die or multiple dice of the same shape
	"""
	def __init__(self, count : int, value : int, descriptor : Optional[str] = None):
		self.count : int = count
		self.value : int = value
		self.descriptor : str = ""

		if descriptor is not None:
			self.descriptor = descriptor

	def __str__(self) -> str:
		return f"{self.descriptor + ': ' if len(self.descriptor) > 0 else ''}{self.count}d{self.value}"

	def roll(self) -> int:
		return sum([random.randint(1, self.value) for n in range(self.count)])

	def getMin(self) -> int:
		return self.count

	def getMax(self) -> int:
		return self.value * self.count

class HitDice(Dice):
	"""
	Specific Representation of a class's hit dice; count is akin to level
	"""
	def __init__(self, count : int, value : int, descriptor : Optional[str] = None):
		super().__init__(count, value, descriptor)
		self.uses : int = count

	def __str__(self) -> str:
		return f"{super().__str__()} ({self.uses}/{self.count})"

	def use(self) -> int:
		if self.uses > 0:
			self.uses -= 1
			return random.randint(1, self.value)

		return 0

	def replenish(self, amount : Optional[int] = 1):
		if amount > 0:
			self.uses += min(self.count - self.uses, amount)

class HitPoints:
	"""
	Representation of a character's hit points, with consideration for hit dice
	"""
	def __init__(self, maximum : int, hitDice : Optional[list[HitDice]] = None):
		self.value : int = maximum
		self.maximum : int = maximum
		self.hitDice = []

		if hitDice is not None:
			for d in hitDice:
				self.hitDice.append(d)
	
