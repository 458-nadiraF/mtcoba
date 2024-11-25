from http.server import BaseHTTPRequestHandler
import json
import requests
import traceback

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
      
        try:
            content_length = int(self.headers.get('Content-Length', 0))  # Default to 0 if not present
            if content_length > 0:
                post_data = self.rfile.read(content_length).decode('utf-8')  # Decode bytes to string
            else:
                post_data = ""  # No data sent
            
            if not post_data.strip():  # Check if the body is empty or whitespace
                raise ValueError("Empty request body")
            
            # Parse JSON
            data = json.loads(post_data)
            #received_json = json.loads(post_data.decode('utf-8'))
            lot=received_json.get('lot')
            sl=received_json.get('sl')
            tp=received_json.get('tp')
            symbol=received_json.get('symbol')
            
            balance=get_account_balance()
            # Define the API endpoint where you want to forward the request
            forward_url = "https://mt-client-api-v1.london.agiliumtrade.ai/users/current/accounts/07a8b605-7615-44cc-95aa-7204ff910e22/trade"  # Replace with your actual API endpoint
            
            buy_json={
               "symbol": symbol,
               "actionType": "ORDER_TYPE_BUY",
               "volume": lot,
               "stopLoss": sl,
               "takeProfit": tp,
               "stopLossUnits": "ABSOLUTE_PRICE",
               "takeProfitUnits": "ABSOLUTE_PRICE"
            }
            #get account balance
            #contoh json
            # {
            #   "symbol": "EURUSD",
            #   "actionType": "ORDER_TYPE_BUY",
            #   "volume": 0.01,
            #   "stopLoss": 1.030,
            #   "takeProfit": 1.06,
            #   "stopLossUnits": "ABSOLUTE_PRICE",
            #   "takeProfitUnits": "ABSOLUTE_PRICE"
            # }
            # Send POST request to the specified API
            headers = {
                'Accept': 'application/json',
                'auth-token':process.env.METAAPI_TOKEN,
                'Content-Type':'application/json'
                # Add any other required headers here
            }
            
            response = requests.post(
                forward_url,
                json=buy_json,
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
            traceback.print_exc()
            self.wfile.write(json.dumps(error_response).encode())
        
        
