# ![CI](https://github.com/ewertones/iot-api/actions/workflows/main.yml/badge.svg?branch=main) IoT API

This repository stores all the backend code for a proposed API to collect IoT devices' data. It is deployed through Cloud Run and uses a Cloud SQL instance (PostgreSQL) to store the information.

You can see the API with its documentation here: <https://iot-api-backend-hmmf62ftsq-uc.a.run.app>

You can see the full architecture diagram in the image below, created using Google Cloud Architecture Diagramming [tool](https://googlecloudcheatsheet.withgoogle.com/architecture):

<p align="center">
  <img width="500" src="https://github.com/ewertones/iot-api/blob/main/docs/architecture-diagram.png">
</p>

Although the ER diagram is simple, you also can see it below:

<p align="center">
  <img width="300" src="https://github.com/ewertones/iot-api/blob/main/docs/er-diagram.png">
</p>

## Why this architecture?

1.  Cloud Run was an excellent choice to host my backend because it provides a scalable, serverless solution. With it, my API can automatically handle spikes in traffic and scale up to millions of requests, ensuring that the service remains fast and responsive. This allows me to focus on development and not worry about managing infrastructure.
2.  In order to store the collected IoT trips data, I decided to use Cloud SQL, a fully managed relational database service. With Cloud SQL, I can easily set up and manage a PostgreSQL database that can store millions of rows of data. Cloud SQL also integrates seamlessly with Cloud Run, ensuring that my data is stored securely and is accessible to my API at all times.
3.  For my API framework, I chose FastAPI, a modern, fast, and easy-to-use Python web framework. One of the key benefits of using FastAPI was its ability to automatically generate documentation, making it easy to share the API with others and allow them to quickly understand how to use it. Additionally, FastAPI's fast performance and asynchronous capabilities made it an ideal choice for handling the large number of post and get requests that my API would be receiving. I also used SQLAlchemy and Pydantic to enforce data validation and make it more manageable to perform operations in my database.

## Local Development

1. Clone the project and `cd` inside directory:

```bash
git clone git@github.com:ewertones/iot-api.git
cd iot-api/
```

2. Build the image:

```bash
docker build -t iot:api .
```

3. Run the container:

```bash
docker run \
-e DB_HOST= \
-e DB_USERNAME= \
-e DB_DATABASE= \
-e DB_PASSWORD= \
-e DB_PORT= \
-p 8080:8080 \
iot:api
```

4. Access it through <http://localhost:8080>.

## Example Payloads

### /GET trips

```bash
curl --request GET 'localhost:8080/trips?skip=0&limit=10'
```

### /POST trip

```bash
curl --request POST 'localhost:8080/trip' \
--header 'Content-Type: application/json' \
--data-raw '{
  "region": "Prague",
  "origin_coord": "POINT (14.4973794438195 50.00136875782316)",
  "destination_coord": "POINT (14.43109483523328 50.04052930943246)",
  "datetime": "2018-05-28 09:03:40",
  "datasource": "funny_car"
}'

```

### /POST trips

```bash
curl --request POST 'localhost:8080/trips' \
--header 'Content-Type: application/json' \
--data-raw '[{
   "region": "Turin",
   "origin_coord": "POINT (7.672837913286881 44.9957109242058)",
   "destination_coord": "POINT (7.720368637535126 45.06782385393849)",
   "datetime": "2018-05-21 02:54:04",
   "datasource": "baba_car"
 },
 {
   "region": "Prague",
   "origin_coord": "POINT (14.32427345662177 50.00002074358429)",
   "destination_coord": "POINT (14.47767895969969 50.09339790740321)",
   "datetime": "2018-05-13 08:52:25",
   "datasource": "cheap_mobile"
 }]'
```
