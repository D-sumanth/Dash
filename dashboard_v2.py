import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import hmac
import yaml
from yaml.loader import SafeLoader

# Security configurations
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password
        else:
            st.session_state["password_correct"] = False

    # First create a secrets.toml file with your password
    if "password_correct" not in st.session_state:
        # First time visitors will see this
        st.markdown("""
        <style>
        .stApp {
            background-color: #000000;
        }
        div[data-testid="stMarkdownContainer"] {
            color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("# 🔒 Secure Dashboard Login")
        st.markdown("Please enter the password to access the dashboard.")
        
        st.text_input(
            "Password", type="password", key="password", on_change=password_entered
        )
        return False
    
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.markdown("""
        <style>
        .stApp {
            background-color: #000000;
        }
        div[data-testid="stMarkdownContainer"] {
            color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("# 🔒 Secure Dashboard Login")
        st.markdown("Please enter the password to access the dashboard.")
        
        st.text_input(
            "Password", type="password", key="password", on_change=password_entered
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct
        return True

# Main dashboard code
if check_password():
    # Set page config
    st.set_page_config(
        page_title="HireSplit Performance Dashboard",
        page_icon="📊",
        layout="wide"
    )

    # Custom CSS for HireSplit colors and dark theme
    st.markdown("""
        <style>
        /* Dark theme for main background */
        .stApp {
            background-color: #000000;
        }
        
        /* Title styling */
        .title-container {
            text-align: center;
            padding: 20px 0;
        }
        
        /* Metric styling */
        div[data-testid="stMetricValue"] {
            background-color: #e2f9ee !important;
            color: #00a939 !important;
            font-size: 64px !important;
            padding: 10px !important;
            border-radius: 10px !important;
            text-align: center !important;
            font-weight: bold !important;
            margin: 0 !important;
            width: 100% !important;
            min-height: 100px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        
        div[data-testid="stMetricLabel"] {
            display: none !important;
        }

        div[data-testid="stMetricDelta"] {
            display: none !important;
        }
        
        .metric-label {
            font-size: 24px !important;
            color: #ffffff !important;
            text-align: left !important;
            padding: 0 !important;
            margin-bottom: 5px !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
            white-space: nowrap !important;
        }

        .metric-icon {
            font-size: 24px !important;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #ffffff !important;
            font-weight: normal !important;
        }
        
        h1 {
            text-align: center !important;
            padding: 20px 0 !important;
        }
        
        /* Dataframe styling */
        [data-testid="stDataFrame"] {
            background-color: #111111;
        }
        
        .stDataFrame table {
            background-color: #111111;
            color: #ffffff;
            font-size: 24px !important;
        }
        
        .stDataFrame th {
            background-color: #000000 !important;
            color: #ffffff !important;
            font-size: 24px !important;
            padding: 20px !important;
            text-align: left !important;
        }
        
        .stDataFrame td {
            background-color: #111111 !important;
            color: #ffffff !important;
            font-size: 24px !important;
            padding: 20px !important;
            text-align: left !important;
        }
        
        /* Dark row styling */
        .stDataFrame tr:nth-child(odd) td {
            background-color: #1a1a1a !important;
        }
        
        /* Container styling */
        [data-testid="stVerticalBlock"] {
            background-color: #000000;
            padding: 10px;
        }

        /* Column gaps */
        [data-testid="column"] {
            padding: 0 5px !important;
        }

        /* Metric container */
        .metrics-container {
            margin: 20px 0 !important;
            padding: 0 10px !important;
        }

        /* Fix for two-line metric labels */
        div[data-testid="column"]:nth-child(4) .metric-label {
            font-size: 22px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Define target companies
    TARGET_COMPANIES = [
        "Sanderson iKas",
        "Sanderson-iKas International (Asia) Pte Ltd "  # Note the space at the end
    ]

    # Load the data
    @st.cache_data
    def load_data():
        try:
            referrers_df = pd.read_excel('Referrers.xlsx')
            applicants_df = pd.read_excel('Applicant Stages.xlsx')
            daily_reports_df = pd.read_excel('Daily Reports.xlsx')
            
            # Filter for target companies
            daily_reports_df = daily_reports_df[daily_reports_df['companyName'].isin(TARGET_COMPANIES)]
            applicants_df = applicants_df[applicants_df['company'].isin(TARGET_COMPANIES)]
            
            return referrers_df, applicants_df, daily_reports_df
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return None, None, None

    referrers_df, applicants_df, daily_reports_df = load_data()

    if referrers_df is not None and applicants_df is not None and daily_reports_df is not None:
        # Header with logo and title
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.image("hiresplit.png", width=250)
        with col2:
            st.markdown('<h1>Sanderson-iKas Performance Dashboard</h1>', unsafe_allow_html=True)

        try:
            # Key Metrics
            st.markdown('<div class="metrics-container">', unsafe_allow_html=True)
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.markdown('<div class="metric-label">📊 Jobs</div>', unsafe_allow_html=True)
                total_jobs = daily_reports_df['proposalCount'].sum()
                st.metric("", int(total_jobs))

            with col2:
                st.markdown('<div class="metric-label">📝 Applications</div>', unsafe_allow_html=True)
                total_applications = len(applicants_df['applicantName'].unique())
                st.metric("", total_applications)

            with col3:
                st.markdown('<div class="metric-label">🔄 Shares</div>', unsafe_allow_html=True)
                total_shares = len(referrers_df['Email'].unique())
                st.metric("", total_shares)

            with col4:
                st.markdown('<div class="metric-label">👥 Registered Referrers</div>', unsafe_allow_html=True)
                registered_referrers = len(referrers_df[
                    (referrers_df['Registered'] == 'Yes') & 
                    (referrers_df['Referrer'] == 'No')
                ])
                st.metric("", registered_referrers)

            with col5:
                st.markdown('<div class="metric-label">⭐ Active Referrers</div>', unsafe_allow_html=True)
                active_referrers = len(referrers_df[referrers_df['Referrer'] == 'Yes'])
                st.metric("", active_referrers)
            st.markdown('</div>', unsafe_allow_html=True)

            # Get all unique consultants from all sources
            consultants_applicants = set(applicants_df['consultant'].unique())
            consultants_daily = set(daily_reports_df['consultantName'].unique())
            consultants_referrers = set(referrers_df['Client Name'].unique())
            
            # Union of all consultants
            all_consultants = consultants_applicants.union(consultants_daily).union(consultants_referrers)
            
            # Consultant Summary
            st.subheader("Consultant Summary")
            
            consultant_data = []
            
            for consultant in all_consultants:
                candidates = len(applicants_df[applicants_df['consultant'] == consultant])
                shares = len(referrers_df[referrers_df['Client Name'] == consultant]['Email'].unique())
                registered = len(referrers_df[(referrers_df['Client Name'] == consultant) & (referrers_df['Registered'] == 'Yes')])
                active = len(referrers_df[(referrers_df['Client Name'] == consultant) & (referrers_df['Proposal Count'] > 0)])
                
                consultant_data.append({
                    'Consultant': consultant,
                    'Candidates': candidates,
                    'Shares': shares,
                    'Registered Referrers': registered,
                    'Active Referrers': active
                })
            
            consultant_summary = pd.DataFrame(consultant_data)
            st.dataframe(
                consultant_summary,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Consultant": st.column_config.TextColumn(
                        "Consultant",
                        help="Consultant name",
                        width=400
                    ),
                    "Candidates": st.column_config.NumberColumn(
                        "Candidates",
                        help="Number of candidates",
                        width=250
                    ),
                    "Shares": st.column_config.NumberColumn(
                        "Shares",
                        help="Number of shares",
                        width=250
                    ),
                    "Registered Referrers": st.column_config.NumberColumn(
                        "Registered Referrers",
                        help="Number of registered referrers",
                        width=300
                    ),
                    "Active Referrers": st.column_config.NumberColumn(
                        "Active Referrers",
                        help="Number of active referrers",
                        width=250
                    )
                }
            )

            st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)  # Spacing

            # Application Status by Consultant
            st.subheader("Application Status by Consultant")

            status_by_consultant = applicants_df.groupby(['consultant', 'status']).size().reset_index(name='count')
            if not status_by_consultant.empty:
                fig = px.bar(
                    status_by_consultant, 
                    x='consultant', 
                    y='count', 
                    color='status',
                    title='Application Status Distribution by Consultant',
                    color_discrete_map={
                        'Hired': '#00a939',
                        'Interview': '#008fdf',
                        'Shortlisted': '#005025',
                        'Rejected': '#dcdcdc'
                    }
                )
                fig.update_layout(
                    plot_bgcolor='#111111',
                    paper_bgcolor='#111111',
                    font_color='#ffffff',
                    xaxis=dict(gridcolor='#333333'),
                    yaxis=dict(gridcolor='#333333')
                )
                st.plotly_chart(fig, use_container_width=True)

            st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)  # Spacing

            # Share Distribution by Platform
            st.subheader("Share Distribution by Platform")

            platform_names = {
                'whatsAppShareCount': 'WhatsApp',
                'telegramShareCount': 'Telegram',
                'linkedInShareCount': 'LinkedIn',
                'lineShareCount': 'LINE'
            }

            share_platforms = daily_reports_df[list(platform_names.keys())].sum()
            if share_platforms.sum() > 0:
                share_platforms.index = [platform_names[col] for col in share_platforms.index]
                fig = px.pie(
                    values=share_platforms.values, 
                    names=share_platforms.index,
                    color_discrete_sequence=['#00a939', '#008fdf', '#005025', '#e2f9ee']
                )
                fig.update_layout(
                    plot_bgcolor='#111111',
                    paper_bgcolor='#111111',
                    font_color='#ffffff'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No sharing activity recorded.")

        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
    else:
        st.error("Failed to load the required data files. Please check if the Excel files are present in the correct location.") 