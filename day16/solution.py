import sys
from typing import List, Tuple
from bitarray import bitarray


def _parse_to_binary(hex_str: str) -> bitarray:
    return bitarray("".join(['{0:04b}'.format(int(h, 16)) for h in hex_str]))


def read_input(path: str) -> bitarray:
    with open(path, "r") as file_handle:
        file_content = file_handle.readlines()
        assert len(file_content) == 1
    return _parse_to_binary(file_content[0][:-1])


class PacketType:
    SUM_OPERATOR = 0
    PRODUCT_OPERATOR = 1
    MIN_OPERATOR = 2
    MAX_OPERATOR = 3
    LITERAL = 4
    GREATER_THAN_OPERATOR = 5
    LESS_THAN_OPERATOR = 6
    EQUAL_TO_OPERATOR = 7


def _bitarray_to_binary(b: bitarray) -> int:
    num = 0
    for bit in b:
        num <<= 1
        if bit:
            num |= 1
    return num


def _get_packet_version(packet: bitarray) -> int:
    return _bitarray_to_binary(packet[:3])


def _get_packet_type(packet: bitarray) -> int:
    return _bitarray_to_binary(packet[3:6])


def _get_literal_value(packet: bitarray) -> Tuple[int, int]:
    assert _get_packet_type(packet) == PacketType.LITERAL
    value = 0
    i = 6
    done = False
    while i < len(packet) and not done:
        if not packet[i]:
            # Group has a leading zero! Last group!
            done = True
        group = packet[i+1:i+5]
        value = (value << 4) | _bitarray_to_binary(group)
        i += 5
    return value, i


class OperatorLengthType:
    TOTAL_LENGTH = 0
    NUM_SUB_PACKETS = 1


def _get_length_type_id(packet: bitarray) -> int:
    assert _get_packet_type(packet) != PacketType.LITERAL
    return _bitarray_to_binary(packet[6:7])


def _get_length_type_total_length(packet: bitarray) -> int:
    return _bitarray_to_binary(packet[7:22])


def _get_length_type_num_sub_packets(packet: bitarray) -> int:
    return _bitarray_to_binary(packet[7:18])


class PacketNode:
    packet: bitarray
    children: List['PacketNode']

    def __init__(self, packet: bitarray, children: List['PacketNode'] = []) -> None:
        self.packet = packet
        self.children = children

    def evaluate(self) -> int:
        packet_type = _get_packet_type(self.packet)

        if packet_type == PacketType.LITERAL:
            return _get_literal_value(self.packet)[0]

        if packet_type == PacketType.SUM_OPERATOR:
            result = 0
            for child in self.children:
                result += child.evaluate()
            return result

        if packet_type == PacketType.PRODUCT_OPERATOR:
            assert len(self.children) > 0
            result = 1
            for child in self.children:
                result *= child.evaluate()
            return result

        if packet_type == PacketType.MIN_OPERATOR:
            assert len(self.children) > 0
            result = self.children[0].evaluate()
            for i in range(1, len(self.children)):
                result = min(result, self.children[i].evaluate())
            return result

        if packet_type == PacketType.MAX_OPERATOR:
            assert len(self.children) > 0
            result = self.children[0].evaluate()
            for i in range(1, len(self.children)):
                result = max(result, self.children[i].evaluate())
            return result

        if packet_type == PacketType.GREATER_THAN_OPERATOR:
            assert len(self.children) == 2
            return 1 if self.children[0].evaluate() > self.children[1].evaluate() else 0

        if packet_type == PacketType.LESS_THAN_OPERATOR:
            assert len(self.children) == 2
            return 1 if self.children[0].evaluate() < self.children[1].evaluate() else 0

        if packet_type == PacketType.EQUAL_TO_OPERATOR:
            assert len(self.children) == 2
            return 1 if self.children[0].evaluate() == self.children[1].evaluate() else 0

        raise ValueError(f"Unknown packet type: {packet_type}")

    def get_version_sum(self) -> int:
        res = _get_packet_version(self.packet)
        for child in self.children:
            res += child.get_version_sum()
        return res


def _build_packet_tree(packet: bitarray) -> Tuple[PacketNode, int]:
    if _get_packet_type(packet) == PacketType.LITERAL:
        _, end = _get_literal_value(packet)
        return PacketNode(packet[:end]), end
    
    if _get_length_type_id(packet) == OperatorLengthType.TOTAL_LENGTH:
        total_length = _get_length_type_total_length(packet)
        
        children = []
        
        length = 0
        i = 22
        while length < total_length:
            child, sub_packet_length = _build_packet_tree(packet[i:])
            children.append(child)
            length += sub_packet_length
            assert length <= total_length
            i += sub_packet_length

        return PacketNode(packet[:i], children), i
    else:
        num_sub_packets = _get_length_type_num_sub_packets(packet)
        
        children = []

        i = 18
        while len(children) < num_sub_packets:
            child, length = _build_packet_tree(packet[i:])
            children.append(child)
            i += length

        return PacketNode(packet[:i], children), i


def build_packet_tree(packet: bitarray) -> PacketNode:
    return _build_packet_tree(packet)[0]


def solve1(packet_tree: PacketNode) -> int:
    return packet_tree.get_version_sum()


def solve2(packet_tree: PacketNode) -> int:
    return packet_tree.evaluate()


if __name__ == "__main__":
    input_path = sys.argv[1]
    packet = read_input(input_path)
    packet_tree = build_packet_tree(packet)
    print(solve1(packet_tree))
    print(solve2(packet_tree))