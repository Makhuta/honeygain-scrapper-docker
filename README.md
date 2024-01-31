# HoneyGain Docker scrapper

## How to run container

Start the Docker container by binding to external port `8080`

```bash
docker run 
	-d --name=honeygain-scrapper
	-p 8080:8080
	-e HG_USERNAME=YOUR_HONEYGAIN_USERNAME
	-e HG_PASSWORD=YOUR_HONEYGAIN_PASSWORD
makhuta/honeygain-scrapper
```

To check if it is working correctly you can check [localhost:8080](http://localhost:8080) (for **localhost** you need to use ip of your server) you should see this:
```bash
{
"Hello":"World"
}
```

For showing all infos you can check [localhost:8080/help](http://localhost:8080/help)

The object is structurized like this:

```bash
{
"CATEGORY": ["FUNCTION_1", "FUNCTION_2", ...]
}
```

And it is used as such: [localhost:8080/CATEGORY/FUNCTION_1](http://localhost:8080/infos/me)
