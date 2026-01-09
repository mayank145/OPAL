# 🧪 Internal Fault Links - Testing Guide

## ✅ Servers Running Successfully!

### Backend
- **URL**: http://localhost:8000
- **Status**: ✅ Connected to production database
- **Health**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs

### Frontend
- **URL**: http://localhost:3000
- **Status**: ✅ Compiled and running

---

## 🎯 How to Test Internal Fault Links

### Step 1: Open the Application
Open your browser and go to: **http://localhost:3000**

You should see the FATS list with recent entries.

---

### Step 2: Create or Edit a Fault

**Option A: Edit an Existing Fault**
1. Click on Fault #4772 (or any other fault)
2. Click the **Edit** button

**Option B: Create a New Fault**
1. Click "Create New FATS Entry" button

---

### Step 3: Add an Internal Fault Link

Look for the **🏷️ (Tag icon)** button in the editor toolbar (it's next to the 🔗 link button).

#### **Method 1: Using the 🏷️ Button (Easiest)**
1. Click the **🏷️** button
2. Enter a fault ID: `4772` (or `4771`, `4754`, `4751`, `4750`)
3. ✅ It will insert: `🔗 Fault #4772`

#### **Method 2: Manual Link**
1. Type some text (e.g., "Related to previous issue")
2. Select the text
3. Click the **🔗** (Link) button
4. Enter: `#fault-4772`
5. ✅ Done!

---

### Step 4: Save the Fault
Click "Save" or "Update" button

---

### Step 5: Test the Link
1. View the fault you just saved
2. You should see the link styled in **RED** with a **🔗** icon
3. **Click the link**
4. ✅ **Expected**: It should open Fault #4772 in a new tab
5. ❌ **If it goes to home page**: Report the error

---

## 🎨 Visual Indicators

### In the Editor Toolbar:
```
Bold | Italic | Underline | Strike | 🔗 Link | 🏷️ Link to Fault | 🖼️ Image
```

### How Links Should Look:

**Internal Fault Link:**
```
🔗 Fault #4772
```
- **Color**: Red
- **Icon**: 🔗
- **Hover**: Light red background

**External Link:**
```
Google ↗
```
- **Color**: Blue
- **Icon**: ↗ (arrow)

---

## 📊 Test Scenarios

### Scenario 1: Link to Specific Fault
1. Edit a fault
2. Add link: `#fault-4772`
3. Save
4. Click link
5. ✅ Opens Fault #4772

### Scenario 2: Multiple Links
1. Add multiple fault links in one description
2. Example: "See 🔗 Fault #4772 and 🔗 Fault #4771"
3. Save
4. Click each link
5. ✅ Each opens the correct fault

### Scenario 3: Mix Internal and External Links
1. Add both internal and external links
2. Example: "Check 🔗 Fault #4772 and visit Google ↗"
3. Save
4. Click each link
5. ✅ Internal opens fault, external opens website

---

## 🐛 Troubleshooting

### Problem: 🏷️ button is missing
**Solution**: Hard refresh the page (Ctrl+Shift+R or Cmd+Shift+R)

### Problem: Links still go to home page
**Possible causes**:
1. JavaScript error in console
2. Format is wrong (missing `#` symbol)
3. Cache issue

**Solutions**:
1. Open browser console (F12) and check for errors
2. Make sure link format is exactly: `#fault-4772`
3. Clear browser cache and refresh

### Problem: Links not appearing red
**Solution**: 
1. Hard refresh (Ctrl+Shift+R)
2. Clear browser cache
3. Check if CSS loaded properly

---

## 📝 Test Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Can see fault list
- [ ] Can open a fault
- [ ] Can see 🏷️ button in editor
- [ ] Can click 🏷️ and enter fault ID
- [ ] Link appears in red with 🔗 icon
- [ ] Clicking link opens correct fault
- [ ] Link does NOT go to home page
- [ ] Works in both Issue and Solution sections
- [ ] Multiple links work correctly
- [ ] External links still work (blue with ↗)

---

## 🔍 Database Information

**Current Setup:**
- Database: MariaDB on `opalfailover.subaru.nao.ac.jp:3306`
- Available Faults: 4772, 4771, 4754, 4751, 4750
- Tables: fault, fcomments, fsection, fstaff, fats_images

---

## 🚀 Next Steps

1. ✅ Test the feature locally
2. ✅ Verify all scenarios work
3. ✅ Push changes to GitHub
4. ✅ Deploy to production
5. ✅ Test on production server

---

## 📌 Important Notes

- The **🏷️** button is specifically for linking to OTHER faults in the system
- The **🔗** button is for general links (external URLs or manual fault links)
- Internal fault links use format: `#fault-XXXX` (e.g., `#fault-4772`)
- External links use standard URLs: `https://example.com`
- All links are styled differently for easy identification

---

**Ready to test! Open http://localhost:3000 and try it out!** 🎉


