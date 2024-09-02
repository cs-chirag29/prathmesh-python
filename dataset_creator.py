import pandas as pd
import numpy as np

# Define the features
room_types = ['Standard', 'Deluxe', 'Suite', 'Private']
views = ['Sea Facing', 'City View', 'None']
jacuzzis = ['Yes', 'No']
balconies = ['Yes', 'No']
bed_types = ['King', 'Queen', 'Double']
technologies = ['Smart TV', 'Standard TV']
seasons = ['Peak', 'Off-Peak']
floor_levels = np.arange(1, 21)  # Floor levels from 1 to 20

# Define the number of entries
num_entries = 1000

# Generate random data
np.random.seed(0)  # For reproducibility

data = {
    'Room Type': np.random.choice(room_types, size=num_entries),
    'Sea Facing': np.random.choice(views, size=num_entries),
    'Jacuzzi': np.random.choice(jacuzzis, size=num_entries),
    'Balcony': np.random.choice(balconies, size=num_entries),
    'Bed Type': np.random.choice(bed_types, size=num_entries),
    'In-Room Technology': np.random.choice(technologies, size=num_entries),
    'Season': np.random.choice(seasons, size=num_entries),
    'Floor Level': np.random.choice(floor_levels, size=num_entries),
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define a simple pricing function
def calculate_price(row):
    base_price = 1000
    price = base_price
    if row['Room Type'] == 'Deluxe':
        price += 550
    elif row['Room Type'] == 'Suite':
        price += 2500
    elif row['Room Type'] == 'Private':
        price += 3500

    if row['Sea Facing'] == 'Sea Facing':
        price += 1000
    elif row['Sea Facing'] == 'City View':
        price += 450

    if row['Jacuzzi'] == 'Yes':
        price += 350

    if row['Balcony'] == 'Yes':
        price += 200

    if row['Bed Type'] == 'King':
        price += 250
    elif row['Bed Type'] == 'Queen':
        price += 150

    if row['In-Room Technology'] == 'Smart TV':
        price += 200

    if row['Season'] == 'Peak':
        price *= 1.2  # 20% increase for peak season

    # Add some variability to the price
    price += np.random.uniform(-10, 10)

    return round(price, 2)

# Apply the pricing function
df['Price'] = df.apply(calculate_price, axis=1)

# Save to CSV
df.to_csv('room_prices_dataset.csv', index=False)
print("Dataset generated and saved as 'room_prices_dataset.csv'")
