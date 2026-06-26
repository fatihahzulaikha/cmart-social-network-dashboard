import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="CMART Insight Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 38px;
        font-weight: bold;
        color: #4B2E2B;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    visitor_df = pd.read_csv("visitor_cleaned_data.csv")
    vendor_df = pd.read_csv("vendor_cleaned_data.csv")
    nodes_df = pd.read_csv("tiktok_nodes_sulam.csv")
    edges_df = pd.read_csv("tiktok_edges_sulam.csv")
    return visitor_df, vendor_df, nodes_df, edges_df

visitor_df, vendor_df, nodes_df, edges_df = load_data()

all_df = pd.concat([visitor_df, vendor_df], ignore_index=True)

st.markdown('<div class="main-title">📊 CMART Changlun Feedback & Social Media Dashboard</div>', unsafe_allow_html=True)
st.markdown("---")

st.sidebar.header("🧭 Navigation Panel")
page = st.sidebar.radio(
    "Go to:",
    [
        "📈 Overview & Metrics",
        "👥 Respondent Analysis",
        "🏪 Vendor Insights",
        "☁️ Word Cloud Main Issue",
        "📱 Social Media Graph Trend",
        "⭐ Influencer Analysis",
        "💡 Action Recommendation",
        "📋 View Raw Data"
    ]
)

if page == "📈 Overview & Metrics":
    st.markdown("""
<style>
.overview-card{
    height:230px;
    border-radius:20px;
    padding:25px;
    text-align:center;
    box-shadow:0 4px 10px rgba(0,0,0,0.08);
    display:flex;
    flex-direction:column;
    justify-content:center;
}

.overview-card h4{
    margin:0;
    font-size:24px;
    font-weight:600;
}

.overview-card h1{
    margin:20px 0 10px 0;
    font-size:54px;
    font-weight:bold;
}

.overview-card p{
    margin:0;
    font-size:16px;
    color:#555;
}
</style>
""", unsafe_allow_html=True)


    st.subheader("📊 Dashboard Overview")

    st.info(
        "This dashboard combines Text Analysis from visitor and vendor feedback with "
        "Social Network Analysis from TikTok data to identify potential loyalty influencers "
        "for CMART Changlun."
    )

    col1, col2, col3, col4, col5 = st.columns(5) 
    
    with col1:
        st.markdown(f"""
        <div class="overview-card" style="background:#FFF7ED;">
            <h4>Total Feedback</h4>
            <h1>{len(all_df)}</h1>
            <p>Visitor + Vendor</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="overview-card" style="background:#ECFDF5;">
            <h4>Visitors</h4>
            <h1>{len(visitor_df)}</h1>
            <p>Customer feedback</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="overview-card" style="background:#EFF6FF;">
            <h4>Vendors</h4>
            <h1>{len(vendor_df)}</h1>
            <p>Business feedback</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="overview-card" style="background:#F5F3FF;">
            <h4>TikTok Users</h4>
            <h1>{len(nodes_df)}</h1>
            <p>Network nodes</p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="overview-card" style="background:#FEF2F2;">
            <h4>Interactions</h4>
            <h1>{len(edges_df)}</h1>
            <p>Network edges</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    left, right = st.columns([1.3, 1])

    with left:
        st.write("### 📱 Social Network Analysis")

        col1, col2, col3 = st.columns([1,3,1])

        with col2: 
            st.image(
                "sna_output.png", width=450)
    
        st.markdown("""
       <div style='text-align:center;'>
       Bigger nodes represent users with stronger influence or more connections.
       </div>
       """, unsafe_allow_html=True)
        
    with right:
        st.write("### 🎯 Dashboard Goal")

        st.markdown("""
        <div class="goal-box">
        <b>Main Goal:</b><br><br>
        Connect influential TikTok users with CMART promotion strategies.
        <br><br>
        These influencers can recommend CMART to their followers, attract more visitors, 
        and help build customer loyalty.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="insight-box">
        <b>Quick Insights:</b><br><br>
        ✅ Visitors mostly give positive feedback.<br>
        ✅ Vendors focus on customers, promotion, and sales.<br>
        ✅ TikTok users can help spread CMART content.<br>
        ✅ Influencers can support repeat visits and loyalty.
        </div>
        """, unsafe_allow_html=True)

    st.write("### ⭐ Top Potential Influencers")

    top_influencers = nodes_df.copy()

    top_influencers = top_influencers[
        top_influencers["Label"].notna() &
        (top_influencers["Label"] != "Unknown")
    ]

    top_influencers = top_influencers.head(10)

    top_influencers["Connection Count"] = range(
        len(top_influencers),
        0,
        -1
    )

    fig_top = px.bar(
        top_influencers,
        x="Connection Count",
        y="Label",
        orientation="h",
        title="Top 10 Potential Influencers",
        color="Connection Count"
    )

    fig_top.update_layout(
        yaxis_title="Username",
        xaxis_title="Influencer Rank Score",
        yaxis={'categoryorder': 'total ascending'}
    )

    st.plotly_chart(fig_top, use_container_width=True)

    st.markdown("---")

    st.write("### 💡 Summary Recommendation")

    rec1, rec2, rec3, rec4 = st.columns(4)

    with rec1:
        st.success("🤝 Collaborate with top TikTok influencers")

    with rec2:
        st.success("🎁 Give rewards for content creators")

    with rec3:
        st.success("📹 Promote vendors using TikTok videos")

    with rec4:
        st.success("❤️ Build loyalty and repeat visits")


elif page == "👥 Respondent Analysis":
    st.subheader("👥 Visitor & Respondent Analysis")

    search_query = st.text_input("🔍 Search visitor comments by keyword:").lower()

    filtered_resp = visitor_df.copy()

    if search_query:
        filtered_resp = filtered_resp[
            filtered_resp["cleaned_data"].str.contains(search_query, na=False, case=False)
        ]
        st.success(f"Found {len(filtered_resp)} matches for '{search_query}'")

    st.write("### 🏷 Most Common Terms in Visitor Feedback")

    all_words = " ".join(filtered_resp["cleaned_data"].dropna().astype(str))

    if all_words.strip():
        wordcloud = WordCloud(
            width=800,
            height=300,
            background_color="white",
            colormap="viridis"
        ).generate(all_words)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("No text data available to generate word cloud.")

    st.write("### 💬 Visitor Responses")
    st.dataframe(filtered_resp[["Respondent", "Text", "cleaned_data"]], use_container_width=True)


elif page == "🏪 Vendor Insights":
    st.subheader("🏪 Vendor Operations & Experience Analysis")

    tiktok_count = vendor_df["cleaned_data"].str.contains("tiktok|media|video|live", na=False, case=False).sum()
    visitor_count = vendor_df["cleaned_data"].str.contains("pengunjung|pelanggan|orang|komuniti", na=False, case=False).sum()
    business_count = vendor_df["cleaned_data"].str.contains("niaga|jual|produk|promosi", na=False, case=False).sum()

    vendor_metrics = pd.DataFrame({
        "Topic Mentioned": ["TikTok / Social Media", "Visitor / Customer", "Business / Product"],
        "Mentions Count": [tiktok_count, visitor_count, business_count]
    })

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write("### 📊 Key Theme Mentions among Vendors")
        fig_bar = px.bar(
            vendor_metrics,
            x="Topic Mentioned",
            y="Mentions Count",
            color="Topic Mentioned"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.write("### 💡 Key Takeaway Highlights")
        st.info(
            "Vendor feedback focuses on business activity, customer attraction, promotion, "
            "and the importance of increasing visitor engagement at CMART Changlun."
        )

    st.write("### 💬 Vendor Statements")
    st.dataframe(vendor_df[["Respondent", "Text", "cleaned_data"]], use_container_width=True)


elif page == "☁️ Word Cloud Main Issue":
    st.subheader("☁️ Word Cloud Main Issue")

    option = st.selectbox("Choose word cloud:", ["Visitor Word Cloud", "Vendor Word Cloud"])

    if option == "Visitor Word Cloud":
        selected_df = visitor_df
    else:
        selected_df = vendor_df

    text = " ".join(selected_df["cleaned_data"].dropna().astype(str))

    if text.strip():
        wordcloud = WordCloud(
            width=1000,
            height=450,
            background_color="white",
            colormap="copper"
        ).generate(text)

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

    st.info("Visitor negative word cloud is not shown because there is no clear negative visitor feedback in the dataset.")


elif page == "📱 Social Media Graph Trend":
    st.subheader("📱 Social Media Graph Trend")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total TikTok Nodes / Users", len(nodes_df))

    with col2:
        st.metric("Total TikTok Edges / Interactions", len(edges_df))

    st.write("### 📊 Interaction Weight Distribution")

    fig = px.histogram(
        edges_df,
        x="Weight",
        nbins=20,
        title="TikTok Interaction Weight Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write("### TikTok Interaction Data")
    st.dataframe(edges_df.head(20), use_container_width=True)


elif page == "⭐ Influencer Analysis":
    st.subheader("⭐ Influencer Analysis")
    st.write("### ⭐ Top Potential Influencers")

    top_influencers = nodes_df.copy()

    top_influencers = top_influencers[
        top_influencers["Label"].notna() &
        (top_influencers["Label"] != "Unknown")
    ]

    top_influencers = top_influencers.head(10)

    top_influencers["Connection Count"] = range(
        len(top_influencers),
        0,
        -1
    )

    fig_top = px.bar(
        top_influencers,
        x="Connection Count",
        y="Label",
        orientation="h",
        title="Top 10 Potential Influencers",
        color="Connection Count"
    )

    fig_top.update_layout(
        yaxis_title="Username",
        xaxis_title="Influencer Rank Score",
        yaxis={'categoryorder': 'total ascending'}
    )

    st.plotly_chart(fig_top, use_container_width=True)

elif page == "💡 Action Recommendation":
    st.subheader("💡 Action Recommendation")

    st.markdown("""
    ### Recommended Actions for CMART Changlun

    **1. Collaborate with TikTok micro-influencers**  
    Use highly connected TikTok users to promote CMART products and events.

    **2. Create a loyalty influencer programme**  
    Reward visitors who post videos, reviews, or recommendations about CMART.

    **3. Improve vendor promotion**  
    Help vendors create short TikTok content to highlight food, products, and promotions.

    **4. Use hashtag campaigns**  
    Suggested hashtags: `#CMARTChanglun`, `#UUMFoodSpot`, `#ChanglunCarbootSale`.

    **5. Support low-traffic periods**  
    Create special promotions during times when visitor numbers are lower.

    **6. Combine text analysis and SNA findings**  
    Text analysis identifies issues and feedback, while SNA identifies who can help spread CMART promotion.
    """)


elif page == "📋 View Raw Data":
    st.subheader("🗂 Full Data Table Inspection")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["👥 Visitor Data", "🏪 Vendor Data", "📱 TikTok Nodes", "🔗 TikTok Edges"]
    )

    with tab1:
        st.dataframe(visitor_df, use_container_width=True)

    with tab2:
        st.dataframe(vendor_df, use_container_width=True)

    with tab3:
        st.dataframe(nodes_df, use_container_width=True)

    with tab4:
        st.dataframe(edges_df, use_container_width=True)