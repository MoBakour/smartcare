import google.generativeai as genai
import os

# Configure Google Generative AI
genai.configure(api_key=os.environ.get('GENAI_API_KEY'))

def analyze_patient(patient):
    try:
        # Create the prompt
        prompt = f"""Analyze the following wound data and provide concise recommendations for treatment methods, medicine, and healthcare practices. Format your response as two bulleted paragraphs: 'Treatment' (medicine recommendations) and 'Practices' (approaches and ways to handle patient) Make your response as concise as possible, maximum of 100 words, skip introductions and conclusions.

Here's the data:

Wound Type,Location,Severity,Infected,Patient Age,Wound Size (cm),Treatment Given,Patient Gender
{patient['wound']['type']},{patient['wound']['location']},{patient['wound']['severity']},{patient['wound']['infected']},{patient['age']},{patient['wound']['size']},{patient['wound']['treatment']},{patient['gender']}"""

        # generate patient data analysis
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            return {"error": "Failed to generate analysis"}
            
        return {
            "analysis": response.text,
        }
    
    except Exception as e:
        print(f"Error in AI analysis: {str(e)}")
        return {"error": str(e)}