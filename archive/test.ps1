# Define the API endpoint
$Uri = 'http://localhost:11434/api/generate'

# Create a hashtable for the JSON payload
$Body = @{
    model = "codellama"
    prompt = "Why is the sky blue?"
    options = @{
        num_ctx = 4096
    }
    stream = $false
}

# Convert the hashtable to a JSON string
$JsonBody = $Body | ConvertTo-Json

# Use Invoke-RestMethod to send a POST request with the JSON payload
$Response = Invoke-RestMethod -Uri $Uri -Method Post -Body $JsonBody -ContentType 'application/json'

# Print the response
$Response
