# Centralized country and region data
COUNTRY_DATA = {
    'US': {
        'name': 'United States',
        'number_types': {
            'local': 1.15,
            'mobile': 1.15,
            'tollfree': 2.15,
        },
        'regions': {
            'Alabama': {'code': 'AL', 'area_codes': [205, 251, 256, 334, 938]},
            'Alaska': {'code': 'AK', 'area_codes': [907]},
            'Arizona': {'code': 'AZ', 'area_codes': [480, 520, 602, 623, 928]},
            'Arkansas': {'code': 'AR', 'area_codes': [479, 501, 870]},
            'California': {'code': 'CA', 'area_codes': [209, 213, 310, 415, 510, 530, 559, 619, 626, 650, 661, 707, 714, 805, 818, 858, 909, 916, 925, 949]},
        }
    },
    'CA': {
        'name': 'Canada',
        'number_types': {
            'local': 1.25,
            'mobile': 1.25,
            'tollfree': 2.25,
        },
        'regions': {
            'Ontario': {'code': 'ON', 'area_codes': [416, 437, 647, 905]},
            'Quebec': {'code': 'QC', 'area_codes': [418, 438, 450, 514, 579, 581, 819]},
            'British Columbia': {'code': 'BC', 'area_codes': [236, 250, 604, 672, 778]},
        }
    },
    'GB': {
        'name': 'United Kingdom',
        'number_types': {
            'local': 1.35,
            'mobile': 1.35,
            'tollfree': 2.35,
        },
        'regions': {
            'London': {'code': 'LDN', 'area_codes': [20]},
            'Manchester': {'code': 'MAN', 'area_codes': [161]},
            'Birmingham': {'code': 'BIR', 'area_codes': [121]},
        }
    },
    'AU': {
        'name': 'Australia',
        'number_types': {
            'local': 1.45,
            'mobile': 1.45,
            'tollfree': 2.45,
        },
        'regions': {
            'New South Wales': {'code': 'NSW', 'area_codes': [2]},
            'Victoria': {'code': 'VIC', 'area_codes': [3]},
            'Queensland': {'code': 'QLD', 'area_codes': [7]},
        }
    }
}

def get_area_codes(country_iso: str):
    country = COUNTRY_DATA.get(country_iso.upper())
    return country['regions'] if country else {}

def validate_country_iso(country_iso: str) -> bool:
    return country_iso.upper() in COUNTRY_DATA

def validate_phone_pattern(pattern: str) -> bool:
    return pattern.isdigit() and 0 < len(pattern) <= 10

def validate_capabilities(capabilities):
    valid = {'voice', 'sms', 'mms'}
    return set(capabilities).issubset(valid)