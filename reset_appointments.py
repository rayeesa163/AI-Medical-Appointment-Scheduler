import pandas as pd

# Create empty DataFrame with new columns
df = pd.DataFrame(
    columns=[
        "Doctor",
        "Slot",
        "PatientType",
        "InsuranceCarrier",
        "MemberID",
        "GroupNumber",
    ]
)

df.to_excel("data/appointments.xlsx", index=False)
print("✅ appointments.xlsx reset successfully with 6 columns")
