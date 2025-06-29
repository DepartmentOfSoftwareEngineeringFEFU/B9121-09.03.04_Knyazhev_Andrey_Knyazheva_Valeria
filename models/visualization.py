import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Tuple, Dict
from ezdxf.math import Vec3


def create_3d_figure() -> Tuple[plt.Figure, Axes3D]:
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.grid(True)
    return fig, ax


def plot_dxf_lines(ax: Axes3D, lines: List[Tuple[Vec3, Vec3]]) -> None:
    for start, end in lines:
        ax.plot(
            [start.x, end.x],
            [start.y, end.y],
            [start.z, end.z],
            color='blue',
            linewidth=1
        )
    ax.set_zlim(0, 5)


def plot_workers(ax: Axes3D, workers: Dict[str, Tuple[float, float, float]]):
    for worker_id, (x, y, z) in workers.items():
        ax.scatter(
            x, y, z,
            color='red',
            s=100,
            label=f'Worker {worker_id}'
        )
        ax.text(x, y, z, worker_id, color='black')
