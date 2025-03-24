import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(
    page_title="HireSplit Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

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
    # Title
    st.title("HireSplit Performance Dashboard")
    st.caption("Filtered for: " + " & ".join(TARGET_COMPANIES))

    try:
        # Key Metrics
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            # Jobs - Sum of proposal count from Daily Reports
            total_jobs = daily_reports_df['proposalCount'].sum()
            st.metric("Jobs", int(total_jobs))

        with col2:
            # Applications - Unique Applicant names from Applicant Stages
            total_applications = len(applicants_df['applicantName'].unique())
            st.metric("Applications", total_applications)

        with col3:
            # Shares - Unique Email count from Referrers
            total_shares = len(referrers_df['Email'].unique())
            st.metric("Shares", total_shares)

        with col4:
            # Registered Referrers - Count of registered non-referrers
            registered_referrers = len(referrers_df[
                (referrers_df['Registered'] == 'Yes') & 
                (referrers_df['Referrer'] == 'No')
            ])
            st.metric("Registered Referrers", registered_referrers)

        with col5:
            # Active Referrers - Count of referrers
            active_referrers = len(referrers_df[referrers_df['Referrer'] == 'Yes'])
            st.metric("Active Referrers", active_referrers)

        # Consultant Summary
        st.subheader("Consultant Summary")

        consultants = daily_reports_df['consultantName'].unique()
        consultant_data = []
        
        for consultant in consultants:
            candidates = len(applicants_df[applicants_df['consultant'] == consultant])
            shares = daily_reports_df[daily_reports_df['consultantName'] == consultant]['shareCount'].sum()
            registered = len(referrers_df[(referrers_df['Client Name'] == consultant) & (referrers_df['Registered'] == 'Yes')])
            active = len(referrers_df[(referrers_df['Client Name'] == consultant) & (referrers_df['Proposal Count'] > 0)])
            
            consultant_data.append({
                'Consultant': consultant,
                'Candidates': candidates,
                'Shares': int(shares),
                'Registered Referrers': registered,
                'Active Referrers': active
            })
        
        consultant_summary = pd.DataFrame(consultant_data)
        st.dataframe(consultant_summary, use_container_width=True)

        # Application Status by Consultant
        st.subheader("Application Status by Consultant")

        status_by_consultant = applicants_df.groupby(['consultant', 'status']).size().reset_index(name='count')
        if not status_by_consultant.empty:
            fig = px.bar(status_by_consultant, 
                        x='consultant', 
                        y='count', 
                        color='status',
                        title='Application Status Distribution by Consultant')
            st.plotly_chart(fig, use_container_width=True)

        # Share Distribution by Platform
        st.subheader("Share Distribution by Platform")

        share_platforms = daily_reports_df[['whatsAppShareCount', 'telegramShareCount', 'linkedInShareCount', 'lineShareCount']].sum()
        if share_platforms.sum() > 0:
            fig = px.pie(values=share_platforms.values, 
                        names=share_platforms.index,
                        title='Share Distribution by Platform')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sharing activity recorded.")

    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
else:
    st.error("Failed to load the required data files. Please check if the Excel files are present in the correct location.") 