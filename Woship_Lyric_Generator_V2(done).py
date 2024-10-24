# Amber Kuhn
# Date Start: 4/26/22
# Date Finish: 5/10/22
# Program: My Worship Lyric Generator

import tkinter as tk
import sqlite3
import tkinter.messagebox
from tkinter import ttk
import os

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

        # Set up FRAMES
        self.top_left = tk.Frame(self.main_window, bg='beige', highlightbackground='light blue',
                                 highlightthickness=10, borderwidth=3, relief='raised')
        self.top_mid = tk.Frame(self.main_window, bg='beige', highlightbackground='light blue',
                                highlightthickness=10, borderwidth=3, relief='raised')
        self.top_right = tk.Frame(self.main_window, background='light blue')
        self.mid_left = tk.Frame(self.main_window, background='light blue')
        self.mid_right = tk.Frame(self.main_window, background='light blue', highlightbackground='light blue',
                                  highlightthickness=10)
        self.bottom_frame = tk.Frame(self.main_window, highlightbackground='light blue',
                                     highlightthickness=10)
        self.display_db_frame = tk.Frame(self.main_window, highlightbackground='light blue',
                                         highlightthickness=10, bg='light blue')
        # create frame for the show lyrics scroll bar label
        self.lyric_frame = tk.Frame(self.main_window, bg='light blue', height=90, width=90)

        # Add labels and widgets to the TOP LEFT FRAME
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

        # add labels and widgets to the TOP MID FRAME
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

        # add button to the TOP RIGHT FRAME
        self.generate1 = tk.Button(self.top_right, text='\nGenerate Songs\n ', bg='light steel blue',
                                   font=('Adobe Arabic', 12), command=self.songs)
        # Create a button to clear the song selection
        self.clear = tk.Button(self.top_right, text='Clear Songs', bg='steel blue', font=('Adobe Arabic', 12),
                               command=self.clear)

        # pack buttons
        self.generate1.pack()
        self.clear.pack()

        # add widgets to the MID LEFT FRAME
        # create label for randomly selected songs
        self.value = tk.StringVar()
        self.label1 = tk.Label(self.mid_left, textvariable=self.value, bg='light steel blue', width=35, height=6,
                               highlightbackground='black', highlightthickness=2)
        self.label2 = tk.Label(self.mid_left, text='Selected Songs: ', bg='light blue', font=('Adobe Arabic', 12))

        # pack the label
        self.label2.pack(anchor='w')
        self.label1.pack()

        # add widgets to the MID RIGHT FRAME
        # create change song and save song buttons
        self.change_song = tk.Button(self.mid_right, text='Change a song', bg='powder blue',
                                     highlightbackground='light blue', highlightthickness=10, font=('Adobe Arabic', 12),
                                     command=self.change)
        self.save_songs = tk.Button(self.mid_right, text='Save selected songs', bg='cadet blue',
                                    font=('Adobe Arabic', 12),
                                    highlightbackground='light blue', highlightthickness=10,
                                    command=self.save)

        # pack the buttons
        self.change_song.pack()
        self.save_songs.pack()

        # add widgets to the DB FRAME
        self.db_button = tk.Button(self.display_db_frame, text='   \nShow\rEntries\rIn The\rDatabase\n   ',
                                   bg='light goldenrod', font=('Adobe Arabic', 12), command=self.db)
        self.close_bd = tk.Button(self.display_db_frame, text='Close Database', bg='light goldenrod',
                                  font=('Adobe Arabic', 12), command=self.db_window_destroy)
        self.db_button.pack()
        self.close_bd.pack()
        self.close_bd.config(state='disabled')

        # add widgets to the LYRIC FRAME
        # create a show lyrics button
        self.show_lyrics = tk.Button(self.lyric_frame, text='\nShow lyrics\n', bg='light steel blue',
                                     font=('Adobe Arabic', 12), command=self.display_lyrics)
        self.show_lyrics.pack()

        # create a scroll bar label widget need a canvas inorder to show scroll bar labels
        self.canvas = tk.Canvas(self.lyric_frame, height=500, width=500)
        self.canvas.pack(side='left', fill='both', expand=1)

        # create the scroll bar
        self.scroll_bar = ttk.Scrollbar(self.lyric_frame, orient='vertical', command=self.canvas.yview)
        self.scroll_bar.pack(side='right', fill='y')
        # put the scroll bar on the canvas
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # create a frame for the actual label
        self.label_frame = tk.Frame(self.canvas)
        # put the frame on the canvas window
        self.canvas.create_window((0, 0), window=self.label_frame, anchor='nw')

        # create the lyric label
        self.lyric_label_var = tk.StringVar()
        self.lyric_label = tk.Label(self.label_frame, textvariable=self.lyric_label_var, bg='light steel blue',
                                    width=70, height=1000, anchor='nw')
        self.lyric_label.grid(row=0)

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
        self.display_db_frame.grid(row=0, rowspan=1, column=4, columnspan=3)
        self.bottom_frame.grid(row=2, columnspan=4)
        self.lyric_frame.grid(row=0, rowspan=10, column=10, columnspan=8)

        tk.mainloop()

    def clear(self):
        self.value.set('')
        DICT.clear()
        self.lyric_label_var.set('')

    def display_lyrics(self):
        if DICT:
            song_number = 0
            print_lyrics = ''
            for k, v in DICT.items():
                song_number += 1
                print_lyrics += '---------------\n' + str(song_number) + '. ' + str(v[2]) + '\n\n' + v[1] + '\n\n'
            # set the lyric label to the lyrics
            self.lyric_label_var.set(print_lyrics)
        else:
            tk.messagebox.showinfo(title='Missing Info', message='You have not selected any songs.')

    # define songs to randomly select users number of songs from database
    def songs(self):

        # Get the users selected genre and number of songs
        genre = self.radio_var.get()
        number = self.num_radio_var.get()

        self.lyric_label_var.set('')

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
        self.value.set(print_results)

        # close the connection
        conn.close()

    # to change a song in the list
    def change(self):
        # Check to make sure there are song selected
        if DICT:

            self.change_song.config(state='disabled')
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
            # create back button
            back_button = tk.Button(self.change_frame, text='Back', bg='tomato', font=('Adobe Arabic', 12),
                                    command=self.back_change_frame)

            # pack the button
            change_button.pack()
            back_button.pack()

            # pack the frame
            self.change_frame.grid(row=3, rowspan=6, column=1, columnspan=2)
        # If the user has not selected any songs give a message
        else:
            tk.messagebox.showinfo(title='Missing Info', message='You have not selected any songs.')

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
        self.value.set(print_new_songs)

        # close the connection to the database
        conn.close()

    # define save to save the current songs
    def save(self):

        if DICT:
            self.save_songs.config(state='disabled')
            # create new frame
            self.save_frame = tk.Frame(self.main_window, bg='cadet blue', highlightbackground='cadet blue',
                                       highlightthickness=10, borderwidth=3, relief='raised')

            # create month day year frame
            mdy_frame = tk.Frame(self.save_frame, bg='cadet blue', highlightbackground='cadet blue',
                                 highlightthickness=10,
                                 borderwidth=3, relief='flat')

            # create save description label
            save_label = tk.Label(self.save_frame, text='Save songs with lyrics:', bg='cadet blue',
                                  font=('Adobe Arabic', 12))

            # create file name label and entry box
            file_name = tk.Label(self.save_frame, text='File Name:', bg='cadet blue',
                                 font=('Adobe Arabic', 12))
            # Declare string variable for file name
            self.file_var = tk.StringVar()

            # set the file var to nothing
            self.file_var.set('')

            # create the file entry box
            file_entry = tk.Entry(self.save_frame, textvariable=self.file_var, font=('Adobe Arabic', 12))

            # Create description label and text box
            description = tk.Label(self.save_frame, text='Description:', bg='cadet blue',
                                   font=('Adobe Arabic', 12))
            # Declare string variable for description
            self.description_var = tk.StringVar()

            # create the description text box
            description_entry = tk.Entry(self.save_frame, textvariable=self.description_var)

            # create date label and three places to select date month, day, year
            date = tk.Label(self.save_frame, text='Date: mm/dd/yy', bg='cadet blue',
                            font=('Adobe Arabic', 12))
            # make list options
            month = ['', '01', '02', '03', '04', '05', '06', '07', '08', '09', 10, 11, 12]
            day = ['', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                   10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
            year = ['', 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]

            # Create data type of menu text
            self.saved_month = tk.StringVar()
            self.saved_day = tk.StringVar()
            self.saved_year = tk.StringVar()

            # Set the drop menus
            self.saved_month.set('')
            self.saved_day.set('')
            self.saved_day.set('')

            # create drop down menus
            drop_month = tk.OptionMenu(mdy_frame, self.saved_month, *month)
            drop_day = tk.OptionMenu(mdy_frame, self.saved_day, *day)
            drop_year = tk.OptionMenu(mdy_frame, self.saved_year, *year)
            # create two slashes for the date
            slash1 = tk.Label(mdy_frame, text='/', bg='cadet blue', font=('System', 13))
            slash2 = tk.Label(mdy_frame, text='/', bg='cadet blue', font=('System', 13))
            # pack the drop menus in the frame
            drop_month.grid(row=0, column=1)
            slash1.grid(row=0, column=2)
            drop_day.grid(row=0, column=3)
            slash2.grid(row=0, column=4)
            drop_year.grid(row=0, column=5)

            # create save button
            save_button = tk.Button(self.save_frame, text='Save file', bg='cadet blue', font=('Adobe Arabic', 12),
                                    command=self.save_file)
            # create back button
            back_button = tk.Button(self.save_frame, text='Back', bg='tomato', font=('Adobe Arabic', 12),
                                    command=self.back_save_frame)

            # pack/grid the info then pack the frame
            save_label.grid(row=0, column=0)
            file_name.grid(row=1, column=0)
            file_entry.grid(row=1, column=1)
            description.grid(row=2, column=0)
            description_entry.grid(row=2, column=1)
            date.grid(row=3, column=0)
            mdy_frame.grid(row=3, column=1)
            save_button.grid(row=4, columnspan=2)
            back_button.grid(row=5, columnspan=2)

            self.save_frame.grid(row=5, rowspan=20, column=3, columnspan=7)

        else:
            tk.messagebox.showinfo(title='Missing Info' ,message='You have not selected any songs.')

    def save_file(self):

        # get the information
        file_name = self.file_var.get()
        month = self.saved_month.get()
        day = self.saved_day.get()
        year = self.saved_year.get()
        description = self.description_var.get()

        # add the songs to the users .txt file
        if file_name != '':
            if month != '' and day != '' and year != '':
                date = month + '/' + day + '/' + year
                file_1 = file_name + '.txt'
                try:
                    open(file_1)
                    tk.messagebox.showinfo(message='The file name you have chosen is already in use.')

                except OSError:

                    open_file = open(file_1, "w")
                    for k, v in DICT.items():
                        open_file.write('\n--------------------------------\n')
                        open_file.write(v[2])
                        open_file.write('\n \n')
                        open_file.write('\n')
                        open_file.write(v[1])
                        open_file.write('\n--------------------------------\n')
                    tk.messagebox.showinfo(title='File Saved',
                                           message=f'The file has been saved as: {file_1}')
                    open_file.close()

                    # connect to database
                    conn = sqlite3.connect('Lyrics.db')
                    # create cursor
                    cur = conn.cursor()

                    # add the event to the database
                    cur.execute('INSERT INTO EventTable (EventDate, Description, FileName) VALUES (?, ?,?)',
                                (date, description, file_1,))
                    conn.commit()

                    # get the created id for the event to use as the event id in song selection table
                    cur.execute('SELECT EventID FROM EventTable WHERE FileName = (?)', (file_1,))
                    result = cur.fetchall()

                    # add the selected songs to a table to reference from
                    for id in result:
                        for k, v in DICT.items():
                            cur.execute('INSERT OR IGNORE INTO SongSelection (EventID, SongNumber)'
                                        ' VALUES (?,?)', (id[0], v[0]))
                            conn.commit()
                    conn.close()
            else:
                tk.messagebox.showinfo(message='Please put the date.')
        else:
            tk.messagebox.showinfo(message='You have not entered a file name.')

    # define back button for the save frame
    def back_save_frame(self):
        self.save_frame.destroy()
        self.save_songs.config(state='normal')

    def back_change_frame(self):
        self.change_frame.destroy()
        self.change_song.config(state='normal')

    def db_window_destroy(self):
        self.db_window.destroy()
        self.db_button.config(state='normal')
        self.lyric_label_var.set('')
        self.close_bd.config(state='disabled')

    def db(self):
        self.db_button.config(state='disabled')
        self.close_bd.config(state='normal')
        # create a new window to put the db info on as a list that can be selected
        self.db_window = tk.Toplevel()
        # name the window and set the color
        self.db_window.title('Edit Worship Lyric Database')
        self.db_window['bg'] = 'light salmon'
        self.db_window.geometry("500x300")

        # create frames for the widgets to be placed in
        self.list_frame = tk.Frame(self.db_window, bg='light salmon')
        self.edit_frame = tk.Frame(self.db_window, pady=10, bg='light salmon')

        # create tree for displaying the information from the db
        self.my_tree = ttk.Treeview(self.list_frame)

        # create and format the columns
        self.my_tree['columns'] = ('Event Date', 'Event ID', 'Description', 'Songs')
        self.my_tree.column("#0", width=0)
        self.my_tree.column("Event Date", anchor='w', width=80)
        self.my_tree.column("Event ID", anchor='center', width=55)
        self.my_tree.column("Description", anchor='w', width=150)
        self.my_tree.column("Songs", anchor='w', width=125)

        # Create headings
        self.my_tree.heading("#0", text='', anchor='w')
        self.my_tree.heading("Event Date", text='Event Date', anchor='w')
        self.my_tree.heading("Event ID", text='Event ID', anchor='center')
        self.my_tree.heading("Description", text='Description', anchor='w')
        self.my_tree.heading("Songs", text='File Name', anchor='w')

        # connect to the database
        conn = sqlite3.connect('Lyrics.db')
        # create cursor
        cur = conn.cursor()

        cur.execute('SELECT * FROM EventTable')
        results = cur.fetchall()
        for result in results:
            self.my_tree.insert(parent='', index='end', iid=result[0], text="",
                                values=(result[1], result[0], result[2], result[3]))
        conn.close()

        # pack info in the frame and pack the frame
        self.my_tree.pack(pady=10)
        self.list_frame.pack()

        # create a button to open the file, one to delete the event, and one to exit the window
        self.open_1 = tk.Button(self.edit_frame, text='Open the file', font=('Adobe Arabic', 12),
                                command=self.open)
        self.delete = tk.Button(self.edit_frame, text='Delete Event',
                                font=('Adobe Arabic', 12), command=self.delete_event)
        self.exit = tk.Button(self.edit_frame, text='Exit Window',
                              font=('Adobe Arabic', 12), command=self.db_window_destroy)

        # pack buttons
        self.open_1.pack(side='left')
        self.delete.pack(side='left')
        self.exit.pack(side='right')

        # pack the frame
        self.edit_frame.pack()

        self.db_window.protocol("WM_DELETE_WINDOW", self.db_window_destroy)

    def open(self):
        # get the name of the file from the treeview window
        try:
            x = self.my_tree.selection()[0]

            # connect to the database
            conn = sqlite3.connect('Lyrics.db')
            # create cursor
            cur = conn.cursor()
            cur.execute('SELECT FileName FROM EventTable WHERE EventID = (?)', (x,))
            result = cur.fetchone()
            # try opening the file with the given file name
            try:
                file = open(result[0])
                data = file.read()
                # print the information back to the user on the first window
                self.lyric_label_var.set(data)
            except OSError:
                tk.messagebox.showerror(title="Error", message='The file you have selected does not exist.',
                                        parent=self.db_window)
        except IndexError:
            tk.messagebox.showwarning(title="Warning", message='You have not selected any entry.',
                                      parent=self.db_window)

    def delete_event(self):
        confirm = tk.messagebox.askyesno(title="Confirmation", message='Are you sure you want to delete this entry?',
                                         parent=self.db_window)
        if confirm:
            try:
                selection = self.my_tree.selection()[0]

                # connect to the database
                conn = sqlite3.connect('Lyrics.db')
                # create cursor
                cur = conn.cursor()
                # get the file name to delete from computer
                cur.execute('SELECT FileName FROM EventTable WHERE EventID = (?)', (selection,))
                result = cur.fetchone()
                # remove the file
                try:
                    os.remove(result[0])
                    delete = True
                except OSError:
                    delete = tk.messagebox.askyesno(title="Warning", message='The file does not exist.\n '
                                                    'Click yes for the event to be deleted.',
                                                    parent=self.db_window)
                if delete:
                    # delete the entries from the database
                    cur.execute('DELETE FROM EventTable WHERE EventID = (?)', (selection,))
                    cur.execute('DELETE FROM SongSelection WHERE EventID = (?)', (selection,))
                    # commit the changes
                    conn.commit()
                    conn.close()
                    # delete the entry in the treeview
                    self.my_tree.delete(selection)
                elif not delete:
                    print('Not deleted')

            except IndexError:
                tk.messagebox.showwarning(title="Warning", message='You have not selected any entry.',
                                          parent=self.db_window)
        elif not confirm:
            print('Not deleted')


# call the class
GUI()
