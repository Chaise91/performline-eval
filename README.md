# Some notes on how I did this

First off I wanted to know what I was working with, so I configure the provided file as a service in my personal lab environment and discovered it to be some sort of webserver hosting a simple webpage.

From there, it came down to putting the right commands in the right order for the user-data. There is some room for improvement with using a custom AMI. For this eval I used Amazon Linux 2.

I have multiple AWS profiles on my computer, so please note that if you want to run the Python yourself, line 13 will likely need to be changed.

```
session = boto3.session.Session(profile_name='performline')
```

## Potential Improvements
- As mentioned before, a customer AMI containing the static items
- Build in handling of resources that already exist
- More verbose outputs
- More efficient way of deleting the resources created by the script