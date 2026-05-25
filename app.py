import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

# Set page config
st.set_page_config(
    page_title="🤖 AI Multi-Module Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .feature-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'feedback_data' not in st.session_state:
    st.session_state.feedback_data = []

# Load feedback data
def load_feedback():
    if os.path.exists('user_feedback.json'):
        with open('user_feedback.json', 'r') as f:
            return json.load(f)
    return []

def save_feedback(data):
    with open('user_feedback.json', 'w') as f:
        json.dump(data, f, indent=2)

# Main Header
st.markdown("""<h1 class='main-header'>🤖 AI Multi-Module Platform</h1>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📦 Modules", "5")
with col2:
    st.metric("🌍 Languages", "50+")
with col3:
    st.metric("⚡ Status", "Active")

st.divider()

# Sidebar for user info
with st.sidebar:
    st.header("👤 User Information")
    user_name = st.text_input("Your Name (Optional):", value=st.session_state.user_name)
    st.session_state.user_name = user_name
    
    st.markdown("---")
    st.markdown("### 📚 Available Modules")
    st.markdown("""
    - 🌍 **Language Translator**
    - 💬 **FAQ Chatbot**
    - 🎵 **Music Generator**
    - 👁️ **Object Detection**
    - 📊 **Analytics & Feedback**
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.info("💡 Each module's results can be downloaded and uploaded to Google Forms!")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌍 Translator", "💬 FAQ Chatbot", "🎵 Music Gen", "👁️ Detection", "📊 Analytics"])

# ==================== TAB 1: TRANSLATOR ====================
with tab1:
    st.header("🌍 Language Translator")
    st.write("Translate text between 50+ languages instantly")
    
    col1, col2 = st.columns(2)
    
    with col1:
        source_lang = st.selectbox(
            "Source Language:",
            ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Hindi", "Arabic"],
            key="source_lang"
        )
    
    with col2:
        target_lang = st.selectbox(
            "Target Language:",
            ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Hindi", "Arabic"],
            key="target_lang"
        )
    
    text_to_translate = st.text_area(
        "Enter text to translate:",
        placeholder="Type your text here...",
        height=150
    )
    
    if st.button("🔄 Translate", key="translate_btn"):
        if text_to_translate:
            with st.spinner("Translating..."):
                # Simulated translation
                translated_text = f"[Translated to {target_lang}] {text_to_translate}"
                st.success("✅ Translation Complete!")
                st.text_area("Translated Text:", value=translated_text, height=150, disabled=True)
                
                # Download button
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download Translation (TXT)",
                        data=translated_text,
                        file_name=f"translation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                
                # Save feedback
                feedback_data = load_feedback()
                feedback_data.append({
                    "timestamp": datetime.now().isoformat(),
                    "user": st.session_state.user_name or "Anonymous",
                    "module": "Translator",
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "text_length": len(text_to_translate),
                    "status": "success"
                })
                save_feedback(feedback_data)
        else:
            st.warning("⚠️ Please enter text to translate")

# ==================== TAB 2: FAQ CHATBOT ====================
with tab2:
    st.header("💬 FAQ Chatbot")
    st.write("Ask any questions and get instant answers")
    
    # FAQ Database
    faq_database = {
        "What is AI?": "Artificial Intelligence (AI) is the simulation of human intelligence by machines.",
        "How do I use this platform?": "Each tab represents a different AI feature. Fill in your inputs and click the action button.",
        "Can I download my results?": "Yes! Every module has a download button to export results.",
        "What languages are supported?": "We support 50+ languages for translation.",
        "How does object detection work?": "Object detection uses deep learning to identify and locate objects in images.",
        "Can I generate music in different styles?": "Yes! Our music generator supports multiple genres and customization.",
        "Is my data saved?": "We track usage for analytics, but don't store personal data.",
        "How accurate is the translation?": "Our translation model has 95%+ accuracy for common language pairs."
    }
    
    # Display chat history
    st.subheader("Chat History")
    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()
    
    chat_container = st.container(height=300, border=True)
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.write(f"**You:** {message['content']}")
            else:
                st.write(f"**Bot:** {message['content']}")
    
    # Question input
    st.subheader("Ask a Question")
    question = st.text_input("Type your question:", placeholder="e.g., How do I use this platform?")
    
    if st.button("🚀 Send", key="send_btn"):
        if question:
            # Find matching answer
            answer = None
            for faq_q, faq_a in faq_database.items():
                if question.lower() in faq_q.lower() or faq_q.lower() in question.lower():
                    answer = faq_a
                    break
            
            if not answer:
                answer = "I'm not sure about that. Please check the FAQ database or contact support."
            
            # Add to chat history
            st.session_state.chat_history.append({"role": "user", "content": question})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            
            # Save feedback
            feedback_data = load_feedback()
            feedback_data.append({
                "timestamp": datetime.now().isoformat(),
                "user": st.session_state.user_name or "Anonymous",
                "module": "FAQ Chatbot",
                "question": question,
                "answer_found": answer != "I'm not sure about that. Please check the FAQ database or contact support.",
                "status": "success"
            })
            save_feedback(feedback_data)
            
            st.rerun()
    
    # Quick suggestion buttons
    st.subheader("Popular Questions")
    cols = st.columns(2)
    popular_questions = list(faq_database.keys())[:4]
    for i, q in enumerate(popular_questions):
        col = cols[i % 2]
        if col.button(q, key=f"faq_{i}"):
            st.session_state.chat_history.append({"role": "user", "content": q})
            st.session_state.chat_history.append({"role": "assistant", "content": faq_database[q]})
            st.rerun()

# ==================== TAB 3: MUSIC GENERATOR ====================
with tab3:
    st.header("🎵 AI Music Generator")
    st.write("Create original music with customizable parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        genre = st.selectbox(
            "Choose Genre:",
            ["Classical", "Jazz", "Electronic", "Ambient", "Folk", "Pop"],
            key="music_genre"
        )
        tempo = st.slider("Tempo (BPM):", 60, 180, 120)
    
    with col2:
        mood = st.selectbox(
            "Choose Mood:",
            ["Happy", "Sad", "Energetic", "Calm", "Mysterious"],
            key="music_mood"
        )
        duration = st.slider("Duration (seconds):", 10, 120, 30)
    
    key = st.selectbox(
        "Musical Key:",
        ["C Major", "G Major", "D Major", "A Major", "E Major", "A Minor"],
        key="music_key"
    )
    
    if st.button("🎼 Generate Music", key="generate_music_btn"):
        with st.spinner("🎵 Creating music..."):
            st.success("✅ Music Generated Successfully!")
            
            # Create mock audio player
            st.info(f"🎵 Generated {genre} music in {key} ({tempo} BPM) - {duration}s")
            
            # Download options
            col1, col2, col3 = st.columns(3)
            with col1:
                st.download_button(
                    label="📥 Download (MP3)",
                    data=b"Mock MP3 Audio",
                    file_name=f"music_{genre}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                    mime="audio/mpeg"
                )
            with col2:
                st.download_button(
                    label="📥 Download (WAV)",
                    data=b"Mock WAV Audio",
                    file_name=f"music_{genre}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav",
                    mime="audio/wav"
                )
            with col3:
                st.download_button(
                    label="📥 Download (MIDI)",
                    data=b"Mock MIDI File",
                    file_name=f"music_{genre}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mid",
                    mime="audio/midi"
                )
            
            # Save feedback
            feedback_data = load_feedback()
            feedback_data.append({
                "timestamp": datetime.now().isoformat(),
                "user": st.session_state.user_name or "Anonymous",
                "module": "Music Generator",
                "genre": genre,
                "mood": mood,
                "tempo": tempo,
                "duration": duration,
                "key": key,
                "status": "success"
            })
            save_feedback(feedback_data)

# ==================== TAB 4: OBJECT DETECTION ====================
with tab4:
    st.header("👁️ Object Detection & Tracking")
    st.write("Detect and identify objects in images")
    
    detection_option = st.radio(
        "Choose input method:",
        ["📸 Upload Image", "🎥 Webcam", "🖼️ Sample Image"],
        key="detection_option"
    )
    
    if detection_option == "📸 Upload Image":
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["jpg", "jpeg", "png", "bmp"],
            key="image_upload"
        )
        
        if uploaded_file is not None:
            if st.button("🔍 Detect Objects", key="detect_btn"):
                with st.spinner("Analyzing image..."):
                    st.success("✅ Detection Complete!")
                    
                    # Display image
                    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
                    
                    # Mock detection results
                    st.subheader("📊 Detection Results")
                    detection_results = {
                        "Objects Detected": 5,
                        "Person": "2 (95% confidence)",
                        "Car": "1 (92% confidence)",
                        "Tree": "1 (88% confidence)",
                        "Building": "1 (91% confidence)"
                    }
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        for key, value in detection_results.items():
                            st.write(f"**{key}:** {value}")
                    
                    with col2:
                        st.metric("Total Objects", detection_results["Objects Detected"])
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Detection Report (CSV)",
                        data=json.dumps(detection_results, indent=2),
                        file_name=f"detection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                    
                    # Save feedback
                    feedback_data = load_feedback()
                    feedback_data.append({
                        "timestamp": datetime.now().isoformat(),
                        "user": st.session_state.user_name or "Anonymous",
                        "module": "Object Detection",
                        "objects_detected": detection_results["Objects Detected"],
                        "file_name": uploaded_file.name,
                        "status": "success"
                    })
                    save_feedback(feedback_data)
    
    elif detection_option == "🎥 Webcam":
        st.info("📷 Webcam feature requires camera access. Enable it in your browser.")
        if st.button("📹 Start Webcam Detection"):
            st.success("✅ Webcam detection started!")
            st.write("[Webcam stream would appear here]")
    
    else:
        st.info("🖼️ Using sample image for demonstration")
        col1, col2, col3 = st.columns(3)
        with col2:
            st.write("[Sample Image Would Display Here]")

# ==================== TAB 5: ANALYTICS ====================
with tab5:
    st.header("📊 Analytics & Feedback")
    
    # Load feedback data
    feedback_data = load_feedback()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📈 Total Interactions", len(feedback_data))
    with col2:
        modules_used = set([f.get("module", "") for f in feedback_data if f.get("module")])
        st.metric("🎯 Modules Used", len(modules_used))
    with col3:
        st.metric("✅ Success Rate", "100%")
    
    st.divider()
    
    # Usage chart
    if feedback_data:
        st.subheader("📊 Usage Statistics")
        
        # Group by module
        module_counts = {}
        for item in feedback_data:
            module = item.get("module", "Unknown")
            module_counts[module] = module_counts.get(module, 0) + 1
        
        if module_counts:
            df = pd.DataFrame(list(module_counts.items()), columns=["Module", "Count"])
            st.bar_chart(df.set_index("Module"))
    
    st.divider()
    
    # User feedback form
    st.subheader("📝 Send Feedback")
    
    feedback_module = st.selectbox(
        "Which module did you use?",
        ["Translator", "FAQ Chatbot", "Music Generator", "Object Detection", "General Feedback"]
    )
    
    feedback_rating = st.slider(
        "Rate your experience:",
        1, 5, 4,
        format="%d ⭐"
    )
    
    feedback_text = st.text_area(
        "Share your feedback:",
        placeholder="Tell us what you think...",
        height=100
    )
    
    if st.button("📤 Submit Feedback", key="submit_feedback"):
        feedback_data = load_feedback()
        feedback_data.append({
            "timestamp": datetime.now().isoformat(),
            "user": st.session_state.user_name or "Anonymous",
            "type": "User Feedback",
            "module": feedback_module,
            "rating": feedback_rating,
            "feedback": feedback_text
        })
        save_feedback(feedback_data)
        st.success("✅ Thank you for your feedback!")
    
    st.divider()
    
    # Recent activity
    st.subheader("📋 Recent Activity")
    if feedback_data:
        recent = feedback_data[-10:]  # Last 10 items
        for item in reversed(recent):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**{item.get('module', 'Unknown')}**")
            with col2:
                st.write(f"by {item.get('user', 'Anonymous')}")
            with col3:
                st.write(item.get('timestamp', '')[:10])
    else:
        st.info("No activity yet. Start using the platform!")
    
    st.divider()
    
    # Export all data
    st.subheader("💾 Export Data")
    if st.button("📥 Download All Feedback (JSON)"):
        st.download_button(
            label="📥 Download Feedback Data",
            data=json.dumps(feedback_data, indent=2),
            file_name=f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    if st.button("📥 Download All Feedback (CSV)"):
        df = pd.DataFrame(feedback_data)
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Feedback (CSV)",
            data=csv,
            file_name=f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🚀 Powered by AI")
with col2:
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
with col3:
    st.caption("✨ Built for Google Forms Integration")
