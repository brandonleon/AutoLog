import typer
from query import query_logs, query_vehicles

app = typer.Typer()


@app.command()
def display_logs(page: int = 1, page_size: int = 10, vehicle_id: str = None):
    """
    View logs from the database with optional filtering and pagination.
    """
    query_logs(page, page_size, vehicle_id)


@app.command()
def display_vehicles(page: int = 1, page_size: int = 10, vehicle_id: str = None):
    """
    View vehicles from the database with optional filtering and pagination.
    """
    query_vehicles(page, page_size, vehicle_id)


if __name__ == '__main__':
    app()
