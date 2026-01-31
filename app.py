import streamlit as st
import httpx
from typing import Optional

# Page configuration
st.set_page_config(
    page_title="Task Manager",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL
API_BASE_URL = "http://localhost:8000"

# Custom CSS for colorful styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #FFA07A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    /* Red delete button styling - targets buttons with delete in key */
    div[data-testid*="delete"] button {
        background-color: #FF4444 !important;
        color: white !important;
        border-color: #FF4444 !important;
    }
    div[data-testid*="delete"] button:hover {
        background-color: #CC0000 !important;
        border-color: #CC0000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📋 Task Manager Dashboard</h1>', unsafe_allow_html=True)

# Helper function to make API calls
def api_get(endpoint: str):
    """Make GET request to API"""
    try:
        response = httpx.get(f"{API_BASE_URL}{endpoint}", timeout=5.0)
        response.raise_for_status()
        return response.json(), None
    except httpx.RequestError as e:
        return None, f"Connection error: {str(e)}"
    except httpx.HTTPStatusError as e:
        return None, f"HTTP error: {e.response.status_code} - {e.response.text}"

def api_post(endpoint: str, data: dict):
    """Make POST request to API"""
    try:
        response = httpx.post(f"{API_BASE_URL}{endpoint}", json=data, timeout=5.0)
        response.raise_for_status()
        return response.json(), None
    except httpx.RequestError as e:
        return None, f"Connection error: {str(e)}"
    except httpx.HTTPStatusError as e:
        return None, f"HTTP error: {e.response.status_code} - {e.response.text}"

def api_patch(endpoint: str, data: dict):
    """Make PATCH request to API"""
    try:
        response = httpx.patch(f"{API_BASE_URL}{endpoint}", json=data, timeout=5.0)
        response.raise_for_status()
        return response.json(), None
    except httpx.RequestError as e:
        return None, f"Connection error: {str(e)}"
    except httpx.HTTPStatusError as e:
        return None, f"HTTP error: {e.response.status_code} - {e.response.text}"

def api_delete(endpoint: str):
    """Make DELETE request to API"""
    try:
        response = httpx.delete(f"{API_BASE_URL}{endpoint}", timeout=5.0)
        response.raise_for_status()
        return response.json(), None
    except httpx.RequestError as e:
        return None, f"Connection error: {str(e)}"
    except httpx.HTTPStatusError as e:
        return None, f"HTTP error: {e.response.status_code} - {e.response.text}"

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["👤 Create User", "👥 View Users", "➕ Create Task", "📝 View Tasks"])
# Tab 1: Create User
with tab1:
    st.header("Create New User", divider="rainbow")
    
    with st.form("create_user_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name *", placeholder="Enter user name")
            role = st.selectbox("Role *", ["admin", "manager", "team member"], help="Select user role")
            email = st.text_input("Email *", placeholder="user@example.com")
        
        with col2:
            phone = st.text_input("Phone", placeholder="+1234567890 (optional)")
            st.markdown("---")
            st.markdown("**Profile Information**")
            st.info("Fill in the user details above")
        
        submit_button = st.form_submit_button("✨ Create User", type="primary", use_container_width=True)
        
        if submit_button:
            if not name or not email:
                st.error("❌ Name and Email are required fields!")
            else:
                # الحقول داخل profile كما يتطلب الـ API
                user_data = {
                    "name": name,
                    "role": role,
                    "profile": {
                        "email": email,
                        "phone": phone if phone else None
                    }
                }
                
                with st.spinner("Creating user..."):
                    result, error = api_post("/users/", user_data)
                
                if error:
                    st.error(f"❌ Error: {error}")
                else:
                    st.success(f"✅ User created successfully! ID: {result['id']}")
                    st.balloons()
                    st.json(result)



# Tab 2: View Users
with tab2:
    st.header("All Users", divider="rainbow")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Refresh", type="primary", key="refresh_users"):
            st.rerun()
    
    with st.spinner("Loading users..."):
        users, error = api_get("/users/")
    
    if error:
        st.error(f"❌ Error: {error}")
    elif users:
        st.success(f"✅ Found {len(users)} user(s)")
        
        # Display users in colorful cards
        for user in users:
            role_colors = {
                "admin": "🔴",
                "manager": "🔵",
                "team member": "🟢"
            }
            role_emoji = role_colors.get(user.get("role", ""), "⚪")
            
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 2])
                with col1:
                    st.markdown(f"### {role_emoji} ID: {user.get('id', '-')}")
                with col2:
                    st.markdown(f"**Name:** {user.get('name', '-')}")
                    st.markdown(f"**Role:** {user.get('role', '-')}")
                with col3:
                    profile = user.get('profile', {})
                    email = profile.get('email') or user.get('email', 'N/A')
                    phone = profile.get('phone') or user.get('phone', None)
                    st.markdown(f"**Email:** {email}")
                    if phone:
                        st.markdown(f"**Phone:** {phone}")
                st.divider()
    else:
        st.info("📭 No users found. Create your first user in the 'Create User' tab!")


# Tab 3: Create Task
with tab3:
    st.header("Create New Task", divider="rainbow")
    
    # Get users for assignment dropdown
    users_data, _ = api_get("/users/")
    user_options = {0: "None"}
    if users_data:
        user_options.update({user["id"]: f"{user['name']} (ID: {user['id']})" for user in users_data})
    
    with st.form("create_task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title *", placeholder="Task title (must start with capital letter)", 
                                help="⚠️ Title must be capitalized!")
            description = st.text_area("Description *", placeholder="Enter task description", height=100)
            priority = st.selectbox("Priority *", ["low", "medium", "high"], 
                                  help="Select task priority level")
        
        with col2:
            status = st.text_input("Status *", placeholder="e.g., pending, in_progress, completed")
            assigned_to = st.selectbox("Assigned To", list(user_options.keys()), 
                                     format_func=lambda x: user_options[x],
                                     help="Select user to assign this task")
            st.markdown("---")
            st.warning("⚠️ Remember: Task title must start with a capital letter!")
        
        submit_button = st.form_submit_button("✨ Create Task", type="primary", use_container_width=True)
        
        if submit_button:
            if not title or not description or not status:
                st.error("❌ Title, Description, and Status are required fields!")
            elif not title[0].isupper():
                st.error("❌ Title must start with a capital letter!")
            else:
                task_data = {
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "status": status,
                    "assigned_to": assigned_to if assigned_to != 0 else None
                }
                
                with st.spinner("Creating task..."):
                    result, error = api_post("/tasks/", task_data)
                
                if error:
                    st.error(f"❌ Error: {error}")
                else:
                    st.success(f"✅ Task created successfully! ID: {result['id']}")
                    st.balloons()
                    st.json(result)

# Tab 4: View Tasks
with tab4:
    st.header("All Tasks", divider="rainbow")
    
    # Get all users once for mapping assigned_to -> name
    users_data, _ = api_get("/users/")
    user_map = {user["id"]: user["name"] for user in users_data} if users_data else {}
    
    # Filter section
    with st.expander("🔍 Filter Tasks", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_status = st.text_input("Filter by Status", placeholder="e.g., pending")
        with col2:
            filter_priority = st.selectbox("Filter by Priority", [None, "low", "medium", "high"])
        with col3:
            filter_assigned = st.number_input("Filter by Assigned User ID", min_value=0, value=0, step=1)
        
        filter_assigned = filter_assigned if filter_assigned > 0 else None
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Refresh", type="primary", key="refresh_tasks"):
            st.rerun()
    
    # Build query parameters
    params = {}
    if filter_status:
        params["status"] = filter_status
    if filter_priority:
        params["priority"] = filter_priority
    if filter_assigned:
        params["assigned_to"] = filter_assigned
    
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    endpoint = f"/tasks/?{query_string}" if query_string else "/tasks/"
    
    with st.spinner("Loading tasks..."):
        tasks, error = api_get(endpoint)
    
    if error:
        st.error(f"❌ Error: {error}")
    elif tasks:
        st.success(f"✅ Found {len(tasks)} task(s)")
        
        # Display tasks in colorful cards
        for task in tasks:
            # Color code by priority
            priority_colors = {
                "low": "🟢",
                "medium": "🟡",
                "high": "🔴"
            }
            priority_emoji = priority_colors.get(task["priority"], "⚪")
            
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
                
                with col1:
                    st.markdown(f"### {priority_emoji} ID: {task['id']}")
                
                with col2:
                    st.markdown(f"**Title:** {task['title']}")
                    st.markdown(f"**Description:** {task['description']}")
                    st.markdown(f"**Priority:** {task['priority']}")
                
                with col3:
                    # Status change dropdown
                    new_status = st.selectbox(
                        "Status",
                        ["pending", "in_progress", "completed", "on_hold", "cancelled"],
                        index=["pending", "in_progress", "completed", "on_hold", "cancelled"].index(task['status']) if task['status'] in ["pending", "in_progress", "completed", "on_hold", "cancelled"] else 0,
                        key=f"status_{task['id']}",
                        label_visibility="visible"
                    )
                    if new_status != task['status']:
                        if st.button("🔄 Update Status", key=f"update_status_{task['id']}", type="secondary"):
                            with st.spinner("Updating status..."):
                                result, error = api_patch(f"/tasks/{task['id']}/status?status_update={new_status}", {})
                            if error:
                                st.error(f"❌ {error}")
                            else:
                                st.success("✅ Status updated!")
                                st.rerun()
                    
                    # Show assigned user name instead of ID
                    assigned_user_name = user_map.get(task.get('assigned_to'), "Not assigned")
                    st.markdown(f"**Assigned To:** {assigned_user_name}")
                
                with col4:
                    # Delete button with red styling
                    st.markdown("<br>", unsafe_allow_html=True)  # Spacing
                    delete_key = f"delete_{task['id']}"
                    if st.button("❌ Delete", key=delete_key, help="Delete this task", type="primary"):
                        with st.spinner("Deleting task..."):
                            result, error = api_delete(f"/tasks/{task['id']}")
                        if error:
                            st.error(f"❌ {error}")
                        else:
                            st.success("✅ Task deleted!")
                            st.rerun()
                
                st.divider()
    else:
        st.info("📭 No tasks found. Create your first task in the 'Create Task' tab!")

# Sidebar with API status
with st.sidebar:
    st.header("🔌 API Status")
    
    if st.button("Check Connection", key="check_connection"):
        with st.spinner("Checking..."):
            result, error = api_get("/")
        if error:
            st.error("❌ API not reachable")
            st.error(error)
        else:
            st.success("✅ API connected!")
            st.json(result)
    
    st.markdown("---")
    st.markdown("### 📚 API Endpoints")
    st.code("GET  /users/")
    st.code("POST /users/")
    st.code("GET  /tasks/")
    st.code("POST /tasks/")
    
    st.markdown("---")
    st.info("💡 Make sure the FastAPI server is running on http://localhost:8000")
