# Prime Society Simulator

A multi-generational socio-economic simulation where society's nutrition comes from prime numbers.

## 🌟 Overview

Prime Society is a complex systems simulator that models an entire civilization where the fundamental resource is based on prime numbers. Instead of traditional food or energy, people survive by consuming numbers, with nutritional value determined by mathematical properties. This creates a unique economy where mathematical knowledge literally becomes power.

## Usage

```
# Basic run
python prime_society.py --days 1000

# With custom settings
python prime_society.py --days 5000 --population 2000 --no-graphs

# Load from checkpoint
python prime_society.py --load checkpoint_day_500.checkpoint --days 1000

# List available saves
python prime_society.py --list-checkpoints
```

## 📐 Core Mathematical Concepts

### The Prime Number Economy

The simulation's economy revolves around a fascinating mathematical principle:

#### Nutrition Function
```python
nutrition(n) = {
    0                           if n = 1
    position(n)                 if n is prime
    Σ(position(pi) × counti)    if n is composite
}
```

Where:
- `position(n)` returns the position of prime n in the sequence (2→1, 3→2, 5→3, 7→4...)
- For composite numbers, we sum the positions of all prime factors

**Examples:**
- nutrition(2) = 1 (first prime)
- nutrition(3) = 2 (second prime)
- nutrition(6) = nutrition(2×3) = 1 + 2 = 3
- nutrition(30) = nutrition(2×3×5) = 1 + 2 + 3 = 6

#### Weight Function
```python
weight(n) = {
    1                           if n = 1
    position(n)²                if n is prime
    Σ(position(pi) × counti)²   if n is composite
}
```

Weight represents the cost/difficulty of handling a number. It grows quadratically with prime position, making higher primes increasingly expensive to transport and store.

#### Efficiency Ratio
```python
efficiency(n) = nutrition(n) / weight(n)
```

This ratio determines which numbers are economically viable. Interestingly, this creates natural trade-offs:
- Small primes (2, 3, 5) are easy to handle but provide less nutrition
- Large primes offer more nutrition but become prohibitively expensive
- Certain composites (like 6, 30) can be more efficient than their prime factors

### Knowledge Prerequisites

A crucial mechanic is that **knowledge is cumulative** - you cannot learn prime P₇ without first knowing P₁ through P₆. This creates a natural technological progression where society must systematically discover each prime in sequence.

Learning difficulty scales as:
- **Cost**: position³ × 100 resources
- **Time**: position² days
- **Intelligence Required**: 30 + (position × 2)

## 🧬 The Personality System

Every person has 10 personality traits on a scale from -100 to +100:

| Trait | -100 (Left) | +100 (Right) | Impact |
|-------|-------------|--------------|---------|
| **Generosity/Greed** | Generous | Greedy | Pricing, charity, resource sharing |
| **Inventive/Imitative** | Inventive | Imitative | Innovation vs copying |
| **Diplomatic/Aggressive** | Diplomatic | Aggressive | Conflict resolution |
| **Humble/Ambitious** | Humble | Ambitious | Career drive, risk-taking |
| **Social/Pragmatic** | Social | Pragmatic | Relationship focus |
| **Sincere/Deceptive** | Sincere | Deceptive | Honesty, corruption |
| **Sharing/Exploiting** | Sharing | Exploiting | Cooperation vs exploitation |
| **Reflective/Impulsive** | Reflective | Impulsive | Decision-making speed |
| **Conservative/Progressive** | Conservative | Progressive | Change acceptance |
| **Materialist/Spiritual** | Materialist | Spiritual | Value priorities |

These traits are:
- **Inherited** from parents with ±20 variation
- **Modified** by cultural memes
- **Drive all decisions** - nothing is random, everything emerges from personality

## 🏃 Running the Simulation

### Basic Usage

```bash
# Run for 1000 days with default settings
python prime_society.py

# Run for 5000 days with larger population
python prime_society.py --days 5000 --population 2000

# Run without graphs for better performance
python prime_society.py --no-graphs

# Set random seed for reproducible runs
python prime_society.py --seed 42
```

### Checkpointing

The simulation automatically saves checkpoints every 100 days:

```bash
# List available checkpoints
python prime_society.py --list-checkpoints

# Load from a checkpoint
python prime_society.py --load day_500_20240101_120000.checkpoint

# Continue for 1000 more days from checkpoint
python prime_society.py --load checkpoint.file --days 1000
```

## 📊 Key Metrics

The simulation tracks numerous metrics in real-time:

- **Population**: Birth rate, death rate, age distribution
- **Economy**: GDP, Gini coefficient, market prices, company dynamics
- **Knowledge**: Average primes known, discovery rate, knowledge clusters
- **Social**: Average happiness, relationship networks, meme spread
- **Political**: Election results, corruption levels, policy effects

## 🔧 Customization Guide

### Modifying Game Balance

Key constants are at the top of the script for easy modification:

```python
# Economic balance
DAILY_ONE_PRODUCTION = 1.0  # Increase for easier game
NUTRITION_REQUIREMENT = 1.0  # Decrease for easier survival
PRIME_DISCOVERY_COST_MULTIPLIER = 100  # Decrease for faster progress

# Social dynamics
TRAIT_INHERITANCE_VARIANCE = 20  # Increase for more diverse children
CHILD_COST = 10 * 365 * 18  # Decrease for population growth

# Political system
ELECTION_CYCLES = {
    'block': 180,     # Days between block elections
    'quarter': 365,   # Days between quarter elections
    'district': 730,  # Days between district elections
    'region': 1095    # Days between regional elections
}
```

### Adding New Features

The modular architecture makes it easy to extend:

#### 1. New Personality Trait
```python
# In the Trait enum, add:
NEW_TRAIT = "new_trait_axis"  # -100 to +100

# In Person.__init__, add to _random_traits or _inherit_traits
# In decision methods, use: self.traits[Trait.NEW_TRAIT]
```

#### 2. New Economic Product
```python
# Modify calculate_nutrition() for special cases
def calculate_nutrition(n: int) -> float:
    if n == 42:  # Special number
        return calculate_nutrition(6) * 1.5  # Bonus nutrition
    # ... existing code
```

#### 3. New Meme Effects
```python
# In Meme.__init__, add custom effects:
if self.name == "Capitalism":
    self.trait_effects[Trait.GENEROSITY_GREED] = 30  # More greedy
    self.trait_effects[Trait.HUMBLE_AMBITIOUS] = 40  # More ambitious
```

#### 4. New Building Types
```python
# In Building.__init__, add:
if self.building_type == "university":
    # Boost learning for residents
    for resident in self.residents:
        resident.intelligence *= 1.1
```

### Performance Optimization

For large populations or long runs:

1. **Disable graphs**: Use `--no-graphs` flag
2. **Reduce interaction radius**: Modify `RELATIONSHIP_DISTANCE_THRESHOLD`
3. **Limit market depth**: Reduce number of products checked in `_phase_market()`
4. **Batch processing**: Process people in chunks rather than individually

### Creating Scenarios

Add custom scenarios in the `Scenarios` class:

```python
@staticmethod
def custom_scenario(world: World):
    """Your scenario description"""
    # Modify world state
    for person in world.people.values():
        person.known_primes.add(11)  # Everyone knows 11
        person.resources *= 2  # Double starting resources
    
    # Create specific conditions
    # Add companies, memes, buildings, etc.
```

## 🎮 Interesting Experiments

1. **Knowledge Monopoly**: What happens if one person learns many primes while others know few?
2. **Cultural Revolution**: Create a powerful meme with extreme trait modifications
3. **Economic Collapse**: Set very high prime discovery costs
4. **Utopia Attempt**: Give everyone high resources and knowledge
5. **Dynasty Building**: Track families across generations

## 📈 Emergent Behaviors

The simulation produces fascinating emergent patterns:

- **Gentrification**: Wealthy individuals naturally cluster, driving up local prices
- **Knowledge Cascades**: Breakthroughs in prime discovery trigger economic booms
- **Cultural Cycles**: Memes rise, spread, and fade naturally
- **Inequality Dynamics**: Wealth tends to concentrate without intervention
- **Innovation Clusters**: High-knowledge areas accelerate learning

## 🐛 Known Limitations

- Population > 10,000 may cause performance issues
- Market matching is simplified (no partial fills)
- Spatial movement is limited (no inter-region migration by default)
- Political system is basic (no parties or coalitions)

## 📚 Mathematical Background

The prime-based economy creates interesting mathematical properties:

1. **Goldbach-like Trading**: Since even numbers > 2 can be expressed as sums of primes, traders seek efficient combinations
2. **Prime Gaps**: Large gaps between consecutive primes create natural scarcity
3. **Multiplicative Structure**: The factorization of composites creates complex supply chains
4. **Euler's Totient**: The number of useful combinations grows in interesting ways

## 🤝 Contributing

This is an experimental simulation designed for exploration and modification. Feel free to:
- Add new economic mechanics
- Implement missing features (parties, migration, etc.)
- Optimize performance
- Create visualization tools
- Design scenario packs

## 📜 License

This project is released into the public domain. Use it however you like!

## 🎯 Philosophy

Prime Society explores what happens when abstract mathematical concepts become concrete survival needs. It's a thought experiment about knowledge, scarcity, and emergence - where the laws of mathematics create the laws of economics, and simple rules generate complex societies.

The core insight: **In a world where knowledge of primes equals power, is meritocracy inevitable or does inherited advantage still dominate?**

---

*"In Prime Society, mathematics isn't just useful - it's nutritious."*