# 🧪 Testing Guide - Social Media Forensic Tool

## Complete Testing Scenarios for Demonstration

---

## 🚀 Pre-Testing Setup

### 1. Start All Services
```powershell
# Terminal 1 - MongoDB
# Ensure MongoDB is running on localhost:27017

# Terminal 2 - Backend
cd backend
.\venv\Scripts\activate
python app.py
# Should show: Running on http://127.0.0.1:5000

# Terminal 3 - Frontend
cd frontend
npm run dev
# Should show: Local: http://localhost:3000
```

### 2. Create Admin Account
```powershell
cd backend
.\venv\Scripts\activate
python create_admin.py

# Use defaults:
# Email: admin@forensictool.com
# Password: Admin@123
```

---

## 📋 Test Scenario 1: Landing Page & Navigation

### Expected UI Elements
✅ Cyber-themed background with animated grid  
✅ Large "Social Media Forensic Tool" title with gradient  
✅ Feature cards (Data Collection, AI Analysis, etc.)  
✅ Security notice in yellow border  
✅ "Official Login" and "Register as Investigator" buttons  

### Actions
1. Open http://localhost:3000
2. Verify all animations are smooth
3. Hover over feature cards (should lift up)
4. Click "Official Login" → Should navigate to /login
5. Go back, click "Register" → Should navigate to /register

---

## 📋 Test Scenario 2: User Registration

### Test Case 2.1: Valid Registration
**Steps:**
1. Go to `/register`
2. Fill form:
   - Full Name: `John Doe`
   - Email: `john.doe@agency.gov`
   - Badge Number: `BADGE-12345`
   - Department: `Cyber Crime Division`
   - Password: `Test@1234`
   - Confirm Password: `Test@1234`
3. Click "Register Account"

**Expected Result:**
✅ Success message appears  
✅ "Awaiting admin approval" text shown  
✅ Redirect to login page after 3 seconds  

### Test Case 2.2: Password Validation
**Steps:**
1. Try weak password: `test123`
2. Submit form

**Expected Result:**
❌ Error: "Password must contain uppercase letter"

### Test Case 2.3: Email Duplication
**Steps:**
1. Register with same email again

**Expected Result:**
❌ Error: "User already exists"

---

## 📋 Test Scenario 3: Admin Login & Dashboard

### Test Case 3.1: Admin Login
**Steps:**
1. Go to `/login`
2. Email: `admin@forensictool.com`
3. Password: `Admin@123`
4. Click "Secure Login"

**Expected Result:**
✅ Redirect to `/admin/dashboard`  
✅ Shows statistics cards  
✅ Sidebar shows "ADMIN" role  
✅ Pending user appears in approval panel  

### Test Case 3.2: User Approval
**Steps:**
1. In Admin Dashboard
2. Find John Doe in "Pending User Approvals"
3. Click "Approve" button

**Expected Result:**
✅ User disappears from pending list  
✅ "Pending Approvals" count decreases  
✅ "Approved Users" count increases  

### Test Case 3.3: Statistics Display
**Verify:**
- Total Users: 2 (admin + john)
- Pending Approvals: 0
- Active Cases: 0
- High Risk Cases: 0

---

## 📋 Test Scenario 4: Investigator Login

### Test Case 4.1: Login Before Approval
**Steps:**
1. Logout from admin
2. Try to login as john.doe@agency.gov

**Expected Result:**
❌ Error: "Account pending approval"

### Test Case 4.2: Login After Approval
**Steps:**
1. Login as john.doe@agency.gov
2. Password: Test@1234

**Expected Result:**
✅ Redirect to `/investigator/dashboard`  
✅ Shows "My Cases" section  
✅ "No cases yet" message  
✅ "Create Your First Case" button  

---

## 📋 Test Scenario 5: Create Investigation Case

### Test Case 5.1: Create New Case
**Steps:**
1. Click "New Investigation" button
2. Fill modal:
   - Target Username: `@suspicious_user`
   - Platform: `Twitter`
   - Description: `Potential fraud investigation`
3. Click "Create Case"

**Expected Result:**
✅ Success alert  
✅ Modal closes  
✅ New case card appears in dashboard  
✅ Case shows "active" status  

---

## 📋 Test Scenario 6: Full Investigation Workflow

### Test Case 6.1: Data Scraping
**Steps:**
1. Click on the case card
2. Should navigate to `/case/{caseId}`
3. Click "Scrape Data" button
4. Wait for process

**Expected Result:**
✅ Button shows "Scraping..."  
✅ Success alert after ~2 seconds  
✅ Evidence hash appears in left panel  
✅ "Analyze Data" button becomes enabled  

**Verify Evidence Hash:**
- Should be 64-character hex string
- Format: SHA-256 hash
- Displayed in monospace font
- Green color (#00ff88)

### Test Case 6.2: Data Analysis
**Steps:**
1. Click "Analyze Data" button
2. Wait for process

**Expected Result:**
✅ Button shows "Analyzing..."  
✅ Success alert after ~2 seconds  
✅ Risk meter appears with score  
✅ All detection panels populate  

**Verify Analysis Results:**

**Risk Meter:**
- Circular progress animation
- Score displayed (0-100)
- Color changes based on risk:
  - Green: 0-24 (LOW)
  - Yellow: 25-49 (MEDIUM)
  - Orange: 50-74 (HIGH)
  - Red: 75-100 (CRITICAL)

**Sentiment Analysis:**
- Overall sentiment (positive/negative/neutral)
- Three progress bars:
  - Positive (green)
  - Negative (red)
  - Neutral (gray)
- Percentages should sum to 100%

**Cyberbullying Detection:**
- Status: DETECTED or NOT DETECTED
- Confidence percentage
- Incidents count
- Red border if detected

**Fraud Detection:**
- Status indicator
- Confidence score
- Suspicious posts count
- Orange border if detected

**Fake Profile Analysis:**
- Potentially fake status
- Fake score /100
- Account age in days
- Risk factors list

### Test Case 6.3: Report Generation
**Steps:**
1. Click "Generate Report" button
2. Modal appears
3. Enter password: `Report@123`
4. Click "Generate Report"
5. Wait for process

**Expected Result:**
✅ Button shows "Generating..."  
✅ Success alert with message about password  
✅ Modal closes  
✅ Report ID stored  

**Note:** In full implementation, download would be available. Current version stores report reference.

---

## 📋 Test Scenario 7: Admin Monitoring

### Test Case 7.1: View All Cases (Admin)
**Steps:**
1. Logout as investigator
2. Login as admin
3. Check "All Cases" count in statistics

**Expected Result:**
✅ Shows 1 total case  
✅ Active cases: 1  

### Test Case 7.2: High-Risk Alert
**If case risk score ≥ 50:**
✅ Appears in "High Risk Cases Alert" panel  
✅ Red glowing border on card  
✅ Shows risk level badge  
✅ Displays risk score  

---

## 📋 Test Scenario 8: Security Testing

### Test Case 8.1: Unauthorized Access
**Steps:**
1. Logout completely
2. Try to access `/admin/dashboard` directly
3. Try to access `/investigator/dashboard` directly

**Expected Result:**
❌ Redirect to `/login`  
❌ No data visible  

### Test Case 8.2: Role Restriction
**Steps:**
1. Login as investigator
2. Try to access `/admin/dashboard`

**Expected Result:**
❌ Redirect or error  
❌ Cannot access admin functions  

### Test Case 8.3: Case Ownership
**Steps:**
1. Create second investigator account
2. Try to access first investigator's case

**Expected Result:**
❌ "Unauthorized access" error  
❌ Cannot view other investigator's cases  

### Test Case 8.4: Failed Login Attempts
**Steps:**
1. Logout
2. Try to login with wrong password 5 times

**Expected Result:**
❌ After 5 attempts: "Account locked"  
❌ Cannot login even with correct password  
❌ Must wait 30 minutes or admin must unlock  

---

## 📋 Test Scenario 9: UI/UX Validation

### Visual Checks
✅ **Colors:**
- Background: Very dark (#050714)
- Cards: Dark with blur (#131829)
- Primary accent: Cyan (#00d4ff)
- Secondary: Green (#00ff88)
- Alerts: Red for danger, Yellow for warnings

✅ **Animations:**
- Smooth page transitions
- Button hover effects (glow)
- Card lift on hover
- Loading spinners
- Progress bars animate

✅ **Responsive Design:**
- Test on different browser sizes
- Cards stack properly on mobile
- Sidebar adapts
- Modals center correctly

✅ **Typography:**
- Headings use Inter font
- Hashes use Courier monospace
- Consistent font sizes
- Good contrast ratios

---

## 📋 Test Scenario 10: Error Handling

### Test Case 10.1: Network Errors
**Steps:**
1. Stop backend server
2. Try to login
3. Try to create case

**Expected Result:**
❌ Proper error messages  
❌ No app crashes  
❌ Can recover when backend restarts  

### Test Case 10.2: Invalid Data
**Steps:**
1. Try to analyze case without scraping first

**Expected Result:**
❌ "No data collected yet" error  
❌ Button disabled  

---

## ✅ Testing Checklist

### Functional Testing
- [ ] User registration works
- [ ] Email validation works
- [ ] Password strength validation works
- [ ] Admin approval workflow works
- [ ] Login authentication works
- [ ] JWT token management works
- [ ] Case creation works
- [ ] Data scraping works
- [ ] Data analysis works
- [ ] Risk scoring works
- [ ] Report generation works
- [ ] Logout works

### Security Testing
- [ ] Passwords are hashed
- [ ] JWT tokens are validated
- [ ] Protected routes work
- [ ] Role-based access works
- [ ] Account lockout works
- [ ] Evidence hashing works
- [ ] Audit logs created

### UI/UX Testing
- [ ] All pages load
- [ ] Animations are smooth
- [ ] Colors match theme
- [ ] Fonts are correct
- [ ] Responsive layout works
- [ ] Modals function properly
- [ ] Forms validate input
- [ ] Error messages display
- [ ] Success messages display
- [ ] Loading states show

### Performance Testing
- [ ] Page loads < 3 seconds
- [ ] API responses < 2 seconds
- [ ] Animations are smooth (60fps)
- [ ] No memory leaks
- [ ] No console errors

---

## 🐛 Common Issues & Solutions

### Issue 1: "Cannot connect to MongoDB"
**Solution:**
```bash
# Start MongoDB service
net start MongoDB

# Or check if running
mongod --version
```

### Issue 2: "Module not found"
**Solution:**
```bash
# Backend
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Issue 3: "Port already in use"
**Solution:**
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or change port in app.py
```

### Issue 4: "CORS error"
**Solution:**
- Check backend is running
- Verify CORS config in app.py
- Check frontend proxy in vite.config.js

### Issue 5: "White screen"
**Solution:**
```bash
# Check browser console
# Clear npm cache
npm cache clean --force
npm install
```

---

## 📊 Expected Test Results Summary

| Test Category | Total Tests | Expected Pass |
|--------------|-------------|---------------|
| Authentication | 8 | 8 ✅ |
| Authorization | 5 | 5 ✅ |
| Case Management | 6 | 6 ✅ |
| Data Analysis | 5 | 5 ✅ |
| UI/UX | 12 | 12 ✅ |
| Security | 6 | 6 ✅ |
| Error Handling | 4 | 4 ✅ |
| **TOTAL** | **46** | **46** ✅ |

---

## 🎬 Demo Script (5 Minutes)

**Minute 1:** Landing & Registration
- Show landing page
- Navigate to registration
- Fill form quickly

**Minute 2:** Admin Approval
- Login as admin
- Show dashboard statistics
- Approve new user

**Minute 3:** Create & Scrape
- Login as investigator
- Create new case
- Scrape data
- Show evidence hash

**Minute 4:** Analysis & Results
- Run analysis
- Show risk meter
- Explain each detection
- Highlight high-risk indicators

**Minute 5:** Reporting & Wrap-up
- Generate encrypted report
- Explain security features
- Show audit logs
- Summarize capabilities

---

## 📝 Testing Notes Template

Use this for documenting test results:

```
Test Date: _______________
Tester: __________________
Environment: Local Development

Test Results:
[ ] All pages load correctly
[ ] Authentication works
[ ] Authorization works
[ ] Case workflow complete
[ ] Analysis accurate
[ ] UI matches design
[ ] No console errors
[ ] No security issues

Issues Found:
1. _______________________
2. _______________________

Overall Status: PASS / FAIL

Notes:
_________________________
_________________________
```

---

**READY FOR TESTING** ✅  
**READY FOR DEMONSTRATION** ✅  
**READY FOR SUBMISSION** ✅
