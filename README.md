# \[GAME_NO_NAME\] (TheHand Project)

## Project Introduction

**\[GAME_NO_NAME\]** is an action and fighting 2D Platformer game made by the **TheHand** team. The core idea is simple: **You don't need a keyboard or mouse\!** You control the character using only your **body movements, voice, and face expressions.** This creates a super fun and healthy way to play, turning your real-life actions into game moves.

## Core Concept: Natural Reaction

The game uses your **Camera and Microphone** for all interactions, challenging your natural reflexes:

- **Voice Commands:** Shout to use a strong skill, whisper to sneak, or use a keyword (like "henshin") to transform.
- **Gesture Control:** Swing your hands, move your feet, or hold specific **poses (Pose Estimation)** to attack, defend, or move your character.
- **Face Expressions:** Use **Face Recognition** to detect expressions (like smiling or opening your mouth wide) to unlock special skills or gain temporary power-ups (buffs).

## Genre & Gameplay

- **Genre:** 2D Platformer, Fighting, Action.
- **Gameplay:** Control your character to fight and defeat enemies, where every move in the game comes from a real-life physical movement.

## Technology Used

To make this unique control system work, the project uses specialized Machine Learning and Game Development tools:

- **Game Engine:** Pygame
- **Gesture/Pose Analysis:** Mediapipe (for Face, Handmark, and Pose Estimation)
- **Voice Recognition:** Moonshine ONNX

## Development Team (TheHand)

| Name            | Student ID |
| :-------------- | :--------- |
| Trần Đức Thịnh  | HE201309   |
| Châm Duy Khoát  | HE204140   |
| Nguyễn Thế Anh  | HE204320   |
| Đinh Duy Khương | HE200217   |
| Hoàng Minh Nhất | HE205173   |

**\[GAME_NO_NAME\] \- Where keyboards and mice are meaningless.**

## For Devs

### Getting Started

- Install `uv`.
- Clone the repo:

```bash
git clone https://github.com/TheHand-FPT/TheHand.git
```

```bash
cd TheHand
```

- Sync virtual env:

```bash
uv sync
```

- Install package as editable:

```bash
uv pip install -e .
```

Now you are ready to go!

### A quick look

Just run any script in `showcase/` to see how it work:

```bash
uv run showcase/show_audition.py
```

```bash
uv run showcase/show_game_dev.py
```
