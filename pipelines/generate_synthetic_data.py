

from pathlib import Path

import pandas as pd
from faker import Faker

RAW_DATA_DIR = Path("data/raw")
fake = Faker()


def generate_users(user_count: int = 1000) -> pd.DataFrame:
    users = []

    countries = ["FR", "US", "GB", "CA", "MA", "BE", "CH"]
    languages = ["fr", "en"]
    genders = ["male", "female", "other"]
    fitness_goals = ["lose_weight", "gain_muscle", "maintain", "health"]
    fitness_levels = ["beginner", "intermediate", "advanced"]
    diet_types = ["standard", "halal", "vegan", "vegetarian", "keto"]
    acquisition_channels = ["organic", "tiktok", "instagram", "google", "referral"]
    device_types = ["ios_pwa", "android_pwa", "desktop"]

    for index in range(user_count):
        signup_date = fake.date_between(start_date="-12M", end_date="today")
        is_premium = fake.boolean(chance_of_getting_true=28)

        users.append(
            {
                "user_id": f"user_{index + 1:05d}",
                "signup_date": signup_date,
                "country": fake.random_element(countries),
                "language": fake.random_element(languages),
                "age": fake.random_int(min=18, max=55),
                "gender": fake.random_element(genders),
                "fitness_goal": fake.random_element(fitness_goals),
                "fitness_level": fake.random_element(fitness_levels),
                "diet_type": fake.random_element(diet_types),
                "acquisition_channel": fake.random_element(acquisition_channels),
                "device_type": fake.random_element(device_types),
                "is_premium": is_premium,
                "created_at": signup_date,
            }
        )

    return pd.DataFrame(users)


def main() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    users = generate_users(user_count=1000)
    users.to_csv(RAW_DATA_DIR / "raw_users.csv", index=False)

    print(f"Generated {len(users)} users")
    print(f"Wrote {RAW_DATA_DIR / 'raw_users.csv'}")


if __name__ == "__main__":
    main()