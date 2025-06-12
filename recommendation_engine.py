class RecommendationEngine:
    """Generates personalized recommendations based on skin analysis results"""
    
    def __init__(self):
        # Define recommendation templates for each condition
        self.condition_recommendations = {
            'Acanthosis Nigricans (Insulin-related Hyperpigmentation)': {
                'lifestyle': [
                    'Maintain regular exercise routine (30+ minutes daily) to improve insulin sensitivity',
                    'Prioritize 7-9 hours of quality sleep to support metabolic health',
                    'Practice stress management techniques like meditation or yoga',
                    'Monitor weight and work towards healthy BMI if needed'
                ],
                'diet': [
                    'Reduce refined sugar and simple carbohydrate intake',
                    'Focus on low-glycemic index foods (vegetables, whole grains, lean proteins)',
                    'Increase fiber intake with fruits, vegetables, and legumes',
                    'Consider intermittent fasting under medical supervision',
                    'Limit processed foods and sugary beverages'
                ],
                'medical': [
                    'Schedule blood glucose and HbA1c testing',
                    'Consider consultation with an endocrinologist',
                    'Discuss insulin resistance screening with your physician',
                    'Monitor blood pressure regularly'
                ]
            },
            'Xanthelasma (Cholesterol Deposits)': {
                'lifestyle': [
                    'Engage in regular cardiovascular exercise',
                    'Quit smoking if applicable (smoking worsens lipid profiles)',
                    'Maintain healthy weight through balanced diet and exercise',
                    'Limit alcohol consumption'
                ],
                'diet': [
                    'Adopt a heart-healthy diet rich in omega-3 fatty acids',
                    'Increase soluble fiber intake (oats, beans, apples)',
                    'Choose lean proteins and limit saturated fats',
                    'Include nuts, seeds, and olive oil for healthy fats',
                    'Reduce trans fats and processed foods'
                ],
                'medical': [
                    'Schedule comprehensive lipid panel testing',
                    'Consider cardiology consultation for cardiovascular risk assessment',
                    'Discuss statin therapy if appropriate',
                    'Monitor blood pressure and diabetes risk factors'
                ]
            },
            'Dry/Dehydrated Skin': {
                'lifestyle': [
                    'Increase daily water intake (8-10 glasses per day)',
                    'Use a humidifier in dry environments',
                    'Take shorter, lukewarm showers to preserve skin oils',
                    'Apply moisturizer immediately after bathing',
                    'Protect skin from harsh weather conditions'
                ],
                'diet': [
                    'Consume foods rich in omega-3 fatty acids (fish, walnuts, flaxseed)',
                    'Include antioxidant-rich fruits and vegetables',
                    'Consider vitamin E and vitamin C supplementation',
                    'Limit caffeine and alcohol which can contribute to dehydration'
                ],
                'medical': [
                    'Consider dermatologist consultation for persistent dryness',
                    'Rule out underlying conditions like thyroid disorders',
                    'Discuss prescription moisturizers or treatments if needed'
                ]
            },
            'Inflammatory Rash': {
                'lifestyle': [
                    'Identify and avoid potential allergens or irritants',
                    'Use gentle, fragrance-free skincare products',
                    'Wear breathable, natural fiber clothing',
                    'Manage stress levels through relaxation techniques',
                    'Keep affected areas clean and dry'
                ],
                'diet': [
                    'Consider an anti-inflammatory diet rich in omega-3s',
                    'Identify potential food triggers (dairy, gluten, nuts)',
                    'Increase intake of anti-inflammatory foods (turmeric, ginger, leafy greens)',
                    'Stay well-hydrated'
                ],
                'medical': [
                    'Schedule dermatologist appointment for proper diagnosis',
                    'Consider allergy testing if recurrent',
                    'Discuss topical or oral anti-inflammatory treatments',
                    'Rule out autoimmune conditions if widespread'
                ]
            },
            'Seborrheic Dermatitis': {
                'lifestyle': [
                    'Use gentle, anti-fungal shampoos and cleansers',
                    'Manage stress levels effectively',
                    'Avoid harsh skincare products with alcohol',
                    'Maintain good hygiene without over-washing'
                ],
                'diet': [
                    'Limit sugar and refined carbohydrates',
                    'Include probiotics and fermented foods',
                    'Consider zinc and B-vitamin supplementation',
                    'Reduce inflammatory foods'
                ],
                'medical': [
                    'Consult dermatologist for antifungal treatments',
                    'Discuss medicated shampoos or topical treatments',
                    'Rule out underlying immune system issues'
                ]
            },
            'Age Spots/Sun Damage': {
                'lifestyle': [
                    'Apply broad-spectrum SPF 30+ sunscreen daily',
                    'Wear protective clothing and wide-brimmed hats',
                    'Seek shade during peak sun hours (10am-4pm)',
                    'Use antioxidant-rich skincare products'
                ],
                'diet': [
                    'Consume antioxidant-rich foods (berries, dark leafy greens)',
                    'Include vitamin C and E rich foods',
                    'Consider lycopene-rich foods (tomatoes, watermelon)',
                    'Stay well-hydrated for skin health'
                ],
                'medical': [
                    'Schedule regular dermatological skin checks',
                    'Discuss treatment options (chemical peels, laser therapy)',
                    'Monitor for changes in existing spots',
                    'Consider prescription retinoids for prevention'
                ]
            }
        }
        
        # General recommendations that apply to most conditions
        self.general_recommendations = {
            'lifestyle': [
                'Maintain consistent sleep schedule of 7-9 hours nightly',
                'Practice regular stress management techniques',
                'Stay physically active with regular exercise',
                'Avoid smoking and limit alcohol consumption'
            ],
            'diet': [
                'Follow a balanced, nutrient-rich diet',
                'Stay adequately hydrated throughout the day',
                'Limit processed foods and excess sugar',
                'Include variety of colorful fruits and vegetables'
            ],
            'medical': [
                'Schedule regular check-ups with your primary care physician',
                'Keep a skin health diary to track changes',
                'Follow up on any concerning or persistent symptoms',
                'Maintain updated health records and medication lists'
            ]
        }
    
    def generate_recommendations(self, analysis_results):
        """
        Generate personalized recommendations based on analysis results
        
        Args:
            analysis_results: Dictionary containing condition analysis results
            
        Returns:
            dict: Categorized recommendations and action items
        """
        recommendations = {
            'lifestyle': set(),
            'diet': set(),
            'medical': set(),
            'action_items': []
        }
        
        # Process each detected condition
        high_confidence_conditions = []
        
        for condition, data in analysis_results.items():
            confidence = data['confidence']
            risk_level = data['risk_level']
            
            # Add condition-specific recommendations based on confidence
            if confidence >= 40:  # Medium to high confidence
                if condition in self.condition_recommendations:
                    condition_recs = self.condition_recommendations[condition]
                    
                    # Add lifestyle recommendations
                    for rec in condition_recs['lifestyle'][:2]:  # Top 2 recommendations
                        recommendations['lifestyle'].add(rec)
                    
                    # Add dietary recommendations
                    for rec in condition_recs['diet'][:3]:  # Top 3 recommendations
                        recommendations['diet'].add(rec)
                    
                    # Add medical recommendations
                    for rec in condition_recs['medical']:
                        recommendations['medical'].add(rec)
                
                # Track high-confidence conditions for action items
                if confidence >= 60:
                    high_confidence_conditions.append((condition, confidence, risk_level))
        
        # Add general recommendations
        recommendations['lifestyle'].update(self.general_recommendations['lifestyle'][:2])
        recommendations['diet'].update(self.general_recommendations['diet'][:2])
        recommendations['medical'].update(self.general_recommendations['medical'][:2])
        
        # Convert sets to lists
        for category in ['lifestyle', 'diet', 'medical']:
            recommendations[category] = list(recommendations[category])
        
        # Generate action items for high-confidence findings
        recommendations['action_items'] = self._generate_action_items(high_confidence_conditions)
        
        return recommendations
    
    def _generate_action_items(self, high_confidence_conditions):
        """Generate specific action items based on high-confidence findings"""
        action_items = []
        
        # Sort by confidence level
        high_confidence_conditions.sort(key=lambda x: x[1], reverse=True)
        
        for condition, confidence, risk_level in high_confidence_conditions:
            if 'Acanthosis Nigricans' in condition:
                action_items.append(
                    f"Schedule blood glucose testing within 2 weeks (detected {confidence}% confidence insulin-related changes)"
                )
            elif 'Xanthelasma' in condition:
                action_items.append(
                    f"Request lipid panel from your physician (detected {confidence}% confidence cholesterol deposits)"
                )
            elif 'Inflammatory Rash' in condition and risk_level == "High":
                action_items.append(
                    f"Schedule dermatologist appointment within 1-2 weeks for {confidence}% confidence inflammatory condition"
                )
            elif 'Age Spots' in condition and confidence >= 70:
                action_items.append(
                    f"Schedule skin cancer screening with dermatologist (significant sun damage detected)"
                )
        
        # Add general action items
        if high_confidence_conditions:
            action_items.append("Take photos to track any changes in skin appearance over time")
            action_items.append("Discuss these findings with your healthcare provider at your next appointment")
        
        return action_items
