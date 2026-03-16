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
    
    # ---------------------------------------------------------
    # PHASE 1: THE HOOK & CORE OFFER (Day 1)
    # Focus: The missing button & $0 hosting offer.
    # ---------------------------------------------------------
    if phase == 1:
        subject = parse_spintax("{Quick question|Important note|Inquiry} regarding [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; color: #1a1a1a;">
            <div style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e1e4e8;">
                <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 30px 20px; text-align: center;">
                    <h1 style="color: #2dd4bf; margin: 0; font-size: 24px; text-transform: uppercase; letter-spacing: 2px;">STOP WEB RENT</h1>
                </div>
                <div style="padding: 30px;">
                    <h2 style="color: #0f172a; font-size: 20px; margin-top: 0;">{greeting} {name} team,</h2>
                    <p style="font-size: 16px; line-height: 1.6; color: #475569;">
                        I was researching <strong>{category}</strong> services in <strong>{address}</strong> and noticed your clinic has an outstanding reputation. However, you are currently missing a critical asset: <strong>A "Website" button on your Google Maps profile.</strong>
                    </p>
                    <p style="font-size: 16px; line-height: 1.6; color: #475569;">
                        We deploy <strong>0.1s Load Speed</strong> frameworks that are unhackable and cost <strong>$0 in monthly hosting fees</strong>.
                    </p>
                    <div style="background-color: #f8fafc; padding: 15px; border-left: 4px solid #0d9488; margin: 25px 0;">
                        <strong>Exclusive Offer:</strong> I will use your current logo and clinic photos to build a live demo. If you don't love the performance, you pay nothing.
                    </div>
                    <a href="https://wa.me/966572562151?text=YES" style="background-color: #0d9488; color: #ffffff; padding: 14px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">REPLY 'YES' ON WHATSAPP FOR FREE DEMO</a>
                </div>
            </div>
        </body>
        </html>
        """
        days_to_next = 3 # Wait 3 days before Phase 2

    # ---------------------------------------------------------
    # PHASE 2: THE QUICK BUMP (Day 4)
    # Focus: Simple, text-based follow-up to bump the previous email.
    # ---------------------------------------------------------
    elif phase == 2:
        subject = f"Re: {name} + Titan Engine"
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #333333; line-height: 1.6;">
            <p>{greeting} again,</p>
            <p>I’m floating this to the top of your inbox. Did you know that local {category} businesses without linked websites lose up to <strong>40% of map traffic</strong> to competitors?</p>
            <p>I have capacity to build 2 free demos this week. Would you like {name} to be one of them? Just reply "YES" to this email.</p>
            <p>Best,<br>Kiran</p>
        </body>
        </html>
        """
        days_to_next = 4 # Wait 4 days before Phase 3

    # ---------------------------------------------------------
    # PHASE 3: THE FINANCIAL LOGIC / STOP WEB RENT (Day 8)
    # Focus: The Math. Wix vs Titan.
    # ---------------------------------------------------------
    elif phase == 3:
        subject = parse_spintax("{How to save|Stop wasting} $2,000+ on {Category} web hosting")
        html = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #1a1a1a;">
            <div style="max-width: 600px; margin: 20px auto; padding: 20px;">
                <p style="font-size: 16px;">{greeting},</p>
                <p style="font-size: 16px;">Most clinics I speak to in {address} are trapped paying "Web Rent" — monthly fees to Wix, Squarespace, or Shopify that add up to thousands over a few years.</p>
                
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0; border: 1px solid #e2e8f0;">
                    <tr style="background-color: #f8fafc;">
                        <th style="padding: 10px; text-align: left;">5-Year Cost Comparison</th>
                        <th style="padding: 10px; color: #0d9488;">Titan Engine</th>
                        <th style="padding: 10px;">Wix/Shopify</th>
                    </tr>
                    <tr>
                        <td style="padding: 10px; border-top: 1px solid #e2e8f0;">Total Cost</td>
                        <td style="padding: 10px; border-top: 1px solid #e2e8f0; font-weight: bold; color: #0d9488;">$274</td>
                        <td style="padding: 10px; border-top: 1px solid #e2e8f0;">$2,115+</td>
                    </tr>
                </table>
                <p style="font-size: 16px;">Why pay rent when you can own your digital asset outright? <a href="https://kiranmondal.gumroad.com/l/titanv50" style="color: #0d9488;">See how the Titan Engine works here.</a></p>
            </div>
        </body>
        </html>
        """
        days_to_next = 5 # Wait 5 days before Phase 4

    # ---------------------------------------------------------
    # PHASE 4: THE FOMO & AI ANGLE (Day 13)
    # Focus: The 2026 Ranking Risk. Urgency.
    # ---------------------------------------------------------
    elif phase == 4:
        subject = parse_spintax("The 2026 Google update & [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #333333; line-height: 1.6;">
            <p>{greeting},</p>
            <p>I wanted to share a quick warning regarding your Google Maps listing for {name}.</p>
            <div style="background-color: #fff1f2; border-left: 4px solid #f43f5e; padding: 15px; margin: 15px 0;">
                <strong>The 2026 AI Algorithm Shift:</strong> Google is rapidly prioritizing businesses with ultra-fast, linked websites. Profiles with missing "Website" buttons are gradually being pushed down the search results.
            </div>
            <p>Our 0.1s load speed architecture is specifically designed to signal high trust to Google's AI. Should I go ahead and build a preview for you so you can see the speed yourself?</p>
            <p>Best,<br>Kiran</p>
        </body>
        </html>
        """
        days_to_next = 5 # Wait 5 days before Phase 5

    # ---------------------------------------------------------
    # PHASE 5: RISK REVERSAL (Day 18)
    # Focus: Removing all friction. It requires 0 effort from them.
    # ---------------------------------------------------------
    elif phase == 5:
        subject = f"Free 24-hour build for {name} (No strings)"
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #333333; line-height: 1.6;">
            <p>{greeting},</p>
            <p>I know as a business owner in {address}, your time is limited. You probably haven't set up a website because of the time it takes to write copy, find photos, and deal with developers.</p>
            <p><strong>Here is my guarantee:</strong></p>
            <ul>
                <li>You don't need to write a single word.</li>
                <li>You don't need to provide photos (I'll use what's on your Google listing).</li>
                <li>You get a live link in 24 hours.</li>
            </ul>
            <p>If you don't like it, we scrap it. No hard feelings. <a href="https://wa.me/966572562151" style="color: #0d9488;">Message me on WhatsApp to start.</a></p>
        </body>
        </html>
        """
        days_to_next = 6 # Wait 6 days before Phase 6

    # ---------------------------------------------------------
    # PHASE 6: THE FOUNDER'S NOTE (Day 24)
    # Focus: Stripped down, plain-text feel. Highly personal.
    # ---------------------------------------------------------
    elif phase == 6:
        subject = "am I off base here?"
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #333333; line-height: 1.6;">
            <p>{greeting},</p>
            <p>I've reached out a few times about getting {name} set up with a proper web engine to avoid the high monthly fees of standard builders.</p>
            <p>Am I totally off base here, or is this just a bad time of year for you?</p>
            <p>Either way, just let me know so I can update my notes.</p>
            <p>- Kiran</p>
        </body>
        </html>
        """
        days_to_next = 5 # Wait 5 days before Phase 7

    # ---------------------------------------------------------
    # PHASE 7: THE BREAKUP (Day 29)
    # Focus: Professional exit, leaving the door open.
    # ---------------------------------------------------------
    elif phase == 7:
        subject = parse_spintax("{Closing your file|Last email} regarding [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #1a1a1a;">
            <div style="max-width: 600px; margin: 20px auto; padding: 20px;">
                <p style="font-size: 16px;">{greeting},</p>
                <p style="font-size: 16px;">Since I haven't heard back, I'm going to assume that upgrading your digital footprint isn't a priority for {name} right now, so this will be my last email.</p>
                <p style="font-size: 16px;">If you ever get tired of losing map traffic to other {category} clinics, or if you just want to stop paying monthly web rent, you know where to find me.</p>
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; font-size: 13px; color: #64748b;">
                    <strong>Kiran Deb Mondal</strong><br>
                    Principal Business Technologist | Stop Web Rent<br>
                    <a href="https://www.StopWebRent.com" style="color: #0d9488;">www.StopWebRent.com</a> | <a href="https://kiranmondal.gumroad.com/l/titanv50" style="color: #0d9488;">Direct Purchase Link</a>
                </div>
            </div>
        </body>
        </html>
        """
        days_to_next = 0 # Campaign Ends Here

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
