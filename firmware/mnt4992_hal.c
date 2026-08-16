#include "mnt4992_hal.h"
#include <stdio.h>
void mnt_clk_init(int c){ (void)c; }
void mnt_dac_write(uint16_t v){ (void)v; }
void mnt_delay_us(uint32_t us){ volatile uint32_t k=us*2; while(k--) __asm__("nop"); }
void mnt_pulse_pa0(uint32_t us){ printf("PA0 pulse %u us\n", us); }
void mnt_lock_indicator_on(void){ printf("LOCK anchor 42e34f88fca79abf coherence 0.99\n"); }
#ifdef __arm__
void mnt_wfi(void){ __asm__("wfi"); }
#else
void mnt_wfi(void){} // host: return, don't hang
#endif
