#include "mnt4992_hal.h"

void kick_watchdog(void) {
#ifndef MNT4992_TEST_MODE
    if (MNT4992_HW) MNT4992_HW->WDT_KICK = 0xCAFE;
#endif
}

void enter_fatal_lockdown(void) {
#ifndef MNT4992_TEST_MODE
    if (MNT4992_HW) MNT4992_HW->SYS_LOCK = 0xDEAD;
#endif
    while (1) {
        compiler_barrier();
    }
}

bool verify_pullup_termination(void) {
#ifdef MNT4992_TEST_MODE
    return true;
#else
    return (MNT4992_HW && (MNT4992_HW->GPIO_STATUS & 0x1));
#endif
}

bool read_otp_333(uint8_t *out_digest) {
    if (!out_digest) return false;

#ifdef MNT4992_TEST_MODE
    for (int i = 0; i < 8; i++) {
        ((uint32_t *)out_digest)[i] = MNT4992_HW->OTP_SHADOW[i];
    }
    compiler_barrier();
    return true;
#else
    MNT4992_HW->OTP_CTRL = OTP_CTRL_READ_EN;
    delay_cycles(100);
    if (!(MNT4992_HW->OTP_CTRL & OTP_CTRL_DONE)) {
        MNT4992_HW->BMR |= BMR_OTP_READ_ERROR;
        return false;
    }
    for (int i = 0; i < 8; i++) {
        ((uint32_t *)out_digest)[i] = MNT4992_HW->OTP[i];
    }
    compiler_barrier();
    return true;
#endif
}
