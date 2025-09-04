import pandas as pd

data = {
    "Doctor": ["Dr. Smith", "Dr. Johnson", "Dr. Lee"],
    "Available Slots": [
        "2025-09-05 09:00, 2025-09-05 10:00, 2025-09-05 11:00",
        "2025-09-05 13:00, 2025-09-05 14:00, 2025-09-05 15:00",
        "2025-09-06 09:30, 2025-09-06 10:30, 2025-09-06 11:30",
    ],
}

df = pd.DataFrame(data)
df.to_excel("data/doctors.xlsx", index=False)

print("✅ doctors.xlsx reset with fresh slots")
