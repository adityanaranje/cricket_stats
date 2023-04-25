from django.shortcuts import render
import pandas as pd
from Mypackage import rankings
import pickle
#from StreamlitApp.Mypackage import dataset, helper

# Create your views here.

def index(request):
    return render(request, 'index.html')

def scorePrediction(request):
    model = pickle.load(open('model/t20score_predictor.pkl','rb'))

    team_avg = pd.read_csv('data/team_average.csv')
    city_avg = pd.read_csv('data/city_average.csv')
    
    abr = ['AFG','AUS','BAN','ENG','IND','IRE','NAM','NED','NZ','OMA','PAK','PNG','SCO','RSA','SL','WI']

    team = list(team_avg['team'])
    bowl_teams = list(team_avg['team'])

    bat_avg = list(team_avg['batting_average'])
    bowl_avg = list(team_avg['bowling_average'])
    cities = list(city_avg['city'])
    c_avg = list(city_avg['Average_runs'])
    
    pred = 0
    if request.method == "POST":
        pred = 1
        bat_team = str(request.POST['bat_team'])
        bowl_team = str(request.POST['bowl_team'])
        city = str(request.POST['city'])
        past_five = request.POST['past_five']
        score = int(request.POST['score'])
        wickets = int(request.POST['wickets'])
        over = int(request.POST['over'])
        ball = int(request.POST['ball'])
        
        balls = over*6 + ball
        balls_left = 120 - balls
        wickets_left = 10 - wickets
        crr = score*6/balls
        
        batting_team_avg = bat_avg[team.index(bat_team)]
        bowling_team_avg = bowl_avg[team.index(bowl_team)]
        city_avg = c_avg[cities.index(city)]
        
        data = pd.DataFrame({'batting_team':[bat_team], 'bowling_team':[bowl_team], 'city':[city],
                            'current_score':[score], 'balls_left':[balls_left],'wickets_left':[wickets_left],
                            'crr':[crr],'last_five':[past_five], 'batting_team_avg':[batting_team_avg],
                            'bowling_team_avg':[bowling_team_avg], 'city_avg':[city_avg]})

        team_name= abr[team.index(bat_team)]

        predicted = int(model.predict(data))
        runs_c = int(score+int(crr*balls_left/6))
        runs_6 = int(score+int(6*balls_left/6))
        runs_8 = int(score+int(8*balls_left/6))
        runs_10 = int(score+int(10*balls_left/6))
        runs_12 = int(score+int(12*balls_left/6))

        
        output = {"bat_team":bat_team, 
                  "bowl_team":bowl_team,
                  "team_name":team_name,
                  "score":score,
                  "wickets":wickets,
                  "over":over,
                  "ball":ball,
                  "crr":round(crr,2),
                  "predicted":predicted, 
                  "runs_crr":runs_c, 
                  "runs_6":runs_6, 
                  "runs_8":runs_8, 
                  "runs_10":runs_10, 
                  "runs_12":runs_12,}
        return render(request, 'score_prediction.html', {"pred":pred,"bat_teams":team,"bowl_teams":bowl_teams,"cities":cities,"output":output})


    return render(request, 'score_prediction.html', {"pred":pred,"bat_teams":team,"bowl_teams":bowl_teams,"cities":cities})

def winPrediction(request):
    
    teams = ['Royal Challengers Bangalore', 'Rajasthan Royals',
       'Chennai Super Kings', 'Mumbai Indians', 'Kings XI Punjab',
       'Kolkata Knight Riders', 'Delhi Capitals', 'Sunrisers Hyderabad',
       "Gujrat Titans","Lucknow Super Giants"]
    bowl_teams = teams.copy()

    logo = ['rcb','rr','csk','mi','pk','kkr','dc','srh',"gt","lsg"]


    cities = ['Dharamsala', 'Kolkata', 'Bangalore', 'Jaipur', 'Mumbai',
    'Chandigarh', 'Abu Dhabi', 'Chennai', 'Durban', 'Delhi','Visakhapatnam',
        'Port Elizabeth', 'Hyderabad', 'Pune','Lucknow','Johannesburg', 'Indore',
        'Sharjah', 'Bengaluru', 'Ranchi','Centurion', 'Cape Town', 'Cuttack',
        'Kimberley', 'Ahmedabad','Raipur', 'Mohali', 'East London', 
        'Bloemfontein', 'Nagpur']
    
    model = pickle.load(open('model/iplwin_predictor.pkl','rb'))
    
    pred = 0
    if request.method == "POST":
        pred = 1
        bat_team = str(request.POST['batteam'])
        
        bowl_team = str(request.POST['bowlteam'])
        
        city = str(request.POST['city'])
        target = int(request.POST['target'])
        score = int(request.POST['score'])
        wickets = int(request.POST['wickets'])
        over = int(request.POST['over'])
        ball = int(request.POST['ball'])
        
        logo1 = logo[teams.index(bat_team)]
        logo2 = logo[teams.index(bowl_team)]
        
        output = {"batteam":bat_team,
                  "bowlteam":bowl_team,
                  "team_name1":logo1.upper(),
                  "team_name2":logo2.upper(),
                  "logo1":logo1,
                  "logo2":logo2}
        
        if bat_team == 'Punjab Kings':
            bat_team = 'Kings XI Punjab'
        if bowl_team == 'Punjab Kings':
            bowl_team = 'Kings XI Punjab'
            
        if bat_team == "Lucknow Super Giants":
            bat_team = "Rajasthan Royals"
        if bowl_team == "Lucknow Super Giants":
            bowl_team = "Rajasthan Royals"
        if bat_team == "Gujrat Titans":
            bat_team = "Kolkata Knight Riders"
        if bowl_team == "Gujrat Titans":
            bowl_team = "Kolkata Knight Riders"
            
        if city=="Lucknow":
            city = "Delhi"
        
        runs_left = target - score
        balls = over*6 + ball
        ball_left = 120 - balls
        
        crr = round(score*6/balls,2)
        rrr = round(runs_left*6/ball_left,2)
        
        
        df = pd.DataFrame({'batting_team':[bat_team], 'bowling_team':[bowl_team], 'city':[city], 'runs_left':[runs_left],
                   'balls_left':[ball_left],'wickets':[wickets], 'total_runs_x':[score], 'crr':[crr], 'rrr':[rrr]})

        

        if model.classes_[0]==0:
            loss = float(model.predict_proba(df)[:,0])
        if model.classes_[1]==0:
            loss = float(model.predict_proba(df)[:,1])

        loss = float(round(loss*100,2))
        if wickets<6 and loss>75 and (rrr-crr)<=4 and ball<=80:
            loss = loss-30

        if wickets<=4 and loss>65 and (rrr-crr)<=5.5 and ball<=90:
            loss = loss-35

        if wickets<8 and loss>80 and (rrr-crr)<=5 and ball_left>=96 and ball_left<120:
            loss = loss-35

        if wickets>=6 and loss<60 and rrr>14 and ball_left<30:
            loss = loss+20

        loss = round(loss,2)
        win = round(100-loss,2)
        
        if bat_team == 'Kings XI Punjab':
            bat_team = 'Punjab Kings'
        if bowl_team == 'Kings XI Punjab':
            bowl_team = 'Punjab Kings'
       
        
        output["score"] = score 
        output["wickets"] = wickets
        output["target"] = target 
        output["over"] = over
        output["ball"] = ball 
        output["crr"] = crr 
        output["rrr"] = rrr 
        output["win"] = win
        output["loss"] = loss
        
        return render(request, 'win_pridection.html', {"pred":pred,"bat_teams":teams, "bowl_teams":bowl_teams,"cities":cities,"output":output})


    

    return render(request, 'win_pridection.html', {"pred":pred,"bat_teams":teams, "bowl_teams":bowl_teams,"cities":cities})


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')


def t20_mens_team(request):
    url = "https://www.icc-cricket.com/rankings/mens/team-rankings/t20i"
            
    rank = rankings.get_team_rankings(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/mens_team.html', {"df":df})

def t20_womens_team(request):
    url = "https://www.icc-cricket.com/rankings/womens/team-rankings/t20i"
            
    rank = rankings.get_team_rankings(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/womens_team.html', {"df":df})

def t20_mens_batting(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/t20i/batting"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/mens_batting.html', {"df":df})

def t20_womens_batting(request):
    url = "https://www.icc-cricket.com/rankings/womens/player-rankings/t20i/batting"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/womens_batting.html', {"df":df})

def t20_mens_bowling(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/t20i/bowling"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/mens_bowling.html', {"df":df})

def t20_womens_bowling(request):
    url = "https://www.icc-cricket.com/rankings/womens/player-rankings/t20i/bowling"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/womens_bowling.html', {"df":df})

def t20_mens_allround(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/t20i/all-rounder"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/mens_allround.html', {"df":df})

def t20_womens_allround(request):
    url = "https://www.icc-cricket.com/rankings/womens/player-rankings/t20i/all-rounder"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 't20/womens_allround.html', {"df":df})


def odi_mens_team(request):
    url = "https://www.icc-cricket.com/rankings/mens/team-rankings/odi"
            
    rank = rankings.get_team_rankings(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/mens_team.html', {"df":df})

def odi_womens_team(request):
    url = "https://www.icc-cricket.com/rankings/womens/team-rankings/odi"
            
    rank = rankings.get_team_rankings(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/womens_team.html', {"df":df})

def odi_mens_batting(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/odi/batting"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/mens_batting.html', {"df":df})

def odi_womens_batting(request):
    url = "https://www.icc-cricket.com/rankings/womens/player-rankings/odi/batting"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/womens_batting.html', {"df":df})

def odi_mens_bowling(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/odi/bowling"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/mens_bowling.html', {"df":df})

def odi_womens_bowling(request):
    url = "https://www.icc-cricket.com/rankings/womens/player-rankings/odi/bowling"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/womens_bowling.html', {"df":df})

def odi_mens_allround(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/odi/all-rounder"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/mens_allround.html', {"df":df})

def odi_womens_allround(request):
    url = "https://www.icc-cricket.com/rankings/womens/player-rankings/odi/all-rounder"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'odi/womens_allround.html', {"df":df})

def test_mens_team(request):
    url = "https://www.icc-cricket.com/rankings/mens/team-rankings/test"
            
    rank = rankings.get_team_rankings(url)
    df = rank.to_dict(orient='records')

    return render(request, 'test/mens_team.html', {"df":df})

def test_mens_batting(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/test/batting"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'test/mens_batting.html', {"df":df})


def test_mens_bowling(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/test/bowling"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'test/mens_bowling.html', {"df":df})


def test_mens_allround(request):
    url = "https://www.icc-cricket.com/rankings/mens/player-rankings/test/all-rounder"
            
    rank = rankings.get_player_ranking(url)
    df = rank.to_dict(orient='records')

    return render(request, 'test/mens_allround.html', {"df":df})
