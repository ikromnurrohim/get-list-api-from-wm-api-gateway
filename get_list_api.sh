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
