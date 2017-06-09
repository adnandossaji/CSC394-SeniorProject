# WHEN/IF PLANNER
## TEAM 4 CSC 394 

## Members:
  * John Pridmore
  * Ashwin Sharma
  * Adnan Dossaji

### WE ARE SUCCESFULLY DEPLOYED ON HEROKU:
  ```
    http://mysterious-lake-23009.herokuapp.com/
  ```

### Username:
  ```
    admin@mail.depaul.edu
  ```

### Password:
  ```
    admin
  ```

If you have an error on our deployed site. Hit this link and logging in again.

  ```
    http://mysterious-lake-23009.herokuapp.com/seedDB
  ```

### Setup:

1. Clone the repo
  ```
  $ git clone https://github.com/nansta/CSC394-SeniorProject.git
  $ cd CSC394-SeniorProject
  ```

2. Initialize and activate a virtualenv:
  ```
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

4. Choose the flask application for flask:
  ```
  $ export FLASK_APP=app.py
  ```

4. Initialize the flask database:
  ```
  $ flask db init
  ```

4. Seed the database:
  ```
  $ python seed_db.py
  ```

5. Run the development server:
  ```
  $ python app.py
  ```

6. Navigate to [http://localhost:8000](http://localhost:8000)

### Server Deployment: