## Sqlalchemy_Challenge10
To help with your trip planning, you decide to do a climate analysis about the area. 
The following sections outline the steps that you need to take to accomplish this task\

## Part 1: Analyze and Explore the Climate Data
In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. 
Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. To do so, complete the following steps:

    1. Use the SQLAlchemy create_engine() function to connect to your SQLite database.

    2. Use the SQLAlchemy automap_base() function to reflect your tables into classes, and then save references to the classes named station and measurement.

    3. Link Python to the database by creating a SQLAlchemy session.

    4. Perform a precipitation analysis and then a station analysis by completing the steps in the following two subsections

        Precipitation Analysis: Find most recent date in dataset and find the previous 12 months of precipitation data, then plot results

        Station Analysis: Query all stations to find most active station and query lowest, highest, and avgerage temperature,
         then plot a histogram of the most active station for last 12 months. 

## Part 2: Design Your Climate App
Design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:
      f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
Run same queries from Part 1 analysis and jsonify all return results


## References:
    I had help from my professor for some aspects of this assignment and I also used Slack Overflow and google searches for help with coding