from django.shortcuts import get_object_or_404, render

from .models import CaseStudy, Client, HomeBanner, Partner, Testimonial


def home(request):
    banner = HomeBanner.objects.filter(is_active=True).first()
    return render(request, "index.html", {"banner": banner})


def about(request):
    testimonials = Testimonial.objects.filter(is_active=True)
    clients = Client.objects.filter(is_active=True)
    partners = Partner.objects.filter(is_active=True)
    return render(
        request,
        "about.html",
        {
            "testimonials": testimonials,
            "clients": clients,
            "partners": partners,
        },
    )


def case_studies(request):
    case_studies_list = CaseStudy.objects.filter(is_published=True)
    featured_testimonial = Testimonial.objects.filter(is_active=True).first()
    return render(
        request,
        "case-studies.html",
        {
            "case_studies": case_studies_list,
            "featured_testimonial": featured_testimonial,
        },
    )


def case_study_detail(request, slug=None):
    case_studies_list = CaseStudy.objects.filter(is_published=True)
    if slug:
        get_object_or_404(CaseStudy, slug=slug, is_published=True)
    return render(request, "case-study-detail.html", {"case_studies": case_studies_list})


def services(request):
    return render(request, "services.html")


def process(request):
    return render(request, "process.html")


def contact(request):
    return render(request, "contact.html")
