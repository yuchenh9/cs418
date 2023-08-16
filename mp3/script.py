import sys
import json

grid_size = sys.argv[1] if len(sys.argv) > 1 else 1

def create_json(grid_size):
    triangles = []
    positions = []
    colors = []
    for y in range(grid_size + 1):
        y_coord = y / (grid_size + 1)
        for x in range(grid_size + 1):
            x_coord = x / (grid_size + 1)
            positions.append([x_coord - 0.5, y_coord - 0.5, -0.5])
            colors.append([y_coord, x_coord, 0.02, 1])
            if x != grid_size and y != grid_size:
                i = y * (grid_size + 1) + x
                triangles.extend([i + 1, i, i + (grid_size + 1)])
                triangles.extend([i + 1, i + (grid_size + 1), i + 1 + (grid_size + 1)])
                print(i)

    return {
        "triangles": triangles,
        "attributes": {
            "position": positions,
            "color": colors,
        },
    }

# Example usage
#grid_size = 5
json_data = create_json(grid_size)

# Write to output.json
with open('output.json', 'w') as file:
    json.dump(json_data, file, indent=4)
