import google.generativeai as genai
import os
from datetime import datetime, UTC


def format_data(data, data_type):
    if data_type == "patient_data":
        return {
            "Wound Type": data['wound']['type'],
            "Location": data['wound']['location'],
            "Severity": data['wound']['severity'],
            "Infected": data['wound']['infected'],
            "Patient Age": data['age'],
            "Size": data['wound']['size'],
            "Treatment": data['wound']['treatment'],
        }
    elif data_type == "health_data":
        return {
            "Time": float(data['Time']),
            "Wound Temperature": float(data['Wound Temperature']),
            "Wound pH": float(data['Wound pH']),
            "Moisture Level": float(data['Moisture Level']),
            "Drug Release": float(data['Drug Release']),
        }


# Healing time left
def calculate_healing_time(prediction, created_at):                        
    days_elapsed = (datetime.now(UTC) - created_at.replace(tzinfo=UTC)).days
    healing_time_left = max(0, prediction - days_elapsed)

    return healing_time_left

# Configure Google Generative AI
genai.configure(api_key=os.environ.get('GENAI_API_KEY'))

def analyze_patient(patient):
    try:
        # Create the prompt
        prompt = f"""Analyze the following wound data and provide concise summary and recommendations for treatment methods, medicine, and healthcare practices. Format your response as three bulleted paragraphs: Summary (summarize patient condition), 'Treatment' (medicine recommendations directed for the wound, each recommendation is made short in a bullet point), and 'Expectations' (what the patient should expect from the treatment). Make your response as concise as possible, maximum of 150 words, skip introductions and conclusions, let the output be only the paragraphs and nothing else.

Here's the data:

Wound Type,Location,Severity,Infected,Patient Age,Wound Size (cm),Treatment Given,Patient Gender,Healing Time Left (days)
{patient['wound']['type']},{patient['wound']['location']},{patient['wound']['severity']},{patient['wound']['infected']},{patient['age']},{patient['wound']['size']},{patient['wound']['treatment']},{patient['gender']},{patient['healing_time_left']}"""

        # generate patient data analysis
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        print(response.text)

        if not response or not response.text:
            return {"error": "Failed to generate analysis"}
            
        return {
            "analysis": response.text,
        }
    
    except Exception as e:
        print(f"Error in AI analysis: {str(e)}")
        return {"error": str(e)}
    



# Helper function to check allowed file extensions
def allowed_file(filename, allowed_extensions):
    ext = os.path.splitext(filename)[1].lower()
    return ext if ext in allowed_extensions else False