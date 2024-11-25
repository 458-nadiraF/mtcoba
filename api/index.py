from http.server import BaseHTTPRequestHandler
import json
import requests

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Hello, world!'.encode('utf-8'))
        return
    def get_account_balance():
        headers = {
            'Accept': 'application/json',
            'auth-token': process.env.METAAPI_TOKEN  # Replace with your actual token
        }
        
        try:
            # Make GET request
            get_balance_url="https://mt-client-api-v1.london.agiliumtrade.ai/users/current/accounts/07a8b605-7615-44cc-95aa-7204ff910e22/account-information"
            response = requests.get(get_balance_url, headers=headers)
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                return data.get('balance')  # Returns the balance value
            else:
                print(f"Error: API request failed with status code {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error fetching balance: {str(e)}")
            return None
    def do_POST(self):
        # terima alert dr tv
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "POST received"}).encode())
        try:
            # Parse the received JSON data
            received_json = json.loads(post_data.decode('utf-8'))
            balance=get_account_balance()
            # Define the API endpoint where you want to forward the request
            forward_url = "https://mt-client-api-v1.london.agiliumtrade.ai/users/current/accounts/07a8b605-7615-44cc-95aa-7204ff910e22/trade"  # Replace with your actual API endpoint


            #get account balance
            
            # Send POST request to the specified API
            headers = {
                'Accept': 'application/json',
                'auth-token':process.env.METAAPI_TOKEN
                # Add any other required headers here
            }
            
            response = requests.post(
                forward_url,
                json=received_json,
                headers=headers
            )
            
            # Send response back to the original client
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # You can customize the response based on the forwarded request's response
            response_data = {
                "message": "POST received and forwarded",
                "forward_status": response.status_code,
                "forward_response": response.json()  # Include this if you want to return the forwarded API's response
            }
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            # Handle any errors
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = {
                "error": str(e),
                "message": "Error processing request"
            }
            self.wfile.write(json.dumps(error_response).encode())
        
        
