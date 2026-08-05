from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("process/", views.process, name="process"),
    path("case-studies/", views.case_studies, name="case_studies"),
    path("case-studies/<slug:slug>/", views.case_study_detail, name="case_study_detail"),
    path("case-study-detail/", views.case_study_detail, name="case_study_detail_all"),
    path("contact/", views.contact, name="contact"),
]
