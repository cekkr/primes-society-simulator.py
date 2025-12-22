#!/usr/bin/env python3
"""
PRIME SOCIETY SIMULATOR
A multi-generational socio-economic simulation where nutrition comes from prime numbers
"""

import numpy as np
import random
import pickle
import zlib
import heapq
import uuid
import argparse
import logging
import json
import math
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any
from enum import Enum
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os
import sys

# ============= GAME CONSTANTS (EASILY TWEAKABLE) =============

# World Parameters
INITIAL_POPULATION = 1000
WORLD_REGIONS = 5
DISTRICTS_PER_REGION = 4
CELLS_PER_DISTRICT = 100  # 10x10 grid
SPACE_PER_CELL = 1000.0  # cubic units

# Resource Parameters
DAILY_ONE_PRODUCTION = 1.0  # "1"s produced per person per day
NUTRITION_REQUIREMENT = 1.0  # nutrition needed per person per day
STARVATION_THRESHOLD = 0.3  # below this, person starts dying

# Economic Parameters
PRIME_DISCOVERY_COST_MULTIPLIER = 100
PRIME_DISCOVERY_TIME_MULTIPLIER = 1
ENTROPY_LOSS = 0.05  # production inefficiency
MARKET_FRICTION = 0.02
KNOWLEDGE_DECAY_RATE = 0.01 / 365  # per day if unused
KNOWLEDGE_TRANSFER_RATE = 1 / 30  # one prime per 30 days of mentoring

# Social Parameters
TRAIT_INHERITANCE_VARIANCE = 20
TRAIT_MUTATION_RATE = 0.1
RELATIONSHIP_DISTANCE_THRESHOLD = 3  # cells
RELATIONSHIP_DECAY = 0.01  # per day without interaction
CHILD_COST = 10 * 365 * 18  # total cost to raise a child
MIN_REPRODUCTION_AGE = 16
MAX_REPRODUCTION_AGE = 55

# Life Cycle Parameters
LIFE_STAGES = {
   'child': (0, 16),
   'young': (16, 25),
   'adult': (25, 55),
   'senior': (55, 70),
   'elder': (70, 120)
}
BASE_LIFE_EXPECTANCY = 75
MAX_AGE = 120

# Political Parameters
ELECTION_CYCLES = {
   'block': 180,
   'quarter': 365,
   'district': 730,
   'region': 1095
}
CORRUPTION_THRESHOLD = 70  # trait value above which corruption likely

# Meme Parameters
MEME_SPREAD_BASE_RATE = 0.1
MEME_DECAY_RATE = 0.05
MEME_MUTATION_CHANCE = 0.01

# Visualization Parameters
ENABLE_GRAPHS = True
GRAPH_UPDATE_FREQUENCY = 10  # days
TRACKED_METRICS = ['population', 'gdp', 'gini', 'happiness', 'knowledge', 'innovation']

# Checkpoint Parameters
CHECKPOINT_FREQUENCY = 100  # days
MAX_CHECKPOINTS = 10
AUTO_SAVE = True
CHECKPOINT_DIR = "checkpoints"

# Logging Configuration
logging.basicConfig(
   level=logging.INFO,
   format='[Day %(day)d] %(levelname)s: %(message)s',
   handlers=[
       logging.StreamHandler(),
       logging.FileHandler('prime_society.log')
   ]
)
logger = logging.getLogger(__name__)

# ============= UTILITY FUNCTIONS =============

def is_prime(n: int) -> bool:
   """Check if a number is prime"""
   if n < 2:
       return False
   for i in range(2, int(math.sqrt(n)) + 1):
       if n % i == 0:
           return False
   return True

def get_prime_position(n: int) -> int:
   """Get the position of a prime in the sequence (2=1, 3=2, 5=3, etc.)"""
   if not is_prime(n):
       return 0
   position = 0
   current = 2
   while current <= n:
       if is_prime(current):
           position += 1
           if current == n:
               return position
       current += 1
   return 0

def factorize(n: int) -> Dict[int, int]:
   """Return prime factorization as {prime: exponent}"""
   factors = {}
   d = 2
   while d * d <= n:
       while n % d == 0:
           factors[d] = factors.get(d, 0) + 1
           n //= d
       d += 1
   if n > 1:
       factors[n] = factors.get(n, 0) + 1
   return factors

def calculate_nutrition(n: int) -> float:
   """Calculate nutritional value of a number"""
   if n == 1:
       return 0
   if is_prime(n):
       return get_prime_position(n)
   
   # For composite numbers, sum the positions of prime factors
   factors = factorize(n)
   nutrition = 0
   for prime, count in factors.items():
       nutrition += get_prime_position(prime) * count
   return nutrition

def calculate_weight(n: int) -> float:
   """Calculate weight/cost of a number"""
   if n == 1:
       return 1
   if is_prime(n):
       pos = get_prime_position(n)
       return pos * pos
   
   # For composite numbers
   factors = factorize(n)
   weight = 0
   for prime, count in factors.items():
       pos = get_prime_position(prime)
       weight += (pos * count) ** 2
   return weight

def calculate_efficiency(n: int) -> float:
   """Calculate efficiency (nutrition/weight ratio)"""
   weight = calculate_weight(n)
   if weight == 0:
       return 0
   return calculate_nutrition(n) / weight

# ============= PERSONALITY TRAITS =============

class Trait(Enum):
   """The 10 personality axes"""
   GENEROSITY_GREED = "generosity_greed"  # -100 generous, +100 greedy
   INVENTIVE_IMITATIVE = "inventive_imitative"  # -100 inventive, +100 imitative
   DIPLOMATIC_AGGRESSIVE = "diplomatic_aggressive"  # -100 diplomatic, +100 aggressive
   HUMBLE_AMBITIOUS = "humble_ambitious"  # -100 humble, +100 ambitious
   SOCIAL_PRAGMATIC = "social_pragmatic"  # -100 social, +100 pragmatic
   SINCERE_DECEPTIVE = "sincere_deceptive"  # -100 sincere, +100 deceptive
   SHARING_EXPLOITING = "sharing_exploiting"  # -100 sharing, +100 exploiting
   REFLECTIVE_IMPULSIVE = "reflective_impulsive"  # -100 reflective, +100 impulsive
   CONSERVATIVE_PROGRESSIVE = "conservative_progressive"  # -100 conservative, +100 progressive
   MATERIALIST_SPIRITUAL = "materialist_spiritual"  # -100 materialist, +100 spiritual

# ============= CORE CLASSES =============

@dataclass
class Location:
   """3D location in the world"""
   region: int
   district: int
   cell_x: int
   cell_y: int
   z: float = 0.0  # height
   
   def distance_to(self, other: 'Location') -> float:
       """Calculate distance to another location"""
       if self.region != other.region:
           return 1000.0  # Different regions are far
       if self.district != other.district:
           return 100.0  # Different districts
       
       dx = self.cell_x - other.cell_x
       dy = self.cell_y - other.cell_y
       dz = self.z - other.z
       return math.sqrt(dx*dx + dy*dy + dz*dz)

class Person:
   """Individual agent in the simulation"""
   
   def __init__(self, traits: Dict[Trait, float] = None, parents: Tuple['Person', 'Person'] = None):
       self.id = str(uuid.uuid4())
       self.age = 0
       self.birth_day = 0
       self.death_day = None
       self.is_alive = True
       self.happiness = 1.0
       self.health = 1.0
       
       # Traits
       if traits:
           self.traits = traits
       elif parents:
           self.traits = self._inherit_traits(parents)
       else:
           self.traits = self._random_traits()
       
       # Derived attributes
       self.intelligence = self._calculate_intelligence()
       self.charisma = self._calculate_charisma()
       
       # Knowledge and skills
       self.known_primes: Set[int] = {2}  # Everyone starts knowing "2"
       self.learning_progress: Dict[int, float] = {}  # Prime -> progress%
       
       # Resources and needs
       self.resources = 100.0  # Starting resources
       self.nutrition_level = 1.0  # Full nutrition
       self.energy = 100.0  # Daily energy
       self.stress = 0.0
       self.happiness = 50.0
       self.health = 100.0
       
       # Relationships
       self.relationships: Dict[str, float] = {}  # person_id -> relationship strength
       self.family: Dict[str, str] = {}  # role -> person_id
       self.employer: Optional['Company'] = None
       self.salary = 0.0
       
       # Location and property
       self.location = Location(
           region=random.randint(0, WORLD_REGIONS-1),
           district=random.randint(0, DISTRICTS_PER_REGION-1),
           cell_x=random.randint(0, 9),
           cell_y=random.randint(0, 9)
       )
       self.owned_space = 0.0
       self.rented_space = 10.0  # Minimum living space
       
       # Memory and experience
       self.memory: deque = deque(maxlen=1000)  # Last 1000 events
       self.reputation = 0.0
       self.political_leaning = [0.0, 0.0]  # [economic, social] axes
   
   def _random_traits(self) -> Dict[Trait, float]:
       """Generate random traits"""
       return {trait: random.uniform(-100, 100) for trait in Trait}
   
   def _inherit_traits(self, parents: Tuple['Person', 'Person']) -> Dict[Trait, float]:
       """Inherit traits from parents with variation"""
       traits = {}
       for trait in Trait:
           parent_avg = (parents[0].traits[trait] + parents[1].traits[trait]) / 2
           variation = random.uniform(-TRAIT_INHERITANCE_VARIANCE, TRAIT_INHERITANCE_VARIANCE)
           traits[trait] = max(-100, min(100, parent_avg + variation))
       return traits
   
   def _calculate_intelligence(self) -> float:
       """Calculate intelligence from traits"""
       base = 50
       inventive_bonus = self.traits[Trait.INVENTIVE_IMITATIVE] * -0.3  # Negative because inventive is -100
       reflective_bonus = self.traits[Trait.REFLECTIVE_IMPULSIVE] * -0.2
       return max(0, min(200, base + inventive_bonus + reflective_bonus + random.uniform(-10, 10)))
   
   def _calculate_charisma(self) -> float:
       """Calculate charisma from traits and state"""
       base = 50
       diplomatic_bonus = self.traits[Trait.DIPLOMATIC_AGGRESSIVE] * -0.3
       social_bonus = self.traits[Trait.SOCIAL_PRAGMATIC] * -0.2
       happiness_bonus = self.happiness * 0.1
       health_bonus = self.health * 0.1
       return max(0, min(100, base + diplomatic_bonus + social_bonus + happiness_bonus + health_bonus))
   
   def age_up(self):
       """Age by one day"""
       self.age += 1
       
       # Health degradation
       if self.age > 365 * 55:  # After 55 years
           self.health -= 0.01
       if self.age > 365 * 70:  # After 70 years
           self.health -= 0.02
       
       # Check for natural death
       life_expectancy_days = BASE_LIFE_EXPECTANCY * 365
       death_probability = max(0, (self.age - life_expectancy_days) / (365 * 10))
       if self.health <= 0 or random.random() < death_probability:
           self.die()
   
   def die(self):
       """Handle death"""
       self.is_alive = False
       self.death_day = self.age
       logger.info(f"Person {self.id} died at age {self.age/365:.1f}")
   
   def daily_routine(self, world: 'World'):
       """Execute daily activities"""
       if not self.is_alive:
           return
       
       self.age_up()
       if not self.is_alive:
           return
       
       # Reset daily energy
       self.energy = 100 - (self.age / (365 * 100)) * 20  # Age reduces energy
       
       # Consume nutrition
       self.nutrition_level -= NUTRITION_REQUIREMENT
       if self.nutrition_level < STARVATION_THRESHOLD:
           self.health -= 5
           self.stress += 10
       
       # Work if employed
       if self.employer and self.age >= 16 * 365:
           self.work()
       
       # Social interactions
       self.socialize(world)
       
       # Learn if young or ambitious
       if self.energy > 20 and (self.age < 25 * 365 or self.traits[Trait.HUMBLE_AMBITIOUS] > 50):
           self.study()
       
       # Update happiness
       self.update_happiness()
   
   def work(self):
       """Perform work activities"""
       if not self.employer:
           return
       
       # Spend energy on work
       work_energy = min(40, self.energy)
       self.energy -= work_energy
       
       # Gain resources from salary
       self.resources += self.salary
       
       # Gain stress from work
       self.stress += 5 * (1 + self.traits[Trait.HUMBLE_AMBITIOUS] / 100)
   
   def study(self):
       """Study to learn new primes"""
       if self.energy < 20:
           return
       
       self.energy -= 20
       
       # Find next prime to learn
       max_known = max(self.known_primes) if self.known_primes else 1
       next_prime = max_known + 1
       while not is_prime(next_prime):
           next_prime += 1
       
       # Check if can learn (needs prerequisites)
       can_learn = True
       for p in range(2, next_prime):
           if is_prime(p) and p not in self.known_primes:
               can_learn = False
               break
       
       if not can_learn:
           return
       
       # Make progress
       if next_prime not in self.learning_progress:
           self.learning_progress[next_prime] = 0
       
       # Learning speed based on intelligence
       daily_progress = (self.intelligence / 100) * 10
       self.learning_progress[next_prime] += daily_progress
       
       # Check if learned
       difficulty = get_prime_position(next_prime) ** 2
       if self.learning_progress[next_prime] >= difficulty:
           self.known_primes.add(next_prime)
           del self.learning_progress[next_prime]
           logger.debug(f"Person {self.id} learned prime {next_prime}")
   
   def socialize(self, world: 'World'):
       """Interact with nearby people"""
       if self.energy < 10:
           return
       
       # Find nearby people
       nearby = world.get_nearby_people(self.location, RELATIONSHIP_DISTANCE_THRESHOLD)
       
       for other in nearby[:5]:  # Interact with up to 5 people
           if other.id == self.id:
               continue
           
           # Update relationship
           compatibility = self.calculate_compatibility(other)
           if other.id not in self.relationships:
               self.relationships[other.id] = 0
           
           self.relationships[other.id] += compatibility * 0.1
           self.relationships[other.id] = max(-100, min(100, self.relationships[other.id]))
           
           self.energy -= 2
           if self.energy <= 0:
               break
   
   def calculate_compatibility(self, other: 'Person') -> float:
       """Calculate compatibility with another person"""
       trait_diff = sum(abs(self.traits[t] - other.traits[t]) for t in Trait)
       return 100 - (trait_diff / len(Trait))
   
   def update_happiness(self):
       """Update happiness based on current state"""
       base = 50
       
       # Needs satisfaction
       nutrition_factor = self.nutrition_level * 20
       health_factor = self.health * 0.2
       stress_factor = -self.stress * 0.3
       
       # Social satisfaction
       relationship_quality = sum(self.relationships.values()) / max(1, len(self.relationships))
       social_factor = relationship_quality * 0.2
       
       # Economic satisfaction
       resource_factor = min(20, self.resources / 100)
       
       self.happiness = max(0, min(100, 
           base + nutrition_factor + health_factor + stress_factor + social_factor + resource_factor
       ))

class Company:
   """Economic entity that employs people and produces goods"""
   
   def __init__(self, founder: Person, name: str = None):
       self.id = str(uuid.uuid4())
       self.name = name or f"Company_{self.id[:8]}"
       self.founder_id = founder.id
       self.founded_day = 0
       
       # Resources
       self.capital = founder.resources * 0.5  # Founder invests half their resources
       founder.resources *= 0.5
       self.inventory: Dict[int, float] = {}  # number -> quantity
       
       # Employees
       self.employees: List[Person] = [founder]
       founder.employer = self
       
       # Knowledge
       self.collective_knowledge: Set[int] = founder.known_primes.copy()
       
       # Production
       self.production_targets: List[int] = []
       self.efficiency = 1.0
       
       # Market position
       self.reputation = 0.0
       self.market_share = 0.0
   
   def update_collective_knowledge(self):
       """Update company's collective knowledge from employees"""
       self.collective_knowledge = set()
       for employee in self.employees:
           self.collective_knowledge.update(employee.known_primes)
   
   def can_produce(self, number: int) -> bool:
       """Check if company can produce a number given employee knowledge"""
       if is_prime(number):
           return number in self.collective_knowledge
       
       # For composite numbers, need all prime factors
       factors = factorize(number)
       return all(prime in self.collective_knowledge for prime in factors.keys())
   
   def produce(self, number: int, quantity: float) -> float:
       """Produce a quantity of a number"""
       if not self.can_produce(number):
           return 0
       
       # Calculate production cost
       weight = calculate_weight(number)
       cost = weight * quantity
       
       if self.capital < cost:
           quantity = self.capital / weight
       
       # Produce with entropy loss
       produced = quantity * (1 - ENTROPY_LOSS)
       self.capital -= cost
       
       if number not in self.inventory:
           self.inventory[number] = 0
       self.inventory[number] += produced
       
       return produced
   
   def hire(self, person: Person, salary: float):
       """Hire a new employee"""
       if person.employer:
           person.employer.fire(person)
       
       self.employees.append(person)
       person.employer = self
       person.salary = salary
       self.update_collective_knowledge()
   
   def fire(self, person: Person):
       """Fire an employee"""
       if person in self.employees:
           self.employees.remove(person)
           person.employer = None
           person.salary = 0
           self.update_collective_knowledge()
   
   def pay_salaries(self):
       """Pay all employees"""
       total_salaries = sum(e.salary for e in self.employees)
       if self.capital >= total_salaries:
           self.capital -= total_salaries
           for employee in self.employees:
               employee.resources += employee.salary
       else:
           # Company bankruptcy
           self.bankruptcy()
   
   def bankruptcy(self):
       """Handle company bankruptcy"""
       logger.info(f"Company {self.name} went bankrupt")
       for employee in self.employees[:]:
           self.fire(employee)
       self.capital = 0
       self.inventory = {}

class Building:
   """Physical structure in the world"""
   
   def __init__(self, location: Location, space: float, builder: Person = None):
       self.id = str(uuid.uuid4())
       self.location = location
       self.total_space = space
       self.used_space = 0
       self.build_day = 0
       self.quality = random.uniform(0.5, 1.0)
       
       # Ownership
       self.owner_id = builder.id if builder else None
       self.residents: List[Person] = []
       self.rent_per_space = 1.0
       
       # Building type and purpose
       self.building_type = "residential"  # residential, commercial, industrial
       self.companies: List[Company] = []
   
   def calculate_value(self, world: 'World') -> float:
       """Calculate current market value"""
       base_value = self.total_space * 10
       
       # Location factors
       location_multiplier = 1.0
       
       # Quality and age factors
       quality_multiplier = self.quality
       age_penalty = 1.0 - (world.current_day - self.build_day) / (365 * 50)
       age_penalty = max(0.5, age_penalty)
       
       return base_value * location_multiplier * quality_multiplier * age_penalty
   
   def add_resident(self, person: Person):
       """Add a resident to the building"""
       if person not in self.residents:
           self.residents.append(person)
           person.location = self.location
           self.used_space += person.rented_space
   
   def remove_resident(self, person: Person):
       """Remove a resident from the building"""
       if person in self.residents:
           self.residents.remove(person)
           self.used_space -= person.rented_space

class Meme:
   """Cultural unit that spreads through population"""
   
   def __init__(self, creator: Person, name: str = None):
       self.id = str(uuid.uuid4())
       self.name = name or f"Meme_{self.id[:8]}"
       self.creator_id = creator.id
       self.created_day = 0
       
       # Effects on traits
       self.trait_effects: Dict[Trait, float] = {}
       for trait in random.sample(list(Trait), 3):  # Affects 3 random traits
           self.trait_effects[trait] = random.uniform(-20, 20)
       
       # Spread dynamics
       self.transmissibility = random.uniform(0.5, 1.5)
       self.carriers: Set[str] = {creator.id}
       self.immunity: Set[str] = set()
       
       # Metrics
       self.total_infections = 1
       self.peak_carriers = 1
   
   def spread(self, from_person: Person, to_person: Person) -> bool:
       """Attempt to spread meme from one person to another"""
       if to_person.id in self.carriers or to_person.id in self.immunity:
           return False
       
       # Calculate spread probability
       compatibility = 0
       for trait, effect in self.trait_effects.items():
           if effect * to_person.traits[trait] > 0:  # Same direction
               compatibility += 0.1
       
       spread_prob = MEME_SPREAD_BASE_RATE * self.transmissibility * (1 + compatibility)
       
       if random.random() < spread_prob:
           self.carriers.add(to_person.id)
           self.total_infections += 1
           
           # Apply trait effects
           for trait, effect in self.trait_effects.items():
               to_person.traits[trait] += effect
               to_person.traits[trait] = max(-100, min(100, to_person.traits[trait]))
           
           return True
       
       return False
   
   def decay(self):
       """Natural decay of meme spread"""
       if random.random() < MEME_DECAY_RATE:
           if self.carriers:
               lost_carrier = random.choice(list(self.carriers))
               self.carriers.remove(lost_carrier)
               self.immunity.add(lost_carrier)

# ============= WORLD AND SYSTEMS =============

class Market:
   """Handles all economic transactions"""
   
   def __init__(self):
       self.order_book: Dict[int, Dict[str, List]] = {}  # number -> {bids: [], asks: []}
       self.prices: Dict[int, float] = {}  # Current market prices
       self.volume: Dict[int, float] = defaultdict(float)  # Daily trading volume
       self.price_history: Dict[int, deque] = defaultdict(lambda: deque(maxlen=365))
       
       # Initialize base prices
       self.prices[1] = 1.0  # Base resource
       self.prices[2] = calculate_nutrition(2) / calculate_weight(2) * 10
   
   def place_order(self, number: int, quantity: float, price: float, is_bid: bool, trader_id: str):
       """Place a buy or sell order"""
       if number not in self.order_book:
           self.order_book[number] = {'bids': [], 'asks': []}
       
       order = (price, quantity, trader_id)
       
       if is_bid:
           heapq.heappush(self.order_book[number]['bids'], (-price, quantity, trader_id))
       else:
           heapq.heappush(self.order_book[number]['asks'], (price, quantity, trader_id))
       
       self.match_orders(number)
   
   def match_orders(self, number: int):
       """Match buy and sell orders"""
       if number not in self.order_book:
           return
       
       book = self.order_book[number]
       
       while book['bids'] and book['asks']:
           bid = book['bids'][0]
           ask = book['asks'][0]
           
           bid_price = -bid[0]
           ask_price = ask[0]
           
           if bid_price >= ask_price:
               # Match found
               execution_price = (bid_price + ask_price) / 2
               quantity = min(bid[1], ask[1])
               
               # Execute trade
               self.execute_trade(number, quantity, execution_price, bid[2], ask[2])
               
               # Update order book
               if bid[1] <= quantity:
                   heapq.heappop(book['bids'])
               else:
                   book['bids'][0] = (-bid_price, bid[1] - quantity, bid[2])
               
               if ask[1] <= quantity:
                   heapq.heappop(book['asks'])
               else:
                   book['asks'][0] = (ask_price, ask[1] - quantity, ask[2])
           else:
               break
   
   def execute_trade(self, number: int, quantity: float, price: float, buyer_id: str, seller_id: str):
       """Execute a trade between buyer and seller"""
       self.prices[number] = price
       self.volume[number] += quantity
       self.price_history[number].append(price)
       
       logger.debug(f"Trade executed: {quantity} of {number} at {price}")
   
   def get_price(self, number: int) -> float:
       """Get current market price or estimate"""
       if number in self.prices:
           return self.prices[number]
       
       # Estimate based on nutrition and weight
       nutrition = calculate_nutrition(number)
       weight = calculate_weight(number)
       
       if weight > 0:
           return (nutrition / weight) * 10
       return 1.0
   
   def calculate_gdp(self) -> float:
       """Calculate total economic activity"""
       return sum(self.volume[n] * self.get_price(n) for n in self.volume)

class PoliticalSystem:
   """Handles elections and governance"""
   
   def __init__(self):
       self.offices: Dict[str, Dict[str, str]] = {
           'block': {},
           'quarter': {},
           'district': {},
           'region': {}
       }
       self.election_countdown: Dict[str, int] = ELECTION_CYCLES.copy()
       self.policies: Dict[str, float] = {
           'tax_rate': 0.1,
           'welfare_spending': 0.2,
           'education_funding': 0.15,
           'research_grants': 0.1
       }
       self.corruption_level = 0.0
   
   def daily_update(self, world: 'World'):
       """Update political system daily"""
       for level in self.election_countdown:
           self.election_countdown[level] -= 1
           if self.election_countdown[level] <= 0:
               self.hold_election(level, world)
               self.election_countdown[level] = ELECTION_CYCLES[level]
   
   def hold_election(self, level: str, world: 'World'):
       """Hold election at specified level"""
       logger.info(f"Holding {level} election")
       
       # Get eligible voters and candidates
       eligible_voters = [p for p in world.people.values() if p.is_alive and p.age >= 18 * 365]
       
       # Generate candidates (simplified)
       num_candidates = min(5, len(eligible_voters) // 100)
       candidates = random.sample(eligible_voters, num_candidates)
       
       # Voting
       votes = defaultdict(int)
       for voter in eligible_voters:
           choice = self.voter_decision(voter, candidates)
           if choice:
               votes[choice.id] += 1
       
       # Determine winner
       if votes:
           winner_id = max(votes, key=votes.get)
           self.offices[level][str(world.current_day)] = winner_id
           logger.info(f"Election winner: {winner_id} with {votes[winner_id]} votes")
   
   def voter_decision(self, voter: Person, candidates: List[Person]) -> Optional[Person]:
       """Determine voter's choice"""
       if not candidates:
           return None
       
       best_candidate = None
       best_score = -float('inf')
       
       for candidate in candidates:
           # Calculate alignment
           trait_alignment = sum(
               -abs(voter.traits[t] - candidate.traits[t]) / 200
               for t in Trait
           )
           
           # Add charisma factor
           charisma_factor = candidate.charisma / 100
           
           # Random factor
           random_factor = random.uniform(-0.2, 0.2)
           
           score = trait_alignment + charisma_factor + random_factor
           
           if score > best_score:
               best_score = score
               best_candidate = candidate
       
       # Abstention based on apathy
       if best_score < -0.5 or random.random() < 0.2:  # 20% abstention rate
           return None
       
       return best_candidate

class World:
   """Main world container and coordinator"""
   
   def __init__(self):
       self.current_day = 0
       self.people: Dict[str, Person] = {}
       self.companies: Dict[str, Company] = {}
       self.buildings: Dict[str, Building] = {}
       self.memes: Dict[str, Meme] = {}
       
       # Systems
       self.market = Market()
       self.political_system = PoliticalSystem()
       
       # Spatial grid: region -> district -> cells
       self.grid = np.zeros((WORLD_REGIONS, DISTRICTS_PER_REGION, 10, 10), dtype=object)
       for r in range(WORLD_REGIONS):
           for d in range(DISTRICTS_PER_REGION):
               for x in range(10):
                   for y in range(10):
                       self.grid[r, d, x, y] = {
                           'people': [],
                           'buildings': [],
                           'resources': SPACE_PER_CELL
                       }
       
       # Statistics tracking
       self.stats = {
           'population': [],
           'gdp': [],
           'gini': [],
           'happiness': [],
           'knowledge': [],
           'innovation': [],
           'births': 0,
           'deaths': 0,
           'companies_founded': 0,
           'companies_failed': 0,
           'buildings_constructed': 0,
           'prime_discoveries': defaultdict(int),
           'meme_spread': []
       }
       
       # Initialize population
       self._initialize_population()
   
   def _initialize_population(self):
       """Create initial population"""
       for i in range(INITIAL_POPULATION):
           person = Person()
           person.age = random.randint(0, 60 * 365)  # Random ages up to 60
           person.resources = random.uniform(50, 500)
           
           # Give some initial knowledge based on age
           if person.age > 16 * 365:
               max_prime = min(7, 2 + person.age // (10 * 365))
               primes = [p for p in range(2, max_prime + 1) if is_prime(p)]
               person.known_primes = set(primes[:random.randint(1, len(primes))])
           
           self.add_person(person)
       
       logger.info(f"Initialized {INITIAL_POPULATION} people")
   
   def add_person(self, person: Person):
       """Add a person to the world"""
       self.people[person.id] = person
       
       # Add to spatial grid
       loc = person.location
       self.grid[loc.region, loc.district, loc.cell_x, loc.cell_y]['people'].append(person.id)
   
   def remove_person(self, person: Person):
       """Remove a person from the world"""
       if person.id in self.people:
           # Remove from grid
           loc = person.location
           cell_people = self.grid[loc.region, loc.district, loc.cell_x, loc.cell_y]['people']
           if person.id in cell_people:
               cell_people.remove(person.id)
           
           # Remove from employer
           if person.employer:
               person.employer.fire(person)
           
           del self.people[person.id]
   
   def get_nearby_people(self, location: Location, radius: float) -> List[Person]:
       """Get people within radius of location"""
       nearby = []
       
       # Simple implementation - check cells in same district
       if radius <= 3:
           # Check only nearby cells
           for dx in range(-int(radius), int(radius) + 1):
               for dy in range(-int(radius), int(radius) + 1):
                   x = location.cell_x + dx
                   y = location.cell_y + dy
                   if 0 <= x < 10 and 0 <= y < 10:
                       cell = self.grid[location.region, location.district, x, y]
                       for person_id in cell['people']:
                           if person_id in self.people:
                               nearby.append(self.people[person_id])
       else:
           # Check whole district
           for x in range(10):
               for y in range(10):
                   cell = self.grid[location.region, location.district, x, y]
                   for person_id in cell['people']:
                       if person_id in self.people:
                           person = self.people[person_id]
                           if person.location.distance_to(location) <= radius:
                               nearby.append(person)
       
       return nearby
   
   def simulate_day(self):
       """Simulate one day in the world"""
       self.current_day += 1
       logger.info(f"Day {self.current_day} - Population: {len(self.people)}")
       
       # Phase 1: Individual activities (40% of processing)
       self._phase_individual()
       
       # Phase 2: Work and production (25%)
       self._phase_work()
       
       # Phase 3: Market transactions (20%)
       self._phase_market()
       
       # Phase 4: Social interactions (10%)
       self._phase_social()
       
       # Phase 5: System updates (5%)
       self._phase_system()
       
       # Collect statistics
       self._collect_stats()
       
       # Auto-balancing
       self._auto_balance()
   
   def _phase_individual(self):
       """Individual daily routines"""
       people_list = list(self.people.values())
       random.shuffle(people_list)
       
       for person in people_list:
           if person.is_alive:
               person.daily_routine(self)
               
               # Handle births
               if self._check_reproduction(person):
                   self._handle_birth(person)
       
       # Remove dead people
       dead = [p for p in self.people.values() if not p.is_alive]
       for person in dead:
           self.stats['deaths'] += 1
           self.remove_person(person)
   
   def _phase_work(self):
       """Work and production phase"""
       # Companies produce goods
       for company in list(self.companies.values()):
           if company.employees:
               # Decide what to produce based on market prices
               profitable_products = []
               for n in range(2, 20):  # Check first 20 numbers
                   if company.can_produce(n):
                       efficiency = calculate_efficiency(n)
                       price = self.market.get_price(n)
                       profit_margin = price * efficiency
                       profitable_products.append((profit_margin, n))
               
               if profitable_products:
                   profitable_products.sort(reverse=True)
                   best_product = profitable_products[0][1]
                   
                   # Produce
                   production_capacity = len(company.employees) * 10
                   produced = company.produce(best_product, production_capacity)
                   
                   if produced > 0:
                       # Place sell order
                       price = self.market.get_price(best_product) * 1.1
                       self.market.place_order(best_product, produced, price, False, company.id)
               
               # Pay salaries
               company.pay_salaries()
       
       # Job market - unemployed look for work
       unemployed = [p for p in self.people.values() 
                     if p.is_alive and p.age >= 16 * 365 and not p.employer]
       
       for person in unemployed[:100]:  # Limit to prevent slowdown
           # Look for job or start company
           if person.resources > 1000 and random.random() < 0.01:
               # Start a company
               company = Company(person, f"{person.id[:8]}_Corp")
               self.companies[company.id] = company
               self.stats['companies_founded'] += 1
           elif self.companies:
               # Look for employment
               for company in random.sample(list(self.companies.values()), 
                                           min(5, len(self.companies))):
                   if len(company.employees) < 20:  # Company size limit
                       # Check if person's knowledge is useful
                       new_knowledge = person.known_primes - company.collective_knowledge
                       if new_knowledge:
                           salary = len(new_knowledge) * 10
                           if company.capital > salary * 30:  # Can afford for 30 days
                               company.hire(person, salary)
                               break
   
   def _phase_market(self):
       """Market transactions and price discovery"""
       # People buy food (numbers for nutrition)
       for person in self.people.values():
           if not person.is_alive:
               continue
           
           # Calculate nutrition need
           need = NUTRITION_REQUIREMENT - person.nutrition_level
           if need > 0 and person.resources > 0:
               # Find affordable nutrition
               best_deal = None
               best_efficiency = 0
               
               for n in range(1, 10):  # Check first 10 numbers
                   nutrition = calculate_nutrition(n)
                   price = self.market.get_price(n)
                   
                   if price <= person.resources and nutrition > 0:
                       efficiency = nutrition / price
                       if efficiency > best_efficiency:
                           best_efficiency = efficiency
                           best_deal = n
               
               if best_deal:
                   # Place buy order
                   quantity = min(person.resources / self.market.get_price(best_deal), 10)
                   self.market.place_order(best_deal, quantity, 
                                         self.market.get_price(best_deal) * 0.9,
                                         True, person.id)
                   
                   # Simplified - immediate consumption
                   person.nutrition_level += calculate_nutrition(best_deal) * quantity * 0.1
                   person.resources -= self.market.get_price(best_deal) * quantity
       
       # Natural "1" production
       ones_produced = len(self.people) * DAILY_ONE_PRODUCTION
       if ones_produced > 0:
           # Distribute randomly to companies
           if self.companies:
               for company in self.companies.values():
                   company.inventory[1] = company.inventory.get(1, 0) + ones_produced / len(self.companies)
                   # Sell some
                   if company.inventory[1] > 10:
                       self.market.place_order(1, company.inventory[1] * 0.5, 1.0, False, company.id)
                       company.inventory[1] *= 0.5
   
   def _phase_social(self):
       """Social interactions and meme spread"""
       # Create new memes occasionally
       if random.random() < 0.001:  # 0.1% chance per day
           creator = random.choice(list(self.people.values()))
           if creator.is_alive:
               meme = Meme(creator, f"Meme_{self.current_day}")
               meme.created_day = self.current_day
               self.memes[meme.id] = meme
       
       # Spread existing memes
       for meme in list(self.memes.values()):
           carriers = [self.people[pid] for pid in meme.carriers if pid in self.people]
           
           for carrier in carriers:
               if not carrier.is_alive:
                   continue
               
               # Try to spread to nearby people
               nearby = self.get_nearby_people(carrier.location, 2)
               for person in nearby[:3]:  # Limit spread attempts
                   meme.spread(carrier, person)
           
           # Natural decay
           meme.decay()
           
           # Track peak
           meme.peak_carriers = max(meme.peak_carriers, len(meme.carriers))
           
           # Remove dead memes
           if not meme.carriers:
               del self.memes[meme.id]
   
   def _phase_system(self):
       """System updates and maintenance"""
       # Political system update
       self.political_system.daily_update(self)
       
       # Building construction
       if random.random() < 0.01:  # 1% chance of new building
           location = Location(
               region=random.randint(0, WORLD_REGIONS-1),
               district=random.randint(0, DISTRICTS_PER_REGION-1),
               cell_x=random.randint(0, 9),
               cell_y=random.randint(0, 9)
           )
           
           # Find a wealthy person to build
           wealthy = [p for p in self.people.values() if p.resources > 5000]
           if wealthy:
               builder = random.choice(wealthy)
               building = Building(location, random.uniform(100, 500), builder)
               building.build_day = self.current_day
               builder.resources -= building.total_space * 10
               self.buildings[building.id] = building
               self.stats['buildings_constructed'] += 1
       
       # Company failures
       for company in list(self.companies.values()):
           if company.capital < 0:
               company.bankruptcy()
               del self.companies[company.id]
               self.stats['companies_failed'] += 1
       
       # Knowledge discovery tracking
       for person in self.people.values():
           for prime in person.known_primes:
               if prime not in self.stats['prime_discoveries']:
                   self.stats['prime_discoveries'][prime] = self.current_day
                   logger.info(f"Prime {prime} discovered on day {self.current_day}")
   
   def _check_reproduction(self, person: Person) -> bool:
       """Check if person should reproduce"""
       if not person.is_alive:
           return False
       
       age_years = person.age / 365
       if age_years < MIN_REPRODUCTION_AGE or age_years > MAX_REPRODUCTION_AGE:
           return False
       
       # Need resources and a partner
       if person.resources < CHILD_COST:
           return False
       
       # Find potential partner
       if person.relationships:
           best_relationship = max(person.relationships.items(), key=lambda x: x[1])
           if best_relationship[1] > 50:  # Strong relationship
               partner_id = best_relationship[0]
               if partner_id in self.people:
                   partner = self.people[partner_id]
                   if partner.is_alive and partner.resources > CHILD_COST / 2:
                       return random.random() < 0.001  # 0.1% chance per day
       
       return False
   
   def _handle_birth(self, parent: Person):
       """Handle birth of new person"""
       # Find partner
       partner = None
       if parent.relationships:
           best_relationship = max(parent.relationships.items(), key=lambda x: x[1])
           partner_id = best_relationship[0]
           if partner_id in self.people:
               partner = self.people[partner_id]
       
       # Create child
       if partner:
           child = Person(parents=(parent, partner))
       else:
           child = Person(parents=(parent, parent))  # Single parent
       
       child.birth_day = self.current_day
       child.location = parent.location
       
       # Parents pay cost
       parent.resources -= CHILD_COST / 2
       if partner:
           partner.resources -= CHILD_COST / 2
       
       # Family relationships
       child.family['parent1'] = parent.id
       if partner:
           child.family['parent2'] = partner.id
       
       parent.family[f'child_{child.id}'] = child.id
       if partner:
           partner.family[f'child_{child.id}'] = child.id
       
       self.add_person(child)
       self.stats['births'] += 1
       
       logger.debug(f"Birth: {child.id} born to {parent.id}")
   
   def _collect_stats(self):
       """Collect daily statistics"""
       # Population
       self.stats['population'].append(len(self.people))
       
       # GDP
       gdp = self.market.calculate_gdp()
       self.stats['gdp'].append(gdp)
       
       # Gini coefficient
       if self.people:
           resources = [p.resources for p in self.people.values() if p.is_alive]
           if resources:
               gini = self._calculate_gini(resources)
               self.stats['gini'].append(gini)
           else:
               self.stats['gini'].append(0)
       
       # Average happiness
       if self.people:
           avg_happiness = np.mean([p.happiness for p in self.people.values() if p.is_alive])
           self.stats['happiness'].append(avg_happiness)
       
       # Average knowledge
       if self.people:
           avg_knowledge = np.mean([len(p.known_primes) for p in self.people.values() if p.is_alive])
           self.stats['knowledge'].append(avg_knowledge)
       
       # Innovation rate (new primes discovered)
       innovation = len(self.stats['prime_discoveries'])
       self.stats['innovation'].append(innovation)
       
       # Meme spread
       total_meme_carriers = sum(len(m.carriers) for m in self.memes.values())
       self.stats['meme_spread'].append(total_meme_carriers)
   
   def _calculate_gini(self, resources: List[float]) -> float:
       """Calculate Gini coefficient"""
       if not resources or len(resources) == 1:
           return 0
       
       sorted_resources = sorted(resources)
       n = len(sorted_resources)
       index = np.arange(1, n + 1)
       
       return (2 * np.sum(index * sorted_resources)) / (n * np.sum(sorted_resources)) - (n + 1) / n
   
   def _auto_balance(self):
       """Automatic balancing to prevent collapse"""
       population = len(self.people)
       
       # Prevent population collapse
       if population < INITIAL_POPULATION * 0.1:
           logger.warning("Population critically low - spawning immigrants")
           for _ in range(50):
               immigrant = Person()
               immigrant.age = random.randint(20 * 365, 40 * 365)
               immigrant.resources = random.uniform(100, 500)
               immigrant.known_primes = {2, 3, 5}
               self.add_person(immigrant)
       
       # Prevent economic collapse
       if self.stats['gdp'] and self.stats['gdp'][-1] < 100:
           logger.warning("Economic collapse detected - injecting resources")
           for person in random.sample(list(self.people.values()), 
                                      min(100, len(self.people))):
               person.resources += 100
       
       # Prevent starvation
       starving = [p for p in self.people.values() 
                  if p.is_alive and p.nutrition_level < STARVATION_THRESHOLD]
       if len(starving) > population * 0.3:
           logger.warning("Mass starvation detected - emergency food distribution")
           for person in starving:
               person.nutrition_level = 1.0

# ============= VISUALIZATION =============

class Visualizer:
   """Handles all visualization and graphing"""
   
   def __init__(self, world: World):
       self.world = world
       self.fig = None
       self.axes = None
       
       if ENABLE_GRAPHS:
           self.setup_plots()
   
   def setup_plots(self):
       """Setup matplotlib figure with subplots"""
       self.fig, self.axes = plt.subplots(2, 3, figsize=(15, 10))
       self.fig.suptitle('Prime Society Simulation')
       
       # Configure subplots
       self.axes[0, 0].set_title('Population')
       self.axes[0, 1].set_title('GDP')
       self.axes[0, 2].set_title('Gini Coefficient')
       self.axes[1, 0].set_title('Average Happiness')
       self.axes[1, 1].set_title('Knowledge Progression')
       self.axes[1, 2].set_title('Innovation & Memes')
       
       plt.tight_layout()
   
   def update_plots(self):
       """Update all plots with current data"""
       if not ENABLE_GRAPHS or not self.axes:
           return
       
       stats = self.world.stats
       days = range(len(stats['population']))
       
       # Clear all axes
       for ax in self.axes.flat:
           ax.clear()
       
       # Population
       self.axes[0, 0].plot(days, stats['population'], 'b-')
       self.axes[0, 0].set_xlabel('Days')
       self.axes[0, 0].set_ylabel('Population')
       self.axes[0, 0].set_title('Population')
       self.axes[0, 0].grid(True)
       
       # GDP
       if stats['gdp']:
           self.axes[0, 1].plot(days, stats['gdp'], 'g-')
           self.axes[0, 1].set_xlabel('Days')
           self.axes[0, 1].set_ylabel('GDP')
           self.axes[0, 1].set_title('Economic Activity')
           self.axes[0, 1].grid(True)
       
       # Gini
       if stats['gini']:
           self.axes[0, 2].plot(days, stats['gini'], 'r-')
           self.axes[0, 2].set_xlabel('Days')
           self.axes[0, 2].set_ylabel('Gini Coefficient')
           self.axes[0, 2].set_title('Inequality')
           self.axes[0, 2].set_ylim([0, 1])
           self.axes[0, 2].grid(True)
       
       # Happiness
       if stats['happiness']:
           self.axes[1, 0].plot(days, stats['happiness'], 'm-')
           self.axes[1, 0].set_xlabel('Days')
           self.axes[1, 0].set_ylabel('Average Happiness')
           self.axes[1, 0].set_title('Well-being')
           self.axes[1, 0].set_ylim([0, 100])
           self.axes[1, 0].grid(True)
       
       # Knowledge
       if stats['knowledge']:
           self.axes[1, 1].plot(days, stats['knowledge'], 'c-')
           self.axes[1, 1].set_xlabel('Days')
           self.axes[1, 1].set_ylabel('Avg Known Primes')
           self.axes[1, 1].set_title('Knowledge Level')
           self.axes[1, 1].grid(True)
       
       # Innovation and Memes
       if stats['innovation']:
           ax = self.axes[1, 2]
           ax.plot(days, stats['innovation'], 'b-', label='Primes Discovered')
           if stats['meme_spread']:
               ax2 = ax.twinx()
               ax2.plot(days, stats['meme_spread'], 'orange', label='Meme Carriers')
               ax2.set_ylabel('Meme Carriers', color='orange')
           ax.set_xlabel('Days')
           ax.set_ylabel('Cumulative Discoveries', color='b')
           ax.set_title('Innovation & Culture')
           ax.grid(True)
       
       plt.draw()
       plt.pause(0.01)
   
   def save_plots(self, filename: str = None):
       """Save current plots to file"""
       if not filename:
           filename = f"prime_society_day_{self.world.current_day}.png"
       
       if self.fig:
           self.fig.savefig(filename, dpi=150, bbox_inches='tight')
           logger.info(f"Plots saved to {filename}")

# ============= CHECKPOINT SYSTEM =============

class CheckpointManager:
   """Handles saving and loading simulation state"""
   
   def __init__(self, world: World):
       self.world = world
       self.checkpoint_dir = CHECKPOINT_DIR
       
       # Create checkpoint directory if it doesn't exist
       os.makedirs(self.checkpoint_dir, exist_ok=True)
       
       self.checkpoints = []
       self.load_checkpoint_list()
   
   def load_checkpoint_list(self):
       """Load list of available checkpoints"""
       self.checkpoints = []
       if os.path.exists(self.checkpoint_dir):
           for file in os.listdir(self.checkpoint_dir):
               if file.endswith('.checkpoint'):
                   self.checkpoints.append(file)
       self.checkpoints.sort()
   
   def save_checkpoint(self, label: str = None):
       """Save current world state"""
       if not label:
           label = f"day_{self.world.current_day}"
       
       filename = f"{label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.checkpoint"
       filepath = os.path.join(self.checkpoint_dir, filename)
       
       # Prepare state dictionary
       state = {
           'day': self.world.current_day,
           'people': self.world.people,
           'companies': self.world.companies,
           'buildings': self.world.buildings,
           'memes': self.world.memes,
           'market': self.world.market,
           'political_system': self.world.political_system,
           'stats': self.world.stats,
           'grid': self.world.grid
       }
       
       # Compress and save
       try:
           with open(filepath, 'wb') as f:
               compressed = zlib.compress(pickle.dumps(state))
               f.write(compressed)
           
           logger.info(f"Checkpoint saved: {filename}")
           self.checkpoints.append(filename)
           
           # Remove old checkpoints if exceeding limit
           if len(self.checkpoints) > MAX_CHECKPOINTS:
               oldest = self.checkpoints.pop(0)
               os.remove(os.path.join(self.checkpoint_dir, oldest))
               
       except Exception as e:
           logger.error(f"Failed to save checkpoint: {e}")
   
   def load_checkpoint(self, filename: str):
       """Load world state from checkpoint"""
       filepath = os.path.join(self.checkpoint_dir, filename)
       
       if not os.path.exists(filepath):
           logger.error(f"Checkpoint not found: {filename}")
           return False
       
       try:
           with open(filepath, 'rb') as f:
               compressed = f.read()
               state = pickle.loads(zlib.decompress(compressed))
           
           # Restore state
           self.world.current_day = state['day']
           self.world.people = state['people']
           self.world.companies = state['companies']
           self.world.buildings = state['buildings']
           self.world.memes = state['memes']
           self.world.market = state['market']
           self.world.political_system = state['political_system']
           self.world.stats = state['stats']
           self.world.grid = state['grid']
           
           logger.info(f"Checkpoint loaded: {filename} (Day {self.world.current_day})")
           return True
           
       except Exception as e:
           logger.error(f"Failed to load checkpoint: {e}")
           return False
   
   def list_checkpoints(self):
       """List available checkpoints"""
       self.load_checkpoint_list()
       
       if not self.checkpoints:
           print("No checkpoints available")
           return
       
       print("\nAvailable checkpoints:")
       for i, checkpoint in enumerate(self.checkpoints):
           # Extract info from filename
           parts = checkpoint.split('_')
           if len(parts) >= 2:
               label = '_'.join(parts[:-2])
               timestamp = parts[-2] + '_' + parts[-1].replace('.checkpoint', '')
               print(f"{i+1}. {label} - {timestamp}")
           else:
               print(f"{i+1}. {checkpoint}")

# ============= MAIN SIMULATION CONTROLLER =============

class SimulationController:
   """Main simulation orchestrator"""
   
   def __init__(self):
       self.world = World()
       self.visualizer = Visualizer(self.world)
       self.checkpoint_manager = CheckpointManager(self.world)
       self.running = False
       self.target_days = 1000
       self.last_checkpoint_day = 0
   
   def run(self, days: int = None):
       """Run simulation for specified number of days"""
       if days:
           self.target_days = days
       
       self.running = True
       start_day = self.world.current_day
       
       logger.info(f"Starting simulation for {self.target_days} days")
       
       try:
           while self.running and self.world.current_day < start_day + self.target_days:
               # Simulate one day
               self.world.simulate_day()
               
               # Update graphs
               if ENABLE_GRAPHS and self.world.current_day % GRAPH_UPDATE_FREQUENCY == 0:
                   self.visualizer.update_plots()
               
               # Auto checkpoint
               if AUTO_SAVE and self.world.current_day - self.last_checkpoint_day >= CHECKPOINT_FREQUENCY:
                   self.checkpoint_manager.save_checkpoint()
                   self.last_checkpoint_day = self.world.current_day
               
               # Check for simulation end conditions
               if len(self.world.people) == 0:
                   logger.warning("Population extinct - ending simulation")
                   break
               
       except KeyboardInterrupt:
           logger.info("Simulation interrupted by user")
       except Exception as e:
           logger.error(f"Simulation error: {e}")
           raise
       finally:
           self.running = False
           
           # Final statistics
           self.print_final_stats()
           
           # Save final plots
           if ENABLE_GRAPHS:
               self.visualizer.save_plots()
   
   def print_final_stats(self):
       """Print summary statistics"""
       stats = self.world.stats
       
       print("\n" + "="*60)
       print("SIMULATION SUMMARY")
       print("="*60)
       print(f"Days simulated: {self.world.current_day}")
       print(f"Final population: {len(self.world.people)}")
       print(f"Total births: {stats['births']}")
       print(f"Total deaths: {stats['deaths']}")
       print(f"Companies founded: {stats['companies_founded']}")
       print(f"Companies failed: {stats['companies_failed']}")
       print(f"Buildings constructed: {stats['buildings_constructed']}")
       
       if stats['prime_discoveries']:
           print(f"\nHighest prime discovered: {max(stats['prime_discoveries'].keys())}")
           print(f"Total primes discovered: {len(stats['prime_discoveries'])}")
       
       if stats['gini']:
           print(f"\nFinal Gini coefficient: {stats['gini'][-1]:.3f}")
       
       if stats['happiness']:
           print(f"Average happiness: {stats['happiness'][-1]:.1f}")
       
       if stats['knowledge']:
           print(f"Average knowledge: {stats['knowledge'][-1]:.2f} primes")
       
       print("\nActive memes: {}".format(len(self.world.memes)))
       print("Active companies: {}".format(len(self.world.companies)))
       
       # Find interesting individuals
       if self.world.people:
           richest = max(self.world.people.values(), key=lambda p: p.resources)
           smartest = max(self.world.people.values(), key=lambda p: len(p.known_primes))
           happiest = max(self.world.people.values(), key=lambda p: p.happiness)
           
           print("\nNotable individuals:")
           print(f"Richest: {richest.resources:.0f} resources")
           print(f"Most knowledgeable: {len(smartest.known_primes)} primes known")
           print(f"Happiest: {happiest.happiness:.1f} happiness")
       
       print("="*60)

# ============= COMMAND LINE INTERFACE =============

def main():
   """Main entry point with CLI arguments"""
   parser = argparse.ArgumentParser(
       description='Prime Society Simulator - A socio-economic simulation based on prime numbers'
   )
   
   parser.add_argument(
       '--days', 
       type=int, 
       default=1000,
       help='Number of days to simulate (default: 1000)'
   )
   
   global INITIAL_POPULATION
   parser.add_argument(
       '--population',
       type=int,
       default=INITIAL_POPULATION,
       help=f'Initial population size (default: {INITIAL_POPULATION})'
   )
   
   parser.add_argument(
       '--load',
       type=str,
       help='Load simulation from checkpoint file'
   )
   
   parser.add_argument(
       '--list-checkpoints',
       action='store_true',
       help='List available checkpoints and exit'
   )
   
   parser.add_argument(
       '--no-graphs',
       action='store_true',
       help='Disable visualization graphs'
   )
   
   global AUTO_SAVE
   parser.add_argument(
       '--auto-save',
       type=bool,
       default=AUTO_SAVE,
       help='Enable automatic checkpointing'
   )
   
   parser.add_argument(
       '--log-level',
       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
       default='INFO',
       help='Set logging level'
   )
   
   parser.add_argument(
       '--seed',
       type=int,
       help='Random seed for reproducibility'
   )
   
   parser.add_argument(
       '--profile',
       action='store_true',
       help='Enable performance profiling'
   )
   
   args = parser.parse_args()
   
   # Configure logging
   logging.getLogger().setLevel(getattr(logging, args.log_level))
   
   # Set random seed if provided
   if args.seed is not None:
       random.seed(args.seed)
       np.random.seed(args.seed)
       logger.info(f"Random seed set to {args.seed}")
   
   # Override global settings   
   INITIAL_POPULATION = args.population
   ENABLE_GRAPHS = not args.no_graphs
   AUTO_SAVE = args.auto_save
   
   # Create simulation controller
   sim = SimulationController()
   
   # Handle checkpoint operations
   if args.list_checkpoints:
       sim.checkpoint_manager.list_checkpoints()
       return
   
   if args.load:
       if not sim.checkpoint_manager.load_checkpoint(args.load):
           print(f"Failed to load checkpoint: {args.load}")
           return
       print(f"Loaded checkpoint: {args.load}")
   
   # Run simulation
   if args.profile:
       import cProfile
       import pstats
       
       profiler = cProfile.Profile()
       profiler.enable()
       
       sim.run(args.days)
       
       profiler.disable()
       stats = pstats.Stats(profiler)
       stats.sort_stats('cumulative')
       stats.print_stats(20)
   else:
       sim.run(args.days)
   
   # Keep plots open if enabled
   if ENABLE_GRAPHS:
       try:
           plt.show()
       except:
           pass

# ============= EXAMPLE SCENARIOS =============

class Scenarios:
   """Predefined scenarios for testing different conditions"""
   
   @staticmethod
   def economic_boom(world: World):
       """Setup conditions for economic prosperity"""
       # Give everyone more resources
       for person in world.people.values():
           person.resources *= 3
           person.known_primes.update([2, 3, 5, 7])
       
       # Create several companies
       wealthy = [p for p in world.people.values() if p.resources > 1000]
       for person in wealthy[:10]:
           company = Company(person, f"Boom_Corp_{person.id[:8]}")
           world.companies[company.id] = company
       
       logger.info("Economic boom scenario initialized")
   
   @staticmethod
   def knowledge_society(world: World):
       """Setup a highly educated population"""
       for person in world.people.values():
           # Everyone knows first 10 primes
           primes = [p for p in range(2, 30) if is_prime(p)]
           person.known_primes.update(primes[:10])
           person.intelligence = min(200, person.intelligence * 1.5)
       
       logger.info("Knowledge society scenario initialized")
   
   @staticmethod
   def inequality_crisis(world: World):
       """Setup extreme inequality"""
       people_list = list(world.people.values())
       
       # Top 1% get 90% of resources
       top_1_percent = int(len(people_list) * 0.01)
       for i, person in enumerate(people_list):
           if i < top_1_percent:
               person.resources = 10000
           else:
               person.resources = 10
       
       logger.info("Inequality crisis scenario initialized")
   
   @staticmethod
   def cultural_revolution(world: World):
       """Create a powerful meme that changes society"""
       if world.people:
           leader = max(world.people.values(), key=lambda p: p.charisma)
           
           # Create revolutionary meme
           meme = Meme(leader, "Revolution")
           meme.transmissibility = 2.0  # Highly contagious
           
           # Strong effects on traits
           meme.trait_effects = {
               Trait.CONSERVATIVE_PROGRESSIVE: 50,
               Trait.HUMBLE_AMBITIOUS: 30,
               Trait.SHARING_EXPLOITING: -40
           }
           
           world.memes[meme.id] = meme
           
           # Infect initial carriers
           for person in random.sample(list(world.people.values()), 
                                      min(50, len(world.people))):
               meme.carriers.add(person.id)
           
           logger.info("Cultural revolution scenario initialized")

# ============= ANALYTICS MODULE =============

class Analytics:
   """Advanced analytics and pattern detection"""
   
   @staticmethod
   def analyze_social_mobility(world: World, days: int = 365):
       """Analyze social mobility over time"""
       if days > len(world.stats['population']):
           days = len(world.stats['population'])
       
       # Track resource percentiles over time
       mobility_data = []
       
       # This would require tracking individual wealth over time
       # Simplified version:
       if world.stats['gini']:
           recent_gini = world.stats['gini'][-days:]
           mobility = np.std(recent_gini)  # Higher variance = more mobility
           
           return {
               'mobility_index': mobility,
               'trend': 'increasing' if recent_gini[-1] > recent_gini[0] else 'decreasing'
           }
       
       return None
   
   @staticmethod
   def detect_dynasties(world: World):
       """Identify family dynasties"""
       dynasties = []
       
       for person in world.people.values():
           if 'parent1' not in person.family:
               # Potential dynasty founder
               descendants = Analytics._count_descendants(person, world)
               if descendants > 5:
                   total_wealth = Analytics._dynasty_wealth(person, world)
                   dynasties.append({
                       'founder': person.id,
                       'descendants': descendants,
                       'total_wealth': total_wealth,
                       'avg_knowledge': Analytics._dynasty_knowledge(person, world)
                   })
       
       return sorted(dynasties, key=lambda x: x['total_wealth'], reverse=True)
   
   @staticmethod
   def _count_descendants(person: Person, world: World) -> int:
       """Count all descendants of a person"""
       count = 0
       for key, child_id in person.family.items():
           if key.startswith('child_') and child_id in world.people:
               count += 1
               count += Analytics._count_descendants(world.people[child_id], world)
       return count
   
   @staticmethod
   def _dynasty_wealth(person: Person, world: World) -> float:
       """Calculate total wealth of a dynasty"""
       wealth = person.resources if person.is_alive else 0
       
       for key, child_id in person.family.items():
           if key.startswith('child_') and child_id in world.people:
               child = world.people[child_id]
               wealth += Analytics._dynasty_wealth(child, world)
       
       return wealth
   
   @staticmethod
   def _dynasty_knowledge(person: Person, world: World) -> float:
       """Calculate average knowledge in a dynasty"""
       knowledge = [len(person.known_primes)] if person.is_alive else []
       
       for key, child_id in person.family.items():
           if key.startswith('child_') and child_id in world.people:
               child = world.people[child_id]
               if child.is_alive:
                   knowledge.append(len(child.known_primes))
       
       return np.mean(knowledge) if knowledge else 0
   
   @staticmethod
   def identify_market_bubbles(world: World):
       """Detect potential market bubbles"""
       bubbles = []
       
       for number, price_history in world.market.price_history.items():
           if len(price_history) > 30:
               recent_prices = list(price_history)[-30:]
               
               # Calculate price acceleration
               price_change = (recent_prices[-1] - recent_prices[0]) / recent_prices[0]
               
               if price_change > 2.0:  # Price more than doubled in 30 days
                   # Check if it's justified by efficiency
                   efficiency = calculate_efficiency(number)
                   if recent_prices[-1] > efficiency * 100:
                       bubbles.append({
                           'number': number,
                           'current_price': recent_prices[-1],
                           'price_increase': price_change,
                           'overvaluation': recent_prices[-1] / (efficiency * 10)
                       })
       
       return bubbles
   
   @staticmethod
   def generate_narrative_events(world: World):
       """Identify interesting narrative events"""
       events = []
       
       # Rags to riches stories
       for person in world.people.values():
           if person.is_alive and len(person.memory) > 100:
               # Check if person went from poor to rich
               if person.resources > 5000:
                   # This would need memory tracking implementation
                   events.append({
                       'type': 'rags_to_riches',
                       'person': person.id,
                       'wealth': person.resources
                   })
       
       # Love stories
       for person in world.people.values():
           if person.relationships:
               best_rel = max(person.relationships.items(), key=lambda x: x[1])
               if best_rel[1] > 90:
                   events.append({
                       'type': 'true_love',
                       'person1': person.id,
                       'person2': best_rel[0],
                       'strength': best_rel[1]
                   })
       
       # Corporate empires
       for company in world.companies.values():
           if len(company.employees) > 50:
               events.append({
                   'type': 'corporate_empire',
                   'company': company.name,
                   'employees': len(company.employees),
                   'capital': company.capital
               })
       
       return events

# ============= EXPERIMENTAL FEATURES =============

class ExperimentalFeatures:
   """Advanced features for experimentation"""
   
   @staticmethod
   def enable_migration(world: World):
       """Enable inter-regional migration"""
       for person in world.people.values():
           if not person.is_alive:
               continue
           
           # Check if should migrate
           if person.happiness < 30 and random.random() < 0.01:
               # Find better region
               current_region = person.location.region
               new_region = random.choice([r for r in range(WORLD_REGIONS) if r != current_region])
               
               person.location.region = new_region
               person.location.district = random.randint(0, DISTRICTS_PER_REGION - 1)
               
               logger.debug(f"Person {person.id} migrated from region {current_region} to {new_region}")
   
   @staticmethod
   def enable_innovation_clusters(world: World):
       """Create innovation clusters where knowledge spreads faster"""
       # Find areas with high knowledge concentration
       knowledge_density = {}
       
       for region in range(WORLD_REGIONS):
           for district in range(DISTRICTS_PER_REGION):
               people_here = []
               for x in range(10):
                   for y in range(10):
                       cell = world.grid[region, district, x, y]
                       for person_id in cell['people']:
                           if person_id in world.people:
                               people_here.append(world.people[person_id])
               
               if people_here:
                   avg_knowledge = np.mean([len(p.known_primes) for p in people_here])
                   knowledge_density[(region, district)] = avg_knowledge
       
       # Boost learning in high-knowledge areas
       for (region, district), density in knowledge_density.items():
           if density > 5:  # High knowledge area
               for x in range(10):
                   for y in range(10):
                       cell = world.grid[region, district, x, y]
                       for person_id in cell['people']:
                           if person_id in world.people:
                               person = world.people[person_id]
                               # Accelerate learning
                               for prime, progress in person.learning_progress.items():
                                   person.learning_progress[prime] = progress * 1.2
   
   @staticmethod
   def enable_technological_revolutions(world: World):
       """Trigger technological revolutions at prime milestones"""
       highest_prime = max(world.stats['prime_discoveries'].keys()) if world.stats['prime_discoveries'] else 2
       
       # Revolution at prime milestones
       revolution_primes = [31, 61, 97, 127]  # 11th, 18th, 25th, 31st primes
       
       if highest_prime in revolution_primes:
           logger.info(f"TECHNOLOGICAL REVOLUTION! Prime {highest_prime} discovered!")
           
           # Boost all production efficiency
           for company in world.companies.values():
               company.efficiency *= 1.5
           
           # Spread knowledge
           for person in random.sample(list(world.people.values()), 
                                      min(100, len(world.people))):
               person.known_primes.add(highest_prime)
           
           # Economic boom
           world.market.prices = {k: v * 0.8 for k, v in world.market.prices.items()}

# ============= RUN SIMULATION =============

if __name__ == "__main__":
   print("""
   ╔══════════════════════════════════════════════════════════════╗
   ║                    PRIME SOCIETY SIMULATOR                   ║
   ║                                                              ║
   ║  A multi-generational socio-economic simulation where       ║
   ║  nutrition comes from prime numbers                         ║
   ╚══════════════════════════════════════════════════════════════╝
   """)
   
   main()