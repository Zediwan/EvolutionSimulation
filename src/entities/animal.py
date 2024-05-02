from __future__ import annotations

import random

import pygame

import settings.colors
import settings.config
from dna.dna import DNA
from entities.organism import Organism
from world.tile import Tile


class Animal(Organism):
    @property
    def MAX_HEALTH(self) -> float:
        return 100

    @property
    def MAX_ENERGY(self) -> float:
        return 200

    @property
    def NUTRITION_FACTOR(self) -> float:
        return 1

    @property
    def REPRODUCTION_CHANCE(self) -> float:
        return 0.001

    @property
    def MIN_REPRODUCTION_HEALTH(self) -> float:
        return 0.5

    @property
    def MIN_REPRODUCTION_ENERGY(self) -> float:
        return 0.75

    animals_birthed: int = 0
    animals_died: int = 0

    def __init__(
        self,
        tile: Tile,
        shape: pygame.Rect | None = None,
        parent: Animal = None,
        dna: DNA = None,
    ):
        if not shape:
            shape = tile.rect.copy()

        if not dna:
            dna = DNA(settings.colors.BASE_ANIMAL_COLOR())

        super().__init__(
            tile,
            shape,
            self.MAX_HEALTH * pygame.math.lerp(0.2, 0.4, random.random()),
            self.MAX_ENERGY * pygame.math.lerp(0.2, 0.4, random.random()),
            dna,
        )

        self.parent: Animal | None = parent

    ########################## Main methods #################################
    def update(self):
        super().update()
        self.energy -= random.random() * 5

        DROWNING_DAMAGE = 10
        if self.tile.has_water:
            self.health -= DROWNING_DAMAGE

        if self.tile.has_plant() and self.wants_to_eat():
            self.attack(self.tile.plant)

        direction = self.think()

        if direction:
            self.enter_tile(direction)

        if self.can_reproduce() and random.random() <= self.REPRODUCTION_CHANCE:
            self.reproduce()

        if not self.is_alive():
            self.die()

    def think(self) -> Tile | None:
        if self.tile.has_plant():
            best_growth = self.tile.plant.health
            destination = None
        else:
            best_growth = 0
            destination = self.tile.get_random_neigbor(no_animal=True)

        ns = self.tile.get_neighbors()
        random.shuffle(ns)
        for n in ns:
            if n.has_animal():
                continue
            if not n.plant:
                continue
            if n.plant.health > 1.5 * best_growth:
                best_growth = n.plant.health
                destination = n

        return destination

    def draw(self):
        super().draw()

        pygame.draw.rect(pygame.display.get_surface(), self.color, self.shape)

    ########################## Tile #################################
    def enter_tile(self, tile: Tile):
        super().enter_tile(tile)
        if tile.has_animal():
            raise ValueError("Animal trying to enter a tile that is already occupied.")

        if self.tile:
            self.tile.remove_animal()

        self.tile = tile
        tile.add_animal(self)

        self.check_tile_assignment()

    def check_tile_assignment(self):
        if not self.tile:
            raise ValueError("Animal does not have a tile!")
        if self != self.tile.animal:
            raise ValueError("Animal-Tile assignment not equal.")

    ########################## Energy and Health #################################
    def die(self):
        super().die()
        Animal.animals_died += 1
        self.tile.remove_animal()

    def attack(self, organism_to_attack: Organism):
        assert (
            self.tile.is_neighbor(organism_to_attack.tile)
            or self.tile == organism_to_attack.tile
        ), "Organism to attack is not a neighbor or on own tile."
        organism_to_attack.get_attacked(self)

    def get_attacked(self, attacking_organism: Organism):
        super().get_attacked(attacking_organism)
        if not self.is_alive():
            attacking_organism.animals_killed += 1

    def wants_to_eat(self) -> bool:
        return self.energy_ratio() < 0.9 or self.health_ratio() < 0.9

    ########################## Reproduction #################################
    def reproduce(self):
        super().reproduce()
        unoccupied_neighbor = self.tile.get_random_neigbor(
            no_animal=True, no_water=True
        )
        if unoccupied_neighbor:
            REPRODUCTION_ENERGY_COST = self.MAX_ENERGY / 2
            self.energy -= REPRODUCTION_ENERGY_COST
            offspring = self.copy(unoccupied_neighbor)
            offspring.mutate()

    def copy(self, tile: Tile) -> Animal:
        super().copy(tile)
        Animal.animals_birthed += 1

        return Animal(tile, parent=self, dna=self.dna.copy())

    def mutate(self):
        super().mutate()
