# Saflizer
 A simple solution to a big problem. A solution to drunk drivers, currently school bus drivers, but could be utilized for others in the future.

 ## The Problem
 Recently, druken drivers have been on the rise, and this affects school buses as well! We consulted with Mrs Rachana Heda, the COO of a local school company, Glentree Academy. They have three schools in Banglore. Mrs Rachana told us about how recently there were some issues with druken drivers. Even the police had instructed schools to conduct random breathalizer tests. However these are inneffective for a number of reasons including,
 1. Manual testing requires a lot of manpower and resources
 2. These tests are often conducted in the morning but, drivers drink when idle between their morning and afternoon trips.
 3. There is no system to do this efficiently and cheaply at the moment

## The Solution
So we devised our solution, the Saflizer Gen X. A simple device that can be installed near the bus parking grounds. How does it work?
1. Everyday drivers just take the test before their trips (30 min window).
2.  The driver is identified with facial recognition. There can be only one person in view to ensure the correct person is taking the test. Thus, installing a booth is recommended.
3.  Then the driver has to simply blow on the breathalizer.
4.  If the test yeilds in results higher than legal limits, an alert is sent to the software. An alert is also sent if a driver misses the test.

## Software Explanation
### The Saflizer Software
With this software, a supervisor can create an account and manage and add drivers he supervises. Then he simply schedules the trips that the drivers have to take.
1. Adding a driver is simple. Simply hit the Add Driver button enter the name and utilize your webcam by hitting the add picture button to add a driver.
2. To schedule a trip, just click the Schedule Trips button, then you can add trips by hitting the Add Trip button. To delete a trip simply click on the trash icon next to it.
3. To view a driver's past record, just click on the driver. Here you can also set whether he is on duty on not.

### The API

### The Breathalize Demo
To utilize the facial recognition, simply start the script. It will ask you to enter your supervisor's username, after setting that the webcam should open. If you are registered, it will recognise you by your driver id. Then hit space to set your alchohol level. It will send an alert if the level is above the legal limit(35mg/l)
