import pygame
import ast

def run(rev_bias, layer_array, widths, first_indexes, n_indexes, p_indexes, sides, a, value):
    # run calculations beforehand
    # initialize
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    font = pygame.font.SysFont('arialms', 12)
    done = False
    clock = pygame.time.Clock()
    xn_start = 50
    yn_start = 150
    xn = 0
    xp = 0
    cxpos = xp
    junc_width = 400
    junc_height = 200
    numlayers = len(layer_array[1:, 0])
    actlayersum = 0
    i = 1
    while i != numlayers + 1:
        actlayersum += ast.literal_eval(layer_array[i, 4])  # in um
        i += 1
    i = 1
    props = []
    while i != numlayers + 1:
        props.append(ast.literal_eval(layer_array[i, 4]) / actlayersum)
        i += 1
    pix_deps = []
    for i in range(len(props)):
        pix_deps.append(props[i] * junc_width)

    pix_to_nm = (junc_width / actlayersum) / 1000  # 1 px for "pix_to_nm" nanometers

    n_high_color = (46, 151, 237)  # blue proportional to dopant concentration
    p_high_color = (21, 227, 150)  # green proportional to dopant concentration
    i = first_indexes[0]
    maxconn = ast.literal_eval(layer_array[i, 3])
    i += 1
    while i != first_indexes[0] - len(n_indexes):
        newcon = ast.literal_eval(layer_array[i, 3])
        if newcon > maxconn:
            maxconn = newcon
        i -= 1
    i = first_indexes[1]
    maxconp = ast.literal_eval(layer_array[i, 3])
    while i != first_indexes[1] + len(p_indexes):
        newcon = ast.literal_eval(layer_array[i, 3])
        if newcon > maxconp:
            maxconp = newcon
        i += 1
    j = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quitting the program
                done = True

        ######## draw base rectangles to show all layers ########
        def draw_base_regions():
            k = 1
            i = 0
            xn = xn_start
            nplus = font.render("n+", True, (255, 255, 255))
            nminus = font.render("n-", True, (255, 255, 255))
            # adjust rectangle color based on dopant concentration
            # draw rectangles
            # draw n layers
            while k != first_indexes[0] + 1:
                currcon = ast.literal_eval(layer_array[k, 3])
                n_color = n_high_color
                if currcon != maxconn:
                    n_color = (46, 151, 237 - (1 / 200) * (maxconn / currcon))
                    screen.blit(nminus, (xn + pix_deps[i] / 2 - 5, yn_start - 20))
                else:
                    screen.blit(nplus, (xn + pix_deps[i] / 2 - 5, yn_start - 20))
                pygame.draw.rect(screen, n_color, pygame.Rect(xn, yn_start, pix_deps[i], junc_height))
                xn += pix_deps[i] - 1
                pygame.draw.line(screen, (255, 255, 255), (xn - 1, yn_start), (xn - 1, yn_start + junc_height - 1))
                i += 1
                k += 1
            mid = xn
            xp = xn
            pplus = font.render("p+", True, (255, 255, 255))
            pminus = font.render("p-", True, (255, 255, 255))
            # draw p layers
            while k != first_indexes[1] + len(p_indexes):
                currcon = ast.literal_eval(layer_array[k, 3])
                p_color = p_high_color
                if currcon != maxconp:
                    p_color = (21, 227 - (1 / 200) * (maxconn / currcon), 150)
                    screen.blit(pminus, (xp + pix_deps[i] / 2 - 5, yn_start - 20))
                else:
                    screen.blit(pplus, (xp + pix_deps[i] / 2 - 5, yn_start - 20))
                pygame.draw.rect(screen, p_color, pygame.Rect(xp + 1, yn_start, pix_deps[i], junc_height))
                xp += pix_deps[i] - 1
                if i != len(pix_deps) - 1:
                    pygame.draw.line(screen, (255, 255, 255), (xp, yn_start), (xp, yn_start + junc_height - 1))
                i += 1
                k += 1

            return mid

        def sketch_all(value, full_dep):
            v = value
            screen.fill((0, 0, 0))
            nw_color = (237, 90, 69)
            pw_color = (231, 149, 75)

            # draw legends and misc
            info = "Full width: " + str(round(full_dep[v] / 1000, 2)) + " um | Reverse Bias -" + str(
                rev_bias[v]) + " V"
            info_text = font.render(info, True, (255, 255, 255))
            screen.blit(info_text, (xp + 70, yn_start + junc_height + 20))
            legend_red = font.render("red", True, nw_color)
            legend_plus = font.render("=  +", True, (255, 255, 255))
            screen.blit(legend_red, (xn + junc_width / 2 + 120, yn_start + junc_height + 20))
            screen.blit(legend_plus, (xn + junc_width / 2 + 140, yn_start + junc_height + 20))
            legend_blue = font.render("orange", True, pw_color)
            legend_minus = font.render("=  -", True, (255, 255, 255))
            screen.blit(legend_blue, (xn + junc_width / 2 + 120, yn_start + junc_height + 45))
            screen.blit(legend_minus, (xn + junc_width / 2 + 160, yn_start + junc_height + 45))
            scale_xstart = xp + 70
            scale_xend = scale_xstart + (pix_to_nm * 500)
            scale_y = yn_start + junc_height + 55
            pygame.draw.line(screen,(255,255,255),(scale_xstart, scale_y), (scale_xend, scale_y))
            scale_text = font.render("= 500 nm",True, (255,255,255))
            screen.blit(scale_text, (scale_xend + 13, scale_y - 8))

            # draw depletion rectangles
            mid = draw_base_regions()
            nw_xpos = mid + pix_to_nm * sides[v, 0]
            pw_xpos = mid + pix_to_nm * sides[v, 1]
            pygame.draw.rect(screen, nw_color, pygame.Rect(nw_xpos, yn_start, mid - nw_xpos, junc_height))
            pygame.draw.rect(screen, pw_color, pygame.Rect(mid, yn_start, pw_xpos - mid, junc_height))
            return v

        full_dep = widths[0:, 2] # total depletion widths

        if a is False: # no discrete adjustment, sweep loop
            if j != len(full_dep): # this is actually a loop
                v = sketch_all(j,full_dep)
                j += 1
            else:
                done = True
        else: # adjustment. runs once
            j = int(value)*2
            v = sketch_all(j,full_dep)
            done = True

        pygame.display.flip()  # update
        clock.tick(60)  # refresh every 1/60 sec