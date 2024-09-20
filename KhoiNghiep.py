import heapq

# Định nghĩa Node để biểu diễn các điểm trên bản đồ
class Node:
    def __init__(self, position, parent=None):
        self.position = position  # Vị trí (x, y)
        self.parent = parent  # Node cha
        self.g = 0  # Chi phí từ điểm bắt đầu đến điểm này
        self.h = 0  # Ước tính chi phí từ điểm này đến điểm đích
        self.f = 0  # Tổng chi phí (g + h)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

# Hàm A* tìm lộ trình tối ưu
def astar(map, start, end):
    open_list = []
    closed_list = []

    start_node = Node(start)
    end_node = Node(end)
    heapq.heappush(open_list, start_node)

    # Các hướng di chuyển có thể (lên, xuống, trái, phải)
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Kiểm tra nếu đã đến đích
        if current_node == end_node:
            path = []
            while current_node is not None:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        # Tạo các node con từ các hướng di chuyển
        for new_position in directions:
            node_position = (current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1])

            if node_position[0] < 0 or node_position[0] >= len(map) or \
               node_position[1] < 0 or node_position[1] >= len(map[0]):
                continue

            # Nếu vị trí là tường hoặc cản trở thì bỏ qua
            if map[node_position[0]][node_position[1]] == -1:
                continue

            child = Node(node_position, current_node)
            if child in closed_list:
                continue

            # Tính chi phí g, h, f
            child.g = current_node.g + 1
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.f = child.g + child.h

            if any(open_node for open_node in open_list if child == open_node and child.g > open_node.g):
                continue

            heapq.heappush(open_list, child)

    return None  # Nếu không tìm được đường

# Ví dụ bản đồ bệnh viện với các trọng số khác nhau (-1 là tường, 1 là đường)
hospital_map = [
    [1, 1, 1, 1, -1, 1, 1],
    [1, -1, 1, 1, -1, 1, 1],
    [1, -1, 1, 1, 1, 1, 1],
    [1, 1, 1, -1, 1, -1, 1],
    [1, 1, 1, -1, 1, 1, 1]
]

# Điểm xuất phát (Bệnh viện) và đích (Hiện trường cấp cứu)
hospital_location = (0, 0)
emergency_location = (4, 6)

# Tìm đường đi tối ưu cho xe cứu thương
path = astar(hospital_map, hospital_location, emergency_location)

print("Lộ trình tối ưu từ bệnh viện đến hiện trường cấp cứu:")
print(path)
