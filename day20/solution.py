import sys
from typing import List, Tuple


LIGHT = 1
DARK = 0


def _make_img_sparse(img: List[List[int]]) -> Tuple[set, int, int]:
        x = len(img)
        y = len(img[0])
        img_sparse = set()

        for i in range(x):
            for j in range(y):
                if img[i][j] == LIGHT:
                    img_sparse.add((i, j))

        return img_sparse, x, y


class Image:
    def __init__(self, img: List[List[int]], img_enhancement_algorithm: List[int]) -> None:
        self.img, self.x, self.y = _make_img_sparse(img)
        self.infinity_pixel = DARK
        self.img_enhancement_algorithm = img_enhancement_algorithm

    def _get_pixel_value(self, i: int, j: int) -> int:
        if i < 0 or i >= self.x or j < 0 or j >= self.y:
            return self.infinity_pixel
        return LIGHT if (i, j) in self.img else DARK

    def _get_3x3(self, r: int, c: int) -> List[int]:        
        field = []

        for i in range(r-1, r+2):
            for j in range(c-1, c+2):
                field.append(self._get_pixel_value(i, j))

        return field

    def _get_algo_idx(self, field: List[int]) -> int:
        idx = 0
        for i, v in enumerate(field):
            idx += (1 << (8 - i)) * v
        return idx

    def _get_new_pixel_value(self, i: int, j: int) -> int:
        idx = self._get_algo_idx(self._get_3x3(i, j))
        return self.img_enhancement_algorithm[idx]

    def enhance(self) -> None:
        new_img = set()
        for i in range(-1, self.x + 1):
            for j in range(-1, self.y + 1):
                if self._get_new_pixel_value(i, j) == LIGHT:
                    new_img.add((i+1, j+1))

        self.img = new_img
        self.x += 2
        self.y += 2

        if self.infinity_pixel == DARK:
            self.infinity_pixel = self.img_enhancement_algorithm[0]
        else:
            assert self.infinity_pixel == LIGHT
            self.infinity_pixel = self.img_enhancement_algorithm[-1]

    def get_light_pixel(self) -> int:
        assert self.infinity_pixel != LIGHT
        return len(self.img)


def read_input(path: str) -> Image:
    parse = lambda c: LIGHT if c == '#' else DARK
    with open(path, "r") as file_handle:
        image_enhancement_algorithm = [parse(c) for c in file_handle.readline()[:-1]]
        file_handle.readline()  # Skip empty line
        input_img = [[parse(c) for c in line[:-1]] for line in file_handle.readlines()]
    return Image(input_img, image_enhancement_algorithm)


def solve1(img: Image) -> int:
    img.enhance()
    img.enhance()
    return img.get_light_pixel()


def solve2(img: Image) -> int:
    for _ in range(50):
        img.enhance()
    return img.get_light_pixel()


if __name__ == "__main__":
    input_path = sys.argv[1]
    print(solve1(read_input(input_path)))
    print(solve2(read_input(input_path)))