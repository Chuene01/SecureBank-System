# Banking System - Cloud Native Application

A modern, secure banking system built with HTML/CSS/JavaScript frontend and Python FastAPI backend, featuring real-time transactions, account management, and comprehensive security.

---

## Team Members

| Name | Role | Responsibilities |
|------|------|-----------------|
| **Kagiso** | Frontend Lead | Architecture, Code Review |
| **Elona** | Frontend/Backend Developer | API Integration |
| **Zwavhudi** | Frontend Developer | Backend Developer |
| **Jaden** | UI/UX Designer | Visual Design |
| **Mthobisi** | UI/UX Designer | Design System, Wireframes |
| **Chuene** | Backend Lead | API Development, MongoDB |
| **Ntando** | DevOps Engineer| Project Manager | Infrastructure, Documentation |
| **Elihle** | Project Manager | Agile Ceremonies, Tracking |

---

## Tech Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with Flexbox/Grid
- **JavaScript (ES6+)** - Vanilla JS for interactivity
- **Fetch API** - HTTP client for API calls

### Backend
- **Python 3.9+** - Programming language
- **FastAPI** - Modern web framework
- **PyMongo** - MongoDB driver
- **PyJWT** - JSON Web Token authentication
- **Bcrypt** - Password hashing
- **Uvicorn** - ASGI server

### Database
- **MongoDB** - NoSQL database for flexible data storage

### DevOps
- **Git & GitHub** - Version control
- **Docker & Docker Compose** - Containerization
- **GitHub Actions** - CI/CD pipeline

---

## Features

### Week 1 Deliverables
- ✅ User Registration & Login
- ✅ Secure Authentication (JWT)
- ✅ Account Dashboard
- ✅ Money Deposit
- ✅ Money Withdrawal
- ✅ Transaction History
- ✅ Responsive Design

### Security Features
- Password hashing with bcrypt
- JWT token-based authentication
- Protected API routes
- Input validation
- CORS protection

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9 or higher** - [Download](https://www.python.org/downloads/)
- **MongoDB 5.0 or higher** - [Download](https://www.mongodb.com/try/download/community)
- **Git** - [Download](https://git-scm.com/downloads)
- **Code Editor** - VS Code recommended

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/DopeGrammerZA/banking-system-cloud-native.git
cd banking-system-cloud-native
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env

# Edit .env file with your settings
# Update MONGODB_URI and JWT_SECRET
```

**requirements.txt** should contain:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pymongo==4.6.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.0
python-dotenv==1.0.0
```

### 3. MongoDB Setup

```bash
# Start MongoDB service
# On Windows:
net start MongoDB

# On macOS (with Homebrew):
brew services start mongodb-community

# On Linux:
sudo systemctl start mongod

# Verify MongoDB is running
mongosh
# You should see MongoDB shell
```

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# No installation needed for vanilla HTML/CSS/JS
# Just open with a local server

# Option 1: Python HTTP Server
python -m http.server 3000

# Option 2: VS Code Live Server Extension
# Right-click index.html → "Open with Live Server"
```

### 5. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python -m http.server 3000
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

## 🌐 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |


### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/transactions/deposit` | Deposit money |
| POST | `/api/transactions/withdraw` | Withdraw money |
| GET | `/api/transactions/history` | Get transaction history |

### Example API Requests

**Register User:**
```json
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**Login:**
```json
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securePassword123"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "...",
    "name": "John Doe",
    "email": "john@example.com",
    "balance": 0
  }
}
```

**Deposit (requires authentication):**
```json
POST /api/transactions/deposit
Authorization: Bearer <your-jwt-token>
Content-Type: application/json

{
  "amount": 1000
}
```

---

## Project Structure

```
banking-system-cloud-native/
├── frontend/
│   ├── css/
│   │   ├── main.css           # Global styles
│   │   ├── login.css          # Login page styles
│   │   ├── dashboard.css      # Dashboard styles
│   │   └── components.css     # Reusable component styles
│   ├── js/
│   │   ├── api.js             # API service layer
│   │   ├── auth.js            # Authentication logic
│   │   ├── utils.js           # Utility functions
│   │   └── pages/
│   │       ├── login.js       # Login page logic
│   │       ├── dashboard.js   # Dashboard logic
│   │       ├── deposit.js     # Deposit page logic
│   │       ├── withdraw.js    # Withdraw page logic
│   │       └── history.js     # History page logic
│   ├── pages/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── deposit.html
│   │   ├── withdraw.html
│   │   └── history.html
│   ├── assets/
│   │   └── images/
│   └── index.html
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py        # Authentication routes
│   │   │   ├── transactions.py # Transaction routes
│   │   │   └── account.py     # Account routes
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py        # User model
│   │   │   └── transaction.py # Transaction model
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   └── auth.py        # JWT verification
│   │   └── config/
│   │       ├── __init__.py
│   │       └── database.py    # MongoDB connection
│   ├── requirements.txt
│   ├── main.py                # Application entry point
│   └── .env.example
│
├── docs/
│   ├── architecture/
│   │   └── system-architecture.md
│   ├── screenshots/
│   └── guides/
│       ├── integration-guide.md
│       └── troubleshooting.md
│
├── docker/
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   └── docker-compose.yml
│
├── .github/
│   └── workflows/
│       └── test.yml           # CI/CD pipeline
│
├── .gitignore
├── README.md
└── .env.example
```

---

## Docker Deployment (Week 2)

### Quick Start with Docker

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Access the application:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- MongoDB: mongodb://localhost:27017

---

## Testing

### Manual Testing Checklist

- [ ] User can register with valid details
- [ ] User cannot register with duplicate email
- [ ] User can login with correct credentials
- [ ] User cannot login with wrong password
- [ ] Dashboard displays correct balance
- [ ] User can deposit money successfully
- [ ] User can withdraw money (if sufficient balance)
- [ ] User cannot withdraw more than balance
- [ ] Transaction history displays all transactions
- [ ] UI is responsive on mobile and desktop

### API Testing with Postman

1. Import the Postman collection from `/docs/postman/`
2. Set environment variables:
   - `base_url`: http://localhost:8000
   - `token`: (auto-populated after login)
3. Run the collection tests

---

## Configuration

### Environment Variables

**Backend (.env):**
```env
MONGODB_URI=mongodb://localhost:27017/banking_system
JWT_SECRET=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
PORT=8000
DEBUG=True
```

**Frontend:**
Update API base URL in `js/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

---

## Troubleshooting

### MongoDB Connection Issues
```bash
# Check if MongoDB is running
mongosh

# If not running, start it:
# Windows:
net start MongoDB

# macOS:
brew services start mongodb-community

# Linux:
sudo systemctl start mongod
```

### Port Already in Use
```bash
# Find process using port
# Windows:
netstat -ano | findstr :8000

# macOS/Linux:
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### CORS Errors
Ensure backend CORS middleware allows your frontend origin:
```python
allow_origins=["http://localhost:3000"]
```

For more troubleshooting, see `/docs/guides/troubleshooting.md`

---

## Documentation

- [Architecture Overview](/docs/architecture/system-architecture.md)
- [API Integration Guide](/docs/guides/integration-guide.md)
- [Troubleshooting Guide](/docs/guides/troubleshooting.md)
- [Docker Setup Guide](/docs/guides/docker-setup.md)

---

## Sprint Progress

### Week 1 (Current Sprint)
- Project setup and repository structure
- Team collaboration tools setup
- UI/UX design and wireframes
- Frontend pages (Login, Dashboard, Deposit, Withdraw, History)
- Backend API implementation
- MongoDB integration
- Authentication system
- Transaction management

### Week 2 (Upcoming)
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Cloud deployment (AWS/Azure/GCP)
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Comprehensive testing

---

## Contributing

1. Create a feature branch from `develop`
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

3. Push to GitHub
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request to `develop` branch
5. Request review from team lead
6. Merge after approval

---

## License

This project is created for educational purposes as part of a software engineering course.

---

## Support

For questions or issues:
- Create an issue on GitHub
- Contact the project manager: Elihle
- Contact the DevOps engineer: Ntando

---

## Acknowledgments

- Team members for their dedication and collaboration
- Course instructors for guidance
- Open source community for excellent tools and frameworks

---

**Last Updated:** November 2025  
