import os

CHROMEDRIVER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "chromedriver.exe"
)
DUESSELDORF_BASE_URL = "https://termine.duesseldorf.de"
BERLIN_BASE_URL = "https://service.berlin.de/terminvereinbarung/termin/all/120703/"
BREMEN_BASE_URL = "https://termin.bremen.de/termine/select2?md=5"

DUESSELDORF = {
    "offices": [
        "Benrath",
        "Bilk",
        "Dienstleistungszentrum",
        "Eller",
        "Garath",
        "Gerresheim",
        "Kaiserswerth",
        "Oberkassel",
        "Rath",
        "Unterbach",
        "Wersten/Holthausen",
    ],
    "base_url": "https://termine.duesseldorf.de",
    "einwohnerangelegenheiten": {
        "id": "buttonfunktionseinheit-4",
        "name": "Einwohnerangelegenheiten",
        "concerns": {
            "meldeangelegenheiten": {
                "id": "header_concerns_accordion-3532",
                "sub_concerns": {
                    "anmeldung": {
                        "id": "button-plus-2751",
                        "name": "Anmeldung in Düsseldorf",
                    },
                    "ummeldung": {
                        "id": "button-plus-315",
                        "name": "Ummeldung innerhalb Düsseldorf",
                    },
                    "adressaenderung": {
                        "id": "button-plus-2786",
                        "name": "Adressänderung Fahrzeugschein bei Ummeldung",
                    },
                    "abmeldung": {
                        "id": "button-plus-3165",
                        "name": "Abmeldung eines wohnsitzes",
                    },
                },
            },
            "ausweise": {
                "id": "header_concerns_accordion-3533",
                "sub_concerns": {
                    "personalausweis_antrag": {
                        "id": "button-plus-2816",
                        "name": "Personalausweis - Antrag",
                    },
                    "vorlaeufiger_personalausweis": {
                        "id": "button-plus-2838",
                        "name": "Vorläufiger Personalausweis - Antrag",
                    },
                    "personalausweis_pin": {
                        "id": "button-plus-2852",
                        "name": "Personalausweis - Neusetzung PIN",
                    },
                    "reisepass_antrag": {
                        "id": "button-plus-2863",
                        "name": "Reisepass - Antrag",
                    },
                    "vorlaeufiger_reisepass": {
                        "id": "button-plus-2886",
                        "name": "Vorläufiger Reisepass - Antrag",
                    },
                },
            },
            "bescheinigungen": {
                "id": "header_concerns_accordion-3534",
                "sub_concerns": {
                    "beglaubigung": {
                        "id": "button-plus-2899",
                        "name": "Amtliche Beglaubigung",
                    },
                    "unterschriftsbeglaubigung": {
                        "id": "button-plus-2910",
                        "name": "Unterschriftsbeglaubigung",
                    },
                    "meldebescheinigung": {
                        "id": "button-plus-3158",
                        "name": "Meldebescheinigung",
                    },
                    "melderegisterauskunft": {
                        "id": "button-plus-2940",
                        "name": "Melderegisterauskunft",
                    },
                },
            },
        },
    },
}
BREMEN = {
    "base_url": "https://termin.bremen.de/termine/select2?md=5",
    "einwohnerangelegenheiten": {
        "name": "Einwohnerangelegenheiten",
        "concerns": {
            "ausweise": {
                "id": "header_concerns_accordion-7738",
                "sub_concerns": {
                    "personalausweis_antrag": {
                        "id": "button-plus-9077",
                        "name": "Personalausweis - Antrag",
                    },
                },
            }
        },
    },
}

HANNOVER = {
    "base_url": "http://termin.hannover-stadt.de/buergeramt",
    "plz": "30159",
    "offices": {
        "Aegi": "Aegi",
        "Bemerode": "Bemerode",
        "Doehren": "Doehren",
        "Herrenhausen": "Herrenhausen",
        "Linden": "Linden",
        "Podbi-Park": "Podbi-Park",
        "Ricklingen": "Ricklingen",
        "Sahlkamp": "Sahlkamp",
        "Schuetzenplatz": "Schuetzenplatz",
    },
    "concerns": {
        "personalausweis_antrag": {
            "id": "service_ede3dafc-4941-4e08-9526-bd70d77160ce",
            "name": "Personalausweis - Antrag",
        },
    },
}

DRESDEN = {
    "offices": {
        "Bürgerbüro Altstadt (barrierefrei)": "Altstadt",
        "Bürgerbüro Blasewitz (Teilweise barrierefrei)": "Blasewitz",
        "Meldestelle Cossebaude (barrierefrei)": "Cossebaude",
        "Bürgerbüro Cotta (Teilweise barrierefrei)": "Cotta",
        "Junioramt": "Junioramt",
        "Bürgerbüro Klotzsche (Teilweise barrierefrei)": "Klotzsche",
        "Meldestelle Langebrück (barrierefrei)": "Langenbrueck",
        "Bürgerbüro Leuben": "Leuben",
        "Bürgerbüro Neustadt (barrierefrei)": "Neustadt",
        "Bürgerbüro Pieschen": "Pieschen",
        "Bürgerbüro Plauen (Teilweise barrierefrei)": "Plauen",
        "Bürgerbüro Prohlis (barrierefrei)": "Prohlis",
        "Meldestelle Weixdorf": "Weixdorf",
    },
    "base_url": "https://termine-buergerbuero.dresden.de/select2?md=2",
    "buergerbueros": {
        "name": "Bürgerbüros",
        "concerns": {
            "personaldokumente": {
                "id": "header_concerns_accordion-172",
                "sub_concerns": {
                    "personalausweis_antrag": {
                        "id": "button-plus-317",
                        "name": "Personalausweis - Antrag",
                    },
                },
            }
        },
    },
}
