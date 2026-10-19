// Diagnostic-only addition to libretro.cpp. Does not alter emulation.
extern "C" RETRO_API unsigned retro_test_read_rom_byte(unsigned address)
{
    uint8 *p = Memory.Map[(address & 0xffffff) >> MEMMAP_SHIFT];
    if (p >= (uint8 *) CMemory::MAP_LAST)
        return p[address & 0xffff];
    return 0x100;
}
