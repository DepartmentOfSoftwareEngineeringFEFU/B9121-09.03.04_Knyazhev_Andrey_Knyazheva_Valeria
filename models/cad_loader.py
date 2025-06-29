import ezdxf
from ezdxf.math import Vec3
from typing import List, Tuple


def load_dxf(filepath: str) -> List[Tuple[Vec3, Vec3]]:
    try:
        doc = ezdxf.readfile(filepath)
        modelspace = doc.modelspace()
        lines = []

        for entity in modelspace:
            if entity.dxftype() == 'LINE':
                start = Vec3(entity.dxf.start)
                end = Vec3(entity.dxf.end)
                lines.append((start, end))

            elif entity.dxftype() == '3DFACE':
                points = [
                    Vec3(entity.dxf.vtx0),
                    Vec3(entity.dxf.vtx1),
                    Vec3(entity.dxf.vtx2),
                    Vec3(entity.dxf.vtx3),
                ]
                for i in range(4):
                    start = points[i]
                    end = points[(i + 1) % 4]
                    lines.append((start, end))

        return lines

    except Exception as e:
        print(f"Ошибка загрузки DXF: {e}")
        return []
