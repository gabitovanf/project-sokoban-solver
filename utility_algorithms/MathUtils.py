class MathUtils:
    @staticmethod
    def find_min(input_list: list):
        min = input_list[0]
        min_index = 0
        for i in range(0, len(input_list), 1):
            current = input_list[i]
            if input_list[i] < min:
                min = current
                min_index = i

        return min, min_index
