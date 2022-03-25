 # REST API FOR MEDICATION TRANSFER SERVICE 

## Install

    npm install

## Run the app

    run flask

## Database

    * Create a database "medication_transfer_service" in mysql 
    * Define credentials in config.py

## Registering a drone

### Request

```POST http://127.0.0.1:5000/drone/add
    Add data in JSON Format 
```

## Registering a medication

### Request

```POST http://127.0.0.1:5000/medication/add
    Add data in JSON Format 
```

## Checking available drones for loading

### Request

`http://127.0.0.1:5000/drones-available`

## Check drone battery level for a given drone

### Request

`http://127.0.0.1:5000/drone/battery-check/<serialno>`
