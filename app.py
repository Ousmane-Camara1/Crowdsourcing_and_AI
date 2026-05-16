import gradio as gr
import os
from main import run_voice_survey

def start_survey(survey_selection, voice_selection):
    # Map friendly UI names directly to your specific JSON tracks
    survey_map = {
        "Community Health Survey": "data/community_health.json",
        "University Mental Health Survey": "data/university_mental_health.json"
    }
    
    file_path = survey_map.get(survey_selection)
    
    if not os.path.exists(file_path):
        return f"Error: Configuration file {file_path} missing."
        
    # Standardize selected voice back into plain text string arguments
    gender = "female" if "Samantha" in voice_selection else "male"
    
    # Run the dynamic instance
    run_voice_survey(file_path, gender)
    return f"Success: {survey_selection} completed using {voice_selection} voice profile."

# Build the Gradio dashboard interface
with gr.Blocks() as app:
    gr.Markdown("# Trust-Centric Voice AI Crowdsourcing Hub")
    gr.Markdown("Configure target parameters. Interactions run dynamically through host local hardware audio channels.")

    with gr.Row():
        survey_dropdown = gr.Dropdown(
            choices=["Community Health Survey", "University Mental Health Survey"], 
            value="Community Health Survey", 
            label="Active Survey Schema"
        )
        voice_dropdown = gr.Radio(
            choices=["Female Profile (Samantha)", "Male Profile (Alex)"], 
            value="Female Profile (Samantha)", 
            label="SSML Synthesizer Configuration"
        )

    start_btn = gr.Button("Initialize Voice Survey Pipeline", variant="primary")
    output = gr.Textbox(label="Runtime Callback Exception Logs")

    start_btn.click(
        fn=start_survey, 
        inputs=[survey_dropdown, voice_dropdown], 
        outputs=output
    )

app.launch()