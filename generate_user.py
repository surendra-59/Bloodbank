import os
import django
import random
from datetime import datetime, timedelta
from faker import Faker

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_sm.settings")  # <- Change this
django.setup()

from myapp.models import CustomUser  # <- Change this

fake = Faker()

GENDERS = ['M', 'F', 'O']
BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

# Replace with actual image path later
sample_identity_path = "C:/Users/suresh/Desktop/ss1.jpg"

for i in range(2, 1001):
    email = f"myuser{i}@gmail.com"
    password = "111"
    # first_name = fake.first_name()
    # last_name = fake.last_name()
    gender = random.choice(GENDERS)
    dob = fake.date_of_birth(minimum_age=18, maximum_age=60)
    blood_group = random.choice(BLOOD_GROUPS)
    # contact_number = fake.phone_number()
    address = fake.address()
    first_name=fake.first_name()[:15]
    last_name=fake.last_name()[:15]
    contact_number=fake.phone_number()[:15]

    # The method CustomUser.objects.create_user() is 
    # responsible for creating a new user record in your PostgreSQL database (via Django's ORM).

    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        dob=dob,
        blood_group=blood_group,
        contact_number=contact_number,
        identity=sample_identity_path,
        address=address,
        user_type="3",
        is_approved=True
    )

    print(f"Created user: {email}")

print("✅ Done creating 1000 users.")
