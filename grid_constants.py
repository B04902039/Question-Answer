grid_loc = []
player_offset = []


def init_grid_loc():
    x_interval = 0.08875
    x_offset = x_interval/4
    y_interval = 0.102
    y_offset = y_interval/2
    for i in range(8):
        grid_loc.append({'x': x_offset + 10*x_interval, 'y': y_offset + (8-i)*y_interval})
    for i in range(11):
        grid_loc.append({'x': x_offset + (10-i)*x_interval, 'y': y_offset/2})
    for i in range(7):
        grid_loc.append({'x': x_offset, 'y': y_offset + (i+1)*y_interval})
    for i in range(10):
        grid_loc.append({'x': x_offset + i*x_interval, 'y': y_offset + 8*y_interval})


def init_player_offset():
    x_sep = 1/40
    y_sep = 1/22
    player_offset.append({'x': 0, 'y': 0})
    player_offset.append({'x': x_sep, 'y': 0})
    player_offset.append({'x': x_sep*2, 'y': 0})
    player_offset.append({'x': 0, 'y': y_sep})
    player_offset.append({'x': x_sep, 'y': y_sep})
    player_offset.append({'x': x_sep*2, 'y': y_sep})

init_grid_loc()
init_player_offset()
