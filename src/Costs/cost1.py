from src.Tower import Tower

def calculate_cost(tower: Tower, frequency):
    """
    Calcula el costo de asignar una frecuencia a una torre, basado en su nivel de equipamiento y otros factores.
    
    :param tower: La instancia de la clase Tower.
    :param frequency: La frecuencia que se quiere asignar a la torre.
    :return: El costo asociado a la asignación de la frecuencia.
    """
    base_cost = 100
    equipment_factor = tower.equipment_level * 10
    frequency_factor = frequency * 5
    total_cost = base_cost + equipment_factor + frequency_factor
    return total_cost
