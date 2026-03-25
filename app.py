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

# --- 3. THE 7-PHASE COPYWRITING ENGINE (ULTRA-MODERN UI) ---
def get_campaign_content(phase, name, category, address):
    """Returns the Subject and HTML Body for the specific phase."""
    
    greeting = random.choice(["Hi", "Hello", "Greetings", "Dear"])
    
    # Cleaners
    display_address = "your city" if ("(" in str(address) or str(address).lower() == "n/a" or not address) else address
    display_cat = "Dental" if (str(category).lower() == "n/a" or not category) else category

    # Global CSS Variables (Inline)
    font_family = "'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Arial, sans-serif"
    bg_body = "#f3f4f6"
    bg_card = "#ffffff"
    text_main = "#334155"
    text_dark = "#0f172a"
    accent = "#0d9488" # Teal
    accent_light = "#f0fdfa"
    warning = "#e11d48" # Crimson
    warning_light = "#fff1f2"

    # Common Footer
    footer = f"""
    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; font-size: 13px; color: #64748b; text-align: center;">
        <strong style="color: {text_dark}; font-size: 14px;">Kiran Deb Mondal</strong><br>
        Principal Technologist | Stop Web Rent<br>
        <span style="display: inline-block; margin-top: 8px;">
            <a href="https://wa.me/966572562151" style="color: {accent}; text-decoration: none;">WhatsApp: +966 572562151</a> | 
            <a href="https://www.stopwebrent.com" style="color: {accent}; text-decoration: none;">StopWebRent.com</a>
        </span>
    </div>
    """

    if phase == 1:
        subject = parse_spintax("{Action Required|Google Maps alert|Missing link} for [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #e5e7eb;">
                <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 30px 20px; text-align: center;">
                    <h1 style="color: #2dd4bf; margin: 0; font-size: 24px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase;">STOP WEB RENT</h1>
                    <p style="color: #94a3b8; margin: 5px 0 0 0; font-size: 13px; font-weight: 500;">High-Velocity Web Architecture</p>
                </div>
                <div style="padding: 35px 30px;">
                    <h2 style="color: {text_dark}; font-size: 20px; margin-top: 0;">{greeting} {name} team,</h2>
                    <p style="font-size: 16px; line-height: 1.6; color: {text_main};">
                        I was researching <strong>{display_cat}</strong> clinics in <strong>{display_address}</strong> and noticed your practice has a fantastic reputation. However, you are missing a critical digital asset:
                    </p>
                    <div style="background-color: {warning_light}; border-left: 4px solid {warning}; padding: 16px; margin: 25px 0; border-radius: 0 8px 8px 0;">
                        <strong style="color: #9f1239; font-size: 16px;">⚠️ Missing Element:</strong><br>
                        <span style="color: {warning}; font-size: 15px;">You do not have a <strong>"Website"</strong> button on your Google Maps profile. Every day, Google’s algorithm is handing your high-value patients to competitors who do.</span>
                    </div>
                    <p style="font-size: 16px; line-height: 1.6; color: {text_main};">
                        I build 0.1s High-Velocity websites specifically for healthcare clinics. <strong>Unlike Wix or Shopify, I charge $0 in monthly hosting fees.</strong>
                    </p>
                    <div style="background-color: {accent_light}; border: 1px solid #ccfbf1; padding: 20px; margin: 25px 0; border-radius: 8px; text-align: center;">
                        <strong style="color: #0f766e; font-size: 16px;">My Offer: A Free 24-Hour Preview</strong><br>
                        <p style="color: #0d9488; font-size: 14px; margin: 8px 0 0 0;">I will use your current logo and photos to build a live demo. If you don't love the performance, you pay nothing.</p>
                    </div>
                    <div style="text-align: center; margin-top: 30px;">
                        <a href="https://wa.me/966572562151?text=YES" style="background-color: {accent}; color: #ffffff; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">REPLY 'YES' FOR FREE DEMO</a>
                    </div>
                    {footer}
                </div>
            </div>
        </body>
        </html>
        """

    elif phase == 2:
        subject = f"Re: {name} digital preview"
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; padding: 35px 30px; border: 1px solid #e5e7eb;">
                <h2 style="color: {text_dark}; font-size: 18px; margin-top: 0;">{greeting} again,</h2>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    I wanted to follow up on my last email. When I build a Titan Engine site for a clinic like <strong>{name}</strong>, it's not just a digital brochure—it's a high-conversion lead generation machine.
                </p>
                <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 25px 0;">
                    <h3 style="color: {text_dark}; font-size: 16px; margin-top: 0;">⚡ Here is what your custom site includes:</h3>
                    <ul style="color: {text_main}; font-size: 15px; line-height: 1.8; margin-bottom: 0; padding-left: 20px;">
                        <li><strong>WhatsApp Booking:</strong> Patients book appointments in one tap.</li>
                        <li><strong>Multilingual Support:</strong> Instantly translates to local languages.</li>
                        <li><strong>Zero-DB Architecture:</strong> 100% unhackable and secure.</li>
                    </ul>
                </div>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="https://hv-furniture-bit.github.io/dental-junction-behala/index.html" style="color: {accent}; font-weight: bold; font-size: 16px; text-decoration: underline;">👉 Click here to play with a live demo of a clinic we recently built</a>
                </div>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main}; text-align: center;">
                    Would you like me to build a custom prototype for {name}? Just reply "YES".
                </p>
                {footer}
            </div>
        </body>
        </html>
        """

    elif phase == 3:
        subject = parse_spintax("{Stop paying|How to save $1,800 on} website rent")
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; padding: 35px 30px; border: 1px solid #e5e7eb;">
                <h2 style="color: {text_dark}; font-size: 20px; margin-top: 0; text-align: center;">Stop Renting. Start Owning.</h2>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main}; text-align: center;">
                    Most business owners are trapped paying $30-$50 every single month to Wix or Shopify. The Titan Engine changes that. <strong>Pay a $199 one-time setup fee, and own it forever.</strong>
                </p>
                
                <div style="border-radius: 8px; overflow: hidden; margin: 30px 0; border: 1px solid #e2e8f0;">
                    <table style="width: 100%; border-collapse: collapse; font-size: 14px; text-align: center;">
                        <tr style="background-color: #f8fafc;">
                            <th style="padding: 15px; border-bottom: 2px solid #e2e8f0; text-align: left;">5-Year Cost</th>
                            <th style="padding: 15px; border-bottom: 2px solid #e2e8f0; background-color: {accent_light}; color: {accent};">Titan Engine</th>
                            <th style="padding: 15px; border-bottom: 2px solid #e2e8f0; color: #64748b;">Wix / Shopify</th>
                        </tr>
                        <tr>
                            <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; text-align: left; font-weight: 500;">Setup Fee</td>
                            <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; background-color: {accent_light}; font-weight: bold;">$199 <span style="font-size: 11px; font-weight: normal;">(Once)</span></td>
                            <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; color: #64748b;">$0</td>
                        </tr>
                        <tr>
                            <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; text-align: left; font-weight: 500;">Monthly Rent</td>
                            <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; background-color: {accent_light}; font-weight: bold; color: {accent};">$0</td>
                            <td style="padding: 15px; border-bottom: 1px solid #e2e8f0; color: #64748b;">$1,740</td>
                        </tr>
                        <tr style="background-color: #0f172a; color: white;">
                            <td style="padding: 15px; text-align: left; font-weight: bold;">Total Cost</td>
                            <td style="padding: 15px; font-weight: bold; color: #2dd4bf;">$274 <span style="font-size: 11px; font-weight: normal;">(w/ domain)</span></td>
                            <td style="padding: 15px; font-weight: bold; color: #f87171;">$2,115</td>
                        </tr>
                    </table>
                </div>
                
                <div style="text-align: center; margin-top: 25px;">
                    <p style="font-size: 16px; color: {text_dark}; font-weight: bold;">That is $1,841 in savings.</p>
                    <a href="https://wa.me/966572562151" style="display: inline-block; margin-top: 10px; background-color: {text_dark}; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 600;">Message me to start saving</a>
                </div>
                {footer}
            </div>
        </body>
        </html>
        """

    elif phase == 4:
        subject = parse_spintax("Update {name} website using Excel?")
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; padding: 35px 30px; border: 1px solid #e5e7eb;">
                <h2 style="color: {text_dark}; font-size: 18px; margin-top: 0;">{greeting},</h2>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    One of the main reasons clinics don't build websites is because they don't want to learn complex dashboards or pay a developer every time they need to change a price.
                </p>
                <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 20px; border-radius: 8px; margin: 25px 0;">
                    <h3 style="color: #166534; font-size: 16px; margin: 0 0 10px 0;">📊 The Spreadsheet CMS</h3>
                    <p style="color: #15803d; font-size: 14px; margin: 0; line-height: 1.5;">
                        With our architecture, <strong>your website is hard-wired directly to a private Google Sheet.</strong> If you or your receptionist can type into an Excel file, you can manage your entire website. 
                    </p>
                </div>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    Change a price in the spreadsheet, and your live website updates globally in seconds. Should I build a quick prototype so you can see how easy this is?
                </p>
                {footer}
            </div>
        </body>
        </html>
        """

    elif phase == 5:
        subject = parse_spintax("The 2026 Google algorithm & [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; padding: 35px 30px; border: 1px solid #e5e7eb; border-top: 5px solid {warning};">
                <h2 style="color: {text_dark}; font-size: 18px; margin-top: 0;">Urgent Ranking Notice for {name}</h2>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    {greeting}, I am reaching out regarding the missing website link on your Google Maps profile because the rules of local SEO are officially changing.
                </p>
                <div style="background-color: {warning_light}; padding: 20px; border-radius: 8px; margin: 25px 0;">
                    <strong style="color: #be123c; font-size: 16px;">The 2026 AI Algorithm Shift:</strong>
                    <p style="color: #9f1239; font-size: 14px; margin: 8px 0 0 0; line-height: 1.5;">
                        Google’s AI search now significantly increases the weight of <i>linked, fast-loading</i> websites. Profiles without them are actively being suppressed and hidden from patients in the Map Pack.
                    </p>
                </div>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    Our architecture achieves a <strong>100/100 Google PageSpeed score</strong>, ensuring you stay at the top of local searches.
                </p>
                <div style="text-align: center; margin-top: 30px;">
                    <a href="https://wa.me/966572562151?text=YES" style="background-color: {text_dark}; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 15px;">SECURE YOUR RANKING (FREE DEMO)</a>
                </div>
                {footer}
            </div>
        </body>
        </html>
        """

    elif phase == 6:
        # Phase 6 stays visually clean and simple to look like a personal follow-up.
        subject = "am I off base here?"
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; padding: 35px 30px; border: 1px solid #e5e7eb;">
                <p style="font-size: 15px; line-height: 1.6; color: {text_main}; margin-top: 0;">{greeting},</p>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    I've reached out a few times about getting a high-speed, $0 monthly fee website set up for {name}.
                </p>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    Am I totally off base here, or is this just a really busy month for the clinic? Just let me know so I can update my notes.
                </p>
                {footer}
            </div>
        </body>
        </html>
        """

    elif phase == 7:
        subject = parse_spintax("{Closing my file|Last email} regarding [Name]").replace("[Name]", name)
        html = f"""
        <html>
        <body style="margin: 0; padding: 20px; background-color: {bg_body}; font-family: {font_family};">
            <div style="max-width: 600px; margin: 0 auto; background-color: {bg_card}; border-radius: 12px; padding: 35px 30px; border: 1px solid #e5e7eb;">
                <div style="text-align: center; margin-bottom: 25px;">
                    <span style="display: inline-block; background-color: #f1f5f9; color: #475569; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase;">File Closed</span>
                </div>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main}; margin-top: 0;">{greeting},</p>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    Since I haven't heard back, I'll assume that fixing the missing website on your Google profile isn't a priority right now. This will be my last email.
                </p>
                <p style="font-size: 15px; line-height: 1.6; color: {text_main};">
                    If you ever get tired of losing map traffic to competitors, or if you just want to stop paying monthly "Web Rent" to Wix or Shopify, you know where to find me. Wishing {name} a highly successful year.
                </p>
                <div style="margin-top: 35px; padding: 25px; background-color: #f8fafc; border-radius: 8px; text-align: center; border: 1px dashed #cbd5e1;">
                    <strong style="color: {text_dark}; font-size: 16px;">Ready to deploy your site instantly?</strong><br>
                    <a href="https://kiranmondal.gumroad.com/l/titanv50" style="display: inline-block; margin-top: 15px; background-color: {accent}; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 14px;">Purchase Direct via Gumroad</a>
                </div>
                {footer}
            </div>
        </body>
        </html>
        """
        
    return subject, html
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
