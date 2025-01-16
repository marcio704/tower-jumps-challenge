# Tower Jumps

## About this project
A mobile carrier (e.g., AT&T, Verizon, T-Mobile) tracks a subscriber’s location using a method called cell tower triangulation, a method for determining the location of a phone by measuring the time it takes for a signal to travel between the phone and multiple cell towers. Cell tower triangulation, unlike GPS, is not very precise. Consider a subscriber who lives very close to a state or country border. The subscriber uses a mobile application that needs to accurately record the state or country that the subscriber is physically located in. The application does not use GPS to minimize battery consumption on the device, but instead only has access to locations based on cell tower triangulation. In such a scenario, the application may receive location data from cellphone towers located in more than one state or country making it appear that the subscriber was in two places at the same time.

You are developing an application that estimates which state (or country) a subscriber may be in during different time intervals during the day, and an indicator that expresses the confidence in the estimated location.

To help with the assignment, attached is a data file that provides location data for a single subscriber, John Doe. John Doe has a home very close to the border of NY and CT and so experiences a ping-pong of locations recorded across state borders. As an example refer to Jan 5-10, 2021 data in the attached data file. Clearly the subscriber cannot be going back and forth between NY and CT so often. But what should the application tell the subscriber? Where are they?  

Carriers determine location of a subscriber based on a number of factors including distance from the cell-phone tower, strength of the signal, humidity, temperature, proximity to a water body etc. The data set provided is only one example. The same subscriber could be in the same actual physical location, but could have had a different set of cell tower readings. Your solution should contemplate these different scenarios.  

‘Page Number’ and ‘Item Number’ refer to the page and the line item from the data report. ‘Record Type’ refers to whether the data is captured by the carrier as a result of a connection that the mobile device made with the carrier for making/receiving a phone call, data or SMS. 

Implement in Python.


### Feature: Determine Location and Confidence Level

  - Scenario: Provide a list of time periods and the state the person was in, as well as a confidence level
  - Given a set of data points with longitude, latitude, timestamp, and current state
  - When the data points are processed
  - Then a report should be provided with a list of time periods
  - And the state where the person likely was during that interval
  - And the confidence level expressed as a percentage


## Solution:
The following test scenario contains a timefrime with 2 pings in NY and 2 pings in CT:
![alt text](https://github.com/marcio704/tower-jumps-challenge/blob/main/boundary_towers_in_different_states.png?raw=true)

### Simple solution
It relies on the occurrences of states for a given timeframe. It assigns the state with the highest count as the estimated state for that interval (does not count on lat/log). In the test scenario above, NY would be the estimate with 50% confidence.

### Accurate solution
It relies on the lat/long points to calculate an average point for a given timeframe. It assigns the state containing the average point as the estimated state for that interval. The further the average point is from the state border, the higher is the confidence level.

## Installation
Make sure you have [pipenv](https://pipenv.pypa.io/en/latest/) and [Make](https://www.gnu.org/software/make/) installed.

- `make install`

## Running locally

### You can generate a visual HTML heatmap for all dataset or a given timeframe of the dataset like this:

- `make generate-heatmap`
- `make START_DATE=2021-01-06T02:15:00 END_DATE=2021-01-06T02:30:00 generate-heatmap`
- `make START_DATE=2021-01-06T03:00:00 END_DATE=2021-01-06T03:15:00 generate-heatmap`


### Run the simple solution:
- `make run-simple-solution`

### Run the accurate solution which .
- `make run-accurate-solution`

## Unit tests

- `make tests`
