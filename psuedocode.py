# Import requests library
# Import datetime from datetime library

# Create Reference to Weather API (OpenWeatherMap)
# Create a variable to store Base Url
# Create a variable to store Forecast Url

# ----------------------------------------------------
# Create a function to get the weather of a city
# Complete the full url using the Base Url and parameters such as city name, api, units
# Send an HTTP Request to the completed url
# Parse the Json Response

# Check errors from the respose
# If there is an error then display the error message
# Otherwise Extract the neccessary information:
# -> City Name
# -> Country
# -> Temperature
# -> Weather Description
# -> Humidity
# -> Wind Speed

# Send another HTTP Request to the Forecast URL using the same parameters
# Parse the JSON response

# Loop through the forecast list:
# -> For each entry, extract the datetime string
# -> Convert it to datetime object
# -> If the hour is 12:00 and the date is not already shown:
#    -> Extract:
#       - Forecast Date
#       - Forecast Description
#       - Forecast Temperature
#    -> Add the date to a set to avoid repeats
#    -> Stop when 3 dates have been shown

# Return the extracted Value 
# ----------------------------------------------------

# ----------------------------------------------------
# Create the main() function
# Prompt the user for a city name
# Call the get_weather function with the city name as the parameter
# Check if the funciton returns anything, if it does then:
# Display:
# Current Weather:
# -> City, Country
# -> Weather Description
# -> Temperature
# -> Humidity
# -> Wind Speed

# Forecast (3-Day):
# -> Tomorrow - (Day, Date - Weather Condition - Temperature)
# -> Next Day
# -> Next Next Day
# ----------------------------------------------------

# Start main()