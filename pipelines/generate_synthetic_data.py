import json
import random
from datetime import datetime, timedelta
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



def generate_events(users: pd.DataFrame) -> pd.DataFrame:
    events = []
    event_id = 1

    for _, user in users.iterrows():
        user_id = user["user_id"]
        signup_date = pd.to_datetime(user["signup_date"]).date()
        end_date = datetime.today().date()

        session_index = 1

        # Signup and onboarding events
        onboarding_events = [
            "user_signed_up",
            "onboarding_started",
            "onboarding_step_completed",
            "onboarding_step_completed",
            "onboarding_step_completed",
            "onboarding_completed",
        ]

        for step_index, event_name in enumerate(onboarding_events):
            event_time = datetime.combine(signup_date, datetime.min.time()) + timedelta(
                minutes=5 * step_index + random.randint(0, 3)
            )

            events.append(
                {
                    "event_id": f"evt_{event_id:08d}",
                    "user_id": user_id,
                    "session_id": f"{user_id}_session_{session_index:04d}",
                    "event_name": event_name,
                    "event_timestamp": event_time,
                    "event_date": event_time.date(),
                    "platform": "pwa",
                    "device_type": user["device_type"],
                    "country": user["country"],
                    "properties": json.dumps(
                        {
                            "source": "onboarding",
                            "language": user["language"],
                            "step_index": step_index,
                        }
                    ),
                }
            )
            event_id += 1

        active_days = random.randint(5, 120)

        for day_offset in range(active_days):
            event_date = signup_date + timedelta(days=day_offset)
            if event_date > end_date:
                break

            # Users are not active every day
            if random.random() > 0.42:
                continue

            session_count = random.choices([1, 2, 3], weights=[70, 22, 8])[0]

            for _ in range(session_count):
                session_index += 1
                session_id = f"{user_id}_session_{session_index:04d}"
                session_start = datetime.combine(event_date, datetime.min.time()) + timedelta(
                    hours=random.randint(6, 22),
                    minutes=random.randint(0, 59),
                )

                daily_events = ["home_viewed"]

                if random.random() < 0.45:
                    daily_events.append("coach_opened")
                    daily_events.append("ai_message_sent")
                    daily_events.append("ai_response_received")

                if random.random() < 0.38:
                    daily_events.append("meal_logged")

                if random.random() < 0.18:
                    daily_events.append("ai_macro_estimate_requested")
                    if random.random() < 0.72:
                        daily_events.append("ai_macro_estimate_accepted")

                if random.random() < 0.24:
                    daily_events.append("workout_logged")

                if random.random() < 0.20:
                    daily_events.append("water_logged")

                if random.random() < 0.08:
                    daily_events.append("weight_logged")

                if random.random() < 0.06:
                    daily_events.append("sleep_logged")

                if random.random() < 0.05:
                    daily_events.append("progress_photo_uploaded")

                if random.random() < 0.16:
                    daily_events.append("walk_opened")
                    if random.random() < 0.70:
                        daily_events.append("walk_route_generated")
                        if random.random() < 0.42:
                            daily_events.append("walk_navigation_started")
                            daily_events.append("walk_completed")
                            daily_events.append("walk_saved")
                    else:
                        daily_events.append("walk_route_generation_failed")

                if random.random() < 0.03:
                    daily_events.append("streak_reminder_clicked")

                for event_position, event_name in enumerate(daily_events):
                    event_time = session_start + timedelta(minutes=event_position * random.randint(1, 4))

                    properties = {
                        "language": user["language"],
                        "fitness_goal": user["fitness_goal"],
                    }

                    if event_name == "ai_message_sent":
                        properties["message_length"] = random.randint(20, 280)

                    if event_name == "meal_logged":
                        properties["meal_type"] = random.choice(["breakfast", "lunch", "dinner", "snack"])
                        properties["calories"] = random.randint(180, 900)

                    if event_name == "workout_logged":
                        properties["workout_type"] = random.choice(
                            ["running", "cycling", "swimming", "strength", "yoga", "walking"]
                        )
                        properties["duration_min"] = random.randint(15, 90)

                    if event_name == "walk_route_generated":
                        properties["route_mode"] = random.choice(["loop", "direct", "custom"])
                        properties["target_type"] = random.choice(["calories", "minutes", "distance"])
                        properties["distance_km"] = round(random.uniform(1.2, 8.5), 2)

                    events.append(
                        {
                            "event_id": f"evt_{event_id:08d}",
                            "user_id": user_id,
                            "session_id": session_id,
                            "event_name": event_name,
                            "event_timestamp": event_time,
                            "event_date": event_time.date(),
                            "platform": "pwa",
                            "device_type": user["device_type"],
                            "country": user["country"],
                            "properties": json.dumps(properties),
                        }
                    )
                    event_id += 1

    return pd.DataFrame(events)


def main() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    users = generate_users(user_count=1000)
    users.to_csv(RAW_DATA_DIR / "raw_users.csv", index=False)

    events = generate_events(users)
    events.to_csv(RAW_DATA_DIR / "raw_events.csv", index=False)

    print(f"Generated {len(users)} users")
    print(f"Wrote {RAW_DATA_DIR / 'raw_users.csv'}")
    print(f"Generated {len(events)} events")
    print(f"Wrote {RAW_DATA_DIR / 'raw_events.csv'}")

    


if __name__ == "__main__":
    main()

