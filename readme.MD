# Get List API From webMethods API Gateway
If you're working with webMethods API Gateway and find yourself needing to retrieve the API list along with nativeEndpoint details, it might take extra time, especially if your API Gateway has numerous APIs.

However, after reading this article, the process of listing all APIs in your gateway will be more efficient.

### Requirement
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


### Conclusion
This script calls APIs from the API Gateway, parses the responses, and stores the required data in separate files.


Thanks for comming, Have a nice days🔥🔥🔥🔥


