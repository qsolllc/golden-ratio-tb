#ifndef MNT4992_HAL_H
#define MNT4992_HAL_H
#include <stdint.h>
void mnt_clk_init(int clk_khz);
void mnt_dac_write(uint16_t val12);
void mnt_delay_us(uint32_t us);
void mnt_pulse_pa0(uint32_t us);
void mnt_lock_indicator_on(void);
void mnt_wfi(void);
float expf(float x);
float cosf(float x);
#endif
