
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("analysis", views.winPrediction, name='analysis'),
    path("score_prediction", views.scorePrediction, name='score_rediction'),
    path("win_prediction", views.winPrediction, name='win_prediction'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("login", views.login, name='login'),
    path("signup", views.signup, name='signup'),
    path("t20/mens_team", views.t20_mens_team, name="t20_mens_team"),
    path("t20/womens_team", views.t20_womens_team, name="t20_womens_team"),
    path("t20/mens_batting", views.t20_mens_batting, name="t20_mens_batting"),
    path("t20/mens_bowling", views.t20_mens_bowling, name="t20_mens_bowling"),
    path("t20/mens_allround", views.t20_mens_allround, name="t20_mens_allround"),
    path("t20/womens_batting", views.t20_womens_batting, name="t20_womens_batting"),
    path("t20/womens_bowling", views.t20_womens_bowling, name="t20_womens_bowling"),
    path("t20/womens_allround", views.t20_womens_allround, name="t20_womens_allround"),
    path("odi/mens_team", views.odi_mens_team, name="odi_mens_team"),
    path("odi/womens_team", views.odi_womens_team, name="odi_womens_team"),
    path("odi/mens_batting", views.odi_mens_batting, name="odi_mens_batting"),
    path("odi/mens_bowling", views.odi_mens_bowling, name="odi_mens_bowling"),
    path("odi/mens_allround", views.odi_mens_allround, name="odi_mens_allround"),
    path("odi/womens_batting", views.odi_womens_batting, name="odi_womens_batting"),
    path("odi/womens_bowling", views.odi_womens_bowling, name="odi_womens_bowling"),
    path("odi/womens_allround", views.odi_womens_allround, name="odi_womens_allround"),
    path("test/mens_team", views.test_mens_team, name="test_mens_team"),
    path("test/mens_batting", views.test_mens_batting, name="test_mens_batting"),
    path("test/mens_bowling", views.test_mens_bowling, name="test_mens_bowling"),
    path("test/mens_allround", views.test_mens_allround, name="test_mens_allround")
]
