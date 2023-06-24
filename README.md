# plate-detection
This project saves name car plates in database and makes it easy to manage in Flask.
This is useful on residential roads when security is important.

Back-End:
1. The IP camera takes a snapshot when it sees a car on the street
2. Watchdog look in directory new image
3. Activate script using yolov3 from OpenCV
4. Save plate numer, day, hour, and url-image in database with SQLAlchemy alembic
5. Generate Flask with pages: home, search_plate, login-bar

Front-End:
1. In all page, we have navigation bar and login bar
2. In home page, are lasts record from database (numer plate, day, hour, plate-image)
3. In search page, we can find records by searching for only details


In progress:
1. User registration (manual addition is currently working)
2. Detection of people, cyclists and categorizing in another db

![search](https://github.com/michal-broda/plate-detection/assets/95285280/e0fc7b5d-7c62-474f-b68b-8e8886f87d01)
