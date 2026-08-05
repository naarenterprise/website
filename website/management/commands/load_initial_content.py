import shutil
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from website.models import CaseStudy, Client, HomeBanner, Partner, Testimonial


class Command(BaseCommand):
    help = "Load initial website content from the static template defaults."

    def handle(self, *args, **options):
        assets_dir = Path(settings.BASE_DIR) / "assets"

        if not HomeBanner.objects.exists():
            banner_path = assets_dir / "case-automotive.jpg"
            if banner_path.exists():
                with banner_path.open("rb") as image_file:
                    HomeBanner.objects.create(
                        title="Default hero banner",
                        image=File(image_file, name="default-hero.jpg"),
                        is_active=True,
                    )
                self.stdout.write(self.style.SUCCESS("Created home banner."))

        case_studies = [
            {
                "slug": "automotive",
                "tag": "AUTOMOTIVE / FINAL ASSEMBLY",
                "title": "Zero-fault final assembly",
                "summary": "A global EV maker reduced manual verification and caught errors before final test.",
                "image": "case-automotive.jpg",
                "challenge": "A complex vehicle subassembly required manual checks for component presence, orientation and finish at the end of the line.",
                "solution": "We designed an enclosed inspection cell with purpose-built fixtures, multi-angle lighting, AI verification and a PLC-connected reject decision.",
                "meta_inspection": "Presence & finish",
                "meta_integration": "PLC & traceability",
                "meta_outcome": "Fewer escapes",
                "order": 1,
            },
            {
                "slug": "electronics",
                "tag": "ELECTRONICS / PCB",
                "title": "Finding what the eye misses",
                "summary": "Vision models made microscopic solder defects traceable at production speed.",
                "image": "case-electronics.jpg",
                "challenge": "Small solder and component-placement errors were difficult to detect consistently across a fast-moving production process.",
                "solution": "A high-resolution AI vision station classified placement, solder and surface anomalies while maintaining a complete board-level image record.",
                "meta_inspection": "Component & solder",
                "meta_integration": "Anomaly detection",
                "meta_outcome": "Traceable quality",
                "order": 2,
            },
            {
                "slug": "medical",
                "tag": "MEDICAL DEVICE / PACKAGING",
                "title": "Every seal accounted for",
                "summary": "Inline inspection brought complete confidence to a high-throughput packaging line.",
                "image": "case-medical.jpg",
                "challenge": "Packaging quality needed a repeatable final check for seal integrity, label placement and readable lot information.",
                "solution": "We integrated vision, OCR and defect rules into a compact automated station that records the decision for every pack.",
                "meta_inspection": "Seal, label & OCR",
                "meta_integration": "Batch traceability",
                "meta_outcome": "Audit-ready record",
                "order": 3,
            },
            {
                "slug": "energy",
                "tag": "ENERGY / BATTERY",
                "title": "Raising the cell quality floor",
                "summary": "Automated detection identified coating variation before it reached pack assembly.",
                "image": "case-energy.jpg",
                "challenge": "Variation in coating and assembly required earlier detection, before components progressed to expensive downstream stages.",
                "solution": "An edge AI inspection system highlights abnormal patterns, links them to process conditions and helps teams isolate the cause quickly.",
                "meta_inspection": "Surface variation",
                "meta_integration": "Process anomaly",
                "meta_outcome": "Earlier intervention",
                "order": 4,
            },
        ]

        for data in case_studies:
            if CaseStudy.objects.filter(slug=data["slug"]).exists():
                continue
            image_path = assets_dir / data["image"]
            case = CaseStudy(
                slug=data["slug"],
                tag=data["tag"],
                title=data["title"],
                summary=data["summary"],
                challenge=data["challenge"],
                solution=data["solution"],
                meta_inspection=data["meta_inspection"],
                meta_integration=data["meta_integration"],
                meta_outcome=data["meta_outcome"],
                order=data["order"],
            )
            if image_path.exists():
                with image_path.open("rb") as image_file:
                    case.image.save(data["image"], File(image_file), save=False)
            case.save()
            self.stdout.write(self.style.SUCCESS(f"Created case study: {case.title}"))

        testimonials = [
            {
                "quote": "The team did not simply install a camera. They engineered a complete inspection station that our operators could trust from the first shift.",
                "attribution": "QUALITY HEAD / AUTOMOTIVE COMPONENTS",
                "order": 1,
            },
            {
                "quote": "We finally have a clear record of every defect, and can see the process patterns before they become a customer issue.",
                "attribution": "OPERATIONS DIRECTOR / PRECISION MANUFACTURING",
                "order": 2,
            },
            {
                "quote": "Naar gave our operators an extra set of expert eyes, with a record of every decision.",
                "attribution": "QUALITY DIRECTOR / TIER 1 MANUFACTURER",
                "order": 3,
            },
        ]

        for data in testimonials:
            Testimonial.objects.get_or_create(
                attribution=data["attribution"],
                defaults={"quote": data["quote"], "order": data["order"]},
            )

        clients = [
            ("AUTOMOTIVE", "Orion Mobility", 1),
            ("CONSUMER ELECTRONICS", "Northstar Devices", 2),
            ("ENERGY", "Gridform", 3),
            ("MEDICAL TECHNOLOGY", "Vitala Systems", 4),
            ("INDUSTRIAL AUTOMATION", "Axial Works", 5),
            ("PACKAGING", "Formline", 6),
            ("MANUFACTURING", "Alloy & Co.", 7),
            ("LOGISTICS", "Forward Assembly", 8),
        ]

        for category, name, order in clients:
            Client.objects.get_or_create(name=name, defaults={"category": category, "order": order})

        partners = [
            ("VISION HARDWARE", "OptiLine Systems", 1),
            ("EDGE COMPUTE", "ForgeEdge", 2),
            ("FACTORY SOFTWARE", "LinePulse", 3),
            ("ROBOTICS", "AxisCell Robotics", 4),
        ]

        for category, name, order in partners:
            Partner.objects.get_or_create(name=name, defaults={"category": category, "order": order})

        media_assets = Path(settings.MEDIA_ROOT) / "seed-assets"
        media_assets.mkdir(parents=True, exist_ok=True)
        for filename in ("case-automotive.jpg", "case-electronics.jpg", "case-medical.jpg", "case-energy.jpg"):
            source = assets_dir / filename
            if source.exists():
                shutil.copy2(source, media_assets / filename)

        self.stdout.write(self.style.SUCCESS("Initial content loaded. Log in to /admin/ to manage it."))
