import glob
from tkinter import *
import pygame
import pygame_menu

import customtkinter as ctk
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandasql import sqldf
from pandastable import Table

class Data_Analyser():
    def __init__(self, width: int, height: int, pos: tuple[int, int] = (0, 0), csv_path: str = None, dataframe: pd.DataFrame = None) -> None:
        if csv_path is None:
            csv_path = Data_Analyser.get_newest_csv()
        if csv_path is None:
            raise ValueError("Cannot find a default csv")

        self.csv_path = csv_path

        if dataframe is None:
            dataframe = pd.read_csv(self.csv_path)

        self.df = dataframe
        self.df.drop(axis="rows", index=0, inplace=True)

        self.rect = pygame.Rect(pos[0], pos[1], width=width, height=height)
        self.surface = pygame.Surface(self.rect.size)
        #region starting menu
        self.starting_menu = pygame_menu.Menu("Welcome", width=self.rect.w, height=self.rect.h)
        self.starting_menu.add.button("Table", self.show_table)
        self.starting_menu.add.button("Graphs", self.show_graphs)
        self.starting_menu.add.button("Back", pygame_menu.pygame_menu.events.BACK)
        #endregion

    def show_table(self):
        pass

    def show_graphs(self):
        pass

    @classmethod
    def get_newest_csv():
        csvs = glob.glob("data/organism_database_*.csv")
        newest_csv = max(csvs)
        return newest_csv

# def pysqldf(query):
#     """Wrapper function for sqldf"""
#     return sqldf(query, globals())


# def update_table(dataframe) -> None:
#     """ "Update the table with new data"""
#     table.model.df = dataframe
#     table.redraw()


# def querry_input(entry_widget):
#     # Get the SQL query from the entry widget
#     user_query = entry_widget.get()

#     # Execute the SQL query on the dataframe
#     try:
#         result = sqldf(user_query, globals())
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return

#     # Update the table with the result
#     update_table(result)


# def new_query(entry_widget, df) -> None:
#     """ "Allows user to make a new querry"""
#     entry_widget.delete(0, ctk.END)  # Clear entry widget
#     update_table(df)


# def main_menu(root_view, dataframe):
#     # Clear the window
#     for widget in root_view.winfo_children():
#         widget.destroy()

#     # Create a label for the title
#     title_label = ctk.CTkLabel(
#         master=root_view, text="Evolution Simulator", font=("Arial", 36)
#     )
#     title_label.pack(pady=20)

#     # Create a frame for the buttons
#     button_frame = ctk.CTkFrame(master=root_view)
#     button_frame.pack(expand=True)

#     # Create the "Table" button
#     table_button = ctk.CTkButton(
#         master=button_frame,
#         text="Table",
#         command=lambda: table_view(root_view, dataframe),
#         width=250,
#         height=100,
#         font=("Arial", 20),
#     )
#     table_button.pack(side="top", padx=10, pady=(10, 10))

#     # Create two more buttons
#     button2 = ctk.CTkButton(
#         master=button_frame,
#         text="Dashboard",
#         command=lambda: dashboard(root_view, dataframe),
#         width=250,
#         height=100,
#         font=("Arial", 20),
#     )
#     button2.pack(side="top", padx=10, pady=(10, 10))

#     button3 = ctk.CTkButton(
#         master=button_frame,
#         text="Exit",
#         command=lambda: exit(),
#         fg_color="red",
#         width=250,
#         height=100,
#         font=("Arial", 20),
#     )
#     button3.pack(side="top", padx=10, pady=(10, 10))


# def dashboard(root_view, dataframe):
#     # Clear the window
#     for widget in root_view.winfo_children():
#         widget.destroy()

#     # Create a new figure for the histogram
#     fig1 = Figure(figsize=(5, 5), dpi=100)
#     ax1 = fig1.add_subplot(111)
#     ax1.hist(dataframe["Time_lived"], bins=20)
#     ax1.set_title("Histogram of Time_lived")

#     # Create a new figure for the scatter plot
#     fig2 = Figure(figsize=(5, 5), dpi=100)
#     ax2 = fig2.add_subplot(111)
#     ax2.scatter(dataframe["Energy"], dataframe["Max_Energy"])
#     ax2.set_title("Scatter plot of Energy vs Max_Energy")

#     # Create a new figure for the pie chart
#     fig3 = Figure(figsize=(5, 5), dpi=100)
#     ax3 = fig3.add_subplot(111)
#     type_counts = dataframe["Type"].value_counts()
#     ax3.pie(type_counts, labels=type_counts.index, autopct="%1.1f%%")
#     ax3.set_title("Pie chart of Type")

#     # Create a canvas for each figure and add it to the window
#     canvas1 = FigureCanvasTkAgg(fig1, master=root_view)
#     canvas1.draw()
#     canvas1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

#     canvas2 = FigureCanvasTkAgg(fig2, master=root_view)
#     canvas2.draw()
#     canvas2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

#     canvas3 = FigureCanvasTkAgg(fig3, master=root_view)
#     canvas3.draw()
#     canvas3.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


# def table_view(root_view, dataframe):
#     for widget in root_view.winfo_children():
#         widget.destroy()
#     # Create a frame for the table on the left side
#     table_frame = ctk.CTkFrame(master=root_view, width=1000, height=700)
#     table_frame.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 10))

#     top_button_frame = ctk.CTkFrame(master=root_view, width=200, height=100)
#     top_button_frame.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))  # Keep row as 0

#     # Create a submit button in the button frame
#     dashboard_button = ctk.CTkButton(
#         master=top_button_frame,
#         text="Dashboard",
#         command=lambda: dashboard(root_view, dataframe),
#         font=("Arial", 12),
#     )
#     dashboard_button.pack(side="top", padx=(5, 5), pady=(10, 10))

#     # Create a table button in the button frame
#     table_button = ctk.CTkButton(
#         master=top_button_frame,
#         text="Table",
#         command=lambda: table_view(root_view, dataframe),
#         font=("Arial", 12),
#     )
#     table_button.pack(side="top", padx=(5, 5), pady=(5, 5))

#     button3 = ctk.CTkButton(
#         master=top_button_frame,
#         text="Exit",
#         command=lambda: exit(),
#         fg_color="red",
#         font=("Arial", 12),
#     )
#     button3.pack(side="top", padx=10, pady=(5, 5))

#     # Create a frame for the bottom
#     bottom_frame = ctk.CTkFrame(master=root_view, width=1200, height=100)
#     bottom_frame.grid(row=1, column=1, padx=(5, 5), pady=(10, 10))
#     bottom_frame.grid_propagate(False)

#     # Create a label for the Entry widget
#     entry_label = ctk.CTkLabel(master=bottom_frame, text="SQL Queries:")
#     entry_label.pack()

#     table = Table(
#         parent=table_frame,
#         dataframe=dataframe,
#         width="900",
#         height="700",
#         showtoolbar=False,
#         showstatusbar=False,
#     )
#     table.Theme = "dark"

#     entry = ctk.CTkEntry(
#         master=bottom_frame, width=750, placeholder_text="Enter SQL queries here"
#     )
#     entry.pack(pady=10)

#     # Create a new frame for the buttons
#     buttons_frame = ctk.CTkFrame(master=bottom_frame)
#     buttons_frame.pack(anchor="center")

#     # Create a submit button in the button frame
#     submit_button = ctk.CTkButton(
#         master=buttons_frame,
#         text="Submit",
#         command=lambda: querry_input(entry),
#         font=("Arial", 14),
#     )
#     submit_button.pack(side="left", padx=(5, 5), pady=(5, 5))

#     # Create a restart button next to the submit button in the button frame
#     restart_button = ctk.CTkButton(
#         master=buttons_frame,
#         text="Restart",
#         command=lambda: new_query(entry, dataframe),
#         font=("Arial", 14),
#     )
#     restart_button.pack(side="left", padx=(5, 5), pady=(5, 5))

#     table.show()


# root = ctk.CTk()
# root.geometry("1000x900")
# root.title("Evolution Simulation")

# ctk.set_appearance_mode("dark")

# main_menu(root, db)

# root.mainloop()
