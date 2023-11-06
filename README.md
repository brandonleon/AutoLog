# VehicleVitals - Vehicle Health and Fuel Management

VehicleVitals is a Python-based tool designed for monitoring the health and fuel consumption of your vehicles. This application enables you to maintain detailed records of fuel purchases, service entries, and mileage, allowing you to efficiently manage your vehicle's performance and expenses.

## Key Features

- **Fuel Consumption Tracking:** Record and manage fuel consumption entries.
- **Mileage and Odometer Readings:** Keep track of mileage and odometer readings.
- **Service Categorization:** Categorize service types and expenses.
- **Detailed Reporting:** Generate reports for vehicle maintenance and expenses.
- **Multi-Vehicle Support:** View historical data for multiple vehicles.

# Getting Started
- Create a database to store your vehicle and fuel consumption data. By default, VehicleVitals uses SQLite.
- Utilize the provided commands to add and manage your vehicle and fuel consumption entries.
- Generate reports and gain insights into your vehicle's performance and expenses.

# Usage
## Command Line Interface
VehicleVitals provides a feature-rich command-line interface (CLI) with the following essential commands:
- ```vv add vehicle```: Add a new vehicle to the database.
- ```vv add fuel-up```: Add fuel consumption or service entries for a vehicle.
- ```vv add service```: Add service entries for a vehicle.
- ```vv display vehicles```: Display a list of all vehicles in the database.
- ```vv display logs```: Display fuel consumption and service entries for a vehicle.

## Examples

### Add a vehicle
```vv add vehicle --make "Toyota" --model "Camry" --year 2020 --mileage 12345```

### Add a fuel entry
```vv add fuel-up --vehicle "Toyota Camry 2020" --odometer 50000 --fuel-type "Regular" --gallons 10.5 --cost 30.00```

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
