# VehicleVitals - Vehicle Health and Fuel Management

VehicleVitals is a Python-based tool designed for monitoring the health and fuel consumption of your vehicles. This application enables you to maintain detailed records of fuel purchases, service entries, and mileage, allowing you to efficiently manage your vehicle's performance and expenses.

## Key Features

- **Fuel Consumption Tracking:** Record and manage fuel consumption entries.
- **Mileage and Odometer Readings:** Keep track of mileage and odometer readings.
- **Service Categorization:** Categorize service types and expenses.
- **Detailed Reporting:** Generate reports for vehicle maintenance and expenses.
- **Multi-Vehicle Support:** View historical data for multiple vehicles.

# Getting Started

Before you start using VehicleVitals, there are a few important things to keep in mind:

- **Database Schema Changes:** This project is currently under development and may undergo occasional database schema changes until version 1.0 is released. These changes could potentially affect the application's functionality and data integrity. As such, it is advisable to back up your data regularly, especially if you are using VehicleVitals in a production environment.

Please be cautious when updating the application or the database structure, and stay tuned for updates as we work towards a stable 1.0 release.

# Installation
- Clone the repository to your local machine.
- Use Poetry to build the project and install the dependencies.

```
poetry install # Install dependencies
poetry build # Build the project
pipx install dist/vehiclevitals-0.1.0-py3-none-any.whl # Install the application
```

- Run the ```vv``` command to start the application.

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
```vv add fuel-up --vehicle "6ce14368a66d" --odometer 50000 --fuel-type "Regular" --gallons 10.5 --cost 30.00```

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
