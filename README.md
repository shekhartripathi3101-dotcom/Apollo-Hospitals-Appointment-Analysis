# Apollo Hospitals – Appointment No-Show & Patient Engagement Analysis

### Exploratory Data Analysis | Python | Healthcare Analytics

## 1. Project Overview

This project analyses 75,000 hospital appointments to identify patterns in appointment no-shows, patient engagement, booking behaviour, financial performance, and doctor utilisation.

The objective is to transform appointment data into meaningful business insights and actionable recommendations that can help improve hospital operations, patient attendance, revenue generation, and healthcare service quality.

## 2. Business Problem

Appointment no-shows create operational challenges for hospitals, including:

- Reduced doctor utilisation.
- Loss of potential revenue.
- Inefficient appointment scheduling.
- Disruption in patient care.
- Underutilisation of healthcare resources.

This analysis explores the factors influencing appointment attendance and identifies opportunities to improve patient engagement.

## 3. Project Objectives

The analysis focuses on six major business areas:

1. **Business Overview:** Appointment trends, appointment outcomes, and booking channel distribution.
2. **No-Show Analysis:** No-show patterns across specialties, cities, booking lead time, appointment slots, and booking channels.
3. **Reminder & Engagement Effectiveness:** Impact of reminders, previous no-show history, Apollo membership, and repeat visits.
4. **Patient & Demographic Segmentation:** Attendance patterns across age groups, gender, chronic conditions, and visit reasons.
5. **Financial Performance:** Revenue analysis, revenue loss, payment methods, and insurance coverage.
6. **Doctor Utilisation & Service Quality:** Doctor utilisation, patient waiting time, consultation duration, satisfaction, and doctor experience.

## 4. Dataset Information

The project uses two datasets:

| Dataset | Records | Columns | Description |
|---|---:|---:|---|
| Apollo Appointments Fact | 75,000 | 52 | Appointment-level information |
| Apollo Doctors Dimension | 320 | 15 | Doctor details and professional attributes |

The datasets are connected using `doctor_id` whenever doctor-level information is required.

**Data Dictionary:** The accompanying Word document explains the dataset fields.

## 5. Tools & Technologies

- **Python:** Data analysis and programming.
- **Pandas:** Data cleaning, manipulation, and aggregation.
- **NumPy:** Numerical operations.
- **Matplotlib:** Data visualisation.
- **Seaborn:** Statistical visualisation, where applicable.
- **VS Code:** Development environment.
- **GitHub:** Project documentation and version control.

## 6. Methodology

The project follows an Exploratory Data Analysis (EDA) workflow:

1. Data loading and inspection.
2. Understanding dataset structure and dimensions.
3. Data type and missing-value checks.
4. Data preparation and transformation.
5. Exploratory analysis using Pandas and NumPy.
6. Aggregation and business metric calculations.
7. Data visualisation using charts and graphs.
8. Interpretation of results and business recommendations.

## 7. Important Business Rules

- No-show rate is calculated using Completed + No-Show + Cancelled appointments as the denominator.
- Scheduled appointments are excluded from the no-show rate denominator.
- Revenue analysis is restricted to Completed appointments.
- Quality metrics such as waiting time, satisfaction, consultation duration, and doctor utilisation are analysed only for Completed appointments.
- Doctor-level attributes are incorporated through the `doctor_id` relationship.

## 8. Project Files

| File | Description |
|---|---|
| `main.py` | Python analysis and visualisation code |
| `Apollo_Hospitals_Appointment_Analysis_Refined.pptx` | Final analytical presentation |
| `Data Dictionary.docx` | Dataset field documentation |

## 9. Deliverables

The repository contains:

- Python source code.
- Final PowerPoint presentation.
- Dataset documentation.
- Project methodology and documentation.

## 10. Key Learning Outcomes

This project demonstrates practical experience in:

- Exploratory Data Analysis.
- Healthcare business analytics.
- Data manipulation using Pandas.
- Statistical and numerical analysis.
- Data visualisation.
- Business problem-solving.
- Translating analytical results into business insights.

## 11. Author

**Shekhar Tripathi**

Aspiring Data Analyst | BBA Student | Python & Data Analytics Learner

---

*This project was developed as part of a Data Analytics Mentorship Programme.
