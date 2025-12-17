class Tower:
    def __init__(
        self,
        location: int,
        equipment_level,
        electricity_consumption: int,
        regulations: int,
    ):
        """
        ### Torre de telefonía.

        Params:
            location (int): Ubicación de la torre.
            equipment_level (int):  Nivel de equipamiento de la torre.
            electricity_consumption (int): Nivel de consumo eléctrico de la torre.
            regulations (int): Regulaciones de la torre.
        """
        self.location: int = location
        self.equipment_level: int = equipment_level
        self.electricity_consumption: int = electricity_consumption
        self.regulations = regulations
