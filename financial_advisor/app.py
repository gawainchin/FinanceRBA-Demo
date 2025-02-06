import gradio as gr
from framework import get_financial_advice

def run_advisor(query, age, risk_tolerance):
    """Handle interface between Gradio and CrewAI framework"""
    client_profile = {
        "age": int(age),
        "risk_tolerance": risk_tolerance.lower()
    }
    return get_financial_advice(query, client_profile)

interface = gr.Interface(
    fn=run_advisor,
    inputs=[
        gr.Textbox(label="Your financial question", placeholder="e.g. How should I allocate my retirement investments?"),
        gr.Number(label="Your age", minimum=18, maximum=100),
        gr.Dropdown(label="Risk tolerance", choices=["Low", "Medium", "High"])
    ],
    outputs=gr.Textbox(label="Financial Advice", lines=10),
    title="AI Financial Advisor",
    description="Get personalized financial advice from our AI expert team",
    allow_flagging="never"
)

if __name__ == "__main__":
    interface.launch(share=True) 