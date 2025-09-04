import pandas as pd

# Create empty DataFrame with headers
df = pd.DataFrame(columns=["Doctor", "Slot", "PatientType"])

# Save as Excel inside /data/
df.to_excel("data/appointments.xlsx", index=False)

print("✅ appointments.xlsx created successfully")
