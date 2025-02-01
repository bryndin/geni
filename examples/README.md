# Examples

> [!NOTE]
> Note: by default, Geni allows a maximum of 1 request per 10 seconds.

```python
from geni import Geni

# Request to Stats/stats endpoint; API key is passed as a parameter
client = Geni("<INSERT YOUR API KEY HERE>")
# the format is: <client>.<API class>.<method>
resp = client.stats.stats()
# Prints `{'stats': [{'name': 'World Family Tree', 'url': 'https://www.geni.com/api/stats/world-family-tree'}]}`
print(resp)
```

```python
from geni import Geni

# Here, the API key is read form the key file.
# (Prerequisite) Create `geni_api.key` file and paste your API key there.
client = Geni()
resp = client.stats.stats()
print(resp)
```

See more examples in `.py` files.