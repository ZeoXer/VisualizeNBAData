import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#------------VisualizeNBAData------------#
class VisualizeNBAData:

    def __init__(self):
        self._teamlist = ['Hawks', 'Celtics', 'Bulls', 'Hornets', 'Nets', 'Cavaliers', 'Heat', 'Knicks', 'Pistons',
                          'Magic', 'Sixers', 'Pacers', 'Wizards', 'Raptors', 'Bucks', 'Mavericks', 'Nuggets',
                          'Warriors', 'Rockets', 'Timberwolves','Clippers', 'Grizzlies', 'Thunder', 'Lakers',
                          'Pelicans', 'Blazers', 'Suns', 'Spurs', 'Jazz', 'Kings']    
        self._team = None
        self._compared_team = None
        self._year = None
        self.build_window()
  
    #-------------------team stats-------------------#
    
    def create_team_stats_df(self, team):
        request_url = "https://tw.global.nba.com/stats2/team/stats.json?locale=zh_TW&teamCode={}".format(team)
        team_dict = requests.get(request_url).json()
        team_stats = team_dict['payload']['seasons']
        annual_dict_list = []
        for i in range(len(team_stats)):
            annual_dict = {}           
            annual_dict['year'] = team_stats[i]['year']
            annual_dict['seasonType'] = team_stats[i]['seasonType']
            for k, v in team_stats[i]['team']['statAverage'].items():
                if isinstance(v, float) or isinstance(v, int):
                    annual_dict[k] = v
            annual_dict_list.append(annual_dict)         
        team_stats_df = pd.DataFrame(annual_dict_list)
        return team_stats_df
    
    def create_team_regular_stats_df(self, team):
        team_stats_df = self.create_team_stats_df(team)
        return team_stats_df[team_stats_df['seasonType'] == '2'].reset_index(drop=True)
    
    def create_team_playoffs_stats_df(self, team):
        team_stats_df = self.create_team_stats_df(team)
        return team_stats_df[team_stats_df['seasonType'] == '4'].reset_index(drop=True)
    
    #-------------------opponent stats-------------------#
    
    def create_opponent_stats_df(self):
        request_url = "https://tw.global.nba.com/stats2/team/stats.json?locale=zh_TW&teamCode={}".format(self._team.lower())
        opponent_dict = requests.get(request_url).json()
        opponent_stats = opponent_dict['payload']['seasons']
        annual_dict_list = []
        for i in range(len(opponent_stats)):
            annual_dict = {}           
            annual_dict['year'] = opponent_stats[i]['year']
            annual_dict['seasonType'] = opponent_stats[i]['seasonType']
            for k, v in opponent_stats[i]['opponent']['statAverage'].items():
                if isinstance(v, float) or isinstance(v, int):
                    annual_dict[k] = v
            annual_dict_list.append(annual_dict)         
        opponent_stats_df = pd.DataFrame(annual_dict_list)
        return opponent_stats_df
    
    def create_opponent_regular_stats_df(self):
        opponent_stats_df = self.create_opponent_stats_df()
        return opponent_stats_df[opponent_stats_df['seasonType'] == '2'].reset_index(drop=True)
    
    def create_opponent_playoffs_stats_df(self):
        opponent_stats_df = self.create_opponent_stats_df()
        return opponent_stats_df[opponent_stats_df['seasonType'] == '4'].reset_index(drop=True)
    
    #-------------------plot functions-------------------#
    
    def plot_regular_stats(self):
        team_regular_stats = self.create_team_regular_stats_df(self._team.lower())
        opponent_regular_stats = self.create_opponent_regular_stats_df()
        stats_cols = ['pointsPg', 'assistsPg', 'rebsPg', 'fgpct', 'tppct', 'turnoversPg']
        years = list(np.array(team_regular_stats['year']).astype(int))
        fig, axes = plt.subplots(2, 3, figsize=(22, 12))
        for num, col in enumerate(stats_cols):
            i = num // 3
            j = num % 3
            team_col = team_regular_stats[col]
            opponent_col = opponent_regular_stats[col]
            axes[i, j].plot(years, team_col, label=self._team, linewidth=2, linestyle="dotted", 
                            marker=".", ms=14, color="darkgreen")
            axes[i, j].bar(years, opponent_col, label='opponents', color="wheat")
            axes[i, j].set_title('{}(regular) - {}'.format(self._team, col), size=13)
            axes[i, j].set_ylim(opponent_col.min() * 0.75)
            axes[i, j].set_xticks(years)
            for x, y in enumerate(team_col):
                axes[i, j].text(2011 + x - 0.4, y * 1.017, f"{y}", size=9)
        axes[0, 0].legend(loc='lower right', fontsize=13)
        plt.tight_layout()
        return fig
        
    def plot_playoffs_stats(self):
        team_playoffs_stats = self.create_team_playoffs_stats_df(self._team.lower())
        opponent_playoffs_stats = self.create_opponent_playoffs_stats_df()
        stats_cols = ['pointsPg', 'assistsPg', 'rebsPg', 'fgpct', 'tppct', 'turnoversPg']
        rows = list(team_playoffs_stats.index)
        fig, axes = plt.subplots(2, 3, figsize=(22, 12))
        for num, col in enumerate(stats_cols):
            i = num // 3
            j = num % 3
            team_col = team_playoffs_stats[col]
            opponent_col = opponent_playoffs_stats[col]
            axes[i, j].bar(rows, opponent_col, alpha=0.6, label='opponents', color="wheat")
            axes[i, j].scatter(rows, team_col, label=self._team, linewidth=5, 
                            marker="*", color="darkgreen")
            axes[i, j].set_title('{}(playoffs) - {}'.format(self._team, col), size=13)
            axes[i, j].set_ylim(team_col.min() * 0.8)
            axes[i, j].set_xticks(rows)
            axes[i, j].set_xticklabels(list(np.array(team_playoffs_stats['year']).astype(int)))
            for x, y in zip(rows, team_col):
                axes[i, j].text(x - 0.3, y * 1.019, f"{y}", size=9)
        axes[0, 0].legend(loc='lower right', fontsize=13)
        plt.tight_layout()
        return fig
        
    def plot_regular_compared_stats(self, target_year):
        year = target_year
        next_year = str(int(target_year) + 1)
        team_regular_stats = self.create_team_regular_stats_df(self._team.lower())
        compared_team_regular_stats = self.create_team_regular_stats_df(self._compared_team.lower())
        stats_cols = ['turnoversPg', 'rebsPg', 'assistsPg', 'tppct', 'fgpct', 'pointsPg']
        text_content = ['TO', "RB", "AST", "3P%", "FG%", "PTS"]
        compared_team_year = compared_team_regular_stats[compared_team_regular_stats['year'] == year]
        team_year = team_regular_stats[team_regular_stats['year'] == year]
        fig, ax = plt.subplots(figsize=(12, 6))
        for row, col, word in zip(list(range(6)), stats_cols, text_content):
            compared_team_col = compared_team_year[col]
            team_col = team_year[col]
            if compared_team_col.values[0] > team_col.values[0]:
                ax.barh(row, compared_team_col, 0.6, label=self._compared_team, alpha=0.5, color='navy')
                ax.barh(row, -team_col, 0.6, label=self._team, alpha=0.4, color='lightgrey')
            else:
                ax.barh(row, compared_team_col, 0.6, label=self._compared_team, alpha=0.4, color='lightgrey')
                ax.barh(row, -team_col, 0.6, label=self._team, alpha=0.5, color='navy')
            ax.text(-3.5, row - 0.05, word, size=14)
            ax.text(-team_col - 14, row - 0.05, f"{team_col.values[0]}", size=14)
            ax.text(compared_team_col + 3, row - 0.05, f"{compared_team_col.values[0]}", size=14)
        ax.set_title(f"{self._team} vs {self._compared_team} ({year[-2:]}-{next_year[-2:]} regular)", size=16)
        ax.text(-125, 0, self._team, size=18)
        ax.text(130 - len(self._compared_team) * 3.5, 0, self._compared_team, size=18)
        ax.set_xlim(-130, 130)
        ax.set_xticks([])
        ax.set_yticks([])
        plt.tight_layout()
        return fig

    def build_window(self):
        #------------command functions------------#
        def confirmed_first_team():
            self._team = first_team_select.get()
            Label(frame, text="???", font=WIDGET_FONT).grid(row=1, column=0)
            Label(frame, text=self._team, font=WIDGET_FONT, width=12).grid(row=1, column=1)

        def confirmed_second_team(): 
            self._compared_team = second_team_select.get()
            Label(frame, text="???", font=WIDGET_FONT).grid(row=3, column=0)
            Label(frame, text=self._compared_team, font=WIDGET_FONT, width=12).grid(row=3, column=1)

        def confirmed_plot_method():
            plot_method = plot_method_select.get()
            arrow_method = Label(frame, text="???", font=WIDGET_FONT)
            method_select_label = Label(frame, text=plot_method, font=WIDGET_FONT, width=12)
            arrow_method.grid(row=5, column=0)
            method_select_label.grid(row=5, column=1)
            if plot_method == "??????????????????":
                year_label.grid(row=6, column=0)
                year_select.grid(row=6, column=1)
                year_select.current(0)
                confirmed_year_button.grid(row=6, column=2)
            else:
                plot_button.pack()
            return plot_method  

        def confirmed_year():
            self._year = year_select.get()
            arrow_year = Label(frame, text="???", font=WIDGET_FONT)
            year_select_label = Label(frame, text=self._year, font=WIDGET_FONT, width=12)
            arrow_year.grid(row=7, column=0)    
            year_select_label.grid(row=7, column=1)
            plot_button.pack()

        def plot_fig():
            plot_method = confirmed_plot_method()
            year_label.grid_remove()
            year_select.grid_remove()
            confirmed_year_button.grid_remove()
            plot_button.pack_forget()
            Label(frame, text="", font=WIDGET_FONT, width=5).grid(row=5, column=0)
            Label(frame, text="", font=WIDGET_FONT, width=12).grid(row=5, column=1)
            Label(frame, text="", font=WIDGET_FONT, width=5).grid(row=7, column=0)
            Label(frame, text="", font=WIDGET_FONT, width=12).grid(row=7, column=1)
            new_top = Toplevel()
            x = window.winfo_screenwidth() - 100
            y = window.winfo_screenheight() - 50
            new_top.geometry(f"{x}x{y}")
            new_top.resizable(False, False)   
            if plot_method == "????????????":
                fig = self.plot_regular_stats()        
                new_top.wm_title("?????????????????????")                
            elif plot_method == "???????????????":
                fig = self.plot_playoffs_stats()
                new_top.wm_title("????????????????????????")
            else:
                fig = self.plot_regular_compared_stats(self._year)
                new_top.wm_title("?????????????????????")
            canvas = FigureCanvasTkAgg(fig, master=new_top)
            canvas.draw()
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            
        def _quit():
            window.quit()
            window.destroy()
            
        #------------window------------#
        WIDGET_FONT = ("jf open ?????? 1.1", 18)
        BUTTON_FONT = ("jf open ?????? 1.1", 14)
        window = Tk()
        window.geometry("700x600")
        window.title("VisualizeNBAData")
        window.resizable(False, False)
        frame = Frame(window)

        #------------widgets------------#
        Label(window, text="", height=2).pack()
        introduction_label = Label(window, text="""????????????????????????????????????NBA????????????(2011-12???)
        ????????????????????????????????????????????????????????????
        ????????????????????????????????????
        --????????????????????????????????????????????????--
        --????????????????????????????????????????????????????????????--""", font=WIDGET_FONT).pack()
        Label(window, text="", height=1).pack()
        frame.pack()

        ##------first team------##
        Label(frame, text="????????????", font=WIDGET_FONT).grid(row=0, column=0)
        first_team_select = ttk.Combobox(frame, font=WIDGET_FONT, values=self._teamlist, width=12, state='readonly')
        first_team_select.grid(row=0, column=1)
        first_team_select.current(0)
        confirmed_first_team_button = Button(frame, text="??????", font=BUTTON_FONT, relief=RAISED, bd=3,
                                             pady=0, command=confirmed_first_team)
        confirmed_first_team_button.grid(row=0, column=2)
        ##-----------------------##

        ##------second team------##
        Label(frame, text="???????????????", font=WIDGET_FONT).grid(row=2, column=0)
        second_team_select = ttk.Combobox(frame, font=WIDGET_FONT, values=["(?????????)", *self._teamlist], width=12, state='readonly')
        second_team_select.grid(row=2, column=1)
        second_team_select.current(0)
        confirmed_second_team_button = Button(frame, text="??????", font=BUTTON_FONT, relief=RAISED, bd=3,
                                             pady=0, command=confirmed_second_team)
        confirmed_second_team_button.grid(row=2, column=2)
        ##-----------------------##

        ##------plot method------##
        Label(frame, text="???????????????", font=WIDGET_FONT, width=10).grid(row=4, column=0)
        plot_method_select = ttk.Combobox(frame, font=WIDGET_FONT, values=["????????????", "???????????????", "??????????????????"],
                                          width=12, state='readonly')
        plot_method_select.grid(row=4, column=1)
        plot_method_select.current(0)
        confirmed_plot_method_button = Button(frame, text="??????", font=BUTTON_FONT, relief=RAISED, bd=3,
                                             pady=0, command=confirmed_plot_method)
        confirmed_plot_method_button.grid(row=4, column=2)
        ##-----------------------##

        ##------year select------##
        year_select = ttk.Combobox(frame, font=WIDGET_FONT, values=list(range(2011, 2021)),
                                          width=10, state='readonly')
        year_label = Label(frame, text="??????", font=WIDGET_FONT)
        confirmed_year_button = Button(frame, text="??????", font=BUTTON_FONT, relief=RAISED, bd=3,
                                             pady=0, command=confirmed_year)
        ##-----------------------##
        plot_button = Button(window, text="??????!", font=WIDGET_FONT, relief=RAISED, bd=3 , command=plot_fig)
        Button(window, text="??????", font=BUTTON_FONT, relief=RAISED, bd=3, command=_quit).place(x=620, y=540)


        window.mainloop()

        

if __name__ == '__main__':        
    vnd = VisualizeNBAData()

