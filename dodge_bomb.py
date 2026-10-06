import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:    (0, -5),
    pg.K_DOWN:  (0, +5),
    pg.K_LEFT:  (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def gameover(screen:pg.Surface) -> None:
    black_sfc = pg.Surface((WIDTH, HEIGHT))
    black_sfc.fill((0, 0, 0))
    black_sfc.set_alpha(150)

    font = pg.font.Font(None, 80)
    txt_sfc = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt_sfc.get_rect(center=(WIDTH//2, HEIGHT//2))

    left_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.0)
    left_rct = left_img.get_rect(center=(WIDTH//2 - 200, HEIGHT//2 ))

    right_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.0)
    right_rct = right_img.get_rect(center=(WIDTH//2 + 200, HEIGHT//2 ))
    
    screen.blit(black_sfc, (0, 0))
    screen.blit(txt_sfc, txt_rct)
    screen.blit(right_img, right_rct)
    screen.blit(left_img,left_rct)

    pg.display.update()
    pg.time.wait(5000)


def init_bb_imgs() -> tuple[list[pg.Surface],list[int]]:
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]

    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs


def check_bound(rect:pg.Rect) -> tuple[bool,bool]:
    yoko,tate = True,True
    if rect.left < 0 or WIDTH < rect.right:
        yoko=False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate=False
    return yoko,tate


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    kk_base = pg.image.load("fig/3.png")

    left = kk_base
    right = pg.transform.flip(kk_base, True, False)

    kk_imgs = {
        (-5, 0): pg.transform.rotozoom(left, 0, 0.9),     # 左
        (-5,-5): pg.transform.rotozoom(left, -45, 0.9),   # 左上
        (-5,+5): pg.transform.rotozoom(left, 45, 0.9),    # 左下
        (+5, 0): pg.transform.rotozoom(right, 0, 0.9),     # 右
        (+5,-5): pg.transform.rotozoom(right, 45, 0.9),   # 右上
        (+5,+5): pg.transform.rotozoom(right, -45, 0.9),    # 右下
        (0, -5): pg.transform.rotozoom(right, 90, 0.9),   # 上
        (0, +5): pg.transform.rotozoom(right, -90, 0.9),    # 下
        (0, 0): pg.transform.rotozoom(left, 0, 0.9),
    }
    return kk_imgs


def main():
    kk_imgs = get_kk_imgs()
    bb_imgs, bb_accs = init_bb_imgs()
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx , vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:

        idx = min(tmr // 500, 9)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_img = bb_imgs[idx]
        old_center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = old_center
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        bb_rct.move_ip(avx,avy)
        screen.blit(bb_img, bb_rct)
        mv_tuple = (sum_mv[0], sum_mv[1])
        if mv_tuple not in kk_imgs:
            mv_tuple = (0, 0)
        kk_img = kk_imgs[mv_tuple]
        screen.blit(kk_img, kk_rct)

        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
