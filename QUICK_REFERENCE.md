# ⚡ Quick Reference Guide

## 🚀 Quick Start (30 seconds)

### Windows
```bash
setup.bat && run_app.bat
```

### Mac/Linux
```bash
bash setup.sh && bash run_app.sh
```

**Opens:** http://localhost:8501

---

## 🎯 5 Modules at a Glance

### 🌍 Translator
- Select languages → Enter text → Click translate → Download
- Output: `.txt` file

### 💬 FAQ Chatbot
- Type question or click suggestion → Get answer → Chat history saved
- Auto-learns from feedback

### 🎵 Music Generator
- Choose genre, mood, tempo → Generate → Download (MP3/WAV/MIDI)
- AI composition engine

### 👁️ Object Detection
- Upload image → Detect objects → View confidence scores → Download report
- Supports PNG, JPG, BMP

### 📊 Analytics
- View usage stats → Submit feedback → Export data
- Download: JSON/CSV

---

## 📋 Google Forms Integration

1. **Use feature** → Get result
2. **Click Download** → Save file
3. **Open Google Form** → Upload/paste result
4. **Submit form** ✅

**Detailed:** See [GOOGLE_FORM_GUIDE.md](GOOGLE_FORM_GUIDE.md)

---

## 🔧 Common Commands

### Start App
```bash
streamlit run app.py
```

### Run on Different Port
```bash
streamlit run app.py --server.port 8502
```

### Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate.bat

# Mac/Linux
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### View All Installed Packages
```bash
pip list
```

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | [Download Python](https://www.python.org/) |
| "Module not found" | `pip install -r requirements.txt --force-reinstall` |
| "Port in use" | `streamlit run app.py --server.port 8502` |
| "Permission denied" | `chmod +x setup.sh run_app.sh` |
| "venv not found" | `python -m venv venv` then activate |
| App won't open | Check browser at `http://localhost:8501` |
| Slow performance | Check RAM (need 4GB+) |

---

## 📁 Important Files

```
app.py              ← RUN THIS
requirements.txt    ← Dependencies
setup.bat/.sh       ← Install
run_app.bat/.sh     ← Quick run
user_feedback.json  ← Auto data
```

---

## 🎓 First Time Users

1. ✅ Run `setup.bat` or `bash setup.sh`
2. ✅ Run `run_app.bat` or `bash run_app.sh`
3. ✅ Try each of the 5 modules
4. ✅ Download a result
5. ✅ Submit feedback

---

## 📊 Data Files

- **user_feedback.json** - Auto-created, tracks all interactions
- **Downloads/** - Your downloaded files go here
- **venv/** - Virtual environment (created by setup)

---

## 🌐 Online Deployment

### Streamlit Cloud (Fastest)
1. Push to GitHub
2. https://share.streamlit.io
3. Select repo → Deploy
4. Get public URL

### Docker
```bash
docker-compose up
```

---

## 💾 Backup & Export

### Export All Feedback
```bash
# JSON format
streamlit run app.py
# Then use Analytics tab → Download

# Or directly:
cp user_feedback.json backup_$(date +%Y%m%d).json
```

---

## 🔐 Security

✅ **All processing is local**
✅ **No data sent to external servers**
✅ **Data stored locally in JSON**
✅ **Export/backup anytime**
✅ **No login required**

---

## 📞 Need More Help?

- **Setup issues?** → [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Google Forms?** → [GOOGLE_FORM_GUIDE.md](GOOGLE_FORM_GUIDE.md)
- **Main docs?** → [README.md](README.md)

---

**✨ You're all set! Start using the platform now!** 🚀
