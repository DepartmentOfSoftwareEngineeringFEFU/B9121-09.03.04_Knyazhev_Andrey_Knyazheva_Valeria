import random


def calculate_positions(wifi_data):
    positions = {}
    for worker_id in wifi_data:
        positions[worker_id] = (
            random.uniform(0, 30),
            random.uniform(0, 20),
            0
        )
    return positions
