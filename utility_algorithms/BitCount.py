class BitCount:
    __bits = None
    __bit_positions = None

    @staticmethod
    def __popcount0(mask):
        count = 0
        while (mask > 0):
            if mask & 1 > 0:
                count += 1
            mask >>= 1

        return count

    @staticmethod
    def __popcount1(mask):
        count = 0
        while (mask > 0):
            count += 1
            mask &= mask - 1

        return count
    
    @classmethod
    def __fill8Bits(cls):
        cls.__bits = list()
        for i in range(0, 255):
            cls.__bits.append(BitCount.__popcount1(i))

    @classmethod
    def __popcountUseCache(cls, mask):
        if cls.__bits == None:
            cls.__fill8Bits()

        count = 0
        while (mask > 0):
            count += cls.__bits[mask & 255]
            mask >>= 8

        return count

    @classmethod
    def popcount(cls, mask, mode:int = 0):
        if mode == 2: return BitCount.__popcount1(mask)
        if mode == 1: return BitCount.__popcount0(mask)
        return BitCount.__popcountUseCache(mask)

    # POSITIONS:
    @staticmethod
    def __popcollectposition0(mask, p_list = None):
        if p_list is None:
            p_list = []
        p = 0
        while (mask > 0):
            if mask & 1 > 0:
                p_list.append(p)
            p += 1
            mask >>= 1

        return p_list
    
    @classmethod
    def __fill8BitPositions(cls):
        bit_positions = list()
        for i in range(0, 255):
            bit_positions.append(BitCount.__popcollectposition0(i))
        cls.__bit_positions = bit_positions

    @classmethod
    def __popcollectpositionUseCache(cls, mask, p_list = None):
        if p_list is None:
            p_list = []
        if cls.__bit_positions == None:
            cls.__fill8BitPositions()

        start = 0
        while (mask > 0):
            p_list_chached = cls.__bit_positions[mask & 255]
            for i in range(0, len(p_list_chached), 1):
                p_list.append(start + p_list_chached[i])
            mask >>= 8
            start += 8

        return p_list
    
    @classmethod
    def get_positions(cls, mask, mode:int = 0, target_list = None) -> list:
        if mode == 1: return BitCount.__popcollectposition0(mask, target_list)
        return BitCount.__popcollectpositionUseCache(mask, target_list)
