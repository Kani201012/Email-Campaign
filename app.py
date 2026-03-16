import streamlit as st
import pandas as pd
import smtplib
import time
import random
import re
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Stop Web Rent | Titan Engine", page_icon="🛡️", layout="wide")

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def init_connection():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    return gspread.authorize(credentials)

gc = init_connection()

# --- SPINTAX PARSER ---
def parse_spintax(text):
    pattern = re.compile(r'\{([^{}]*)\}')
    while True:
        match = pattern.search(text)
        if not match: break
        options = match.group(1).split('|')
        text = text[:match.start()] + random.choice(options) + text[match.end():]
    return text

# --- 7-PHASE TEMPLATE ENGINE ---
def get_campaign_content(phase, name, category, address):
    """Returns the Subject, HTML Body, and Days until next phase."""
    
    greeting = random.choice(["Hi", "Hello", "Greetings", "Hey"])
    
    # PHASE 1: The Hook & The Problem (Your original template)
    if phase == 1:
        subject = parse_spintax("{Quick question|Important note|Inquiry} regarding [Name]").replace("[Name]", name)
        html = f"""
        <html><body style="font-family: Arial, sans-serif; color: #1a1a1a;">
            <h2>{greeting} {name} team,</h2>
            <p>I was researching <strong>{category}</strong> services in <strong>{address}</strong> and noticed your clinic has an outstanding reputation. However, you are currently missing a critical asset: <strong>A "Website" button on your Google Maps profile.</strong></p>
            <p>We deploy <strong>0.1s Load Speed</strong> frameworks that cost <strong>$0 in monthly hosting fees</strong>.</p>
            <p><a href="https://wa.me/966572562151?text=YES">REPLY 'YES' FOR FREE DEMO</a></p>
        </body></html>
        """
        days_to_next = 3 # Wait 3 days before sending Phase 2
        
    # PHASE 2: The Value Add / Quick Follow-up
    elif phase == 2:
        subject = f"Re: {name} + Titan Engine"
        html = f"""
        <html><body style="font-family: Arial, sans-serif; color: #1a1a1a;">
            <p>{greeting} again,</p>
            <p>I wanted to float this to the top of your inbox. Did you know that clinics without websites lose up to 40% of map traffic?</p>
            <p>Let me build you a free 24-hour demo to show you how our Titan Architecture fixes this instantly.</p>
        </body></html>
        """
        days_to_next = 3
        
    # PHASE 3: Case Study / Social Proof
    elif phase == 3:
        subject = parse_spintax("{Case Study|Quick Example}: $0 hosting fees")
        html = f"<p>{greeting}, just wanted to share how another {category} business saved $2,000/year using our framework...</p>"
        days_to_next = 4
        
    # Add Phases 4, 5, 6 here following the same pattern...
    
    # PHASE 7: The Breakup Email
    elif phase == 7:
        subject = "Closing your file"
        html = f"<p>{greeting}, I haven't heard back so I'll assume {name} isn't looking to upgrade your digital footprint right now. If things change, you know where to find me!</p>"
        days_to_next = 0 # End of campaign
        
    else:
        return None, None, 0

    return subject, html, days_to_next

# --- UI & DASHBOARD ---
st.title("🛡️ Titan Engine v2.0 | 7-Phase Campaign Manager")
st.markdown("Automated Lead Routing, Scheduling, and Delivery")

with st.expander("⚙️ Server Configurations", expanded=False):
    col1, col2, col3 = st.columns(3)
    smtp_user = col1.text_input("Workspace Email", value="kiran@kaydiemscriptlab.com")
    smtp_pass = col2.text_input("App Password", type="password")
    sheet_url = col3.text_input("Google Sheet URL")
    
    col4, col5 = st.columns(2)
    daily_limit = col4.number_input("Max Emails to Send Today", value=40, max_value=200)
    delay_sec = col5.slider("Delay between emails (seconds)", 10, 120, 60)

if sheet_url:
    try:
        sh = gc.open_by_url(sheet_url)
        worksheet = sh.sheet1
        df = pd.DataFrame(worksheet.get_all_records())
        
        # Dashboard Metrics
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        # Filter logic: Which leads are ready to receive an email today?
        def is_due(row):
            if row.get('Campaign_Status') in ['Replied', 'Bounced', 'Unsubscribed', 'Completed']:
                return False
            next_date = str(row.get('Next_Send_Date', '')).strip()
            if not next_date: # Never sent before
                return True
            return next_date <= today_str # Date is today or in the past
            
        due_leads = df[df.apply(is_due, axis=1)]
        
        st.divider()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Leads in DB", len(df))
        m2.metric("Pending/Due Today", len(due_leads))
        m3.metric("Replied/Stopped", len(df[df['Campaign_Status'] == 'Replied']))
        m4.metric("Completed 7 Phases", len(df[df['Campaign_Status'] == 'Completed']))

        if len(due_leads) > 0:
            st.info(f"🎯 Found {len(due_leads)} leads ready for their next sequence.")
            
            if st.button("🚀 IGNITE TITAN CAMPAIGN", type="primary", use_container_width=True):
                
                # SMTP Setup
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(smtp_user, smtp_pass)
                
                # Get Column Indexes for updating
                headers = [h.strip() for h in worksheet.row_values(1)]
                idx_status = headers.index("Campaign_Status") + 1
                idx_phase = headers.index("Current_Phase") + 1
                idx_date = headers.index("Next_Send_Date") + 1
                
                sent_count = 0
                progress_bar = st.progress(0)
                status_text = st.empty()

                for index, row in due_leads.iterrows():
                    if sent_count >= daily_limit:
                        break
                        
                    email = str(row.get('Email', '')).strip()
                    name = str(row.get('Business Name', 'Clinic')).strip()
                    cat = str(row.get('Category', 'Dental')).strip()
                    addr = str(row.get('Address', 'your area')).strip()
                    current_phase = int(row.get('Current_Phase') or 0)
                    
                    if "@" not in email:
                        continue
                        
                    # Calculate next phase
                    target_phase = current_phase + 1
                    if target_phase > 7:
                        worksheet.update_cell(index + 2, idx_status, "Completed")
                        continue

                    # Get Content for this specific phase
                    subject, html_content, days_to_next = get_campaign_content(target_phase, name, cat, addr)
                    
                    if not subject:
                        continue

                    # Send Email
                    msg = MIMEMultipart()
                    msg['From'] = f"Kiran Deb Mondal <{smtp_user}>"
                    msg['To'] = email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(html_content, 'html'))
                    
                    try:
                        server.send_message(msg)
                        
                        # Calculate next send date
                        next_date_str = (datetime.now() + timedelta(days=days_to_next)).strftime("%Y-%m-%d")
                        new_status = "Completed" if target_phase == 7 else "Active"
                        
                        # Update Google Sheet
                        worksheet.update_cell(index + 2, idx_phase, target_phase)
                        worksheet.update_cell(index + 2, idx_date, next_date_str)
                        worksheet.update_cell(index + 2, idx_status, new_status)
                        
                        sent_count += 1
                        
                        # Update UI visually without crashing
                        progress_bar.progress(sent_count / daily_limit)
                        status_text.write(f"✅ Sent Phase {target_phase} to {name} ({email}) | Next: {next_date_str}")
                        
                        # Only sleep if we haven't hit the limit yet
                        if sent_count < daily_limit:
                            time.sleep(delay_sec)
                            
                    except Exception as e:
                        st.error(f"❌ Failed for {email}: {str(e)}")

                server.quit()
                st.success(f"🎉 Campaign run complete! {sent_count} emails processed.")
                st.balloons()
        else:
            st.success("✅ All caught up! No emails are scheduled to go out today.")
            
    except Exception as e:
        st.error(f"Critical Error: {e}")
