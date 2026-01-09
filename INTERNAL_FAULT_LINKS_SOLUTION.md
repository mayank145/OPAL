# 🔗 Internal Fault Links - Complete Solution

## 🎯 **The Goal**

Allow users to create links to other faults within the FATS system. For example:
- Write: "This is related to Fault #4767"
- Click the link
- Opens Fault #4767 details (not home page!)

---

## 🛠️ **Solution Overview**

We need to:
1. Create a special link format for internal faults: `#fault-4767`
2. Detect when these links are clicked
3. Open the corresponding fault instead of navigating away
4. Make it easy to create these links in the editor

---

## 📋 **Implementation Steps**

### Step 1: Add Link Click Handler to FATSDetailInline

This will intercept clicks on fault links and open the fault details.

### Step 2: Update Link Format

Use a special format like:
- `#fault-4767` → Opens fault 4767
- `https://example.com` → Opens external URL in new tab

### Step 3: Add Helper in MenuBar

Add a button to easily insert fault links.

---

## 💻 **Code Implementation**

### 1. Update FATSDetailInline.js - Add Click Handler

Add this function to handle fault link clicks:

```javascript
// Add this function in FATSDetailInline component
const handleLinkClick = (e) => {
  const target = e.target.closest('a');
  if (!target) return;
  
  const href = target.getAttribute('href');
  
  // Check if it's an internal fault link
  if (href && href.startsWith('#fault-')) {
    e.preventDefault();
    const faultId = href.replace('#fault-', '');
    
    // Call the onViewFATS callback to open the fault
    if (window.handleViewFATS) {
      window.handleViewFATS(parseInt(faultId));
    }
  }
  // External links will open normally with target="_blank"
};

// Add to useEffect
useEffect(() => {
  const container = document.querySelector('.fault-description');
  if (container) {
    container.addEventListener('click', handleLinkClick);
    return () => container.removeEventListener('click', handleLinkClick);
  }
}, []);
```

### 2. Update App.js - Expose handleViewFATS Globally

```javascript
// In App.js, expose the function globally
useEffect(() => {
  window.handleViewFATS = handleViewFATS;
  return () => {
    delete window.handleViewFATS;
  };
}, []);
```

### 3. Update MenuBar.js - Add Fault Link Button

Add a new button to insert fault links easily:

```javascript
import { Tag as TagIcon } from '@mui/icons-material';

// Add this button to MenuBar
<Button
  onClick={() => {
    const faultId = window.prompt('Enter Fault ID (e.g., 4767):');
    if (faultId) {
      const faultNumber = parseInt(faultId);
      if (!isNaN(faultNumber)) {
        editor
          .chain()
          .focus()
          .setLink({ href: `#fault-${faultNumber}` })
          .insertContent(`Fault #${faultNumber}`)
          .run();
      } else {
        alert('Please enter a valid fault ID number');
      }
    }
  }}
  title="Link to Fault"
>
  <TagIcon fontSize="small" />
</Button>
```

---

## 🎨 **Visual Styling**

Make internal fault links look different from external links:

```css
/* Add to FATSDetailInline styles */
'& a[href^="#fault-"]': {
  color: '#d32f2f',  // Red color for internal links
  fontWeight: 'bold',
  textDecoration: 'underline',
  '&::before': {
    content: '"🔗 "',
    fontSize: '0.9em',
  },
  '&:hover': {
    color: '#b71c1c',
    backgroundColor: 'rgba(211, 47, 47, 0.1)',
  }
},
```

---

## 📝 **Usage Guide**

### For Users - How to Link to Another Fault:

**Method 1: Using the Fault Link Button (Recommended)**
1. Click the "Fault Link" button (🏷️) in the editor toolbar
2. Enter the fault ID (e.g., 4767)
3. The link "Fault #4767" is inserted automatically
4. ✅ Clicking it will open Fault #4767

**Method 2: Manual Link**
1. Select text (e.g., "related issue")
2. Click the Link button (🔗)
3. Enter: `#fault-4767`
4. ✅ Clicking it will open Fault #4767

**Method 3: Type and Link**
1. Type: "See Fault #4767"
2. Select "Fault #4767"
3. Click Link button
4. Enter: `#fault-4767`
5. ✅ Done!

---

## 🔍 **Link Format Reference**

| Link Type | Format | Example | Opens |
|-----------|--------|---------|-------|
| **Internal Fault** | `#fault-{id}` | `#fault-4767` | Fault 4767 details |
| **External URL** | `https://...` | `https://google.com` | External site (new tab) |
| **Email** | `mailto:...` | `mailto:eric@subaru.org` | Email client |

---

## ✅ **Expected Behavior**

### Internal Fault Links:
```
User clicks "Fault #4767" → 
  Detects #fault-4767 → 
  Opens Fault 4767 in new tab → 
  ✅ Fault details displayed
```

### External Links:
```
User clicks "Google" (https://google.com) → 
  Opens in new tab → 
  ✅ External site
```

---

## 🧪 **Testing Checklist**

- [ ] Create a fault with text "Related to Fault #4767"
- [ ] Add link `#fault-4767` to that text
- [ ] Save the fault
- [ ] View the fault
- [ ] Click the link
- [ ] ✅ **Expected**: Opens Fault #4767 in new tab
- [ ] ✅ **Expected**: Link appears in red with 🔗 icon

---

## 🎯 **Complete Code Files**

I'll create the complete updated files for you. Would you like me to:
1. ✅ Update all the files with the complete solution
2. ✅ Test it locally
3. ✅ Commit and push

Let me know and I'll implement this properly!


