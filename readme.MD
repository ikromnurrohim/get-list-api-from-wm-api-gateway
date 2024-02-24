# Get List API From webMethods API Gateway
If you're working with webMethods API Gateway and find yourself needing to retrieve the API list along with nativeEndpoint details, it might take extra time, especially if your API Gateway has numerous APIs.

However, after reading this article, the process of listing all APIs in your gateway will be more efficient.

### Requirement
- Install [jq](https://github.com/jqlang/jq)
- Have an Access to API Gateway UI
- Bash


The script for retrieving what you need is down below guys!
```bash
#!/bin/bash

# variables
apigw='<domain-or-ip>/apigatewayui/'
cookie='Cookie: JSESSIONID=<value>; API_GW_JSESSIONID=<value>'  # this cookie get from your login in apigw ui
accept='Accept: application/json'
asset_dir='<absolute-path-for-store-the-data>'


# get list api
curl --location "$apigw/apigateway/apis/" -H "$cookie" -H "$accept" > $asset_dir/apis.json


# using jq to parse apiName, apiVersion, apiId and isActive from file apis.json
jq '.apiResponse[].api.apiName' $asset_dir/apis.json  | tr -d '"' > $asset_dir/apiName
jq '.apiResponse[].api.apiVersion' $asset_dir/apis.json  | tr -d '"' > $asset_dir/apiVersion
jq '.apiResponse[].api.id' $asset_dir/apis.json  | tr -d '"' > $asset_dir/apiId
jq '.apiResponse[].api.isActive' $asset_dir/apis.json > $asset_dir/isActive


# looping through list apiId apiDetails, then we query apiDetails to get gatewayEndpoints and policiesId
while read apiId; do
    curl --location "$apigw/apigateway/apis/$apiId" -H "$cookie" -H "$accept" > $asset_dir/apiDetails
    jq '.apiResponse.gatewayEndPoints' $asset_dir/apiDetails >> $asset_dir/gatewayEndpoints
    jq '.apiResponse.api.policies' $asset_dir/apiDetails | tr -d '["][:space:]'>> $asset_dir/policiesId && echo >> $asset_dir/policiesId
done < $asset_dir/apiId


# looping through policiesId to get endpointUri
while read policiesId; do
    curl --location "$apigw/facade/apigateway/policies/$policiesId" -H "$cookie" -H "$accept" > $asset_dir/policies
    jq '.policy.stageEnforcements[] | select(.stageKey == "routing")' $asset_dir/policies > $asset_dir/policyRouting
    jq '.policyActions[0].parameters[] | select(.templateKey == "endpointUri")' $asset_dir/policyRouting > $asset_dir/endpointUri
    jq '.values' $asset_dir/endpointUri | tr -d '["][:space:]' >> $asset_dir/endpointUris
    echo "" >> $asset_dir/endpointUris
done < $asset_dir/policiesId
```



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


Thanks for reading, Have a nice days🔥🔥🔥🔥


