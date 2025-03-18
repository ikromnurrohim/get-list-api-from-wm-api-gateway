# Get List API From webMethods API Gateway
If you're working with webMethods API Gateway and find yourself needing to retrieve the API list along with nativeEndpoint details, it might take extra time, especially if your API Gateway has numerous APIs.

However, if your using this tool, the process of listing all APIs in your gateway will be more efficient.

In this tools I have share two script, first main.sh script that running on bash and second one script writen in python.
I create thoose two type to meet our environment something our server in intranet so can't access internet for downloading tools like lib from python, so if your environment can't access internet you can use bash script instead python script, but if your server can access internet I suggest you to use python script which can have more advantages in result.

### Requirement For Bash Script
- Install [jq](https://github.com/jqlang/jq)
- Have an Access to API Gateway UI
- Bash


After running that bash script piece of file will be crated on which directory you been assing to variable *asset_dir*

<table>
<thead>
<tr>
<th>fileName</th>
<th>storedValue</th>
</tr>
<thead>
<tbody>
<tr>
<td>apiName</td>
<td>API Name</td>
</tr>
<tr>
<td>apiVersion</td>
<td>API Version</td>
</tr>
<tr>
<td>isActive</td>
<td>API Status (true or false)</td>
</tr>
<tr>
<td>gatewayEndpoints</td>
<td>Gateway Endpoints (If the value is stored as [], it means the API is not active)</td>
</tr>
<tr>
<td>endpointUris</td>
<td>Backend Endpoints</td>
</tr>
</tbody>
</table>


### Requirement For Python Script
- create virtualenv
- install requirements using command bellow
```console
foo@bar:~$ pip install -r requirements.txt 
```
- update some config in file main.py to meet to your webmethods apigateway ip and user-pass
- running and you will see the csv file that contain apis in apigateway data


### Conclusion
This script calls APIs from the API Gateway, parses the responses, and stores the required data in separate files.


Thanks for comming, Have a nice days🔥🔥🔥🔥


