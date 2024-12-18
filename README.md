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
The recommended method is to use pipx or uv to install the package. If you do not have Python set up on your system, uv will likely be easier, as it manages the creation of virtual environments and installs Python for you. On the other hand, pipx requires Python to be installed on your system beforehand.

1. Install the package using pipx or uv.
## Install using uv
Visit the [uv](https://docs.astral.sh/uv/getting-started/installation/) documentation for installation instructions.

```
uv tool install https://github.com/brandonleon/VehicleVitals.git
```

## Install using pipx
Visit the [pipx](https://pipx.pypa.io/stable/installation/) documentation for installation instructions.
```
pipx install https://github.com/brandonleon/VehicleVitals.git
```
2. Run the ```vv --help``` or ```vv --version``` command to verify the installation.

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
