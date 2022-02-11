import subprocess
from tkinter import *
from tkinter.font import Font
from visualization import main

# def threading():
#     t1 = Thread(target=main)
#     t1.start()

def start_game():
    root.destroy()
    subprocess.call("python main.py", shell=True)

def start_visual():
    # for widgets in root.winfo_children():
    #     widgets.destroy()
    # # sleep(5)
    # # main()
    # t1 = Thread(target=main, daemon=True)
    # t1.start()
    root.destroy()
    main()


root = Tk()
root.title("3D Visualisation")
# root.geometry("500x500")
root.resizable(width=False, height=False)

'''Buttons Properties'''
btn_width = 25
btn_height = 2

'''Fonts and Color'''
mainFont = Font(family = "Arial", size=20, weight="bold")
buttonFont = Font(family = "Arial", size=14, weight="bold")

blue = '#005eff'
red = '#fa4a6d'
milk_white = '#e8eef9'

'''Centering the the GUI Window'''
window_height = 500
window_width = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width/2) - (window_width/2))
y_coordinate = int((screen_height/2) - (window_height/2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

'''Label'''
welcome_label = Label(root, text="Welcome to 3D Visualisation", font=mainFont)
welcome_label.place(x=250, y=50, anchor="center")

'''Buttons'''
start_vis_btn = Button(root, text="Start 3D Visualisation", command=start_visual, borderwidth=0, height=btn_height, width=btn_width, font=buttonFont, bg=blue, fg=milk_white)
# start_vis_btn.configure()
start_vis_btn.place(x=250, y=150, anchor="center")

start_game_btn = Button(root, text="Start Game", command=start_game, borderwidth=0, height=btn_height, width=btn_width ,font=buttonFont, bg=blue, fg=milk_white)
start_game_btn.place(x=250, y=250, anchor="center")

quit_btn = Button(root, text="Quit", borderwidth=0, command=root.destroy, height=2, width=btn_width, font=buttonFont, bg=red, fg=milk_white)
quit_btn.place(x=250, y=350, anchor="center")


root.mainloop()