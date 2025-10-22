# Game Design Document: [GAME_NOT_FOUND\!] (TheHand Project)

## 1. Introduction

**[GAME_NOT_FOUND\!]** is an interactive game where the core idea is simple: **You don't need a keyboard or mouse!** Players control using only their body movements, voice, and facial expressions. This creates a unique, fun, and healthy gameplay experience by translating real-life actions directly into game moves.

## 2. Core Concept: Natural Reaction

The game is built around the concept of "Natural Reaction." It uses the player's camera and microphone for all interactions, challenging their physical reflexes and expressiveness.

- **Voice Commands:** Shout to use a strong skill, or use a keyword.
- **Gesture Control:** Swing your hands, move your feet, or hold specific poses to attack, defend, or move your character.
- **Face Expressions:** Use facial recognition to detect expressions (like smiling or opening your mouth wide) to unlock special skills or gain temporary power-ups.

## 3. Technology Stack

- **Game Engine:** Pygame
- **Gesture/Pose Analysis:** MediaPipe (Hand, Face, and Pose Landmarkers)
- **Voice Recognition:** Moonshine ONNX

## 4. Game Engine Overview

The project utilizes a lightweight, "homemade" game engine built around the `thehand.core` module.

### 4.1. Scene Management

The game is structured around a `SceneManager` that manages a collection of `Scene` objects. Each `Scene` implements its own `setup()`, `handle_events()`, `update()`, and `render()` methods. The `SceneManager` continuously calls these methods each frame, providing a simple yet effective structure for game flow.

### 4.2. Core Input Modules

The heart of the game's "Natural Reaction" concept lies in these modules:

- **`SpeechRecognition`**: Processes audio input from the microphone.
- **`HandLandmarker`**: Processes hand landmarks.
- **`FaceLandmarker`**: Processes facial expressions.
- **`PoseLandmarker`**: Processes full-body poses.

These components work with a callback system, allowing different game scenes to react to various player inputs.

## 5. Game Structure & Scenes

The game is composed of several types of scenes, suggesting a modular structure, possibly a collection of mini-games tied together by a central menu.

### 5.1. Decorative Scenes

- **`SplashScene`**: A loading or initial branding screen.
- **`HintScene`**: Provides instructions or tips to the player.
- **`CreditScene`**: Displays the development team credits.

### 5.2. Common Scenes

- **`MainMenuScene`**: The central hub where players can select a game mode or level.
- **`NovelScene`**: A visual-novel style scene, used for storytelling or tutorials.

### 5.3. Game Levels (Mini-Games)

The codebase points to several distinct mini-games, each with its own mechanics:

- **`PacmanScene`**: A version of the classic Pac-Man, controlled by hand movement.
- **`RPSScene`**: A Rock-Paper-Scissors game, where players use hand gestures (rock, paper, scissors) to play.
- **`MLRSScene`**: A missile-launching game.
- **`MagicGestureScene`**: A game use hand gestures to catch gestures dropdown from the sky.

## 6. Assets

The project contains a simple collection of assets:

- **Audio (`data/audio/`)**: Includes background music, sound effects for UI, and specific gameplay sounds for Pac-Man, MLRS, and magic spells.
- **Fonts (`data/fonts/`)**: A variety of fonts for displaying text.
- **Images (`data/imgs/`)**: Contains sprites, backgrounds, and UI elements for all game levels, including Pac-Man characters, gesture icons, and tutorial images.

## 7. Development Team (TheHand)

| Name            | Student ID |
| :-------------- | :--------- |
| Trần Đức Thịnh  | HE201309   |
| Châm Duy Khoát  | HE204140   |
| Nguyễn Thế Anh  | HE204320   |
| Đinh Duy Khương | HE200217   |
| Hoàng Minh Nhất | HE205173   |
