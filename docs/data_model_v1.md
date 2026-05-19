# FitConnect Analytics Platform - Data Model V1

## Objective

This project simulates the analytics platform of FitConnect Hub, a production AI fitness PWA.

The V1 data model follows a Product Analytics SaaS approach:
- users
- events
- subscriptions

The goal is to analyze activation, engagement, retention, churn, AI coach usage, walking route usage, and subscription revenue.

## Raw Tables

### raw_users

Grain: one row per user.

Columns:
- user_id
- signup_date
- country
- language
- age
- gender
- fitness_goal
- fitness_level
- diet_type
- acquisition_channel
- device_type
- is_premium
- created_at

### raw_events

Grain: one row per product event.

Columns:
- event_id
- user_id
- session_id
- event_name
- event_timestamp
- event_date
- platform
- device_type
- country
- properties

### raw_subscriptions

Grain: one row per subscription lifecycle record.

Columns:
- subscription_id
- user_id
- plan
- status
- started_at
- ended_at
- monthly_amount_eur
- billing_period
- trial_started_at
- converted_at
- cancelled_at
- cancel_reason

## Core Event Taxonomy

- user_signed_up
- onboarding_started
- onboarding_step_completed
- onboarding_completed
- home_viewed
- coach_opened
- ai_message_sent
- ai_response_received
- checkin_generated
- checkin_clicked
- meal_logged
- ai_macro_estimate_requested
- ai_macro_estimate_accepted
- workout_logged
- weight_logged
- water_logged
- sleep_logged
- mood_logged
- progress_photo_uploaded
- progress_photo_compared
- walk_opened
- walk_route_generated
- walk_route_generation_failed
- walk_navigation_started
- walk_completed
- walk_saved
- notification_permission_requested
- notification_permission_granted
- streak_reminder_sent
- streak_reminder_clicked
- trial_started
- subscription_started
- subscription_cancelled
- subscription_renewed
- user_churned