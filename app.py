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
def get_campaign_content(phase, name, category, address, contact_name="Team"):
    """Returns the Subject, HTML Body, and Days until next phase."""
    
    greeting = random.choice(["Hi", "Hello", "Greetings", "Dear"])
    
    # ---------------------------------------------------------
    # PHASE 1: THE HOOK & THE OFFER (Day 1)
    # Goal: Get a "YES" to the free demo. Keep it short.
    # ---------------------------------------------------------
    if phase == 1:
        subject = parse_spintax("{Missing link|Google Maps error|Quick question} regarding [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting} {contact_name},</p>
            <p>I was researching <strong>{category}</strong> clinics in <strong>{address}</strong> and noticed your practice has a fantastic reputation. However, you are missing a critical asset: <strong>a "Website" button on your Google Maps profile.</strong></p>
            <p>Every day without that button, Google’s algorithm pushes you down the rankings, handing high-value patients to your competitors.</p>
            <p>I build 0.1s High-Velocity websites specifically for healthcare clinics. <strong>Unlike Wix or Shopify, I charge $0 in monthly hosting fees.</strong></p>
            <div style="background-color: #f8fafc; padding: 15px; border-left: 4px solid #0d9488; margin: 20px 0;">
                <strong>My Offer: A Free 24-Hour Preview</strong><br>
                I will use your current logo and photos to build a live demo. If you don't love the performance, you pay nothing.
            </div>
            <p>Reply <strong>"YES"</strong> to this email (or <a href="https://wa.me/966572562151" style="color: #0d9488; font-weight: bold;">message me on WhatsApp here</a>), and I'll send you a private link to review your new site.</p>
            <p>Best regards,<br><strong>Kiran Deb Mondal</strong><br>Principal Technologist | Stop Web Rent</p>
        </body>
        </html>
        """
        days_to_next = 3

    # ---------------------------------------------------------
    # PHASE 2: VISUAL PROOF & WHATSAPP INTEGRATION (Day 4)
    # Goal: Highlight the features seen in your demo video.
    # ---------------------------------------------------------
    elif phase == 2:
        subject = f"Re: {name} digital preview"
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting} again,</p>
            <p>I wanted to follow up on my last email. When I build a Titan Engine site for a clinic like {name}, it's not just a digital brochure—it's a lead generation machine.</p>
            <p><strong>Here is what your custom site will include:</strong></p>
            <ul>
                <li><strong>WhatsApp Booking:</strong> Patients can book appointments or chat with your reception desk in one tap.</li>
                <li><strong>Multilingual Support:</strong> Instantly translates to Hindi, Bengali, Spanish, French, etc.</li>
                <li><strong>Mobile-First Design:</strong> Looks and feels like a native app on your patients' phones.</li>
            </ul>
            <p><a href="https://dental-junction-behala.github.io/index.html" style="color: #0d9488; font-weight: bold;">You can click here to play with a live demo of a clinic we recently built.</a></p>
            <p>Would you like me to build a custom prototype for {name}? Just reply "YES".</p>
            <p>- Kiran</p>
        </body>
        </html>
        """
        days_to_next = 4

    # ---------------------------------------------------------
    # PHASE 3: THE FINANCIAL MATH (Day 8)
    # Goal: Use the pricing table from your PDF to show the $1,841 savings.
    # ---------------------------------------------------------
    elif phase == 3:
        subject = parse_spintax("{Stop paying|How to save $1,800 on} website rent")
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting} {contact_name},</p>
            <p>Most business owners are trapped paying "Web Rent"—$30 to $50 every single month to Wix, Shopify, or WordPress just to keep their site online.</p>
            <p>The Titan Engine changes that. <strong>Pay a $199 one-time setup fee, and own the asset forever.</strong></p>
            
            <table style="width: 100%; max-width: 500px; border-collapse: collapse; margin: 20px 0; border: 1px solid #e2e8f0; text-align: left;">
                <tr style="background-color: #f8fafc;">
                    <th style="padding: 10px; border-bottom: 2px solid #e2e8f0;">5-Year Cost</th>
                    <th style="padding: 10px; border-bottom: 2px solid #e2e8f0; color: #0d9488;">Titan Engine</th>
                    <th style="padding: 10px; border-bottom: 2px solid #e2e8f0;">Wix / Shopify</th>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">Setup Fee</td>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: bold;">$199 (Once)</td>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">$0</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">Hosting/Rent</td>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: #0d9488;">$0</td>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;">$1,740</td>
                </tr>
                <tr style="background-color: #fff1f2;">
                    <td style="padding: 10px; font-weight: bold;">Total Cost</td>
                    <td style="padding: 10px; font-weight: bold; color: #0d9488;">$274 (incl. domain)</td>
                    <td style="padding: 10px; font-weight: bold; color: #e11d48;">$2,115</td>
                </tr>
            </table>
            
            <p>That is <strong>$1,841 in savings</strong>. If you want to stop renting and start owning, let's chat. <a href="https://wa.me/966572562151" style="color: #0d9488;">WhatsApp me here.</a></p>
            <p>- Kiran</p>
        </body>
        </html>
        """
        days_to_next = 4

    # ---------------------------------------------------------
    # PHASE 4: THE GOOGLE SHEET CMS (Day 12)
    # Goal: Remove the "tech barrier". Dentists hate complex dashboards.
    # ---------------------------------------------------------
    elif phase == 4:
        subject = parse_spintax("Update {name} website using Excel?")
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting},</p>
            <p>One of the main reasons clinics don't build websites is because they don't want to learn complex dashboards or pay a web developer every time they need to change a price or add a new service.</p>
            <p>With our architecture, <strong>your website is hard-wired directly to a private Google Sheet.</strong></p>
            <p>If you or your receptionist can type into an Excel file, you can manage your entire website. Change a price in the spreadsheet, and your live website updates globally in seconds.</p>
            <p>Should I build a quick prototype so you can see how easy this is?</p>
            <p>- Kiran</p>
        </body>
        </html>
        """
        days_to_next = 6

    # ---------------------------------------------------------
    # PHASE 5: THE FOMO / RANKING FEAR (Day 18)
    # Goal: Create urgency. Action is required to survive.
    # ---------------------------------------------------------
    elif phase == 5:
        subject = parse_spintax("The 2026 Google algorithm & [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting} {contact_name},</p>
            <p>I am reaching out one last time regarding the missing website link on your Google Maps profile because the rules of local SEO are changing.</p>
            <div style="background-color: #fff1f2; border-left: 4px solid #f43f5e; padding: 15px; margin: 15px 0;">
                <strong>The 2026 AI Algorithm Shift:</strong> Google’s AI search now significantly increases the weight of <i>linked, fast-loading</i> websites. Profiles without them are actively being suppressed in the Map Pack.
            </div>
            <p>Our Static-Site Architecture is unhackable and achieves a 100/100 Google PageSpeed score, ensuring you stay at the top of local searches.</p>
            <p>Let me build a risk-free demo to secure your ranking. Reply "YES" and I'll start immediately.</p>
            <p>- Kiran</p>
        </body>
        </html>
        """
        days_to_next = 6

    # ---------------------------------------------------------
    # PHASE 6: THE HUMAN CHECK-IN (Day 24)
    # Goal: Plain text, highly personal. Sparks a reply.
    # ---------------------------------------------------------
    elif phase == 6:
        subject = "am I off base here?"
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting},</p>
            <p>I've reached out a few times about getting a high-speed, $0 monthly fee website set up for {name}.</p>
            <p>Am I totally off base here, or is this just a really busy month for the clinic?</p>
            <p>Just let me know so I can update my notes.</p>
            <p>- Kiran</p>
        </body>
        </html>
        """
        days_to_next = 6

    # ---------------------------------------------------------
    # PHASE 7: THE BREAKUP (Day 30)
    # Goal: Take the offer away. Provide direct buy links.
    # ---------------------------------------------------------
    elif phase == 7:
        subject = parse_spintax("{Closing my file|Last email} regarding [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; font-size: 15px; color: #1a1a1a; line-height: 1.6;">
            <p>{greeting},</p>
            <p>Since I haven't heard back, I'll assume that fixing the missing website on your Google profile isn't a priority right now. This will be my last email.</p>
            <p>If you ever get tired of losing map traffic to competitors, or if you just want to stop paying monthly "Web Rent" to Wix or Shopify, you know where to find me.</p>
            <p>Wishing {name} a highly successful year.</p>
            <br>
            <p style="font-size: 13px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 15px;">
                <strong>Kiran Deb Mondal</strong><br>
                Principal Technologist | Stop Web Rent<br>
                WhatsApp: <a href="https://wa.me/966572562151" style="color: #0d9488;">+966 572562151</a><br>
                Website: <a href="https://www.stopwebrent.com" style="color: #0d9488;">www.stopwebrent.com</a>
            </p>
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
