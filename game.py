from __future__ import annotations

from dataclasses import dataclass


START_COINS = 100
START_ENERGY = 40
BASE_STORAGE = 120
BASE_RATE_PER_HOUR = 18
MAX_ENERGY_BASE = 40
ENERGY_REGEN_SECONDS = 90

DAILY_QUESTS = [
    {"key": "tap_25", "title": "Tap 25 times", "description": "Charge the BitCore coin by tapping.", "reward": 75},
    {"key": "collect_1", "title": "Collect storage", "description": "Move mined coins from storage to wallet.", "reward": 90},
    {"key": "launch_1", "title": "Play Core Launch", "description": "Start one reactor launch round.", "reward": 120},
    {"key": "wheel_1", "title": "Spin the Wheel", "description": "Take one wheel risk.", "reward": 100},
]

ACHIEVEMENTS = [
    {"key": "first_tap", "title": "First Spark", "description": "Make your first tap.", "reward": 100},
    {"key": "tap_100", "title": "Core Clicker", "description": "Reach 100 tap-mined coins.", "reward": 250},
    {"key": "collector", "title": "Vault Runner", "description": "Collect storage 5 times.", "reward": 300},
    {"key": "launcher", "title": "Reactor Pilot", "description": "Play Core Launch 5 times.", "reward": 400},
    {"key": "rich_1000", "title": "First Thousand", "description": "Hold 1,000 coins.", "reward": 500},
    {"key": "ref_1", "title": "First Recruit", "description": "Invite 1 miner.", "reward": 250},
    {"key": "ref_5", "title": "Mining Crew", "description": "Invite 5 miners.", "reward": 900},
]

BOOSTERS = {
    "tap_x2": {"title": "Tap Overdrive", "description": "x2 tap power for 5 minutes.", "cost": 180, "minutes": 5},
    "mine_x2": {"title": "Mine Surge", "description": "x2 passive mining for 1 hour.", "cost": 260, "minutes": 60},
}

SKINS = {
    "classic": {"title": "Classic Core", "cost": 0},
    "gold": {"title": "Gold Core", "cost": 350},
    "plasma": {"title": "Plasma Core", "cost": 650},
    "diamond": {"title": "Diamond Core", "cost": 1200},
}

CHEST_REWARDS = [
    {"kind": "coins", "label": "+120 coins", "amount": 120, "weight": 35},
    {"kind": "coins", "label": "+250 coins", "amount": 250, "weight": 18},
    {"kind": "energy", "label": "+25 energy", "amount": 25, "weight": 24},
    {"kind": "booster", "label": "Tap Overdrive", "amount": 1, "weight": 15},
    {"kind": "coins", "label": "Jackpot +900", "amount": 900, "weight": 3},
]

TAP_LEVELS = [
    (1, "Spark Miner", 0, 1),
    (2, "Core Striker", 10_000_000, 2),
    (3, "Plasma Clicker", 25_000_000, 3),
    (4, "Vault Breaker", 50_000_000, 4),
    (5, "Neon Prospector", 90_000_000, 5),
    (6, "Circuit Baron", 150_000_000, 6),
    (7, "Reactor Lord", 250_000_000, 7),
    (8, "Quantum Driller", 400_000_000, 8),
    (9, "BitCore Master", 650_000_000, 9),
    (10, "Genesis Miner", 1_000_000_000, 10),
]


@dataclass(frozen=True)
class Upgrade:
    key: str
    title: str
    emoji: str
    description: str
    base_cost: int
    growth: float

    def cost(self, current_level: int) -> int:
        return int(self.base_cost * (self.growth ** max(current_level - 1, 0)))


UPGRADES = {
    "drill": Upgrade(
        key="drill",
        title="Plasma Drill",
        emoji="[D]",
        description="Increases passive coin mining.",
        base_cost=80,
        growth=1.75,
    ),
    "generator": Upgrade(
        key="generator",
        title="Bit Reactor",
        emoji="[R]",
        description="Unlocks higher mine tiers and boosts mining rate.",
        base_cost=120,
        growth=1.9,
    ),
    "storage": Upgrade(
        key="storage",
        title="Core Vault",
        emoji="[V]",
        description="Increases the maximum stored mined coins.",
        base_cost=70,
        growth=1.7,
    ),
}


def rate_per_hour(drill_level: int, generator_level: int) -> int:
    return BASE_RATE_PER_HOUR + (drill_level - 1) * 12 + (generator_level - 1) * 8


def storage_capacity(storage_level: int) -> int:
    return BASE_STORAGE + (storage_level - 1) * 90


def max_energy(generator_level: int) -> int:
    return MAX_ENERGY_BASE + (generator_level - 1) * 8


def tap_level_for(total_tapped: int) -> dict:
    current = TAP_LEVELS[0]
    next_level = None
    for level in TAP_LEVELS:
        if total_tapped >= level[2]:
            current = level
        elif next_level is None:
            next_level = level
            break

    level_number, title, required, power = current
    next_required = next_level[2] if next_level else required
    progress = 100 if not next_level else int(((total_tapped - required) / (next_required - required)) * 100)
    return {
        "level": level_number,
        "title": title,
        "required": required,
        "nextRequired": next_required,
        "progress": max(0, min(progress, 100)),
        "tapPower": power,
        "maxLevel": level_number == TAP_LEVELS[-1][0],
    }


def mine_tier(generator_level: int) -> str:
    if generator_level >= 8:
        return "Quantum Core"
    if generator_level >= 5:
        return "Neon Rift"
    if generator_level >= 3:
        return "Deep Circuit"
    return "Starter Shaft"
