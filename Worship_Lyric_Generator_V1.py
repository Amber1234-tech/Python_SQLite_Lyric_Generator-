# Amber Kuhn
# Date Start: 4/26/22
# Date Finish:
# Program: My Worship Lyric Generator

import tkinter as tk
import sqlite3
import tkinter.messagebox

DICT = {}


class GUI:

    def __init__(self):
        # Create main window and name it
        self.main_window = tk.Tk()

        # name the window and set the color
        self.main_window.title('Worship Lyric Generator')
        self.main_window['bg'] = 'light blue'

        # make the window full screen
        width = self.main_window.winfo_screenwidth()
        height = self.main_window.winfo_screenheight()
        self.main_window.geometry("%dx%d" % (width, height))

        # Set up frames
        self.top_left = tk.Frame(self.main_window, bg='beige', highlightbackground='light blue',
                                 highlightthickness=10, borderwidth=3, relief='raised')
        self.top_mid = tk.Frame(self.main_window, bg='beige', highlightbackground='light blue',
                                highlightthickness=10, borderwidth=3, relief='raised')
        self.top_right = tk.Frame(self.main_window)
        self.mid_left = tk.Frame(self.main_window, background='light blue')
        self.mid_right = tk.Frame(self.main_window, background='light blue', highlightbackground='light blue',
                                  highlightthickness=10)
        self.bottom_frame = tk.Frame(self.main_window, highlightbackground='light blue',
                                     highlightthickness=10)

        # Add labels and widgets to the top left frame
        # Create label for selecting song genre
        self.genre_label = tk.Label(self.top_left, text='Pick Genre', bg='light blue', font=('Adobe Arabic', 12),
                                    width=15, height=2)
        self.genre_label.pack(side='top')
        # Create an IntVar object to use with the radio button
        self.radio_var = tk.StringVar()

        # set the invar object to 1, one option will always be selected
        self.radio_var.set('Hymn')

        # Make radio buttons for song genre selection
        self.hymn = tk.Radiobutton(self.top_left, text='Hymn',
                                   variable=self.radio_var, value='Hymn', bg='beige')
        self.christian_rock = tk.Radiobutton(self.top_left, text='Christian rock',
                                             variable=self.radio_var, value='Christian Rock', bg='beige')
        self.gospel_music = tk.Radiobutton(self.top_left, text='Gospel music',
                                           variable=self.radio_var, value='Gospel Music', bg='beige')

        # pack radio buttons
        self.hymn.pack(anchor='w')
        self.christian_rock.pack(anchor='w')
        self.gospel_music.pack(anchor='w')

        # add labels and widgets to the top mid-frame
        # create label for selecting number of songs
        self.num_label = tk.Label(self.top_mid, text='Pick number of songs \n (For selected Genre)',
                                  font=('Adobe Arabic', 12), bg='light blue')
        self.num_label.pack(side='top')

        # create another int-var object for these radio buttons
        self.num_radio_var = tk.IntVar()
        self.num_radio_var.set(3)

        # create radio buttons
        self.num_1 = tk.Radiobutton(self.top_mid, text='3',
                                    variable=self.num_radio_var, value=3, bg='beige')
        self.num_2 = tk.Radiobutton(self.top_mid, text='4',
                                    variable=self.num_radio_var, value=4, bg='beige')
        self.num_3 = tk.Radiobutton(self.top_mid, text='5',
                                    variable=self.num_radio_var, value=5, bg='beige')

        # pack radio buttons
        self.num_1.pack(anchor='center')
        self.num_2.pack(anchor='center')
        self.num_3.pack(anchor='center')

        # add button to the final top frame
        self.generate1 = tk.Button(self.top_right, text='\nGenerate Songs\n ', bg='sky blue', font=('Adobe Arabic', 12),
                                   command=self.songs)

        # pack button
        self.generate1.pack()

        # add widgets to the mid left frame
        # create label for randomly selected songs
        self.value1 = tk.StringVar()
        self.label1 = tk.Label(self.mid_left, textvariable=self.value1, bg='sky blue', width=35, height=6,
                               highlightbackground='black', highlightthickness=2)
        self.label2 = tk.Label(self.mid_left, text='Selected Songs: ', bg='light blue', font=('Adobe Arabic', 12))

        # pack the label
        self.label2.pack(anchor='n')
        self.label1.pack()

        # add widgets to the mid right frame
        # create change song and save song buttons
        self.change_song = tk.Button(self.mid_right, text='Change a song', bg='powder blue',
                                     highlightbackground='light blue', highlightthickness=10, font=('Adobe Arabic', 12),
                                     command=self.change)
        self.save_songs = tk.Button(self.mid_right, text='Save selected songs', bg='teal', font=('Adobe Arabic', 12),
                                    highlightbackground='light blue', highlightthickness=10,
                                    command=self.save)

        # pack the buttons
        self.change_song.pack()
        self.save_songs.pack()

        # create quit button in the bottom frame
        self.quit_button = tk.Button(self.bottom_frame, text='Quit', bg='red', border=10, height=1, width=10,
                                     command=self.main_window.destroy)
        # pack the button
        self.quit_button.pack()

        # create grid with frames
        self.top_left.grid(row=0, column=1)
        self.top_mid.grid(row=0, column=2)
        self.top_right.grid(row=0, column=3)
        self.mid_left.grid(row=1, columnspan=3)
        self.mid_right.grid(row=1, column=3)
        self.bottom_frame.grid(row=3, columnspan=4)

        tk.mainloop()

    # define songs to randomly select users number of songs from database
    def songs(self):

        # Get the users selected genre and number of songs
        genre = self.radio_var.get()
        number = self.num_radio_var.get()

        # connect to the database
        conn = sqlite3.connect('Lyrics.db')
        # create cursor
        cur = conn.cursor()

        # show the info
        cur.execute('SELECT * FROM song WHERE Genre =(?) ORDER BY random() limit (?)', (genre, number))
        results = cur.fetchall()
        print(results)
        print_results = ''
        song_number = 0

        # Loop results and add them to the dictionary
        for result in results:
            song_number += 1
            DICT[song_number] = result
            print_results += str(song_number) + '. ' + str(result[2]) + '\n'
        print(DICT)
        # set the label to the results
        self.value1.set(print_results)

        # close the connection
        conn.close()

    # to change a song in the list
    def change(self):

        # Check to make sure there are song selected
        if DICT:

            # create frames to pop up on main screen
            self.change_frame = tk.Frame(self.main_window, bg='powder blue', highlightbackground='powder blue',
                                    highlightthickness=10, borderwidth=3, relief='raised')

            # create label
            change_label1 = tk.Label(self.change_frame, text='Which song do you want to change?', bg='powder blue',
                                     font=('Adobe Arabic', 12))
            change_label1.pack()

            # create dropdown choice for user to pick song to change
            number = self.num_radio_var.get()
            self.clicked = tk.StringVar()
            self.clicked.set('1')
            # Create option list to use
            op1 = [1, 2, 3]
            op2 = [1, 2, 3, 4]
            op3 = [1, 2, 3, 4, 5]
            drop = ''
            # decide which options should be displayed
            if number == 3:
                drop = tk.OptionMenu(self.change_frame, self.clicked, *op1)
            if number == 4:
                drop = tk.OptionMenu(self.change_frame, self.clicked, *op2)
            if number == 5:
                drop = tk.OptionMenu(self.change_frame, self.clicked, *op3)

            # Pack the drop menu
            drop.pack()

            # create a button to make a new song
            change_button = tk.Button(self.change_frame, text='Change selected song',
                                      bg='sky blue', font=('Adobe Arabic', 12), command=self.new_song)

            # pack the button
            change_button.pack()

            # pack the frame
            self.change_frame.grid(row=4, column=0, columnspan=3)
        # If the user has not selected any songs give a message
        else:
            tk.messagebox.showinfo(message='You have not selected any songs.')

    # to randomly select a new song
    def new_song(self):
        # get the selected song number to change
        song_selection = int(self.clicked.get())

        # connect to database
        conn = sqlite3.connect('Lyrics.db')
        # create cursor
        cur = conn.cursor()

        # Select a random song
        cur.execute('SELECT * FROM song ORDER BY random() limit 1')
        results = cur.fetchall()

        # set song number
        song_number = 0
        print_new_songs = ''

        # add the new song to the dictionary
        for result in results:
            DICT[song_selection] = result
            # print the new song to the label widget
            for k, v in DICT.items():
                song_number += 1
                print_new_songs += str(song_number) + '. ' + str(v[2] + '\n')

        # set the label to the new song list
        self.value1.set(print_new_songs)

        # close the connection to the database
        conn.close()

    # define save to save the current songs
    def save(self):

        if DICT:
            # create new frame
            self.save_frame = tk.Frame(self.main_window, bg='teal', highlightbackground='teal',
                                  highlightthickness=10, borderwidth=3, relief='raised')

            # create month day year frame
            mdy_frame = tk.Frame(self.save_frame, bg='teal', highlightbackground='teal', highlightthickness=10, borderwidth=3, relief='flat')

            # create save description label
            save_label = tk.Label(self.save_frame, text='Save songs with lyrics:', bg='teal',
                                  font=('Adobe Arabic', 12))

            # create file name label and entry box
            file_name = tk.Label(self.save_frame, text='File Name:', bg='teal',
                                 font=('Adobe Arabic', 12))
            # Declare string variable for file name
            self.file_var = tk.StringVar()

            # create the file entry box
            file_entry = tk.Entry(self.save_frame, textvariable=self.file_var, font=('Adobe Arabic', 12))

            # Create description label and text box
            description = tk.Label(self.save_frame, text='Description:', bg='teal',
                                   font=('Adobe Arabic', 12))
            # Declare string variable for description
            self.description_var = tk.StringVar()

            # create the description text box
            description_entry = tk.Entry(self.save_frame, textvariable=self.description_var)

            # create date label and three places to select date month, day, year
            date = tk.Label(self.save_frame, text='Date: mm/dd/yy', bg='teal',
                            font=('Adobe Arabic', 12))
            # make list options
            month = ['', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            day = ['', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
            year = ['', 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]

            # Create data type of menu text
            self.saved_month = tk.StringVar()
            self.saved_day = tk.StringVar()
            self.saved_year = tk.StringVar()

            # create drop down menus
            drop_month = tk.OptionMenu(mdy_frame, self.saved_month, *month)
            drop_day = tk.OptionMenu(mdy_frame, self.saved_day, *day)
            drop_year = tk.OptionMenu(mdy_frame, self.saved_year, *year)
            # create two slashes for the date
            slash1 = tk.Label(mdy_frame, text='/', bg='teal', font=('System', 13))
            slash2 = tk.Label(mdy_frame, text='/', bg='teal', font=('System', 13))
            # pack the drop menus in the frame
            drop_month.grid(row=0, column=1)
            slash1.grid(row=0, column=2)
            drop_day.grid(row=0, column=3)
            slash2.grid(row=0, column=4)
            drop_year.grid(row=0, column=5)

            # create save button
            save_button = tk.Button(self.save_frame, text='Save file', bg='teal', font=('Adobe Arabic', 12),
                                    command=self.save_file)

            # pack/grid the info then pack the frame
            save_label.grid(row=0, column=0)
            file_name.grid(row=1, column=0)
            file_entry.grid(row=1, column=1)
            description.grid(row=2, column=0)
            description_entry.grid(row=2, column=1)
            date.grid(row=3, column=0)
            mdy_frame.grid(row=3, column=1)
            save_button.grid(row=4, columnspan=2)

            self.save_frame.grid(row=4, rowspan=2, column=3, columnspan=3)

        else:
            tk.messagebox.showinfo(message='You have not selected any songs.')

    def destroy_change(self):
        self.change_frame.destroy()

    def destroy_save(self):
        self.save_frame.destroy()

    def save_file(self):
        print('hi')

# call the class
GUI()
