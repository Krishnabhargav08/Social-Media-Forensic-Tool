# Quick Setup Guide - Social Media Forensic Tool

## 🚀 Fast Setup (5 Minutes)

### Step 1: Install MongoDB
1. Download MongoDB Community Edition
2. Install and start MongoDB service
3. MongoDB should run on `mongodb://localhost:27017`

### Step 2: Backend Setup
```powershell
# Open PowerShell in SFT/backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Start backend server
python app.py
```

Backend will run on: `http://localhost:5000`

### Step 3: Frontend Setup
```powershell
# Open NEW PowerShell in SFT/frontend folder
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: `http://localhost:3000`

### Step 4: Create Admin Account

**Method 1: Manual Registration (Recommended)**
1. Go to `http://localhost:3000`
2. Click "Register as Investigator"
3. Fill form with admin details
4. Open MongoDB Compass or mongo shell
5. Connect to `mongodb://localhost:27017`
6. Go to `forensic_tool` database → `users` collection
7. Find your user and edit:
   - Change `role` from `"investigator"` to `"admin"`
   - Change `status` from `"pending"` to `"approved"`
8. Save and login

**Method 2: Python Script**
```python
# Create admin_setup.py in backend folder
from pymongo import MongoClient
import bcrypt

client = MongoClient('mongodb://localhost:27017/')
db = client['forensic_tool']

# Hash password
password = "Admin@123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))

# Create admin
db.users.insert_one({
    'email': 'admin@forensictool.com',
    'password': hashed,
    'full_name': 'System Administrator',
    'badge_number': 'ADMIN-001',
    'department': 'System Administration',
    'role': 'admin',
    'status': 'approved',
    'login_attempts': 0,
    'account_locked': False,
    'created_at': datetime.utcnow(),
    'updated_at': datetime.utcnow()
})

print("Admin created!")
print("Email: admin@forensictool.com")
print("Password: Admin@123")
```

Then run:
```bash
python admin_setup.py
```

---

## ✅ Verification

### Test Backend
```bash
# Check health endpoint
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "online",
  "message": "Social Media Forensic Tool API is running",
  "version": "1.0.0"
}
```

### Test Frontend
1. Open browser: `http://localhost:3000`
2. Should see cyber-themed landing page
3. Click "Official Login"
4. Login with admin credentials

---

## 🧪 Complete Test Flow

### As Admin:
1. Login → `http://localhost:3000/login`
2. Email: `admin@forensictool.com`
3. Password: `Admin@123` (or what you set)
4. Should redirect to Admin Dashboard
5. Register a new investigator from another browser/incognito
6. Approve the investigator from admin panel

### As Investigator:
1. Register → `http://localhost:3000/register`
   - Email: `john.doe@agency.gov`
   - Password: `Test@1234` (must meet requirements)
   - Full Name: `John Doe`
   - Badge: `BADGE-001`
   - Department: `Cyber Crime Division`
2. Wait for admin approval
3. Login after approval
4. Create new case:
   - Username: `@suspicious_user`
   - Platform: `Twitter`
5. Click "Scrape Data" (simulated data will be collected)
6. Click "Analyze Data" (AI analysis will run)
7. View risk score and detection results
8. Generate report with password: `Report@123`
9. Remember the password for later download

---

## 🐛 Troubleshooting

### MongoDB Connection Error
```
Error: MongoClient connection refused
```
**Solution**: Start MongoDB service
```powershell
# Windows
net start MongoDB

# Or use MongoDB Compass
```

### Backend Port Already in Use
```
Error: Address already in use: 5000
```
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Frontend Build Errors
```
npm ERR! code ERESOLVE
```
**Solution**:
```bash
npm install --legacy-peer-deps
```

### Python Module Not Found
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**: Make sure venv is activated
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📦 Required Software Versions

- **Node.js**: v16.0.0 or higher
- **Python**: 3.8 or higher
- **MongoDB**: 5.0 or higher
- **npm**: 7.0 or higher
- **pip**: 21.0 or higher

### Check Versions
```powershell
node --version
python --version
mongod --version
npm --version
pip --version
```

---

## 🎯 Default Ports

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000
- **MongoDB**: mongodb://localhost:27017

---

## 📁 Important Files

### Backend
- `backend/app.py` - Main Flask application
- `backend/.env` - Environment variables (CREATE THIS!)
- `backend/requirements.txt` - Python dependencies

### Frontend
- `frontend/package.json` - Node dependencies
- `frontend/vite.config.js` - Dev server config
- `frontend/src/App.jsx` - Main React component

---

## 🔒 Default Credentials (After Setup)

**Admin Account**:
- Email: `admin@forensictool.com`
- Password: `Admin@123`

**Test Investigator** (after registration):
- Email: `john.doe@agency.gov`
- Password: `Test@1234`

⚠️ **CHANGE THESE IN PRODUCTION!**

---

## 🎓 For Project Submission

1. ✅ Ensure both servers are running
2. ✅ Take screenshots of all pages
3. ✅ Document test scenarios
4. ✅ Create demo video
5. ✅ Prepare presentation

---

## 💡 Quick Tips

1. **Always activate venv** before running backend
2. **Keep MongoDB running** in background
3. **Use different browsers** for admin/investigator testing
4. **Check browser console** for frontend errors
5. **Check terminal** for backend errors

---

## 🎉 You're Ready!

Your Social Media Forensic Tool is now set up and ready for testing and demonstration!

For detailed documentation, see the main [README.md](README.md)
