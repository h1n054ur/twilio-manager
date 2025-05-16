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
            # ... include all regions as needed
        }
    },
    # Add other countries: CA, GB, AU, etc.
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