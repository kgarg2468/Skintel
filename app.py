import streamlit as st
import io
import numpy as np
from PIL import Image
import cv2
from image_processor import ImageProcessor
from skin_analyzer import SkinAnalyzer
from recommendation_engine import RecommendationEngine

# Page configuration
st.set_page_config(
    page_title="Skin Health Analysis",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize components
@st.cache_resource
def load_components():
    """Load and cache the analysis components"""
    processor = ImageProcessor()
    analyzer = SkinAnalyzer()
    recommender = RecommendationEngine()
    return processor, analyzer, recommender

def main():
    """Main application function"""
    
    # Load components
    processor, analyzer, recommender = load_components()
    
    # Header
    st.title("🔬 AI-Powered Skin Health Analysis")
    st.markdown("""
    Upload a high-quality photo of your skin for AI-powered analysis. Our system uses advanced computer vision 
    to detect potential skin biomarkers and provide personalized health recommendations.
    """)
    
    # Privacy notice
    with st.expander("🔒 Privacy & Anonymity Notice", expanded=False):
        st.markdown("""
        - **No data storage**: Your images are processed in memory and immediately discarded
        - **Anonymous processing**: No personal information is collected or stored
        - **Secure upload**: All data transmission is encrypted
        - **No account required**: Use the service without registration or login
        """)
    
    # Medical disclaimer
    with st.expander("⚠️ Medical Disclaimer", expanded=False):
        st.markdown("""
        **IMPORTANT**: This tool is for educational and informational purposes only. It is NOT a substitute for 
        professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals 
        for any health concerns. The AI analysis provides screening suggestions only and should not be used as 
        the sole basis for medical decisions.
        """)
    
    # File upload section
    st.header("📤 Upload Your Skin Photo")
    
    uploaded_file = st.file_uploader(
        "Choose a skin photo (JPEG/PNG, max 5MB)",
        type=['jpg', 'jpeg', 'png'],
        help="For best results, use a well-lit, clear photo of the skin area you want analyzed"
    )
    
    if uploaded_file is not None:
        # Validate file size
        file_size = len(uploaded_file.getvalue())
        max_size = 5 * 1024 * 1024  # 5MB in bytes
        
        if file_size > max_size:
            st.error(f"File size ({file_size / (1024*1024):.1f} MB) exceeds the 5MB limit. Please upload a smaller image.")
            return
        
        # Display uploaded image
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Size: {image.size[0]}x{image.size[1]} pixels", use_container_width=True)
            
            # Image info
            st.write(f"**File size:** {file_size / (1024*1024):.1f} MB")
            st.write(f"**Format:** {image.format}")
            st.write(f"**Dimensions:** {image.size[0]} x {image.size[1]} pixels")
        
        with col2:
            st.subheader("🔄 Processing Analysis...")
            
            # Progress indicator
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Image preprocessing
                status_text.text("Step 1/4: Preprocessing image...")
                progress_bar.progress(25)
                processed_image, preprocessing_info = processor.preprocess_image(image)
                
                # Step 2: Feature extraction
                status_text.text("Step 2/4: Extracting features...")
                progress_bar.progress(50)
                features = processor.extract_features(processed_image)
                
                # Step 3: AI analysis
                status_text.text("Step 3/4: Running AI analysis...")
                progress_bar.progress(75)
                analysis_results = analyzer.analyze_skin_conditions(features)
                
                # Step 4: Generate recommendations
                status_text.text("Step 4/4: Generating recommendations...")
                progress_bar.progress(100)
                recommendations = recommender.generate_recommendations(analysis_results)
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                # Display results
                display_results(analysis_results, recommendations, preprocessing_info)
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                st.error("Please try uploading a different image or contact support if the problem persists.")

def display_results(analysis_results, recommendations, preprocessing_info):
    """Display analysis results and recommendations in dashboard style"""
    
    st.success("✅ Analysis Complete!")
    
    # Get top finding for summary banner
    sorted_conditions = sorted(analysis_results.items(), key=lambda x: x[1]['confidence'], reverse=True)
    top_condition, top_data = sorted_conditions[0]
    
    # TOP-LEVEL SUMMARY BANNER
    display_summary_banner(top_condition, top_data)
    
    st.divider()
    
    # CONDITION DASHBOARD TILES
    st.header("🔍 Health Insights Dashboard")
    display_condition_dashboard(sorted_conditions)
    
    st.divider()
    
    # ACTION CATEGORIES
    st.header("💡 Your Action Plan")
    display_action_categories(recommendations)
    
    # Processing info (collapsed by default)
    with st.expander("🔧 Processing Details", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original Size", f"{preprocessing_info['original_size'][0]}x{preprocessing_info['original_size'][1]}")
        with col2:
            st.metric("Processed Size", f"{preprocessing_info['processed_size'][0]}x{preprocessing_info['processed_size'][1]}")
        with col3:
            st.metric("Skin Coverage", f"{preprocessing_info['skin_coverage']:.1f}%")

def display_summary_banner(condition, data):
    """Display prominent summary banner with key insight"""
    confidence = data['confidence']
    risk_level = data['risk_level']
    
    # Determine banner style based on risk level
    if risk_level == "High":
        banner_color = "#ffebee"  # Light red
        icon = "⚠️"
        border_color = "#f44336"  # Red
    elif risk_level == "Medium":
        banner_color = "#fff8e1"  # Light orange
        icon = "🟡"
        border_color = "#ff9800"  # Orange
    else:
        banner_color = "#e8f5e8"  # Light green
        icon = "✅"
        border_color = "#4caf50"  # Green
    
    # Create concise message
    if "Acanthosis" in condition:
        message = f"High Insulin Risk Detected – Cut Added Sugars"
        action = "Focus on low-sugar diet and exercise"
    elif "Xanthelasma" in condition:
        message = f"Cholesterol Deposits Found – Heart Health Priority"
        action = "Schedule lipid panel and adopt heart-healthy diet"
    elif "Dry" in condition:
        message = f"Skin Dehydration Detected – Boost Hydration"
        action = "Increase water intake and use moisturizer"
    elif "Inflammatory" in condition:
        message = f"Skin Inflammation Present – Reduce Irritants"
        action = "See dermatologist and avoid triggers"
    elif "Seborrheic" in condition:
        message = f"Skin Condition Detected – Manage Stress"
        action = "Use gentle products and reduce stress"
    else:
        message = f"Sun Damage Detected – Protect Your Skin"
        action = "Daily SPF and regular skin checks"
    
    # Display banner
    st.markdown(f"""
    <div style="
        background-color: {banner_color};
        border-left: 5px solid {border_color};
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
    ">
        <h2 style="margin: 0; color: #1f1f1f;">
            {icon} {message}
        </h2>
        <p style="margin: 10px 0 0 0; color: #666; font-size: 16px;">
            {action} • Confidence: {confidence}%
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_condition_dashboard(sorted_conditions):
    """Display condition cards in dashboard layout"""
    
    # Limit to top 6 conditions to avoid overwhelming
    display_conditions = sorted_conditions[:6]
    
    # Create grid layout - 2 columns on desktop, 1 on mobile
    cols = st.columns(2)
    
    for idx, (condition, data) in enumerate(display_conditions):
        col = cols[idx % 2]
        
        with col:
            create_condition_card(condition, data)

def create_condition_card(condition, data):
    """Create individual condition card with progress ring"""
    confidence = data['confidence']
    risk_level = data['risk_level']
    description = data['description']
    
    # Get condition-specific icon and colors
    if "Acanthosis" in condition:
        icon = "🩸"
        card_title = "Insulin Resistance"
    elif "Xanthelasma" in condition:
        icon = "💛"
        card_title = "Cholesterol Deposits"
    elif "Dry" in condition:
        icon = "💧"
        card_title = "Skin Dehydration"
    elif "Inflammatory" in condition:
        icon = "🔥"
        card_title = "Inflammation"
    elif "Seborrheic" in condition:
        icon = "🧴"
        card_title = "Seborrheic Dermatitis"
    else:
        icon = "☀️"
        card_title = "Sun Damage"
    
    # Risk level colors
    if risk_level == "High":
        color = "#f44336"  # Red
        bg_color = "#ffebee"
    elif risk_level == "Medium":
        color = "#ff9800"  # Orange
        bg_color = "#fff8e1"
    else:
        color = "#4caf50"  # Green
        bg_color = "#e8f5e8"
    
    # Create expandable card
    with st.container():
        # Card header
        st.markdown(f"""
        <div style="
            background-color: {bg_color};
            border: 2px solid {color};
            border-radius: 12px;
            padding: 16px;
            margin: 8px 0;
        ">
            <div style="display: flex; align-items: center; margin-bottom: 12px;">
                <span style="font-size: 24px; margin-right: 12px;">{icon}</span>
                <h3 style="margin: 0; color: #1f1f1f;">{card_title}</h3>
            </div>
            <div style="margin: 8px 0;">
                <div style="
                    background-color: #f0f0f0;
                    border-radius: 10px;
                    height: 8px;
                    overflow: hidden;
                ">
                    <div style="
                        background-color: {color};
                        height: 100%;
                        width: {confidence}%;
                        transition: width 0.3s ease;
                    "></div>
                </div>
                <p style="margin: 8px 0 0 0; font-size: 14px; color: #666;">
                    {confidence}% confidence • {risk_level} priority
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Expandable details
        with st.expander(f"Learn more about {card_title}", expanded=False):
            st.write(f"**Description:** {description}")
            if 'detected_features' in data:
                st.write("**Key indicators detected:**")
                for feature, value in data['detected_features'].items():
                    st.write(f"• {feature.replace('_', ' ').title()}: {value}")

def display_action_categories(recommendations):
    """Display action categories with touch-friendly tiles"""
    
    # Create three columns for action categories
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🍎 Diet")
        create_action_tiles(recommendations['diet'], "diet")
    
    with col2:
        st.markdown("### 🏃 Lifestyle")
        create_action_tiles(recommendations['lifestyle'], "lifestyle")
    
    with col3:
        st.markdown("### 🩺 Medical")
        create_action_tiles(recommendations['medical'], "medical")
    
    # Action items section
    if recommendations.get('action_items'):
        st.markdown("### 📋 Priority Actions")
        for i, item in enumerate(recommendations['action_items'], 1):
            st.markdown(f"""
            <div style="
                background-color: #e3f2fd;
                border-left: 4px solid #2196f3;
                padding: 12px;
                margin: 8px 0;
                border-radius: 4px;
            ">
                <strong>{i}.</strong> {item}
            </div>
            """, unsafe_allow_html=True)

def create_action_tiles(recommendations, category):
    """Create action tiles for each category"""
    
    # Color scheme for categories
    colors = {
        'diet': '#4caf50',      # Green
        'lifestyle': '#2196f3', # Blue
        'medical': '#f44336'    # Red
    }
    
    color = colors.get(category, '#666')
    
    # Display top recommendations as tiles
    for rec in recommendations[:3]:  # Limit to top 3 per category
        st.markdown(f"""
        <div style="
            background-color: white;
            border: 2px solid {color};
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
            cursor: pointer;
            transition: all 0.2s ease;
        " onmouseover="this.style.backgroundColor='#f5f5f5'" 
           onmouseout="this.style.backgroundColor='white'">
            <p style="margin: 0; font-size: 14px; color: #333;">
                {rec}
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
