from __future__ import annotations

import math
import noise
from .setting import Setting, BoundedSetting
import pygame_menu
import pygame


class NoiseFunction():
    # TODO add the option to display the function as it is written
    FACTOR_MIN = 0
    FACTOR_MAX = 10
    OFFSET_MIN = -20
    OFFSET_MAX = abs(OFFSET_MIN)
    POW_MIN = 0
    POW_MAX = 2
    FUDGE_MIN = 0.5
    FUDGE_MAX = 1.5
    FUNCTION_ID = 0
    DEFAULT_WEIGHT = 1

    def __init__(self, *args, factor_x = 1, factor_y = 1, offset_x = 0, offset_y = 0, pow_x = 1, pow_y = 1, pow = 1, fudge = 1.2) -> None:
        self.id = NoiseFunction.FUNCTION_ID
        NoiseFunction.FUNCTION_ID += 1

        self.factor_x = BoundedSetting(*args, value=factor_x, name="Factor x", min = self.FACTOR_MIN, max=self.FACTOR_MAX, type="onchange")
        self.factor_y = BoundedSetting(*args, value=factor_y, name="Factor y", min = self.FACTOR_MIN, max=self.FACTOR_MAX, type="onchange")
        self.offset_x = BoundedSetting(*args, value=offset_x, name="Offset x", min = self.OFFSET_MIN, max=self.OFFSET_MAX, type="onchange")
        self.offset_y = BoundedSetting(*args, value=offset_y, name="Offset y", min = self.OFFSET_MIN, max=self.OFFSET_MAX, type="onchange")
        self.pow_x = BoundedSetting(*args, value=pow_x, name="Pow x", min = self.POW_MIN, max=self.POW_MAX, type="onchange", increment = 1)
        self.pow_y = BoundedSetting(*args, value=pow_y, name="Pow y", min = self.POW_MIN, max=self.POW_MAX, type="onchange", increment = 1)
        self.pow = BoundedSetting(*args, value=pow, name="Pow", min = self.POW_MIN, max=self.POW_MAX, type="onchange", increment = 1)
        self.fudge = BoundedSetting(*args, value=fudge, name="Fudge", min = self.FUDGE_MIN, max=self.FUDGE_MAX, type="onchange")
        
        self.settings: list[Setting] = []
        self.settings.append(self.factor_x)
        self.settings.append(self.factor_y)
        self.settings.append(self.offset_x)
        self.settings.append(self.offset_y)
        self.settings.append(self.pow_x)
        self.settings.append(self.pow_y)
        self.settings.append(self.pow)
        self.settings.append(self.fudge)

        self.menu: pygame_menu.Menu = None

    def function(self, x: float, y: float) -> tuple[float, float]:
        """
        Calculate the transformed coordinates based on the input x and y values.

        Parameters:
        x (float): The x-coordinate value.
        y (float): The y-coordinate value.

        Returns:
        tuple[float, float]: A tuple containing the transformed x and y coordinates.
        """
        _x = x * self.factor_x._value
        _y = y * self.factor_y._value

        try:
            _x = math.pow(_x, self.pow_x._value) # TODO figure cause of ValueError "math domain error" in math.pow
        except ValueError:
            print("math domain error!")
        try:
            _y = math.pow(_y, self.pow_y._value) # TODO figure cause of ValueError "math domain error" in math.pow
        except ValueError:
            print("math domain error!")

        _x += self.offset_x._value
        _y += self.offset_y._value

        return _x, _y

    def noise(self, x:float, y:float) -> float:
        """
        Calculate the noise value at the given coordinates (x, y) using Perlin noise.

        Parameters:
        x (float): The x-coordinate value.
        y (float): The y-coordinate value.

        Returns:
        float: The noise value at the specified coordinates, normalized to the range [0, 1].
        Raises:
        ValueError: If the noise value is not within the range [0, 1].
        """
        _x, _y = self.function(x, y)
        _noise = noise.snoise2(_x, _y)
        _noise = NoiseFunction._normalise(_noise)
        _noise *= self.fudge._value
        try:
            value = math.pow(_noise, self.pow._value) # TODO figure cause of ValueError "math domain error" in math.pow
        except ValueError:
            print("math domain error!")
            value = _noise

        value = pygame.math.clamp(value, 0, 1)
        if not(0 <= value <= 1):
            raise ValueError(f"noise value not in range [0, 1] {value}")
        return value
    
    def add_submenu(self, menu: pygame_menu.Menu, add_randomiser = False) -> pygame_menu.Menu:
        """
        Add a submenu to the specified menu for the NoiseFunction instance.

        Parameters:
        menu (pygame_menu.Menu): The menu to which the submenu will be added.
        add_randomiser (bool): Flag indicating whether to add a randomiser button to the submenu. Default is False.

        Returns:
        pygame_menu.Menu: The created submenu for the NoiseFunction instance.

        """
        # Create submenu
        self.menu = pygame_menu.Menu(
            width=menu.get_width(),
            height=menu.get_height(),
            position=(menu.get_position()[0], menu.get_position()[1], False),
            theme=menu.get_theme(),
            title=f"Function {self.id}" #TODO implement name updating
        )
        # Create the button in the parent menu that leads to the submenu
        self.hook_button = menu.add.button(f"Function {self.id}", self.menu) #TODO implement name updating

        # if wanted add Randomiser
        if add_randomiser:
            self.menu.add.button("Randomise", self.randomise)

        # Add setting controllers
        for setting in self.settings:
            setting.add_controller_to_menu(self.menu, randomiser=True)

        # Add a back button
        self.menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)

        return self.menu

    def randomise(self) -> None:
        """
        Randomise the values of all settings in the NoiseFunction instance using a Gaussian distribution.

        Parameters:
        None

        Returns:
        None
        """
        for setting in self.settings:
            setting.randomise_value(type="gauss")

    @classmethod
    def _normalise(cls, value) -> float:
        """
        Normalize the input value to the range [0, 1] using a linear transformation.

        This should only be used together with noise.snoise2(x, y) as this method returns values between -1 and 1 and we only want values between 0 and 1

        Parameters:
        value: The input value to be normalized.

        Returns:
        float: The normalized value within the range [0, 1].

        Raises:
        ValueError: If the normalized value is not within the range [0, 1].
        """
        value += 1
        value /= 2
        if not(0 <= value <= 1):
            raise ValueError(f"noise value not in range [0, 1] {value}")
        return value
    
    @classmethod
    def weigh(cls, x:float, y:float, functions: list[NoiseFunction], weights: list[float] = None) -> float:
        """
        Calculate the weighted average of noise values generated by multiple NoiseFunction instances at the given coordinates (x, y).

        Parameters:
        x (float): The x-coordinate value.
        y (float): The y-coordinate value.
        functions (list[NoiseFunction]): A list of NoiseFunction instances to calculate noise values from.
        weights (list[float], optional): A list of weights corresponding to each NoiseFunction instance. If not provided, defaults to equal weights for all functions.

        Returns:
        float: The weighted average noise value at the specified coordinates, normalized to the range [0, 1].

        Raises:
        ValueError: If the list of functions is empty or if the resulting noise value is not within the range [0, 1].
        """
        if not functions:
            raise ValueError("The list of functions cannot be empty.")

        if not weights:
            weights = []
        while len(weights) < len(functions):
            weights.append(cls.DEFAULT_WEIGHT)

        total_noise = 0
        weight_sum = 0
        for function, weight in zip(functions, weights):
            total_noise += function.noise(x, y) * weight
            weight_sum += weight
        value = total_noise / weight_sum
        
        if not(0 <= value <= 1):
            raise ValueError(f"noise value not in range [0, 1] {value}")

        return value
        