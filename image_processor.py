import numpy as np
import cv2
from PIL import Image
import io

class ImageProcessor:
    """Handles image preprocessing and feature extraction for skin analysis"""
    
    def __init__(self):
        self.target_size = (224, 224)
        self.skin_hsv_lower = np.array([0, 20, 70])
        self.skin_hsv_upper = np.array([20, 255, 255])
    
    def preprocess_image(self, pil_image):
        """
        Preprocess the uploaded image for analysis
        
        Args:
            pil_image: PIL Image object
            
        Returns:
            tuple: (processed_image_array, preprocessing_info)
        """
        # Convert PIL to OpenCV format
        img_array = np.array(pil_image)
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img_bgr = img_array
        
        original_size = img_bgr.shape[:2]
        
        # Resize image to target size
        img_resized = cv2.resize(img_bgr, self.target_size)
        
        # Convert to HSV for skin detection
        img_hsv = cv2.cvtColor(img_resized, cv2.COLOR_BGR2HSV)
        
        # Create skin mask
        skin_mask = cv2.inRange(img_hsv, self.skin_hsv_lower, self.skin_hsv_upper)
        
        # Calculate skin coverage percentage
        skin_coverage = (np.count_nonzero(skin_mask) / (self.target_size[0] * self.target_size[1])) * 100
        
        # Apply slight gaussian blur for noise reduction
        img_processed = cv2.GaussianBlur(img_resized, (3, 3), 0)
        
        # Normalize pixel values to [0, 1]
        img_normalized = img_processed.astype(np.float32) / 255.0
        
        # Prepare preprocessing info
        preprocessing_info = {
            'original_size': original_size,
            'processed_size': self.target_size,
            'skin_coverage': skin_coverage,
            'normalization': 'Applied [0,1] scaling'
        }
        
        return img_normalized, preprocessing_info
    
    def extract_features(self, processed_image):
        """
        Extract relevant features from the processed image
        
        Args:
            processed_image: Normalized image array
            
        Returns:
            dict: Dictionary containing extracted features
        """
        # Convert back to uint8 for feature extraction
        img_uint8 = (processed_image * 255).astype(np.uint8)
        
        # Convert to different color spaces for analysis
        img_rgb = cv2.cvtColor(img_uint8, cv2.COLOR_BGR2RGB)
        img_hsv = cv2.cvtColor(img_uint8, cv2.COLOR_BGR2HSV)
        img_lab = cv2.cvtColor(img_uint8, cv2.COLOR_BGR2LAB)
        
        features = {}
        
        # Color distribution features
        features['mean_rgb'] = np.mean(img_rgb, axis=(0, 1))
        features['std_rgb'] = np.std(img_rgb, axis=(0, 1))
        features['mean_hsv'] = np.mean(img_hsv, axis=(0, 1))
        features['mean_lab'] = np.mean(img_lab, axis=(0, 1))
        
        # Texture features using Local Binary Pattern approximation
        gray = cv2.cvtColor(img_uint8, cv2.COLOR_BGR2GRAY)
        
        # Calculate contrast and homogeneity
        features['contrast'] = np.std(gray)
        features['brightness'] = np.mean(gray)
        
        # Edge detection for texture analysis
        edges = cv2.Canny(gray, 50, 150)
        features['edge_density'] = np.count_nonzero(edges) / (gray.shape[0] * gray.shape[1])
        
        # Color uniformity
        features['color_variance'] = np.var(img_rgb)
        
        # Yellowness index (potential xanthelasma indicator)
        b_channel = img_lab[:, :, 2]  # b* channel in LAB
        features['yellowness'] = np.mean(b_channel[b_channel > 128])
        
        # Darkness patterns (potential hyperpigmentation)
        dark_threshold = 0.3 * 255
        dark_pixels = gray < dark_threshold
        features['dark_pixel_ratio'] = np.count_nonzero(dark_pixels) / (gray.shape[0] * gray.shape[1])
        
        # Redness analysis (potential inflammation)
        r_channel = img_rgb[:, :, 0]
        g_channel = img_rgb[:, :, 1]
        b_channel = img_rgb[:, :, 2]
        redness_index = (r_channel.astype(float) - g_channel.astype(float)) / (r_channel.astype(float) + g_channel.astype(float) + 1e-6)
        features['redness_index'] = np.mean(redness_index)
        
        # Dryness indicators (texture roughness)
        features['texture_roughness'] = self._calculate_roughness(gray)
        
        return features
    
    def _calculate_roughness(self, gray_image):
        """Calculate texture roughness as a dryness indicator"""
        # Use Sobel operators to detect texture variations
        sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
        
        # Calculate magnitude
        magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        
        # Return normalized roughness score
        return np.mean(magnitude) / 255.0
