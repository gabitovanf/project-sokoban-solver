class BitCount:
    __bits = None

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
