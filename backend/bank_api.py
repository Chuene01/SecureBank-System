"""
Banking API with MongoDB
"""
from datetime import datetime
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pymongo import MongoClient
import urllib.parse

class MongoDBBankingAPI:
    def __init__(self, mongo_uri="mongodb://localhost:27017"):
        # Connect to MongoDB
        self.client = MongoClient(mongo_uri)
        self.db = self.client["banking_db"]
        self.users_collection = self.db["users"]
        self.transactions_collection = self.db["transactions"]
        
        # Create indexes
        self.users_collection.create_index("username", unique=True)
        self.transactions_collection.create_index("username")
        
        # Initialize with test users if empty
        self._initialize_test_data()
    
    def _initialize_test_data(self):
        """Initialize with test users if database is empty"""
        if self.users_collection.count_documents({}) == 0:
            test_users = [
                {
                    "username": "john",
                    "email": "john@example.com",
                    "password": "password123",
                    "balance": 1000.0,
                    "created_at": datetime.now().isoformat()
                },
                {
                    "username": "jane",
                    "email": "jane@example.com",
                    "password": "password456",
                    "balance": 2500.0,
                    "created_at": datetime.now().isoformat()
                }
            ]
            self.users_collection.insert_many(test_users)
            print("Initialized database with test users")
    
    def register(self, username, email, password):
        """Register a new user"""
        username = username.strip()
        email = email.strip()
        
        # Check if user exists
        if self.users_collection.find_one({"username": username}):
            raise Exception("Username already exists")
        
        user_data = {
            "username": username,
            "email": email,
            "password": password,  # In production, hash this!
            "balance": 0.0,
            "created_at": datetime.now().isoformat()
        }
        
        self.users_collection.insert_one(user_data)
        
        return {
            "message": f"User {username} registered successfully",
            "username": username,
            "email": email,
            "balance": 0.0
        }
    
    def login(self, username, password):
        """User login"""
        username = username.strip()
        user = self.users_collection.find_one({"username": username})
        
        if not user or user["password"] != password:
            raise Exception("Invalid username or password")
        
        # Remove password from response
        user.pop("password", None)
        user.pop("_id", None)
        
        return {
            "message": "Login successful",
            **user
        }
    
    def get_balance(self, username):
        """Get user balance"""
        username = username.strip()
        user = self.users_collection.find_one({"username": username})
        
        if not user:
            raise Exception("User not found")
        
        return {
            "username": username,
            "balance": user["balance"]
        }
    
    def deposit(self, username, amount):
        """Make a deposit"""
        username = username.strip()
        
        # Validate amount
        try:
            amount = float(amount)
        except ValueError:
            raise Exception("Amount must be a number")
        
        if amount <= 0:
            raise Exception("Amount must be positive")
        
        # Update user balance
        result = self.users_collection.update_one(
            {"username": username},
            {"$inc": {"balance": amount}}
        )
        
        if result.modified_count == 0:
            raise Exception("User not found")
        
        # Get updated balance
        user = self.users_collection.find_one({"username": username})
        
        # Record transaction
        transaction = {
            "username": username,
            "type": "deposit",
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "new_balance": user["balance"]
        }
        self.transactions_collection.insert_one(transaction)
        
        return {
            "message": "Deposit successful",
            "username": username,
            "amount": amount,
            "new_balance": user["balance"]
        }
    
    def withdraw(self, username, amount):
        """Make a withdrawal"""
        username = username.strip()
        
        # Validate amount
        try:
            amount = float(amount)
        except ValueError:
            raise Exception("Amount must be a number")
        
        if amount <= 0:
            raise Exception("Amount must be positive")
        
        # Check if user has sufficient funds
        user = self.users_collection.find_one({"username": username})
        if not user:
            raise Exception("User not found")
        
        if user["balance"] < amount:
            raise Exception(f"Insufficient funds. Available balance: {user['balance']}")
        
        # Update user balance
        result = self.users_collection.update_one(
            {"username": username},
            {"$inc": {"balance": -amount}}
        )
        
        # Get updated balance
        user = self.users_collection.find_one({"username": username})
        
        # Record transaction
        transaction = {
            "username": username,
            "type": "withdraw",
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "new_balance": user["balance"]
        }
        self.transactions_collection.insert_one(transaction)
        
        return {
            "message": "Withdrawal successful",
            "username": username,
            "amount": amount,
            "new_balance": user["balance"]
        }
    
    def get_transactions(self, username, limit=50):
        """Get user transactions"""
        username = username.strip()
        
        # Check if user exists
        user = self.users_collection.find_one({"username": username})
        if not user:
            raise Exception("User not found")
        
        # Get transactions
        transactions = list(self.transactions_collection.find(
            {"username": username},
            {"_id": 0}  # Exclude MongoDB _id field
        ).sort("timestamp", -1).limit(limit))
        
        return {
            "username": username,
            "transactions": transactions,
            "count": len(transactions)
        }
    
    def list_users(self):
        """List all users (without passwords)"""
        users = list(self.users_collection.find(
            {},
            {"_id": 0, "password": 0}  # Exclude password and _id
        ))
        
        return {"users": users}

# Create API instance
# You can change the connection string here
MONGO_URI = "mongodb://localhost:27017"  # Change this if using MongoDB Atlas
api = MongoDBBankingAPI(MONGO_URI)

class BankingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request("GET")
    
    def do_POST(self):
        self.handle_request("POST")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
    
    def handle_request(self, method):
        path = self.path.split('?')[0]
        
        # Parse request body
        body_data = {}
        if method == "POST":
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length).decode('utf-8')
                try:
                    body_data = json.loads(body)
                except json.JSONDecodeError:
                    self.send_error_response(400, "Invalid JSON")
                    return
        
        # Route handling
        try:
            if path == "/":
                result = self.home()
            elif path == "/register" and method == "POST":
                result = api.register(
                    body_data.get("username"),
                    body_data.get("email"),
                    body_data.get("password")
                )
            elif path == "/login" and method == "POST":
                result = api.login(
                    body_data.get("username"),
                    body_data.get("password")
                )
            elif path == "/balance" and method == "POST":
                result = api.get_balance(body_data.get("username"))
            elif path == "/deposit" and method == "POST":
                result = api.deposit(
                    body_data.get("username"),
                    body_data.get("amount")
                )
            elif path == "/withdraw" and method == "POST":
                result = api.withdraw(
                    body_data.get("username"),
                    body_data.get("amount")
                )
            elif path == "/transactions" and method == "POST":
                result = api.get_transactions(body_data.get("username"))
            elif path == "/users" and method == "GET":
                result = api.list_users()
            else:
                self.send_error_response(404, f"Endpoint {path} not found")
                return
            
            self.send_success_response(result)
            
        except Exception as e:
            self.send_error_response(400, str(e))
    
    def home(self):
        return {
            "message": "Banking API with MongoDB",
            "database": "MongoDB",
            "endpoints": [
                {"path": "/", "methods": ["GET"], "description": "API information"},
                {"path": "/register", "methods": ["POST"], "description": "Register new user"},
                {"path": "/login", "methods": ["POST"], "description": "User login"},
                {"path": "/balance", "methods": ["POST"], "description": "Get user balance"},
                {"path": "/deposit", "methods": ["POST"], "description": "Make a deposit"},
                {"path": "/withdraw", "methods": ["POST"], "description": "Make a withdrawal"},
                {"path": "/transactions", "methods": ["POST"], "description": "Get user transactions"},
                {"path": "/users", "methods": ["GET"], "description": "List all users"}
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    def send_success_response(self, data):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    def send_error_response(self, status_code, error_message):
        self.send_response(status_code)
        self.send_cors_headers()
        self.end_headers()
        response = {"error": error_message}
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def log_message(self, format, *args):
        pass

def run_server(port=8000):
    print(f"╔════════════════════════════════════════════════════╗")
    print(f"║       Banking API with MongoDB                     ║")
    print(f"╠════════════════════════════════════════════════════╣")
    print(f"║ Server URL: http://localhost:{port}                ║")
    print(f"║ MongoDB URI: {MONGO_URI}                           ║")
    print(f"║                                                    ║")
    print(f"║ Available Endpoints:                               ║")
    print(f"║ • GET  /              - API information            ║")
    print(f"║ • POST /register      - Register new user          ║")
    print(f"║ • POST /login         - User login                 ║")
    print(f"║ • POST /balance       - Get user balance           ║")
    print(f"║ • POST /deposit       - Make a deposit             ║")
    print(f"║ • POST /withdraw      - Make a withdrawal          ║")
    print(f"║ • POST /transactions  - Get user transactions      ║")
    print(f"║ • GET  /users         - List all users             ║")
    print(f"║                                                    ║")
    print(f"║ Press Ctrl+C to stop the server                    ║")
    print(f"╚════════════════════════════════════════════════════╝")
    
    server = HTTPServer(('localhost', port), BankingHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()

if __name__ == "__main__":
    run_server(8000)