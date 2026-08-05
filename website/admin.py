from django.contrib import admin

from .models import CaseStudy, Client, HomeBanner, Partner, Testimonial

admin.site.site_header = "Naar Enterprise CMS"
admin.site.site_title = "Naar Admin"
admin.site.index_title = "Manage website content"


@admin.register(HomeBanner)
class HomeBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "updated_at")
    list_filter = ("is_active",)
    list_editable = ("is_active",)


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "order", "is_published", "updated_at")
    list_filter = ("is_published",)
    list_editable = ("order", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "tag", "summary")
    fieldsets = (
        (None, {"fields": ("title", "slug", "tag", "summary", "image", "order", "is_published")}),
        ("Detail page", {"fields": ("challenge", "solution")}),
        (
            "Meta labels",
            {
                "fields": ("meta_inspection", "meta_integration", "meta_outcome"),
                "description": "Shown in the three columns on the case study detail page.",
            },
        ),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("attribution", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("quote", "attribution")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "category")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "category")
