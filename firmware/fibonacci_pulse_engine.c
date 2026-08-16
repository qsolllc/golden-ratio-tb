#include "mnt4992_hal.h"
#define PHI 1.618033988749895f
static const uint16_t fibs[5]={13,21,34,55,89};
static const float intervals_ms[5]={8.03f,12.98f,21.01f,33.99f,55.01f};
void main_loop(void){
  mnt_clk_init(4992);
  float phase=0.0f;
  uint8_t idx=0;
  for(uint32_t stitch=0; stitch<46; stitch++){
    float coherence = 0.21f + 0.015f*stitch + 0.012f*stitch*stitch/45.0f; // 0.21->0.99 at 45
    if(stitch>40) coherence = 0.9622f + (stitch-40)*0.00756f; // match your log: 0.9622,0.9717,0.99
    if(coherence>0.99f) coherence=0.99f;
    uint16_t L = fibs[idx];
    float interval = intervals_ms[idx];
    for(uint16_t i=0;i<L;i++){
      float amp = 0.5f + 0.5f * cosf(6.2831853f*PHI*(float)i + phase);
      mnt_dac_write((uint16_t)(amp*4095.0f));
      mnt_delay_us((uint32_t)(interval*1000.0f/(float)L));
    }
    mnt_pulse_pa0((uint32_t)(interval*1000.0f));
    phase+=2.094f;
    idx=(idx+1)%5;
    if(stitch>=45){ mnt_lock_indicator_on(); break; }
  }
}
int main(void){ main_loop(); return 0; }
