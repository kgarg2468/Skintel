# AI-Powered Skin Health Analysis App

## Overview
An AI-powered skin health analysis app using Streamlit that processes uploaded photos to detect skin conditions and provide health recommendations. The app uses computer vision and machine learning to analyze skin features and generate personalized health insights.

## Project Architecture
- **Frontend**: Streamlit web interface with file upload and results display
- **Image Processing**: OpenCV/PIL pipeline for skin feature extraction
- **AI Analysis**: Feature-based skin condition detection using weighted scoring models
- **Recommendations**: Rule-based recommendation engine generating lifestyle, diet, and medical advice
- **Deployment**: Configured for Replit with proper port settings (5000)

## User Preferences
- Simple, everyday language - user is non-technical
- Dashboard-style results interface with visual cards and progress indicators
- Mobile-responsive design with clear visual hierarchy
- Color-coded risk levels (red/orange/green) with accessibility considerations

## Recent Changes
**June 14, 2025**
- Received new UI/UX specification for redesigned results screen
- Need to implement: summary banner, condition dashboard tiles, action categories, traffic-light color scheme
- Current implementation uses basic list format - needs complete redesign to match specification

## Technical Stack
- Python 3.11
- Streamlit for web interface
- OpenCV for image processing
- NumPy/PIL for image manipulation
- Custom modules: ImageProcessor, SkinAnalyzer, RecommendationEngine

## Current Status
App is running and functional with basic results display. Ready to implement new dashboard-style UI according to provided specifications.