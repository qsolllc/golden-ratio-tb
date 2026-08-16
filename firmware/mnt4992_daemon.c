#define _GNU_SOURCE
#include "mnt4992_daemon.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <pthread.h>
#include <errno.h>
#include <time.h>

#define MNT4992_MMIO_BASE 0x40000000UL
#define MMIO_SIZE 0x1000

struct mnt4992_dev {
    int fd;
    volatile uint32_t *base;
    pthread_mutex_t lock;
    int ref_count;
};

static inline uint32_t read_reg(volatile uint32_t *base, uint32_t off){ return base[off>>2]; }
static inline void write_reg(volatile uint32_t *base, uint32_t off, uint32_t val){ base[off>>2]=val; }

mnt4992_dev_t* mnt4992_open(const char *device_path) {
    int fd = open(device_path, O_RDWR | O_SYNC);
    if (fd < 0) return NULL;
    void *map = mmap(NULL, MMIO_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, MNT4992_MMIO_BASE);
    if (map == MAP_FAILED) { close(fd); return NULL; }
    mnt4992_dev_t *dev = calloc(1, sizeof(mnt4992_dev_t));
    if (!dev) { munmap(map, MMIO_SIZE); close(fd); return NULL; }
    dev->fd = fd; dev->base = (volatile uint32_t *)map;
    pthread_mutex_init(&dev->lock, NULL); dev->ref_count = 1;
    return dev;
}

void mnt4992_close(mnt4992_dev_t *dev) {
    if (!dev) return;
    pthread_mutex_lock(&dev->lock);
    if (--dev->ref_count > 0) { pthread_mutex_unlock(&dev->lock); return; }
    pthread_mutex_unlock(&dev->lock);
    pthread_mutex_destroy(&dev->lock);
    munmap((void *)dev->base, MMIO_SIZE);
    close(dev->fd);
    free(dev);
}

mnt4992_state_t mnt4992_get_state(mnt4992_dev_t *dev) {
    if (!dev) return MNT4992_STATE_ZEROIZED;
    pthread_mutex_lock(&dev->lock);
    uint32_t ssr = read_reg(dev->base, 0x00);
    pthread_mutex_unlock(&dev->lock);
    return (mnt4992_state_t)(ssr & 0x0F);
}

uint32_t mnt4992_get_faults(mnt4992_dev_t *dev) {
    if (!dev) return 0xFFFFFFFF;
    pthread_mutex_lock(&dev->lock);
    uint32_t bmr = read_reg(dev->base, 0x08);
    pthread_mutex_unlock(&dev->lock);
    return bmr;
}

bool mnt4992_request_sealing(mnt4992_dev_t *dev) {
    if (!dev) return false;
    pthread_mutex_lock(&dev->lock);
    uint32_t cur = read_reg(dev->base, 0x00);
    if ((cur & 0x0F) != MNT4992_STATE_RUNNING) { pthread_mutex_unlock(&dev->lock); return false; }
    write_reg(dev->base, 0x00, MNT4992_STATE_SEALING);
    uint32_t check = read_reg(dev->base, 0x00);
    bool ok = ((check & 0x0F) == MNT4992_STATE_SEALING);
    pthread_mutex_unlock(&dev->lock);
    return ok;
}

bool mnt4992_request_quarantine(mnt4992_dev_t *dev) {
    if (!dev) return false;
    pthread_mutex_lock(&dev->lock);
    uint32_t cur = read_reg(dev->base, 0x00);
    if ((cur & 0x0F) != MNT4992_STATE_SEALING) { pthread_mutex_unlock(&dev->lock); return false; }
    write_reg(dev->base, 0x00, MNT4992_STATE_QUARANTINE);
    uint32_t check = read_reg(dev->base, 0x00);
    bool ok = ((check & 0x0F) == MNT4992_STATE_QUARANTINE);
    pthread_mutex_unlock(&dev->lock);
    return ok;
}

void mnt4992_enter_highz(mnt4992_dev_t *dev, uint32_t ns_plz, uint32_t ns_pzh) {
    if (!dev) return;
    pthread_mutex_lock(&dev->lock);
    write_reg(dev->base, 0x04, read_reg(dev->base, 0x04) | 0x1);
    usleep(ns_plz/1000 + 1);
    if (read_reg(dev->base, 0x08) & 0x1) { /* fault */ }
    write_reg(dev->base, 0x04, read_reg(dev->base, 0x04) & ~0x1);
    usleep(ns_pzh/1000 + 1);
    pthread_mutex_unlock(&dev->lock);
}

void mnt4992_exit_highz(mnt4992_dev_t *dev) {
    if (!dev) return;
    pthread_mutex_lock(&dev->lock);
    write_reg(dev->base, 0x04, read_reg(dev->base, 0x04) & ~0x1);
    pthread_mutex_unlock(&dev->lock);
}

bool mnt4992_run_attestation(mnt4992_dev_t *dev, const uint8_t *expected_root) {
    (void)dev; (void)expected_root;
    return true; // placeholder
}

void mnt4992_kick_watchdog(mnt4992_dev_t *dev) {
    if (!dev) return;
    pthread_mutex_lock(&dev->lock);
    write_reg(dev->base, 0x34, 0xDEADBEEF);
    pthread_mutex_unlock(&dev->lock);
}
