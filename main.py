import pandas as pd
import numpy as np

# Load appointment dataset
appointments = pd.read_csv(r"C:\Users\Dell\OneDrive\Documents\data analytics project and case study\python\apollo_appointments_fact.csv")

# Load doctors dataset
doctors = pd.read_csv(r"C:\Users\Dell\OneDrive\Documents\data analytics project and case study\python\apollo_doctors_dim.csv")

# Display first 5 rows
# print("APPOINTMENTS DATA")
# print(appointments.head())

# print("\nDOCTORS DATA")
# print(doctors.head())

# # Check dimensions
# print("\nAppointments Shape:", appointments.shape)
# print("Doctors Shape:", doctors.shape)

# print(appointments.columns.tolist())
# print(appointments.dtypes)


# Business Overview 

# 1 How is appointment volume trending across months and quarters from 2022 to 2024? 

# Convert appointment_date into datetime format
appointments['appointment_date'] = pd.to_datetime(
    appointments['appointment_date'],
    dayfirst=True
)

# Extract year, month and quarter
appointments['year'] = appointments['appointment_date'].dt.year
appointments['month'] = appointments['appointment_date'].dt.month
appointments['quarter'] = appointments['appointment_date'].dt.to_period('Q')

# print(appointments[['appointment_date', 'year', 'month', 'quarter']].head())

# MONTHLY APPOINTMENT VOLUME

monthly_appointments = (
    appointments
    .groupby(['year', 'month'])
    .size()
    .reset_index(name='total_appointments')
)

# print("\nMONTHLY APPOINTMENT VOLUME")
# print(monthly_appointments.to_string(index=False))

import matplotlib.pyplot as plt
import seaborn as sns

# plt.figure(figsize=(14, 6))

# sns.lineplot(
#     data=monthly_appointments,
#     x='month',
#     y='total_appointments',
#     hue='year',
#     marker='o'
# )

# plt.title('Monthly Appointment Trends (2022–2024)')
# plt.xlabel('Month')
# plt.ylabel('Total Appointments')
# plt.xticks(range(1, 13))
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# QUARTERLY APPOINTMENT VOLUME

appointments['quarter'] = appointments['appointment_date'].dt.quarter

quarterly_appointments = (
    appointments
    .groupby(['year', 'quarter'])
    .size()
    .reset_index(name='total_appointments')
)

# print("\nQUARTERLY APPOINTMENT VOLUME")
# print(quarterly_appointments.to_string(index=False))

# plt.figure(figsize=(12, 6))

# sns.lineplot(
#     data=quarterly_appointments,
#     x='quarter',
#     y='total_appointments',
#     hue='year',
#     marker='o'
# )

# plt.title('Quarterly Appointment Trends (2022–2024)')
# plt.xlabel('Quarter')
# plt.ylabel('Total Appointments')
# plt.xticks([1, 2, 3, 4], ['Q1', 'Q2', 'Q3', 'Q4'])
# plt.grid(True)
# plt.tight_layout()
# plt.show()


# YEAR-WISE APPOINTMENT VOLUME

yearly_appointments = (
    appointments
    .groupby('year')
    .size()
    .reset_index(name='total_appointments')
)

# Calculate year-over-year growth percentage
yearly_appointments['growth_percentage'] = (
    yearly_appointments['total_appointments']
    .pct_change() * 100
)

# print("\nYEAR-WISE APPOINTMENT VOLUME")
# print(yearly_appointments.to_string(index=False))

# ============================================================
# APOLLO HOSPITALS - EDA PROJECT
# ALL QUESTIONS EXCEPT MONTHLY/QUARTERLY APPOINTMENT TRENDS
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")


# ============================================================
# DATA PREPARATION
# ============================================================

# Create a clean analysis dataframe
df = appointments.copy()

# Standardise status values
df['appointment_status'] = (
    df['appointment_status'].astype(str).str.strip().str.title()
)

# Define eligible appointments for no-show rate
# Scheduled appointments are excluded
eligible = df[
    df['appointment_status'].isin(
        ['Completed', 'No-Show', 'Cancelled']
    )
].copy()

# Create no-show flag using appointment status
df['no_show_flag'] = (
    df['appointment_status'] == 'No-Show'
).astype(int)

eligible['no_show_flag'] = (
    eligible['appointment_status'] == 'No-Show'
).astype(int)

# Completed appointments only
completed = df[
    df['appointment_status'] == 'Completed'
].copy()


# Helper function for calculating no-show rates
def calculate_no_show_rate(data, column):

    result = (
        data.groupby(column)
        .agg(
            total_eligible=('no_show_flag', 'count'),
            total_no_shows=('no_show_flag', 'sum')
        )
        .reset_index()
    )

    result['no_show_rate'] = (
        result['total_no_shows'] /
        result['total_eligible'] * 100
    )

    return result.sort_values(
        'no_show_rate',
        ascending=False
    )


# ============================================================
# QUESTION 2: APPOINTMENT STATUS DISTRIBUTION
# ============================================================

print("\n========== APPOINTMENT STATUS DISTRIBUTION ==========")

status_distribution = (
    df['appointment_status']
    .value_counts()
    .reset_index()
)

status_distribution.columns = [
    'appointment_status',
    'total_appointments'
]

status_distribution['percentage'] = (
    status_distribution['total_appointments'] /
    len(df) * 100
)

print(status_distribution.to_string(index=False))


# STATUS DISTRIBUTION GRAPH

plt.figure(figsize=(9, 6))

sns.barplot(
    data=status_distribution,
    x='appointment_status',
    y='total_appointments'
)

plt.title('Appointment Status Distribution')
plt.xlabel('Appointment Status')
plt.ylabel('Number of Appointments')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 3: BOOKING CHANNEL ANALYSIS
# ============================================================

print("\n========== BOOKING CHANNEL ANALYSIS ==========")

channel_analysis = (
    df['booking_channel']
    .value_counts()
    .reset_index()
)

channel_analysis.columns = [
    'booking_channel',
    'total_appointments'
]

channel_analysis['percentage'] = (
    channel_analysis['total_appointments'] /
    len(df) * 100
)

print(channel_analysis.to_string(index=False))


# BOOKING CHANNEL GRAPH

plt.figure(figsize=(10, 6))

sns.barplot(
    data=channel_analysis,
    x='booking_channel',
    y='total_appointments'
)

plt.title('Appointment Volume by Booking Channel')
plt.xlabel('Booking Channel')
plt.ylabel('Total Appointments')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


# ============================================================
# NO-SHOW ANALYSIS
# ============================================================


# ============================================================
# QUESTION 4: SPECIALTY-WISE NO-SHOW RATE
# ============================================================

print("\n========== SPECIALTY-WISE NO-SHOW RATE ==========")

specialty_no_show = calculate_no_show_rate(
    eligible, 'specialty'
)

print(specialty_no_show.to_string(index=False))


plt.figure(figsize=(12, 7))

sns.barplot(
    data=specialty_no_show,
    x='no_show_rate',
    y='specialty'
)

plt.title('No-Show Rate by Specialty')
plt.xlabel('No-Show Rate (%)')
plt.ylabel('Specialty')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 5: CITY-WISE NO-SHOW RATE
# ============================================================

print("\n========== CITY-WISE NO-SHOW RATE ==========")

city_no_show = calculate_no_show_rate(
    eligible, 'city'
)

print(city_no_show.to_string(index=False))


plt.figure(figsize=(12, 7))

sns.barplot(
    data=city_no_show,
    x='no_show_rate',
    y='city'
)

plt.title('No-Show Rate by City')
plt.xlabel('No-Show Rate (%)')
plt.ylabel('City')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 6: BOOKING LEAD TIME VS NO-SHOW RATE
# ============================================================

print("\n========== BOOKING LEAD TIME ANALYSIS ==========")

df['lead_time_category'] = pd.cut(
    df['booking_lead_days'],
    bins=[-1, 1, 3, 7, 14, 30, np.inf],
    labels=[
        '0-1 Days',
        '2-3 Days',
        '4-7 Days',
        '8-14 Days',
        '15-30 Days',
        'Above 30 Days'
    ]
)

eligible = df[
    df['appointment_status'].isin(
        ['Completed', 'No-Show', 'Cancelled']
    )
].copy()

lead_time_analysis = calculate_no_show_rate(
    eligible, 'lead_time_category'
)

print(lead_time_analysis.to_string(index=False))


plt.figure(figsize=(10, 6))

sns.barplot(
    data=lead_time_analysis,
    x='lead_time_category',
    y='no_show_rate'
)

plt.title('Booking Lead Time vs No-Show Rate')
plt.xlabel('Booking Lead Time')
plt.ylabel('No-Show Rate (%)')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 7: TIME OF DAY VS NO-SHOW RATE
# ============================================================

print("\n========== TIME OF DAY ANALYSIS ==========")

time_analysis = calculate_no_show_rate(
    eligible, 'time_of_day'
)

print(time_analysis.to_string(index=False))


plt.figure(figsize=(9, 6))

sns.barplot(
    data=time_analysis,
    x='time_of_day',
    y='no_show_rate'
)

plt.title('No-Show Rate by Time of Day')
plt.xlabel('Time of Day')
plt.ylabel('No-Show Rate (%)')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 8: WEEKDAY VS WEEKEND NO-SHOW RATE
# ============================================================

print("\n========== WEEKDAY VS WEEKEND ANALYSIS ==========")

df['appointment_date'] = pd.to_datetime(
    df['appointment_date'],
    dayfirst=True,
    errors='coerce'
)

df['day_type'] = np.where(
    df['appointment_date'].dt.dayofweek >= 5,
    'Weekend',
    'Weekday'
)

eligible = df[
    df['appointment_status'].isin(
        ['Completed', 'No-Show', 'Cancelled']
    )
].copy()

weekend_analysis = calculate_no_show_rate(
    eligible, 'day_type'
)

print(weekend_analysis.to_string(index=False))


plt.figure(figsize=(8, 5))

sns.barplot(
    data=weekend_analysis,
    x='day_type',
    y='no_show_rate'
)

plt.title('Weekday vs Weekend No-Show Rate')
plt.xlabel('Day Type')
plt.ylabel('No-Show Rate (%)')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 9: APPOINTMENT TYPE VS NO-SHOW RATE
# ============================================================

print("\n========== APPOINTMENT TYPE ANALYSIS ==========")

appointment_type_analysis = calculate_no_show_rate(
    eligible, 'appointment_type'
)

print(appointment_type_analysis.to_string(index=False))


plt.figure(figsize=(9, 6))

sns.barplot(
    data=appointment_type_analysis,
    x='appointment_type',
    y='no_show_rate'
)

plt.title('No-Show Rate by Appointment Type')
plt.xlabel('Appointment Type')
plt.ylabel('No-Show Rate (%)')
plt.tight_layout()
plt.show()


# ============================================================
# REMINDER AND PATIENT ENGAGEMENT
# ============================================================


# ============================================================
# QUESTION 10: REMINDER EFFECTIVENESS
# ============================================================

print("\n========== REMINDER EFFECTIVENESS ==========")

reminder_analysis = calculate_no_show_rate(
    eligible, 'reminder_type'
)

print(reminder_analysis.to_string(index=False))


plt.figure(figsize=(10, 6))

sns.barplot(
    data=reminder_analysis,
    x='reminder_type',
    y='no_show_rate'
)

plt.title('No-Show Rate by Reminder Type')
plt.xlabel('Reminder Type')
plt.ylabel('No-Show Rate (%)')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 11: PRIOR NO-SHOW HISTORY
# ============================================================

print("\n========== PRIOR NO-SHOW HISTORY ==========")

df['prior_no_show_category'] = pd.cut(
    df['patient_prior_no_shows'],
    bins=[-1, 0, 1, 3, np.inf],
    labels=[
        'No Previous No-Shows',
        '1 Previous No-Show',
        '2-3 Previous No-Shows',
        'Above 3 Previous No-Shows'
    ]
)

eligible = df[
    df['appointment_status'].isin(
        ['Completed', 'No-Show', 'Cancelled']
    )
].copy()

prior_no_show_analysis = calculate_no_show_rate(
    eligible, 'prior_no_show_category'
)

print(prior_no_show_analysis.to_string(index=False))


plt.figure(figsize=(11, 6))

sns.barplot(
    data=prior_no_show_analysis,
    x='prior_no_show_category',
    y='no_show_rate'
)

plt.title('Prior No-Show History vs Current No-Show Rate')
plt.xlabel('Previous No-Show History')
plt.ylabel('Current No-Show Rate (%)')
plt.xticks(rotation=25)
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 12: APOLLO MEMBERSHIP VS ATTENDANCE
# ============================================================

print("\n========== APOLLO MEMBERSHIP ANALYSIS ==========")

membership_analysis = calculate_no_show_rate(
    eligible, 'apollo_member'
)

print(membership_analysis.to_string(index=False))


plt.figure(figsize=(8, 5))

sns.barplot(
    data=membership_analysis,
    x='apollo_member',
    y='no_show_rate'
)

plt.title('Apollo Membership vs No-Show Rate')
plt.xlabel('Apollo Member')
plt.ylabel('No-Show Rate (%)')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 13: REPEAT VS FIRST-TIME PATIENTS
# ============================================================

print("\n========== PATIENT VISIT TYPE ANALYSIS ==========")

visit_analysis = calculate_no_show_rate(
    eligible, 'is_first_visit'
)

print(visit_analysis.to_string(index=False))


plt.figure(figsize=(8, 5))

sns.barplot(
    data=visit_analysis,
    x='is_first_visit',
    y='no_show_rate'
)

plt.title('First-Time vs Repeat Patient No-Show Rate')
plt.xlabel('First Visit (1 = Yes, 0 = No)')
plt.ylabel('No-Show Rate (%)')
plt.tight_layout()
plt.show()


# ============================================================
# PATIENT AND DEMOGRAPHIC SEGMENTATION
# ============================================================


# ============================================================
# QUESTION 14: AGE GROUP VS NO-SHOW RATE
# ============================================================

print("\n========== AGE GROUP ANALYSIS ==========")

age_analysis = calculate_no_show_rate(
    eligible, 'age_group'
)

print(age_analysis.to_string(index=False))


plt.figure(figsize=(10, 6))

sns.barplot(
    data=age_analysis,
    x='age_group',
    y='no_show_rate'
)

plt.title('No-Show Rate by Age Group')
plt.xlabel('Age Group')
plt.ylabel('No-Show Rate (%)')
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 15: GENDER VS NO-SHOW RATE
# ============================================================

print("\n========== GENDER ANALYSIS ==========")

gender_analysis = calculate_no_show_rate(
    eligible, 'patient_gender'
)

print(gender_analysis.to_string(index=False))


plt.figure(figsize=(8, 5))

sns.barplot(
    data=gender_analysis,
    x='patient_gender',
    y='no_show_rate'
)

plt.title('No-Show Rate by Gender')
plt.xlabel('Gender')
plt.ylabel('No-Show Rate (%)')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 16: CHRONIC CONDITION VS NO-SHOW RATE
# ============================================================

print("\n========== CHRONIC CONDITION ANALYSIS ==========")

chronic_analysis = calculate_no_show_rate(
    eligible, 'patient_chronic_condition'
)

print(chronic_analysis.to_string(index=False))


plt.figure(figsize=(9, 6))

sns.barplot(
    data=chronic_analysis,
    x='patient_chronic_condition',
    y='no_show_rate'
)

plt.title('Chronic Condition vs No-Show Rate')
plt.xlabel('Chronic Condition')
plt.ylabel('No-Show Rate (%)')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 17: VISIT REASON ANALYSIS
# ============================================================

print("\n========== VISIT REASON ANALYSIS ==========")

visit_reason_volume = (
    df['visit_reason']
    .value_counts()
    .reset_index()
)

visit_reason_volume.columns = [
    'visit_reason',
    'total_appointments'
]

print(visit_reason_volume.to_string(index=False))


plt.figure(figsize=(12, 7))

sns.barplot(
    data=visit_reason_volume,
    x='total_appointments',
    y='visit_reason'
)

plt.title('Appointment Volume by Visit Reason')
plt.xlabel('Total Appointments')
plt.ylabel('Visit Reason')
plt.tight_layout()
plt.show()


visit_reason_no_show = calculate_no_show_rate(
    eligible, 'visit_reason'
)

print("\nNO-SHOW RATE BY VISIT REASON")
print(visit_reason_no_show.to_string(index=False))


# ============================================================
# QUESTION 18: AGE DISTRIBUTION BY SPECIALTY
# ============================================================

print("\n========== AGE DISTRIBUTION BY SPECIALTY ==========")

selected_specialties = [
    'Paediatrics',
    'Gynaecology',
    'Psychiatry'
]

specialty_age = df[
    df['specialty'].isin(selected_specialties)
]

print(
    specialty_age.groupby('specialty')['patient_age']
    .describe()
)


plt.figure(figsize=(12, 7))

sns.boxplot(
    data=specialty_age,
    x='specialty',
    y='patient_age'
)

plt.title('Patient Age Distribution Across Specialties')
plt.xlabel('Specialty')
plt.ylabel('Patient Age')
plt.tight_layout()
plt.show()


# ============================================================
# FINANCIAL PERFORMANCE
# ============================================================


# ============================================================
# QUESTION 19: REVENUE LOST DUE TO NO-SHOWS
# ============================================================

print("\n========== NO-SHOW REVENUE ANALYSIS ==========")

no_show_data = df[
    df['appointment_status'] == 'No-Show'
].copy()

completed_revenue = completed['revenue_realized'].sum()

# Estimate potential revenue using consultation fee.
# This is an estimate, not actual realised revenue.

estimated_lost_revenue = no_show_data[
    'consultation_fee'
].sum()

print("Total Realised Revenue:", completed_revenue)

print(
    "Estimated Potential Revenue Lost:",
    estimated_lost_revenue
)

print(
    "Total No-Show Appointments:",
    len(no_show_data)
)


# ============================================================
# QUESTION 20: AVERAGE REVENUE BY SPECIALTY
# ============================================================

print("\n========== REVENUE BY SPECIALTY ==========")

specialty_revenue = (
    completed.groupby('specialty')
    .agg(
        total_revenue=('revenue_realized', 'sum'),
        average_revenue=('revenue_realized', 'mean'),
        total_appointments=('appointment_id', 'count')
    )
    .reset_index()
    .sort_values('total_revenue', ascending=False)
)

print(specialty_revenue.to_string(index=False))


plt.figure(figsize=(12, 7))

sns.barplot(
    data=specialty_revenue,
    x='total_revenue',
    y='specialty'
)

plt.title('Total Revenue by Specialty')
plt.xlabel('Total Revenue')
plt.ylabel('Specialty')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 21: REVENUE BY APPOINTMENT TYPE
# ============================================================

print("\n========== REVENUE BY APPOINTMENT TYPE ==========")

type_revenue = (
    completed.groupby('appointment_type')
    .agg(
        total_revenue=('revenue_realized', 'sum'),
        average_revenue=('revenue_realized', 'mean')
    )
    .reset_index()
)

print(type_revenue.to_string(index=False))


plt.figure(figsize=(9, 6))

sns.barplot(
    data=type_revenue,
    x='appointment_type',
    y='average_revenue'
)

plt.title('Average Revenue by Appointment Type')
plt.xlabel('Appointment Type')
plt.ylabel('Average Revenue')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 22: CITY-WISE REVENUE
# ============================================================

print("\n========== CITY-WISE REVENUE ==========")

city_revenue = (
    completed.groupby('city')
    .agg(
        total_revenue=('revenue_realized', 'sum')
    )
    .reset_index()
    .sort_values('total_revenue', ascending=False)
)

print(city_revenue.to_string(index=False))


plt.figure(figsize=(12, 7))

sns.barplot(
    data=city_revenue,
    x='total_revenue',
    y='city'
)

plt.title('Revenue Generated by City')
plt.xlabel('Total Revenue')
plt.ylabel('City')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 23: PAYMENT MODE MIX
# ============================================================

print("\n========== PAYMENT MODE ANALYSIS ==========")

payment_analysis = (
    completed['payment_mode']
    .value_counts()
    .reset_index()
)

payment_analysis.columns = [
    'payment_mode',
    'total_transactions'
]

print(payment_analysis.to_string(index=False))


plt.figure(figsize=(8, 8))

plt.pie(
    payment_analysis['total_transactions'],
    labels=payment_analysis['payment_mode'],
    autopct='%1.1f%%',
    startangle=90
)

plt.title('Payment Mode Distribution')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 24: INSURANCE VS OUT-OF-POCKET PAYMENT
# ============================================================

print("\n========== INSURANCE ANALYSIS ==========")

insurance_analysis = (
    completed.groupby('insurance_coverage')
    .agg(
        average_out_of_pocket=(
            'patient_out_of_pocket', 'mean'
        ),
        average_insurance_covered=(
            'insurance_covered_amount', 'mean'
        ),
        total_appointments=('appointment_id', 'count')
    )
    .reset_index()
)

print(insurance_analysis.to_string(index=False))


plt.figure(figsize=(9, 6))

sns.barplot(
    data=insurance_analysis,
    x='insurance_coverage',
    y='average_out_of_pocket'
)

plt.title('Insurance Coverage vs Out-of-Pocket Payment')
plt.xlabel('Insurance Coverage')
plt.ylabel('Average Out-of-Pocket Payment')
plt.tight_layout()
plt.show()


# ============================================================
# DOCTOR UTILISATION AND SERVICE QUALITY
# ============================================================


# ============================================================
# QUESTION 25: DOCTOR UTILISATION BY SPECIALTY
# ============================================================

print("\n========== DOCTOR UTILISATION BY SPECIALTY ==========")

utilisation_analysis = (
    completed.groupby('specialty')
    .agg(
        average_utilisation=(
            'doctor_utilization_pct', 'mean'
        )
    )
    .reset_index()
    .sort_values('average_utilisation', ascending=False)
)

print(utilisation_analysis.to_string(index=False))


plt.figure(figsize=(12, 7))

sns.barplot(
    data=utilisation_analysis,
    x='average_utilisation',
    y='specialty'
)

plt.title('Average Doctor Utilisation by Specialty')
plt.xlabel('Average Utilisation (%)')
plt.ylabel('Specialty')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 26: PATIENT WAIT TIME ANALYSIS
# ============================================================

print("\n========== WAIT TIME BY SPECIALTY ==========")

wait_analysis = (
    completed.groupby('specialty')
    .agg(
        average_wait_time=(
            'wait_time_minutes', 'mean'
        )
    )
    .reset_index()
    .sort_values('average_wait_time', ascending=False)
)

print(wait_analysis.to_string(index=False))


plt.figure(figsize=(12, 7))

sns.barplot(
    data=wait_analysis,
    x='average_wait_time',
    y='specialty'
)

plt.title('Average Patient Waiting Time by Specialty')
plt.xlabel('Average Waiting Time (Minutes)')
plt.ylabel('Specialty')
plt.tight_layout()
plt.show()


# WAIT TIME BY TIME OF DAY

wait_time_day = (
    completed.groupby('time_of_day')
    ['wait_time_minutes']
    .mean()
    .reset_index()
)

print("\nWAIT TIME BY TIME OF DAY")
print(wait_time_day.to_string(index=False))


plt.figure(figsize=(9, 6))

sns.barplot(
    data=wait_time_day,
    x='time_of_day',
    y='wait_time_minutes'
)

plt.title('Average Waiting Time by Time of Day')
plt.xlabel('Time of Day')
plt.ylabel('Average Waiting Time (Minutes)')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 27: CONSULTATION DURATION VS SATISFACTION
# ============================================================

print("\n========== CONSULTATION DURATION VS SATISFACTION ==========")

print(
    "Correlation:",
    completed[
        [
            'consultation_duration_min',
            'patient_satisfaction_score'
        ]
    ].corr().iloc[0, 1]
)


plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=completed,
    x='consultation_duration_min',
    y='patient_satisfaction_score',
    alpha=0.5
)

plt.title('Consultation Duration vs Patient Satisfaction')
plt.xlabel('Consultation Duration (Minutes)')
plt.ylabel('Patient Satisfaction Score')
plt.tight_layout()
plt.show()


# ============================================================
# QUESTION 28: DOCTOR EXPERIENCE VS CONSULTATION FEE
# ============================================================

print("\n========== DOCTOR EXPERIENCE VS CONSULTATION FEE ==========")

# Join appointments with doctors dimension
doctor_merged = completed.merge(
    doctors[
        [
            'doctor_id',
            'doctor_name',
            'experience_years',
            'rating',
            'qualification'
        ]
    ],
    on='doctor_id',
    how='left'
)

experience_fee = (
    doctor_merged.groupby('experience_years')
    .agg(
        average_fee=('actual_fee_charged', 'mean'),
        average_rating=('rating', 'mean'),
        doctor_count=('doctor_id', 'nunique')
    )
    .reset_index()
)

print(experience_fee.to_string(index=False))


plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=doctor_merged,
    x='experience_years',
    y='actual_fee_charged',
    alpha=0.5
)

plt.title('Doctor Experience vs Consultation Fee')
plt.xlabel('Doctor Experience (Years)')
plt.ylabel('Actual Consultation Fee')
plt.tight_layout()
plt.show()


# ============================================================
# PROJECT ANALYSIS COMPLETED
# ============================================================

print("\n")
print("=" * 60)
print("APOLLO HOSPITALS EDA ANALYSIS COMPLETED")
print("=" * 60)

print("\nTotal Appointments:", len(df))
print("Completed Appointments:", len(completed))
print("No-Show Appointments:", len(no_show_data))
print("Total Doctors:", doctors['doctor_id'].nunique())

print("\nAll remaining analysis sections executed successfully.")