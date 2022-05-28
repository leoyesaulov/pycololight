from .constants import (
    CUSTOM_EFFECT_COLOURS,
    CUSTOM_EFFECT_MODES,
    DEFAULT_EFFECTS,
)


class CycleSpeedException(Exception):
    pass


class ColourSchemeException(Exception):
    pass


class ColourException(Exception):
    pass


class ModeExecption(Exception):
    pass


class Effects:
    """
    Effects for cololight devices
    """

    def __init__(self, device) -> None:
        self._device = device
        self._default_effects = DEFAULT_EFFECTS.copy()

    def _cycle_speed_hex(self, cycle_speed, mode):
        if not 1 <= cycle_speed <= 32:
            raise CycleSpeedException
        if mode in [2]:
            # Mode 2 only has speeds 1, 2, 3, which are mapped differently to other modes
            cycle_speed_values = [3, 11, 19]
            cycle_speed_value = cycle_speed_values[min(3, cycle_speed) - 1]
        else:
            cycle_speed_value = list(reversed(range(33)))[cycle_speed - 1]

        cycle_speed_hex = "{:02x}".format(cycle_speed_value)
        return cycle_speed_hex

    def _colour_hex(self, colour_scheme, colour, mode):
        if colour_scheme not in self.custom_effect_colour_schemes():
            raise ColourSchemeException
        if colour not in self.custom_effect_colour_scheme_colours(colour_scheme):
            raise ColourException

        starting_decimal = CUSTOM_EFFECT_COLOURS[colour_scheme]["decimal"]
        colour_key = CUSTOM_EFFECT_COLOURS[colour_scheme]["colours"].index(colour)
        if mode in [13, 14, 15, 22, 23, 24]:
            # These modes have a lower starting decimal of 128
            starting_decimal = starting_decimal - 128
        colour_decimal = starting_decimal + colour_key
        colour_hex = "{:02x}".format(colour_decimal)
        return colour_hex

    def _mode_hex(self, mode):
        if not 1 <= mode <= len(CUSTOM_EFFECT_MODES):
            raise ModeExecption

        return CUSTOM_EFFECT_MODES[mode - 1]

    @property
    def default_effects(self) -> dict:
        """
        Returns a dict of default effects with names and command hex values for the device.
        """
        return self._default_effects

    def custom_effect_command(
        self, colour_scheme: str, colour: str, cycle_speed: int, mode: int
    ) -> str:
        """
        Returns command hex for custom effect.
        """
        cycle_speed_hex = self._cycle_speed_hex(int(cycle_speed), int(mode))
        colour_hex = self._colour_hex(colour_scheme, colour, int(mode))
        mode_hex = self._mode_hex(int(mode))

        if mode in [2]:
            # Mode 2 has bytes arranged differently to other modes
            custom_effect_hex = (
                f"{mode_hex[0]}{cycle_speed_hex}{colour_hex}{mode_hex[1]}"
            )
        else:
            custom_effect_hex = (
                f"{mode_hex[0]}{colour_hex}{cycle_speed_hex}{mode_hex[1]}"
            )

        return custom_effect_hex

    def custom_effect_colour_schemes(self) -> list:
        """
        Returns a list of the available colour schemes for custom efects.
        """
        return list(CUSTOM_EFFECT_COLOURS.keys())

    def custom_effect_colour_scheme_colours(self, colour_scheme) -> list:
        """
        Returns a list of the available colours for a given colour schemes for custom efects.
        """
        return list(filter(None, CUSTOM_EFFECT_COLOURS[colour_scheme]["colours"]))
