from . import Base

from sqlalchemy import Boolean, Column, Float, Integer, String

import enum, sqlalchemy


class LevelType(enum.Enum):
    NUMBER = enum.auto()
    SOULBOUND = enum.auto()
    UNASSIGNED = enum.auto()

class Equip(Base):
    __tablename__ = 'equip'

    id: int = Column(Integer, primary_key=True)
    key: str = Column(String, primary_key=True)

    last_updated: float = Column(Float, nullable=False)
    owner: str = Column(String)
    tradable: bool = Column(Boolean, nullable=False)
    type: str = Column(String, nullable=False)

    level: int = Column(Integer)
    level_type: LevelType = Column(sqlalchemy.Enum(LevelType), nullable=False)

    category: str = Column(String, nullable=False)
    condition_current: int = Column(Integer, nullable=False)
    condition_max: int = Column(Integer, nullable=False)
    potency_level: int = Column(Integer, nullable=False)
    potency_xp_current: int = Column(Integer)
    potency_xp_max: int = Column(Integer)
    
    physical_damage: float = Column(Float)
    physical_damage_type: str = Column(String)
    strike_1: str = Column(String)
    strike_2: str = Column(String)

    # main stats
    attack_accuracy: float = Column(Float)
    attack_crit_chance: float = Column(Float)
    attack_crit_damage: float = Column(Float)
    attack_speed: float = Column(Float)
    block_chance: float = Column(Float)
    burden: float = Column(Float)
    casting_speed: float = Column(Float)
    counter_parry: float = Column(Float)
    counter_resist: float = Column(Float)
    evade_chance: float = Column(Float)
    hp_bonus: float = Column(Float)
    interference: float = Column(Float)
    magic_accuracy: float = Column(Float)
    magic_damage: float = Column(Float)
    magical_mitigation: float = Column(Float)
    mana_conservation: float = Column(Float)
    parry_chance: float = Column(Float)
    physical_mitigation: float = Column(Float)
    resist_chance: float = Column(Float)
    spell_crit_damage: float = Column(Float)

    # spell damage
    cold_spell_dmg: float = Column(Float)
    dark_spell_dmg: float = Column(Float)
    elec_spell_dmg: float = Column(Float)
    fire_spell_dmg: float = Column(Float)
    holy_spell_dmg: float = Column(Float)
    wind_spell_dmg: float = Column(Float)

    # proficiency
    deprecating_prof: float = Column(Float)
    divine_prof: float = Column(Float)
    elemental_prof: float = Column(Float)
    forbidden_prof: float = Column(Float)
    supportive: float = Column(Float)

    # mitigations
    crushing: float = Column(Float)
    piercing: float = Column(Float)
    slashing: float = Column(Float)
    cold: float = Column(Float)
    dark: float = Column(Float)
    elec: float = Column(Float)
    fire: float = Column(Float)
    holy: float = Column(Float)
    wind: float = Column(Float)

    # pabs
    agility: float = Column(Float)
    dexterity: float = Column(Float)
    endurance: float = Column(Float)
    intelligence: float = Column(Float)
    strength: float = Column(Float)
    wisdom: float = Column(Float)

    # potencies
    coldproof: float = Column(Float)
    darkproof: float = Column(Float)
    elecproof: float = Column(Float)
    fireproof: float = Column(Float)
    holyproof: float = Column(Float)
    windproof: float = Column(Float)
    capacitor: float = Column(Float)
    juggernaut: float = Column(Float)
    butcher: float = Column(Float)
    fatality: float = Column(Float)
    overpower: float = Column(Float)
    swift_strike: float = Column(Float)
    annihilator: float = Column(Float)
    archmage: float = Column(Float)
    economizer: float = Column(Float)
    penetrator: float = Column(Float)
    spellweaver: float = Column(Float)

    # upgrades
    base_physical_damage: float = Column(Float)
    physical_hit_chance: float = Column(Float)
    physical_crit_chance: float = Column(Float)
    base_magical_damage: float = Column(Float)
    magical_hit_chance: float = Column(Float)
    magical_crit_chance: float = Column(Float)
    physical_defense: float = Column(Float)
    evade_chance: float = Column(Float)
    block_chance: float = Column(Float)
    parry_chance: float = Column(Float)
    elemental_magic_proficiency: float = Column(Float)
    divine_magic_proficiency: float = Column(Float)
    forbidden_magic_proficiency: float = Column(Float)
    depreciating_magic_proficiency: float = Column(Float)
    supportive_magic_proficiency: float = Column(Float)
    fire_spell_damage: float = Column(Float)
    cold_spell_damage: float = Column(Float)
    elec_spell_damage: float = Column(Float)
    wind_spell_damage: float = Column(Float)
    holy_spell_damage: float = Column(Float)
    dark_spell_damage: float = Column(Float)
    crushing_mitigation: float = Column(Float)
    slashing_mitigation: float = Column(Float)
    piercing_mitigation: float = Column(Float)
    fire_mitigation: float = Column(Float)
    cold_mitigation: float = Column(Float)
    elec_mitigation: float = Column(Float)
    wind_mitigation: float = Column(Float)
    holy_mitigation: float = Column(Float)
    dark_mitigation: float = Column(Float)
    strength: float = Column(Float)
    dexterity: float = Column(Float)
    agility: float = Column(Float)
    endurance: float = Column(Float)
    intelligence: float = Column(Float)
    wisdom: float = Column(Float)
    magical_mitigation: float = Column(Float)
    resist_chance: float = Column(Float)
    