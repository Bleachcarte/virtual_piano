# virtual_piano
# 🎺 Virtual Piano with Hand Tracking

A computer vision project that turns your webcam into a responsive two-handed virtual piano using MediaPipe and OpenCV. Detects finger taps and plays corresponding notes in real-time.

---

## ✨ Features

* 👋 **Two-Handed Play**: Supports both left and right hand tracking.
* 🎯 **Finger Detection**: Tracks thumb, index, and middle fingers.
* 🖼️ **Visual Feedback**: Keys highlight on press; notes can be visualized.
* 🎵 **Real-Time Sound**: Plays corresponding .wav sounds using pygame.
* 🎺 **Responsive Layout**: Adapts keyboard to screen size.
* 🎨 **Custom Key Styling**: Includes black and white keys, customizable width.

---

## 📦 Dependencies

* Python 3.13+
* OpenCV
* MediaPipe
* Pygame

Install with:

```bash
pip install mediapipe opencv-contrib-python pygame
```

---

## 🚀 How to Run

```bash
python virtual_piano.py
```

Use your webcam. Tap the air above the keys to "press" a piano note.

---

## 🗂️ Folder Structure

```
virtual-piano/
│
├── virtual_piano.py         # Main app loop
├── piano_sounds/            # .wav files for each key
├── utils.py                 # Helper functions (optional)
├── README.md
└── .gitignore
```

---

## ✅ To-Do

* [x] Dual keyboard layout
* [x] Black keys and accurate note mapping
* [x] Responsive layout based on screen width
* [ ] Record and export performance
* [ ] MIDI output support

---

## 🧠 Inspiration

Inspired by interactive music experiences like Google’s "AI Duet" and the idea of contactless instruments using vision models.

---

## 📸 Demo

> *(Optional)* Insert a screenshot or demo GIF here

---

## 🤝 Contributing

Pull requests are welcome. Let’s make this more powerful together!

---

## 🪪 License

MIT License — use freely, credit appreciated.
# virtual_piano
