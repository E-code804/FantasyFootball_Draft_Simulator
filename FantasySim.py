import pygame
import os
import time
import datetime
import random

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1350, 775
team1, team2, team3, team4, team5, = {}, {}, {}, {}, {}
list_of_teams = [team1, team2, team3, team4, team5]
draft_boards = [pygame.image.load("Team1_turn.png"), pygame.image.load("Team2_turn.png"), pygame.image.load("Team3_turn.png"), pygame.image.load("Team4_turn.png"), pygame.image.load("Team5_turn.png")]
player_ranking_imgs = {"Christian McCafferey" : "cmac.png", "Dalvin Cook" : "cook.png", "Saquon Barkley" : "saquon.png", "Ezekiel Elliot" : "zeke.png", "Derrick Henry" : "henry.png", "Davante Adams" : "davante.png", "Travis Kelce" : "kelce.png", "Stefon Diggs" : "diggs.png", "Calvin Ridley" : "ridely.png", "Darren Waller" : "waller.png", "DeAndre Hopkins" : "dhop.png", "Justin Jefferson" : "justin.png", "George Kittle" : "kittle.png", "Patrick Mahomes" : "mahomes.png", "T.J. Hockenson" : "hock.png", "Josh Allen" : "allen.png", "Mark Andrews" : "andrews.png", "Lamar Jackson" : "lamar.png", "Dak Prescott" : "dak.png", "Russel Wilson" : "russel.png"}
player_ranking_pts = {"Christian McCafferey" : [350, WIDTH, 254, 287], "Dalvin Cook" : [350, WIDTH, 287, 322], "Saquon Barkley" : [350, WIDTH, 322, 359], "Ezekiel Elliot" : [350, WIDTH, 359, 394], "Derrick Henry" : [350, WIDTH, 394, 429], "Davante Adams" : [350, WIDTH, 429, 464], "Travis Kelce" : [350, WIDTH, 464, 499], "Stefon Diggs" : [350, WIDTH, 499, 534], "Calvin Ridley" : [350, WIDTH, 534, 569], "Darren Waller" : [350, WIDTH, 569, 604], "DeAndre Hopkins" : [350, WIDTH, 604, 639], "Justin Jefferson" : [350, WIDTH, 639, 674], "George Kittle" : [350, WIDTH, 674, 709], "Patrick Mahomes" : [350, WIDTH, 709, 744], "T.J. Hockenson" : [350, WIDTH, 744, 779], "Josh Allen" : [350, WIDTH, 779, 814], "Mark Andrews" : [350, WIDTH, 814, 849], "Lamar Jackson" : [350, WIDTH, 849, 884], "Dak Prescott" : [350, WIDTH, 884, 919], "Russel Wilson" : [350, WIDTH, 919, 954]}
player_rankings = {"Christian McCafferey" : "1", "Dalvin Cook" : "2", "Saquon Barkley" : "3", "Ezekiel Elliot" : "4", "Derrick Henry" : "5", "Davante Adams" : "5", "Travis Kelce" : "6", "Stefon Diggs" : "7", "Calvin Ridley" : "8", "Darren Waller" : "9", "DeAndre Hopkins" : "10", "Justin Jefferson" : "11", "George Kittle" : "12", "Patrick Mahomes" : "13", "T.J. Hockenson" : "14", "Josh Allen" : "15", "Mark Andrews" : "16", "Lamar Jackson" : "17", "Dak Prescott" : "18", "Russel Wilson" : "20"}

main_font = pygame.font.SysFont("comicsans", 30)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fantasy Draft Room")

# Takes the current drafter to determine which UI to display, and displays
# all current available players on to the main screen.
def display_player(current_drafter):
    win.blit(draft_boards[current_drafter], (0,0))
    rank_x, name_x, y, remove_player = 397, 472, 263, ""

    for player in player_rankings.keys():
        # In main, when a user confirms to draft a player, that same player's
        # rank will be turned to None, indicating that he no longer will be displayed
        if player_rankings[player] == None:
            remove_player = player
            # If a player has y coordinates larger than the drafted player,
            # move players after up 35 points.
            for x in player_ranking_pts.keys():
                if player_ranking_pts[player][2] < player_ranking_pts[x][2]:
                    player_ranking_pts[x][2] -= 35
                    player_ranking_pts[x][3] -= 35
            player_ranking_pts.pop(player)
        else:
            # When there's no None type, simply display players as they come.
            rank = main_font.render(player_rankings[player], 1, (0,0,0))
            name = main_font.render(player, 1, (0,0,0))
            win.blit(rank, (397,y))
            win.blit(name, (472,y))
            y += 35
    if remove_player != "":
        player_rankings.pop(remove_player)

# Displays and updates the drafted teams real time
def display_teams():
    x1, x2, x3, x4, x5, y = 385, 585, 785, 985, 1185, 275
    win.blit(pygame.image.load("Team_Display.png"), (0,0))
    team_pictures(x1, y, team1)
    team_pictures(x2, y, team2)
    team_pictures(x3, y, team3)
    team_pictures(x4, y, team4)
    team_pictures(x5, y, team5)

# Refactored Code for displaying each player from each team
def team_pictures(x, y, team):
    for player in team:
        win.blit(pygame.transform.scale(pygame.image.load(team[player]), (125, 100)), (x, y))
        y += 125

# Utilize x,y points to determine if a player is selected by drafter.
# the selected player will then appear at top of screen with draft button
# return True to indicate that the drafter is ready to draft a player
def selectable_player(x,y, current_drafter):
    for player_pts in player_ranking_pts.keys():
        if player_ranking_pts[player_pts][0] < x < player_ranking_pts[player_pts][1] and player_ranking_pts[player_pts][2] < y < player_ranking_pts[player_pts][3]:
            win.blit(draft_boards[current_drafter], (0,0))
            display_player(current_drafter)
            win.blit(pygame.transform.scale(pygame.image.load(player_ranking_imgs[player_pts]), (125,100)), (408, 5))
            win.blit(pygame.image.load("draft_button.png"), (50, 5))
            return True, player_pts

def main():
    # now = datetime.datetime.now()
    # sec = now.strftime("%S")
    # while sec != 40:
    #     current = sec
    #     if current != sec:
    #         print(sec)
    #     now = datetime.datetime.now()
    #     sec = now.strftime("%S")
    run = True
    start, round = 0, 1
    display_player(start)
    will_draft, player = False, ""
    while run: # can prob put the time in here while it updates
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 854 < pos[0] < 1350 and 115 < pos[1] < 215:
                    display_teams()
                elif 350 < pos[0] < 853 and 115 < pos[1] < 215:
                    display_player(start)
                elif not will_draft:
                    will_draft, player = selectable_player(pos[0], pos[1], start)
                else:
                    if 656 < pos[0] < 856 and 40 < pos[1] < 90:
                        player_rankings[player] = None
                        list_of_teams[start][player] = player_ranking_imgs[player]
                        if round % 2 == 0:
                            start -= 1
                        else:
                            start += 1
                        if start == 5:
                            round += 1
                            start -= 1
                        elif start == -1:
                            round += 1
                            start += 1
                        display_player(start)
                    will_draft = False
        #now = datetime.datetime.now()
        #time_label

main()
