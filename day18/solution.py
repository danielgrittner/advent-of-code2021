import sys
from typing import List, Tuple
import abc


class Node(object):
    parent: 'Node'
    
    def __init__(self, parent: 'Node') -> None:
        self.parent = parent
    
    @abc.abstractmethod
    def magnitude(self) -> int:
        return -1

    @abc.abstractmethod
    def _reduce_with_explosion(self, depth: int) -> 'Node':
        return

    @abc.abstractmethod
    def _reduce_with_split(self) -> Tuple[bool, 'Node']:
        return

    @abc.abstractmethod
    def get_str(self) -> str:
        return ""

    @abc.abstractmethod
    def copy(self) -> 'Node':
        return


class Pair(Node):
    left: Node
    right: Node

    def __init__(self, left: Node, right: Node, parent: Node=None) -> None:
        super(Pair, self).__init__(parent)
        self.left = left
        self.left.parent = self
        self.right = right
        self.right.parent = self

    def magnitude(self):
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def _explode(self) -> Node:
        # LEFT
        assert isinstance(self.left, RegularNumber)
        left_value = self.left.get_value()
        # We must propagate the left value to the left side
        current = self.parent
        previous = self
        while current is not None:
            if current.left != previous:
                # We found a downwards path!
                current = current.left
                while not isinstance(current, RegularNumber):
                    current = current.right
                current.value += left_value
                break
            
            previous = current
            current = current.parent

        # RIGHT
        assert isinstance(self.right, RegularNumber)
        right_value = self.right.get_value()
        # We must propagate the right value to the right side
        current = self.parent
        previous = self
        while current is not None:
            if current.right != previous:
                # We found a downwards path!
                current = current.right
                while not isinstance(current, RegularNumber):
                    current = current.left
                current.value += right_value
                break
            
            previous = current
            current = current.parent

        return RegularNumber(0)

    def _reduce_with_explosion(self, depth: int) -> Node:
        if depth == 4:
            return self._explode()
        # Left
        self.left = self.left._reduce_with_explosion(depth + 1)
        self.left.parent = self
        # Right
        self.right = self.right._reduce_with_explosion(depth + 1)
        self.right.parent = self
        return self

    def _reduce_with_split(self) -> Tuple[bool, 'Node']:
        did_split, self.left = self.left._reduce_with_split()
        self.left.parent = self
        if did_split:
            return True, self

        did_split, self.right = self.right._reduce_with_split()
        self.right.parent = self
        if did_split:
            return True, self
        
        return False, self

    def add(self, other: Node) -> 'Pair':
        new_pair = Pair(self, other)
        
        # Reduce new pair
        while True:
            new_pair = new_pair._reduce_with_explosion(0)
            did_split, new_pair = new_pair._reduce_with_split()
            if not did_split:
                break

        return new_pair

    def get_str(self) -> str:
        return f"[{self.left.get_str()}, {self.right.get_str()}]"

    def copy(self) -> 'Node':
        return Pair(self.left.copy(), self.right.copy())


class RegularNumber(Node):
    value: int

    def __init__(self, value: int, parent: Node=None) -> None:
        super(RegularNumber, self).__init__(parent)
        self.value = value

    def get_value(self) -> int:
        return self.value

    def magnitude(self) -> int:
        return self.value

    def _split(self) -> Tuple[bool, Node]:
        # Perform split
        left_val = self.value // 2
        left_node = RegularNumber(left_val)

        right_val = (self.value + 1) // 2
        right_node = RegularNumber(right_val)

        return True, Pair(left_node, right_node)

    def _reduce_with_explosion(self, _: int) -> 'Node':
        return self

    def _reduce_with_split(self) -> Tuple[bool, 'Node']:
        if self.value >= 10:
            return self._split()
        return False, self

    def get_str(self) -> str:
        return str(self.value)

    def copy(self) -> 'Node':
        return RegularNumber(self.value)
    

def parse_pair(pair: str) -> List[Pair]:
    stack = []
    for c in pair:
        if c.isdigit():
            stack.append(RegularNumber(int(c)))
        elif c == ']':
            assert len(stack) >= 2
            new_pair = Pair(stack[-2], stack[-1])
            stack = stack[:-2]
            stack.append(new_pair)
    assert len(stack) == 1, f"{len(stack)}"
    return stack[0]


def read_input(path: str) -> List[Pair]:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()
    return [parse_pair(line[:-1]) for line in file_content]


def solve1(snail_numbers: List[Pair]) -> int:
    current = snail_numbers[0]
    for i in range(1, len(snail_numbers)):
        current = current.add(snail_numbers[i])
    return current.magnitude()


def solve2(snail_numbers: List[Pair]) -> int:
    max_magnitude = 0

    for i in range(len(snail_numbers)):
        for j in range(i + 1, len(snail_numbers)):
            m1 = snail_numbers[i].copy().add(snail_numbers[j].copy()).magnitude()
            max_magnitude = max(max_magnitude, m1)
            
            m2 = snail_numbers[j].copy().add(snail_numbers[i].copy()).magnitude()
            max_magnitude = max(max_magnitude, m2)

    return max_magnitude


if __name__ == "__main__":
    input_path = sys.argv[1]
    l = read_input(input_path)
    print(solve1(l))
    l = read_input(input_path)
    print(solve2(l))