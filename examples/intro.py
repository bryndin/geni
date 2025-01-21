### Note: by default, Geni allows a maximum of 1 request per 10 seconds.
### The library's rate limiter is per client instance, not global.
### Executing all 3 examples below (the separate instances of the client),
### will cause the last two to hit the rate limit.
### ```
### python3 examples/intro.py
### {'stats': [{'name': 'World Family Tree', 'url': 'https://www.geni.com/api/stats/world-family-tree'}]}
### {'error': {'type': 'ApiException', 'message': 'Rate limit exceeded.'}}
### {'error': {'type': 'ApiException', 'message': 'Rate limit exceeded.'}}
### ```

# ----------------------------------------------------------------------------
from geni import Geni

# Request to Stats/stats endpoint; API key is passed as a parameter
client = Geni("<INSERT YOUR API KEY HERE>")
# the format is: <client>.<API class>.<method>
resp = client.stats.stats()
# Prints `{'stats': [{'name': 'World Family Tree', 'url': 'https://www.geni.com/api/stats/world-family-tree'}]}`
print(resp)

# ----------------------------------------------------------------------------
from geni import Geni

# Here, the API key is read form the key file.
# (Prerequisite) Create `geni_api.key` file and paste your API key there.
client = Geni()
resp = client.stats.stats()
print(resp)

# ----------------------------------------------------------------------------
from geni import Stats

# API classes can be used directly, instead of instantiating the whole client.
# This approach is not recommended, unless you stick to using only one class,
# as the rate limiter won't be shared.
stats = Stats("<INSERT YOUR API KEY HERE>")  # or just `Stats()` is API key is used
# the format is: <API class>.<method>
resp = stats.stats()
print(resp)
