#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


class VisualizeNBAData:
    
    def __init__(self, team, compared_team=None):
        self._team = team
        self._compared_team = compared_team
    
    #-------------------team stats-------------------#
    
    def create_team_stats_df(self):
        request_url = "https://tw.global.nba.com/stats2/team/stats.json?locale=zh_TW&teamCode={}".format(self._team.lower())
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
    
    def create_team_regular_stats_df(self):
        team_stats_df = self.create_team_stats_df()
        return team_stats_df[team_stats_df['seasonType'] == '2'].reset_index(drop=True)
    
    def create_team_playoffs_stats_df(self):
        team_stats_df = self.create_team_stats_df()
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
    
    #-------------------compared team stats-------------------#
    
    def create_compared_team_stats(self):
        try:
            request_url = "https://tw.global.nba.com/stats2/team/stats.json?locale=zh_TW&teamCode={}".format(self._compared_team.lower())
            compared_team_dict = requests.get(request_url).json()
            compared_team_stats = compared_team_dict['payload']['seasons']
            annual_dict_list = []
            for i in range(len(compared_team_stats)):
                annual_dict = {}           
                annual_dict['year'] = compared_team_stats[i]['year']
                annual_dict['seasonType'] = compared_team_stats[i]['seasonType']
                for k, v in compared_team_stats[i]['team']['statAverage'].items():
                    if isinstance(v, float) or isinstance(v, int):
                        annual_dict[k] = v
                annual_dict_list.append(annual_dict)         
            compared_team_stats_df = pd.DataFrame(annual_dict_list)
            return compared_team_stats_df
        except:
            print("Can't find the compared team!")
    
    def create_compared_team_regular_stats(self):
        try:
            compared_team_stats_df = self.create_compared_team_stats()
            return compared_team_stats_df[compared_team_stats_df['seasonType'] == '2'].reset_index(drop=True)
        except:
            pass
    
    def create_compared_team_playoffs_stats(self):
        try:
            compared_team_stats_df = self.create_compared_team_stats()
            return compared_team_stats_df[compared_team_stats_df['seasonType'] == '4'].reset_index(drop=True)
        except:
            pass
    
    #-------------------plot functions-------------------#
    
    def plot_regular_stats(self):
        team_regular_stats = self.create_team_regular_stats_df()
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
            axes[i, j].set_title('{}(regular) - {}'.format(self._team, col), size=22)
            axes[i, j].set_ylim(opponent_col.min() * 0.75)
            axes[i, j].set_xticks(years)
            axes[i, j].set_xlabel('Years', size=20)
            axes[i, j].set_ylabel(col, size=20)
            for x, y in enumerate(team_col):
                axes[i, j].text(2011 + x - 0.4, y * 1.017, f"{y}", size=15)
        axes[0, 0].legend(loc='lower right', fontsize=16)
        plt.tight_layout()
        plt.show()
        
    def plot_playoffs_stats(self):
        team_playoffs_stats = self.create_team_playoffs_stats_df()
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
            axes[i, j].set_title('{}(playoffs) - {}'.format(self._team, col), size=22)
            axes[i, j].set_ylim(team_col.min() * 0.8)
            axes[i, j].set_xticks(rows)
            axes[i, j].set_xticklabels(list(np.array(team_playoffs_stats['year']).astype(int)))
            axes[i, j].set_xlabel('Years', size=20)
            axes[i, j].set_ylabel(col, size=20)
            for x, y in zip(rows, team_col):
                axes[i, j].text(x - 0.2, y * 1.019, f"{y}", size=15)
        axes[0, 0].legend(loc='lower right', fontsize=16)
        plt.tight_layout()
        plt.show()  
        
    def plot_regular_compared_stats(self, target_year):
        year = str(target_year)
        next_year = str(target_year + 1)
        team_regular_stats = self.create_team_regular_stats_df()
        compared_team_regular_stats = self.create_compared_team_regular_stats()
        stats_cols = ['turnoversPg', 'rebsPg', 'assistsPg', 'tppct', 'fgpct', 'pointsPg']
        text_content = ['TO', "RB", "AST", "3P%", "FG%", "PTS"]
        try:
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
                ax.text(-6, row - 0.1, word, size=14)
                ax.text(-team_col - 16, row - 0.1, f"{team_col.values[0]}", size=14)
                ax.text(compared_team_col + 3, row - 0.1, f"{compared_team_col.values[0]}", size=14)
            ax.set_title(f"{self._team} vs {self._compared_team} ({year[-2:]}-{next_year[-2:]} regular)", size=16)
            ax.set_xlim(-130, 130)
            ax.text(-125, 0, self._team, size=18)
            ax.text(95, 0, self._compared_team, size=18)
            ax.set_xticks([])
            ax.set_yticks([])
            plt.show()
        except:
            pass

if __name__ == "__main__":
    vnd = VisualizeNBAData("Nuggets")
