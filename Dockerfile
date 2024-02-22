FROM python:3.9.13

# Install necessary packages for ODBC
RUN apt-get update && \
    apt-get install -y unixodbc-dev gcc g++ apt-transport-https && \
    # Download the Microsoft repository GPG keys
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    # Register the Microsoft SQL Server Ubuntu repository
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    # Update the list of products
    apt-get update && \
    # Install SQL Server drivers and tools
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

    

WORKDIR /Code/
COPY Code/ /Code/

# Install dependencies from requirements.txt
COPY requirements.txt /Code/
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]