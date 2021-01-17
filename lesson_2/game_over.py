from curses_tools import draw_frame, get_frame_size


GAME_OVER = """   _____                         ____                 
  / ____|                       / __ \                
 | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
 | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
 | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   
  \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   
                                                      
                                                      """


def game_over_draw(canvas):
    canvas_rows_size, canvas_columns_size = canvas.getmaxyx()
    row_size, column_size = get_frame_size(GAME_OVER)
    row = (canvas_rows_size - row_size) // 2
    column = (canvas_columns_size - column_size) // 2
    draw_frame(canvas, row, column, GAME_OVER)