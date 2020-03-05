from office.models import Office


mock_data = [
    {
        "name": "Test Clinic 1",
        "street_address": "First Street Address",
        "city": "Bangalore",
        "state": "Karnataka",
        "country": "India",
        "zip": 560102
    },
    {
        "name": "Test Clinic 2",
        "street_address": "Second Street Address",
        "city": "Bangalore",
        "state": "Karnataka",
        "country": "India",
        "zip": 560102
    },
    {
        "name": "Test Clinic 3",
        "street_address": "Third Street Address",
        "city": "Bangalore",
        "state": "Karnataka",
        "country": "India",
        "zip": 560102
    }
]


def create_office():
    for datum in mock_data:
        Office.objects.create(
            name=datum['name'],
            street_address=datum['street_address'],
            city=datum['city'],
            state=datum['state'],
            country=datum['country'],
            zip=datum['zip']
        )

create_office()
