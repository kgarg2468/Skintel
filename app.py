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
            st.image(image, caption=f"Size: {image.size[0]}x{image.size[1]} pixels", use_column_width=True)
            
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
    """Display analysis results and recommendations"""
    
    st.success("✅ Analysis Complete!")
    
    # Analysis Results Section
    st.header("📊 Analysis Results")
    
    # Preprocessing summary
    with st.expander("🔧 Image Processing Summary", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Original Size", f"{preprocessing_info['original_size'][0]}x{preprocessing_info['original_size'][1]}")
        with col2:
            st.metric("Processed Size", f"{preprocessing_info['processed_size'][0]}x{preprocessing_info['processed_size'][1]}")
        with col3:
            st.metric("Skin Coverage", f"{preprocessing_info['skin_coverage']:.1f}%")
    
    # Detected conditions
    st.subheader("🔍 Detected Skin Conditions")
    
    # Sort conditions by confidence score
    sorted_conditions = sorted(analysis_results.items(), key=lambda x: x[1]['confidence'], reverse=True)
    
    for condition, data in sorted_conditions:
        confidence = data['confidence']
        description = data['description']
        risk_level = data['risk_level']
        
        # Color code based on risk level
        if risk_level == "High":
            color = "🔴"
        elif risk_level == "Medium":
            color = "🟡"
        else:
            color = "🟢"
        
        # Display condition card
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"{color} **{condition}**")
                st.write(f"*{description}*")
            
            with col2:
                st.metric("Confidence", f"{confidence}%")
            
            with col3:
                st.write(f"Risk: **{risk_level}**")
            
            st.divider()
    
    # Recommendations Section
    st.header("💡 Personalized Recommendations")
    
    tab1, tab2, tab3 = st.tabs(["🏃 Lifestyle", "🥗 Diet", "🏥 Medical"])
    
    with tab1:
        st.subheader("Lifestyle Recommendations")
        for rec in recommendations['lifestyle']:
            st.write(f"• {rec}")
    
    with tab2:
        st.subheader("Dietary Recommendations")
        for rec in recommendations['diet']:
            st.write(f"• {rec}")
    
    with tab3:
        st.subheader("Medical Recommendations")
        for rec in recommendations['medical']:
            st.write(f"• {rec}")
    
    # Action items
    if recommendations.get('action_items'):
        st.header("📋 Recommended Action Items")
        for i, item in enumerate(recommendations['action_items'], 1):
            st.write(f"{i}. {item}")
    
    # Download report option
    st.header("📥 Export Report")
    if st.button("Generate PDF Report", type="secondary"):
        st.info("PDF generation feature will be available in a future update. For now, you can screenshot or print this page.")

if __name__ == "__main__":
    main()
