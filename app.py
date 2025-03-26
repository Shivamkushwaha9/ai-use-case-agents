import streamlit as st
import asyncio
from main import AIUseCaseGenerator
import json
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="AI Use Case Generator", layout="wide")

if 'proposal' not in st.session_state:
    st.session_state.proposal = None

st.title("🤖 AI Use Case Generator")
st.markdown("""
This tool is a Multi-Agent architecture system that generates relevant AI and Generative AI (GenAI) use cases for a given Company or Industry.
The system will conduct market research, understand the industry and product, and provide resource assets for AI/ML solutions, focusing on enhancing operations and customer experiences.
Enter a company name below to get started!
""")

# API Key
api_key = os.getenv("GOOGLE_API_KEY")

# Company input
company_name = st.text_input("Enter Company Name:", placeholder="e.g., Tesla")

# Generate button
if st.button("Generate Use Cases"):
    if not api_key:
        st.error("Please enter your Google API Key")
    elif not company_name:
        st.error("Please enter a company name")
    else:
        with st.spinner("Generating AI use cases... This might take a minute..."):
            try:
                generator = AIUseCaseGenerator(api_key)
                st.session_state.proposal = asyncio.run(generator.generate_proposal(company_name))
                st.success("Generation complete!")
            except Exception as e:
                st.error(f"Error generating proposal: {str(e)}")

# Displaying results
if st.session_state.proposal:
    # Create tabs for different sections
    company_tab, usecase_tab, resource_tab = st.tabs(["Company Analysis", "Use Cases", "Resources"])
    
    with company_tab:
        st.header("Company Analysis")
        for key, value in st.session_state.proposal["company_analysis"].items():
            st.subheader(key.replace('_', ' ').title())
            st.write(value)
    
    with usecase_tab:
        st.header("AI/ML Use Cases")
        for use_case in st.session_state.proposal["use_cases"]:
            with st.expander(f"📌 {use_case['title']}", expanded=True):
                st.markdown("**Description:**")
                st.write(use_case['description'])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Benefits:**")
                    st.write(use_case['benefits'])
                    st.markdown("**Complexity:**")
                    st.write(use_case['complexity'])
                
                with col2:
                    st.markdown("**ROI Impact:**")
                    st.write(use_case['roi_impact'])
                    st.markdown("**Technologies:**")
                    st.write(use_case['technologies'])
    
    with resource_tab:
        st.header("Resources & References")
        for use_case_title, resources in st.session_state.proposal["resources"].items():
            with st.expander(f"🔍 Resources for: {use_case_title}", expanded=True):
                for category, links in resources.items():
                    st.subheader(category.replace('_', ' ').title())
                    if isinstance(links, list):
                        for link in links:
                            st.markdown(f"- {link}")
                    else:
                        st.write(links)

    #download buttons
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download JSON",
            data=json.dumps(st.session_state.proposal, indent=2),
            file_name=f"{company_name}_proposal.json",
            mime="application/json"
        )
    
    with col2:
        # Create markdown content
        markdown_content = f"""# AI Use Case Proposal for {company_name}\n\n"""
        # Adding company analysis
        markdown_content += "## Company Analysis\n"
        for key, value in st.session_state.proposal["company_analysis"].items():
            markdown_content += f"### {key.replace('_', ' ').title()}\n{value}\n\n"
        
        # Add use cases
        markdown_content += "## Use Cases\n"
        for use_case in st.session_state.proposal["use_cases"]:
            markdown_content += f"### {use_case['title']}\n"
            markdown_content += f"**Description:** {use_case['description']}\n\n"
            markdown_content += f"**Benefits:** {use_case['benefits']}\n\n"
            markdown_content += f"**Complexity:** {use_case['complexity']}\n\n"
            markdown_content += f"**ROI Impact:** {use_case['roi_impact']}\n\n"
            markdown_content += f"**Technologies:** {use_case['technologies']}\n\n"
            markdown_content += "---\n\n"
        
        st.download_button(
            label="Download Markdown",
            data=markdown_content,
            file_name=f"{company_name}_proposal.md",
            mime="text/markdown"
        )

# Footer here
st.markdown("---")